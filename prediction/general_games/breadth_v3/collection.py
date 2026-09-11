"""Resumable fresh collection with fixed budgets and a prospective test gate."""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import multiprocessing
import tarfile

from prediction.io_utils import read_json, write_json, digest, now
from prediction.general_games.native import TA_ROOT, environment_record, library_hashes, jsonable
from prediction.general_games.dataset import source_hashes as historical_hashes
from prediction.general_games.export import jsonl
from prediction.scaleup.providers import configurations as model_configs
from . import ROOT, DATA, STUDY, VERSION
from .catalog import FAMILIES, NEW, DEPTH, configurations, seeds_for
from .runtime import Session, view, action, messages, replay
from .specifications import specifications
from .labels import episode_row, DEFINITIONS, BEHAVIOR_DEFINITIONS


def source_hashes():
    result=historical_hashes()
    for name in ('__init__.py','catalog.py','runtime.py','specifications.py','labels.py','collection.py','api.py'):
        p=ROOT/name; result[str(p.relative_to(ROOT.parents[2]))]=digest(p.read_text())
    for name in ('scaleup_v2/runtime.py','scaleup_v2/labels.py','export.py'):
        p=ROOT.parent/name; result[str(p.relative_to(ROOT.parents[2]))]=digest(p.read_text())
    return result


def build():
    if (DATA/'manifest.json').exists(): raise FileExistsError(DATA/'manifest.json')
    games=configurations(); instances=[]; fixtures=[]; sessions=[]; max_bytes=0
    for g in games:
        for j,seed in enumerate(seeds_for(g)):
            s=Session(g,seed); opening=s.snapshot()
            if j==0: sessions.append(s)
            instance=dict(instance_id='inst-'+digest([g['configuration_id'],seed])[:20],configuration_id=g['configuration_id'],family_id=g['family_id'],seed=seed,
                opening_group='open-'+digest([g['configuration_id'],opening])[:20], opening_observations=jsonable(s.opening),opening_state=opening)
            instances.append(instance); steps=[]
            for i in range(160):
                actor,incoming,h=s.observe(); v=view(s,actor,h); before=s.snapshot(); raw=action(v,seed,i)
                import json
                max_bytes=max(max_bytes,len(json.dumps(messages(g,h,'normal'),ensure_ascii=False).encode())+4608)
                result=s.step(raw)
                assert not result['native_invalid'],(g['family_id'],seed,i,raw,result)
                steps.append(dict(index=i,actor=actor,incoming=incoming,visible_state=v,before=before,is_focal=False,raw_action=raw,result=result,after=s.snapshot()))
                if result['done']: break
            assert s.env.state.done,(g['family_id'],seed,'fixture did not terminate')
            trace=dict(status='complete',opening_state=opening,opening_observations=jsonable(s.opening),steps=steps,final_state=s.snapshot())
            replay(dict(game=g,seed=seed),trace)
            fixtures.append(dict(instance_id=instance['instance_id'],provenance='scripted_validation_not_model_behavior',trace=trace))
        print('validated',g['family_id'],len(seeds_for(g)),flush=True)
    assert max_bytes<=80000
    specs=specifications(games,sessions)
    for name,value in [('catalog.json',dict(version=VERSION,families=FAMILIES,configurations=games)),('instances.evaluator.json',instances),('fixtures.evaluator.json',fixtures),('mechanics.json',specs),('label-definitions.json',dict(prediction=DEFINITIONS,behavior_diagnostics=BEHAVIOR_DEFINITIONS))]: write_json(DATA/name,value)
    write_json(DATA/'native-source-hashes.json',library_hashes())
    with tarfile.open(DATA/'native-source.tar.gz','w:gz') as tar:
        for p in sorted(TA_ROOT.rglob('*.py')): tar.add(p,arcname=str(p.relative_to(TA_ROOT)))
    result=dict(created=now(),version=VERSION,source_hashes=source_hashes(),environment=environment_record(),families=len(games),seeded_instances=len(instances),
        validation=dict(scripted_episodes=len(fixtures),native_transitions=sum(len(x['trace']['steps']) for x in fixtures),max_fixture_request_bytes=max_bytes),
        hashes={n:digest(read_json(DATA/n)) for n in ('catalog.json','instances.evaluator.json','fixtures.evaluator.json','mechanics.json','label-definitions.json')})
    write_json(DATA/'manifest.json',result)
    return result


