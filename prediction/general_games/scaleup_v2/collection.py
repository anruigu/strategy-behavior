"""Replicated training, prospective tests, and native validation of the extension."""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor,as_completed
from copy import deepcopy
import hashlib
import multiprocessing
from pathlib import Path
import tarfile

from prediction.io_utils import read_json,write_json,digest,now
from prediction.general_games.native import Session,environment_record,TA_ROOT,library_hashes
from prediction.general_games.dataset import source_hashes as old_hashes
from prediction.scaleup.providers import configurations as models
from . import ROOT,DATA,STUDY,VERSION
from .catalog import FAMILIES,NEW,ANCHORS,SEEDS,configurations,anchor_games
from .runtime import view,action,messages,replay
from .specifications import specification
from .labels import episode_row,DEFINITIONS


def source_hashes():
    result=old_hashes()
    for name in ('__init__.py','catalog.py','runtime.py','specifications.py','labels.py','collection.py'):
        p=ROOT/name;result[str(p.relative_to(ROOT.parents[2]))]=digest(p.read_text())
    for p in (ROOT.parent/'export.py',ROOT.parent/'evaluation/checks.py'):
        result[str(p.relative_to(ROOT.parents[2]))]=digest(p.read_text())
    return result


def build():
    if (DATA/'manifest.json').exists():raise FileExistsError(DATA/'manifest.json')
    games=configurations();instances=[];fixtures=[];specs={};transitions=0
    for game in games:
        for seed in SEEDS:
            s=Session(game,seed);opening=s.snapshot()
            instance=dict(instance_id='inst-'+digest([game['configuration_id'],seed])[:20],configuration_id=game['configuration_id'],
                family_id=game['family_id'],seed=seed,opening_group='open-'+digest([game['configuration_id'],opening])[:20],
                opening_observations=s.opening,opening_state=opening)
            instances.append(instance)
            if game['family_id'] not in specs:specs[game['family_id']]=specification(game,s)
            steps=[]
            for i in range(128):
                actor,incoming,history=s.observe();v=view(s,actor,history);before=s.snapshot();raw=action(v,seed,i);result=s.step(raw)
                assert not result['native_invalid'],(game['family_id'],seed,i,raw,result)
                steps.append(dict(index=i,actor=actor,incoming=incoming,visible_state=v,before=before,is_focal=False,raw_action=raw,result=result,after=s.snapshot()))
                if result['done']:break
            assert s.env.state.done,game['family_id']
            record=dict(status='complete',opening_state=opening,opening_observations=s.opening,steps=steps,final_state=s.snapshot())
            replay(dict(game=game,seed=seed),record)
            fixtures.append(dict(instance_id=instance['instance_id'],provenance='scripted_fixture_only',trace=record));transitions+=len(steps)
        print('validated',game['family_id'],game['configuration_id'],flush=True)
    write_json(DATA/'catalog.json',dict(version=VERSION,families=FAMILIES,configurations=games))
    write_json(DATA/'instances.evaluator.json',instances);write_json(DATA/'fixtures.evaluator.json',fixtures)
    write_json(DATA/'mechanics.json',specs);write_json(DATA/'label-definitions.json',DEFINITIONS)
    write_json(DATA/'native-source-hashes.json',library_hashes())
    DATA.mkdir(parents=True,exist_ok=True)
    with tarfile.open(DATA/'native-source.tar.gz','w:gz') as tar:
        for p in sorted(TA_ROOT.rglob('*.py')):tar.add(p,arcname=str(p.relative_to(TA_ROOT)))
    manifest=dict(version=VERSION,created=now(),environment=environment_record(),source_hashes=source_hashes(),
        families=len(FAMILIES),new_families=sorted(NEW),configurations=len(games),seeds=SEEDS,
        seeded_instances=len(instances),distinct_openings=len({i['opening_group'] for i in instances}),
        validation=dict(scripted_episodes=len(fixtures),native_transitions=transitions),
        hashes={name:digest(read_json(DATA/name)) for name in ('catalog.json','instances.evaluator.json','mechanics.json','label-definitions.json')},
        native_archive_sha256=hashlib.sha256((DATA/'native-source.tar.gz').read_bytes()).hexdigest())
    write_json(DATA/'manifest.json',manifest)
    return manifest


