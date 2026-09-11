"""Bounded native rollouts, durable checkpoints, and exact deterministic replay."""
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
import multiprocessing
from pathlib import Path

from prediction.io_utils import read_json,write_json,digest,now
from .native import Session,messages,environment_record
from .policies import view,action
from .dataset import source_hashes,DEFAULT_RUN


def replay(item,record,raw_dir=None):
    session=Session(item['game'],item['seed'])
    if session.snapshot()!=record['opening_state'] or session.opening!= {int(k):v for k,v in record['opening_observations'].items()}:
        raise AssertionError('Opening mismatch')
    for i,step in enumerate(record['steps']):
        actor,incoming,history=session.observe()
        if [actor,incoming,view(session,actor,history),session.snapshot()]!=[step['actor'],step['incoming'],step['visible_state'],step['before']]:
            raise AssertionError(f'Pre-action replay mismatch: {i}')
        if step['is_focal']:
            expected=messages(item['game'],history,item['condition'])
            if expected!=step['messages']: raise AssertionError('Prompt replay mismatch')
            if raw_dir:
                call=read_json(Path(raw_dir)/(step['call']['call_id']+'.json'))
                if call['status']!='ok' or call['request']['messages']!=expected or call['response']['choices'][0]['message']['content']!=step['raw_action']:
                    raise AssertionError('Raw call mismatch')
        elif action(step['visible_state'],item['seed'],i)!=step['raw_action']: raise AssertionError('Bot replay mismatch')
        if session.step(step['raw_action'])!=step['result'] or session.snapshot()!=step['after']:
            raise AssertionError(f'Transition replay mismatch: {i}')
    return session


def run_episode(run_dir,item):
    from prediction.client import Client,ModelConfig,Ledger
    run_dir=Path(run_dir); plan=read_json(run_dir/'plan.json'); path=run_dir/'episodes'/(item['episode_id']+'.json')
    raw_dir=run_dir/'raw_calls'
    if path.exists():
        record=read_json(path)
        if record['item']!=item: raise AssertionError('Episode configuration mismatch')
        session=replay(item,record,raw_dir)
        if record['status'] in ('complete','censored'): return item['episode_id'],record['status'],len(record['steps'])
    else:
        session=Session(item['game'],item['seed'])
        record=dict(item=item,started=now(),status='running',opening_state=session.snapshot(),opening_observations=session.opening,
                    steps=[],attempts={},errors=[])
        write_json(path,record)
    client=Client(ModelConfig(**plan['models'][item['model']]),raw_dir,Ledger(run_dir/'budget.sqlite',plan['budget_usd']),
                  Ledger(run_dir/'stage-budget.sqlite',plan['budget_usd']),max_tokens=plan['max_tokens'])
    try:
        while not session.env.state.done:
            i=len(record['steps']); focal_count=sum(x['is_focal'] for x in record['steps'])
            if i>=plan['max_steps'] or focal_count>=plan['max_focal_actions']:
                record.update(status='censored',censor_reason='external_action_limit'); break
            actor,incoming,history=session.observe(); v=view(session,actor,history); before=session.snapshot(); focal=actor==item['seat']
            step=dict(index=i,actor=actor,is_focal=focal,incoming=incoming,visible_state=v,before=before)
            if focal:
                prompt=messages(item['game'],history,item['condition']); attempts=record['attempts'].setdefault(str(i),[])
                usable=next((x for x in attempts if x['meta']['status']=='ok'),None)
                while usable is None and len(attempts)<plan['max_attempts_per_decision']:
                    raw,meta=client.generate(prompt,purpose=item['episode_id']+f'/step-{i}')
                    attempt=dict(raw=raw,meta=meta); attempts.append(attempt); write_json(path,record)
                    if meta['status']=='ok': usable=attempt
                if usable is None:
                    record.update(status='incomplete',failure_reason='inference_attempts_exhausted'); break
                raw=usable['raw']; step.update(messages=prompt,call=usable['meta'])
            else: raw=action(v,item['seed'],i)
            step.update(raw_action=raw,result=session.step(raw),after=session.snapshot())
            record['steps'].append(step); write_json(path,record)
        if session.env.state.done: record['status']='complete'
    except Exception as exc:
        record.update(status='incomplete',failure_reason=type(exc).__name__)
        # No exception text from provider credentials; raw Client logs redact keys.
        record['errors'].append(dict(time=now(),type=type(exc).__name__))
    record.update(updated=now(),final_state=session.snapshot()); write_json(path,record)
    return item['episode_id'],record['status'],len(record['steps'])


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--run',type=Path,default=DEFAULT_RUN); parser.add_argument('--workers',type=int,default=6); parser.add_argument('--limit',type=int)
    args=parser.parse_args(); plan=read_json(args.run/'plan.json')
    if plan['environment']!=environment_record() or plan['source_hashes']!=source_hashes(): raise AssertionError('Collection source or installed native code changed')
    if plan['data_manifest_sha256']!=digest(read_json(Path(plan['data_dir'])/'manifest.json')): raise AssertionError('Dataset changed')
    from prediction.client import Ledger
    for name in ['budget.sqlite','stage-budget.sqlite']: Ledger(args.run/name,plan['budget_usd'])
    episodes=plan['episodes'][:args.limit] if args.limit else plan['episodes']
    with ProcessPoolExecutor(max_workers=args.workers,mp_context=multiprocessing.get_context('spawn')) as pool:
        futures=[pool.submit(run_episode,str(args.run.resolve()),item) for item in episodes]
        for future in as_completed(futures): print(*future.result(),flush=True)


if __name__=='__main__': main()