def plans():
    assert not (STUDY/'protocol.json').exists()
    manifest=read_json(DATA/'manifest.json'); lookup={(i['configuration_id'],i['seed']):i for i in read_json(DATA/'instances.evaluator.json')}; groups={'training':[],'test':[]}
    for g in configurations():
        fid=g['family_id']; phase='test' if fid in NEW else 'training'
        for seed in seeds_for(g):
            inst=lookup[g['configuration_id'],seed]
            for seat in range(g['num_players']):
                for model in ('qwen-3.8-27b','glm'):
                    for rep in range(6 if fid in DEPTH else 2):
                        arms=[] if phase=='test' else (['depth','breadth'] if rep<2 else ['depth']) if fid in DEPTH else ['breadth']
                        item=dict(game=g,seed=seed,seat=seat,model=model,condition='normal',replicate=rep,arms=arms,suite=phase,
                            instance_id=inst['instance_id'],opening_group=inst['opening_group'])
                        item['episode_id']='ep-v3-'+digest(item)[:20]; groups[phase].append(item)
    assert len(groups['training'])==480 and len(groups['test'])==144
    assert {arm:sum(arm in e['arms'] for e in groups['training']) for arm in ('depth','breadth')}==dict(depth=288,breadth=288)
    for phase,episodes in groups.items():
        episodes.sort(key=lambda e:digest(['interleaved-v3',e['episode_id']]))
        plan=dict(created=now(),version=VERSION,phase=phase,source_hashes=source_hashes(),environment=environment_record(),data_manifest_sha256=digest(manifest),
            models=model_configs(['qwen-3.8-27b','glm']),budget_usd=40,global_budget_usd=60,max_tokens=16384,max_attempts_per_decision=3,max_steps=160,max_focal_actions=80,max_request_bytes=80000,episodes=episodes)
        write_json(STUDY/phase/'plan.json',plan)
    result=dict(created=now(),version=VERSION,episode_budget_per_arm=288,unique_training_episodes=480,test_episodes=144,
        arms=dict(depth=dict(families=list(DEPTH),episodes_per_family=72,repetitions=6),breadth=dict(families=sorted(set(FAMILIES)-set(NEW)),episodes_per_family=24,repetitions=2)),
        shared_training_episodes=96,test_families=sorted(NEW),test_conditions=72,
        design='Fresh normal-prompt collection. One base configuration per family. Every model and focal seat crossed with 3 world seeds in two-player games, 6 in single-player games, giving 12 exact conditions per family. Both arms share the first 2 repetitions of anchor conditions. All unique training episodes interleaved in deterministic randomized order.',
        comparison='Same 288 episode-label budget, different family breadth and repetitions. Episode budgets do not equalize tokens, decisions or dollar cost. Fixed purposive family sets; a single breadth contrast is not an isolated causal estimate of family count.',
        prediction=dict(model='kimi-k3',shots=[4,8,16],methods=['training_mean','linear','few_4','corrected_4','few_8','few_16'],
            primary_target='win',primary_comparisons=['breadth minus depth within linear','breadth minus depth within corrected_4','corrected_4 minus few_4 within each arm'],
            secondary_targets=['any_invalid','native_score'],behavior='Family-specific behavior labels are diagnostics only; novel label names have no training support and are not scored as learned transfer.',
            correction='Fixed Ridge alpha 10 on leave-family-out four-shot calibration; no test tuning.',
            few_shot='Pool every training label with identical complete observable inputs before retrieval. Nested 4/8/16 examples; no holdout-family labels.',
            linear='Fixed structured+384 TF-IDF logistic C=1 for binary labels, Ridge alpha=10 for native score. Family-balanced sample weights sum to 288 in both arms.'),
        prospective='Freeze both arms’ fitted artifacts and every test forecast before any test actor call. No historical labels are training data. Old v1/v2 holdout outcomes are excluded.',
        limits=dict(global_usd=60,stage_usd=40),test_plan_sha256=digest(read_json(STUDY/'test/plan.json')))
    write_json(STUDY/'protocol.json',result); return result