def plans():
    manifest=read_json(DATA/'manifest.json');instances={(i['configuration_id'],i['seed']):i for i in read_json(DATA/'instances.evaluator.json')}
    groups={'training':[],'test':[]}
    for game in anchor_games()+[g for g in configurations() if g['family_id'] in NEW]:
        is_new=game['family_id'] in NEW
        is_test=is_new or game['parameters'][ANCHORS[game['family_id']][0]]==ANCHORS[game['family_id']][3]
        phase='test' if is_test else 'training';replicates=2 if is_new else 5
        for seed in SEEDS:
            instance=instances[game['configuration_id'],seed]
            for seat in range(game['num_players']):
                for model in ('qwen-3.8-27b','glm'):
                    for replicate in range(replicates):
                        item=dict(game=game,seed=seed,seat=seat,model=model,condition='normal',replicate=replicate,
                            suite='family' if is_new else 'parameter' if is_test else 'training',
                            instance_id=instance['instance_id'],opening_group=instance['opening_group'])
                        item['episode_id']='ep-v2-'+digest(item)[:20];groups[phase].append(item)
    for phase,episodes in groups.items():
        path=STUDY/phase/'plan.json'
        if path.exists():raise FileExistsError(path)
        # Interleave repeats and conditions to reduce collection-order confounding.
        episodes.sort(key=lambda e:(e['replicate'],digest(['collection-order-v2',e['episode_id']])))
        plan=dict(version=VERSION,created=now(),phase=phase,source_hashes=source_hashes(),environment=environment_record(),
            data_manifest_sha256=digest(manifest),models=models(['qwen-3.8-27b','glm']),budget_usd=50,global_budget_usd=75,
            max_tokens=16384,max_attempts_per_decision=3,max_steps=128,max_focal_actions=64,episodes=episodes,
            protocol='Normal player prompt; model × environment seed × every focal seat fully crossed; five identical-condition repeats in anchors, two in new families. Native transitions unmodified.')
        write_json(path,plan)
    historical=[]
    parent=ROOT.parent/'runs'
    for name in ('pilot-20260910','parameter-check-20260910'):
        plan=read_json(parent/name/'plan.json')
        for item in plan['episodes']:
            fid=item['game']['family_id']
            if fid in ANCHORS and item['game']['parameters'][ANCHORS[fid][0]]==ANCHORS[fid][3]:continue
            row,_=episode_row(read_json(parent/name/'episodes'/(item['episode_id']+'.json')),name)
            historical.append(row)
    assert len(historical)==120 and len(groups['training'])==320 and len(groups['test'])==272
    write_json(STUDY/'historical-training.evaluator.json',historical)
    protocol=dict(created=now(),training_episodes=len(groups['training']),test_episodes=len(groups['test']),historical_training_episodes=len(historical),
        learning_curve_episode_budgets=[120,248,440],new_families=sorted(NEW),anchor_axes=ANCHORS,shots=[4,8,16],
        predictor='kimi-k3',primary_target='win',secondary_targets=list(DEFINITIONS)[1:],
        primary_comparison='learned correction to 4-shot versus uncorrected 4-shot; all shot counts reported',
        testing='Higher anchor values and all four new families are held out. Freeze every test forecast and fitted model before the first new test-player call.',
        condition_replication='Five independent LLM samplings of an identical configuration, world seed, seat, model and prompt. World seed and seat are independently crossed. New families have two repeats.',
        prospective_test_plan_sha256=digest(read_json(STUDY/'test/plan.json')))
    write_json(STUDY/'protocol.json',protocol)
    return protocol


