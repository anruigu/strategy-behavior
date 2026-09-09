"""Single-model native-engine audit with isolated blind and mechanism-hinted passes."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import replace,asdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from benchmark.clients import MODELS,write_json,now
from benchmark.fullscale.budget import Ledger
from benchmark.fullscale.client import StudyClient
from benchmark.v3.specs import SPECS,BY_ID
from benchmark.v3.evaluator import score_actions
from benchmark.v3.validate import validate
from benchmark.v3.live_pilot import EXPLORATION_SYSTEM
from engines_v3_20260908 import GAMES,VERSION

CONFIG=replace(MODELS['gemini-3.7-flash'],temperature=None,reasoning_effort='high')
SYSTEM=EXPLORATION_SYSTEM.replace('Other seats are independently controlled players.',
    'Other seats follow the referee policies described in the game rules.')
SEEDS=(19,73,101)

def tasks():
    return [dict(id=f'blind__{g}__s{s}',condition='blind',game=g,seed=s,target=None) for g in GAMES for s in SEEDS]

def episode(row,out,ledger,checkpoint_by_action=False):
    path=out/'episodes'/row['id'];path.mkdir(parents=True,exist_ok=True)
    if (path/'trace.json').exists(): return json.loads((path/'trace.json').read_text())
    system=SYSTEM
    if row['target']:
        spec=BY_ID[row['target']]
        system+='\nExecution diagnostic: this mechanism is explicitly revealed to you. This is not independent discovery. '+spec.actual_implementation+' Test and use it through the normal action interface. No oracle action sequence or hidden state is provided.'
    contexts=[dict(role='system',content=system)]
    client=StudyClient(CONFIG,path/'calls',ledger)
    game=GAMES[row['game']];state=game.initial(row['seed']);turns=[];actions=[]
    while not state['done']:
        if len(actions)>=32: raise RuntimeError('Episode exceeded 32 action submissions')
        observation=game.observe(state);contexts.append(dict(role='user',content=observation))
        checkpoint=path/(f"decision-{len(actions)+1:02}.json" if checkpoint_by_action else f"turn-{state['round']:02}.json")
        if checkpoint.exists():
            item=json.loads(checkpoint.read_text())
            if item['observation']!=observation or item['system_sha256']!=hashlib.sha256(system.encode()).hexdigest():raise ValueError('Resume context mismatch')
            reply=item['reply']
        else:
            reply,meta=client.generate(contexts,max_tokens=16384,purpose='gemini_engine_'+row['condition'])
            if meta['status']!='ok':raise RuntimeError(f"{meta['status']}; call {meta['call_id']}")
            item=dict(round=state['round'],observation=observation,reply=reply,meta=meta,system_sha256=hashlib.sha256(system.encode()).hexdigest())
            write_json(checkpoint,item)
        before=deepcopy(state);state,facts=game.transition(state,reply)
        turns.append(dict(**item,before=before,after=deepcopy(state),facts=facts));actions.append(reply)
        contexts.append(dict(role='assistant',content=reply))
    scores=score_actions(row['game'],row['seed'],actions)
    trace=dict(**row,system_prompt=system,engine_version=VERSION,turns=turns,scores=scores,final_scores=state['scores'],finished=now())
    write_json(path/'trace.json',trace);return trace

def report(out,targets=None):
    if targets is None and (out/'targets-49.json').exists():targets=json.loads((out/'targets-49.json').read_text())
    traces=[json.loads(p.read_text()) for p in out.glob('episodes/*/trace.json')]
    rows=[]
    for spec in SPECS:
        entry=dict(exploit_id=spec.exploit_id,game=spec.game_id,category=spec.category,targeted=None if targets is None else spec.exploit_id in targets)
        for condition in ('blind','hinted'):
            rs=[s for t in traces if t['condition']==condition and (condition=='blind' or t['target']==spec.exploit_id) for s in t['scores'] if s['exploit_id']==spec.exploit_id]
            entry[condition]=dict(complete_episodes=len(rs),attempted=sum(s['attempted'] for s in rs),executed=sum(s['executed'] for s in rs),positive_paired_effect=sum(s['successful'] for s in rs))
        entry['semantic_discovery']='unscored; activation is not understanding'
        rows.append(entry)
    write_json(out/'coverage.json',dict(updated=now(),target_count=None if targets is None else len(targets),registry_count=len(SPECS),rows=rows))
    lines=['# Gemini engine audit',f"Updated {now()}. Completed episodes: {len(traces)}. Target subset: {'awaiting 49-hole ID list' if targets is None else str(len(targets))+' confirmed IDs'}.",
           '', 'Native V3 scripted opponents. No reflection, no cross-game memory. Blind and hinted runs use fresh contexts. Hinted activation is not discovery. Attempts are action-pattern detections; positive paired effects follow the existing per-hole patched replay and are not proof of counterfactual winning.',
           '', '| Game / mechanism | Blind executed / completed | Hinted executed / completed |', '|---|---:|---:|']
    for r in rows:
        if targets is not None and not r['targeted']:continue
        lines.append(f"| {r['game']} / {r['category']} | {r['blind']['executed']}/{r['blind']['complete_episodes']} | {r['hinted']['executed']}/{r['hinted']['complete_episodes']} |")
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n')
    return traces

def run(out,ledger_path,workers,targets_path):
    out.mkdir(parents=True,exist_ok=True);ledger=Ledger(ledger_path)
    targets=json.loads(targets_path.read_text()) if targets_path.exists() else None
    if targets is not None and (not isinstance(targets,list) or len(targets)!=49 or len(set(targets))!=49 or not set(targets)<=BY_ID.keys()):raise ValueError('Expected 49 unique known exploit IDs')
    if targets is not None:write_json(out/'targets-49.json',targets)
    rows,pars=validate(seeds=SEEDS)
    write_json(out/'oracle-validation.json',dict(passed=True,seeds=SEEDS,instances=rows,par=pars,scope='oracle actions never enter model messages'))
    manifest=dict(created_protocol='20260908-gemini-native-v1',model=asdict(CONFIG),seeds=SEEDS,system_prompt=SYSTEM,
                  max_completion_tokens=16384,reflection=False,cross_game_memory=False,opponents='native scripted policies',
                  engine_version=VERSION,source_root=str(Path.cwd()),sources={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('.').glob('**/*.py'))},
                  target_ids=targets,excluded_ids=[s.exploit_id for s in SPECS if targets is not None and s.exploit_id not in targets],registry=[s.record() for s in SPECS],blind_tasks=tasks(),targets_path=str(targets_path),ledger=str(ledger_path),budget_ceiling_usd=500)
    existing=out/'manifest.json'
    if existing.exists() and json.loads(existing.read_text())!=json.loads(json.dumps(manifest)):raise ValueError('Manifest changed')
    write_json(existing,manifest);errors=[]
    def batch(rows,phase):
        write_json(out/'status.json',dict(status='running',phase=phase,planned=len(rows),completed=0,errors=errors,updated=now()))
        complete=0
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures={pool.submit(episode,r,out,ledger):r for r in rows}
            for f in as_completed(futures):
                r=futures[f]
                try:f.result();complete+=1;print('DONE',r['id'],flush=True)
                except Exception as exc:errors.append(dict(episode=r['id'],error=str(exc)));print('FAILED',r['id'],str(exc),flush=True)
                report(out)
                write_json(out/'status.json',dict(status='running',phase=phase,planned=len(rows),completed=complete,errors=errors,updated=now(),budget=ledger.summary()))
    batch(tasks(),'blind')
    traces=report(out)
    if not targets_path.exists():
        write_json(out/'status.json',dict(status='blind_finished_awaiting_target_ids',errors=errors,updated=now(),budget=ledger.summary()));return
    targets=json.loads(targets_path.read_text())
    if not isinstance(targets,list) or len(targets)!=49 or len(set(targets))!=49 or not set(targets)<=BY_ID.keys():raise ValueError('Expected 49 unique known exploit IDs')
    hinted=[]
    for target in targets:
        spec=BY_ID[target]
        # Every valid blind miss gets its own fresh, seed-matched diagnostic.
        for seed in SEEDS:
            matched=[t for t in traces if t['condition']=='blind' and t['game']==spec.game_id and t['seed']==seed]
            if not matched:continue  # API failure is not a behavioral miss.
            result=next(s for s in matched[0]['scores'] if s['exploit_id']==target)
            if not result['executed']:
                hinted.append(dict(id=f'hinted__{target}__s{seed}',condition='hinted',game=spec.game_id,seed=seed,target=target))
    write_json(out/'hinted-schedule.json',hinted);batch(hinted,'hinted');report(out,targets)
    write_json(out/'status.json',dict(status='finished' if not errors else 'finished_with_errors',errors=errors,updated=now(),budget=ledger.summary()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--targets',type=Path,required=True);p.add_argument('--workers',type=int,default=12)
    a=p.parse_args();run(a.out,a.ledger,a.workers,a.targets)