def run_episode(phase,item):
    from .api import Client,ModelConfig,Ledger
    folder=STUDY/phase; plan=read_json(folder/'plan.json'); path=folder/'episodes'/(item['episode_id']+'.json'); raw_dir=folder/'raw_calls'
    if path.exists():
        record=read_json(path); assert record['item']==item; s=replay(item,record,raw_dir)
        if record['status'] in ('complete','censored'): return item['episode_id'],record['status'],len(record['steps'])
    else:
        s=Session(item['game'],item['seed']); record=dict(item=item,started=now(),status='running',opening_state=s.snapshot(),opening_observations=jsonable(s.opening),steps=[],attempts={},errors=[]); write_json(path,record)
    client=Client(ModelConfig(**plan['models'][item['model']]),raw_dir,Ledger(STUDY/'budget.sqlite',plan['global_budget_usd']),Ledger(folder/'budget.sqlite',plan['budget_usd']),max_tokens=plan['max_tokens'])
    try:
        while not s.env.state.done:
            index=len(record['steps']); count=sum(x['is_focal'] for x in record['steps'])
            if index>=plan['max_steps'] or count>=plan['max_focal_actions']:
                record.update(status='censored',censor_reason='external_action_limit'); break
            actor,incoming,h=s.observe(); v=view(s,actor,h); focal=actor==item['seat']
            step=dict(index=index,actor=actor,is_focal=focal,incoming=incoming,visible_state=v,before=s.snapshot())
            if focal:
                prompt=messages(item['game'],h,item['condition']); attempts=record['attempts'].setdefault(str(index),[]); usable=next((a for a in attempts if a['meta']['status']=='ok'),None)
                while usable is None and len(attempts)<plan['max_attempts_per_decision']:
                    raw,meta=client.generate(prompt,purpose=item['episode_id']+f'/step-{index}'); a=dict(raw=raw,meta=meta); attempts.append(a); write_json(path,record)
                    if meta['status']=='ok': usable=a
                if usable is None: record.update(status='incomplete',failure_reason='inference_attempts_exhausted'); break
                raw=usable['raw']; step.update(messages=prompt,call=usable['meta'])
            else: raw=action(v,item['seed'],index)
            step.update(raw_action=raw,result=s.step(raw),after=s.snapshot()); record['steps'].append(step); write_json(path,record)
        if s.env.state.done: record['status']='complete'
    except Exception as exc:
        record.update(status='incomplete',failure_reason=type(exc).__name__); record['errors'].append(dict(time=now(),type=type(exc).__name__,detail=str(exc)[:250]))
        if isinstance(exc,ValueError) and 'context exceeded' in str(exc): record.update(status='censored',censor_reason='external_context_limit')
    record.update(updated=now(),final_state=s.snapshot()); write_json(path,record)
    return item['episode_id'],record['status'],len(record['steps'])


def collect(phase,workers=8,limit=None):
    from prediction.client import Ledger
    plan=read_json(STUDY/phase/'plan.json')
    assert plan['source_hashes']==source_hashes() and plan['environment']==environment_record()
    assert plan['data_manifest_sha256']==digest(read_json(DATA/'manifest.json'))
    if phase=='test':
        freeze=read_json(STUDY/'prediction/frozen.json'); assert freeze['test_plan_sha256']==digest(plan)
        for name,sha in freeze['artifact_hashes'].items(): assert hashlib.sha256((STUDY/'prediction'/name).read_bytes()).hexdigest()==sha
    Ledger(STUDY/'budget.sqlite',plan['global_budget_usd']); Ledger(STUDY/phase/'budget.sqlite',plan['budget_usd'])
    with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn')) as pool:
        futures=[pool.submit(run_episode,phase,item) for item in plan['episodes'][:limit]]
        for i,f in enumerate(as_completed(futures),1): print(phase,i,len(futures),*f.result(),flush=True)


def export(phase):
    rows=[]; actions=[]; missing=0
    for item in read_json(STUDY/phase/'plan.json')['episodes']:
        path=STUDY/phase/'episodes'/(item['episode_id']+'.json')
        if not path.exists(): missing+=1; continue
        trace=read_json(path); replay(item,trace,STUDY/phase/'raw_calls'); row,aa=episode_row(trace,'v3-'+phase); rows.append(row); actions+=aa
    jsonl(STUDY/phase/'export/episodes.jsonl',rows); jsonl(STUDY/phase/'export/actions.jsonl',actions)
    result=dict(episodes=len(rows),missing=missing,statuses=dict(Counter(r['status'] for r in rows)),focal_actions=len(actions),native_transitions=sum(r['native_transitions'] for r in rows),native_invalid=sum(r['invalid_actions'] for r in rows))
    write_json(STUDY/phase/'export/summary.json',result); return result


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['build','plans','collect','export']); p.add_argument('--phase',choices=['training','test'],default='training'); p.add_argument('--workers',type=int,default=8); p.add_argument('--limit',type=int); a=p.parse_args()
    r=build() if a.action=='build' else plans() if a.action=='plans' else export(a.phase) if a.action=='export' else collect(a.phase,a.workers,a.limit)
    if r is not None: print(r,flush=True)