def run_episode(phase,item):
    from prediction.client import Client,ModelConfig,Ledger
    folder=STUDY/phase;plan=read_json(folder/'plan.json');path=folder/'episodes'/(item['episode_id']+'.json');raw_dir=folder/'raw_calls'
    if path.exists():
        record=read_json(path);assert record['item']==item;s=replay(item,record,raw_dir)
        if record['status'] in ('complete','censored'):return item['episode_id'],record['status'],len(record['steps'])
    else:
        s=Session(item['game'],item['seed']);record=dict(item=item,started=now(),status='running',opening_state=s.snapshot(),opening_observations=s.opening,steps=[],attempts={},errors=[])
        write_json(path,record)
    client=Client(ModelConfig(**plan['models'][item['model']]),raw_dir,Ledger(STUDY/'budget.sqlite',plan['global_budget_usd']),Ledger(folder/'budget.sqlite',plan['budget_usd']),max_tokens=plan['max_tokens'])
    try:
        while not s.env.state.done:
            index=len(record['steps']);focal_count=sum(x['is_focal'] for x in record['steps'])
            if index>=plan['max_steps'] or focal_count>=plan['max_focal_actions']:
                record.update(status='censored',censor_reason='external_action_limit');break
            actor,incoming,h=s.observe();v=view(s,actor,h);before=s.snapshot();focal=actor==item['seat']
            step=dict(index=index,actor=actor,is_focal=focal,incoming=incoming,visible_state=v,before=before)
            if focal:
                prompt=messages(item['game'],h,item['condition']);attempts=record['attempts'].setdefault(str(index),[])
                usable=next((x for x in attempts if x['meta']['status']=='ok'),None)
                while usable is None and len(attempts)<plan['max_attempts_per_decision']:
                    raw,meta=client.generate(prompt,purpose=item['episode_id']+f'/step-{index}');a=dict(raw=raw,meta=meta);attempts.append(a);write_json(path,record)
                    if meta['status']=='ok':usable=a
                if usable is None:record.update(status='incomplete',failure_reason='inference_attempts_exhausted');break
                raw=usable['raw'];step.update(messages=prompt,call=usable['meta'])
            else:raw=action(v,item['seed'],index)
            step.update(raw_action=raw,result=s.step(raw),after=s.snapshot());record['steps'].append(step);write_json(path,record)
        if s.env.state.done:record['status']='complete'
    except Exception as exc:
        record.update(status='incomplete',failure_reason=type(exc).__name__);record['errors'].append(dict(time=now(),type=type(exc).__name__))
    record.update(updated=now(),final_state=s.snapshot());write_json(path,record)
    return item['episode_id'],record['status'],len(record['steps'])


def collect(phase,workers=8,limit=None):
    from prediction.client import Ledger
    plan=read_json(STUDY/phase/'plan.json')
    assert plan['source_hashes']==source_hashes() and plan['environment']==environment_record()
    assert plan['data_manifest_sha256']==digest(read_json(DATA/'manifest.json'))
    if phase=='test':
        frozen=read_json(STUDY/'prediction/frozen.json')
        assert frozen['test_plan_sha256']==digest(plan)
        for name,sha in frozen['artifact_hashes'].items():assert hashlib.sha256((STUDY/'prediction'/name).read_bytes()).hexdigest()==sha
    Ledger(STUDY/'budget.sqlite',plan['global_budget_usd']);Ledger(STUDY/phase/'budget.sqlite',plan['budget_usd'])
    with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn')) as pool:
        futures=[pool.submit(run_episode,phase,item) for item in plan['episodes'][:limit]]
        for i,f in enumerate(as_completed(futures),1):print(i,len(futures),*f.result(),flush=True)


def export(phase):
    from prediction.general_games.export import jsonl
    plan=read_json(STUDY/phase/'plan.json');rows=[];actions=[];missing=0
    for item in plan['episodes']:
        path=STUDY/phase/'episodes'/(item['episode_id']+'.json')
        if not path.exists():missing+=1;continue
        trace=read_json(path);replay(item,trace,STUDY/phase/'raw_calls')
        row,aa=episode_row(trace,'v2-'+phase);rows.append(row);actions+=aa
    jsonl(STUDY/phase/'export/episodes.jsonl',rows);jsonl(STUDY/phase/'export/actions.jsonl',actions)
    summary=dict(planned=len(plan['episodes']),missing=missing,statuses=dict(Counter(r['status'] for r in rows)),episodes=len(rows),
        focal_actions=len(actions),native_transitions=sum(r['native_transitions'] for r in rows),native_invalid=sum(not a['valid'] for a in actions))
    write_json(STUDY/phase/'export/summary.json',summary)
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['build','plans','collect','export']);parser.add_argument('--phase',choices=['training','test'],default='training');parser.add_argument('--workers',type=int,default=8);parser.add_argument('--limit',type=int)
    args=parser.parse_args();result=build() if args.action=='build' else plans() if args.action=='plans' else export(args.phase) if args.action=='export' else collect(args.phase,args.workers,args.limit)
    if result is not None:print(result,flush=True)
