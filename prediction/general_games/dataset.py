"""Build a native-game catalog, scripted fixtures, and matched live pilot plan."""
import argparse
from collections import Counter
from pathlib import Path
import sys

from prediction.io_utils import digest,write_json,read_json,now
from . import VERSION
from .catalog import FAMILIES,configurations
from .native import Session,environment_record,library_hashes
from .policies import view,action

DEFAULT_DATA=Path('prediction/general_games/data/20260910-v1')
DEFAULT_RUN=Path('prediction/general_games/runs/pilot-20260910')
SEEDS=[6100,6101,6102,6103]


def source_hashes():
    paths=[p for p in Path(__file__).parent.glob('*.py') if p.name in ('__init__.py','catalog.py','native.py','policies.py','runner.py','dataset.py')]
    paths += [Path(p) for p in ('prediction/client.py','prediction/scaleup/providers.py','prediction/io_utils.py','benchmark/clients.py','benchmark/fullscale/budget.py')]
    return {str(p.resolve().relative_to(Path(__file__).resolve().parents[2])):digest(p.read_text()) for p in paths}


def build(directory):
    directory=Path(directory); directory.mkdir(parents=True,exist_ok=True)
    games=configurations(); instances=[]; fixtures=[]; transitions=0
    write_json(directory/'native-source-hashes.json',library_hashes())
    for game in games:
        for seed in SEEDS:
            s=Session(game,seed); opening=s.snapshot()
            instance=dict(instance_id='inst-'+digest([game['configuration_id'],seed])[:20],configuration_id=game['configuration_id'],
                family_id=game['family_id'],seed=seed,
                opening_group='open-'+digest([game['configuration_id'],opening])[:20],
                opening_observations=s.opening,opening_state=opening)
            instances.append(instance); steps=[]
            for i in range(128):
                actor,incoming,history=s.observe(); v=view(s,actor,history); raw=action(v,seed,i)
                result=s.step(raw)
                if result['native_invalid']: raise AssertionError((game['family_id'],seed,i,raw,result))
                steps.append(dict(actor=actor,observation=incoming,action=raw,result=result,after=s.snapshot()))
                if result['done']: break
            if not s.env.state.done: raise AssertionError('Scripted fixture did not terminate: '+game['family_id'])
            replay=Session(game,seed)
            if replay.snapshot()!=opening: raise AssertionError('Opening is nondeterministic')
            for step in steps:
                actor,incoming,_=replay.observe()
                if actor!=step['actor'] or incoming!=step['observation']: raise AssertionError('Observation replay mismatch')
                if replay.step(step['action'])!=step['result'] or replay.snapshot()!=step['after']: raise AssertionError('Transition replay mismatch')
            transitions+=len(steps)
            fixtures.append(dict(instance_id=instance['instance_id'],source='scripted_validation_only',steps=steps))
        print('validated',game['family_id'],game['configuration_id'],flush=True)
    # Whole family/configuration/opening groups, never action-row random splits.
    def assignments(groups):
        ordered=sorted(set(groups),key=lambda g:digest(['split-v1',g])); n=len(ordered)
        return {g:('test' if i>=int(.8*n) else 'validation' if i>=int(.6*n) else 'train') for i,g in enumerate(ordered)}
    splits={key:assignments(x[key] for x in instances) for key in ('family_id','configuration_id','opening_group')}
    write_json(directory/'catalog.json',dict(version=VERSION,families=FAMILIES,configurations=games))
    write_json(directory/'instances.evaluator.json',instances)
    write_json(directory/'fixtures.evaluator.json',fixtures)
    write_json(directory/'splits.json',splits)
    manifest=dict(version=VERSION,created=now(),environment=environment_record(),source_hashes=source_hashes(),
        families=len(FAMILIES),configurations=len(games),seeded_instances=len(instances),distinct_opening_groups=len(set(x['opening_group'] for x in instances)),
        seeds=SEEDS,validation=dict(scripted_episodes=len(fixtures),replayed_transitions=transitions,invalid_actions=0),
        hashes={name:digest(read_json(directory/name)) for name in ('catalog.json','instances.evaluator.json','fixtures.evaluator.json','splits.json')})
    write_json(directory/'manifest.json',manifest)
    return manifest


def plan(data,run):
    from prediction.scaleup.providers import configurations as models
    data=Path(data).resolve(); run=Path(run).resolve()
    manifest=read_json(data/'manifest.json'); catalog=read_json(data/'catalog.json')
    instances={(x['configuration_id'],x['seed']):x for x in read_json(data/'instances.evaluator.json')}
    games=[g for g in catalog['configurations'] if g['intervention_axis'] is None]
    episodes=[]
    for game in games:
        for block,seed in enumerate(SEEDS[:2]):
            instance=instances[game['configuration_id'],seed]
            for model in ['qwen-3.8-27b','glm']:
                for condition in ['normal','active_exploration']:
                    item=dict(game=game,seed=seed,seat=block%game['num_players'],model=model,condition=condition,
                        instance_id=instance['instance_id'],opening_group=instance['opening_group'],seed_seat_block=block)
                    item['episode_id']='ep-'+digest(item)[:20]; episodes.append(item)
    result=dict(version=VERSION,created=now(),data_dir=str(data),data_manifest_sha256=digest(manifest),
        environment=environment_record(),source_hashes=source_hashes(),models=models(['qwen-3.8-27b','glm']),
        max_tokens=16384,max_attempts_per_decision=3,max_steps=128,max_focal_actions=64,budget_usd=50,
        protocol='one focal LLM; one information-restricted scripted opponent in 2p games; native single-player games',
        episodes=episodes)
    path=run/'plan.json'
    if path.exists(): raise FileExistsError('Plan already exists; resume with runner instead')
    write_json(path,result)
    return dict(episodes=len(episodes),run_dir=str(run))


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('command',choices=['build','plan']); parser.add_argument('--data',type=Path,default=DEFAULT_DATA); parser.add_argument('--run',type=Path,default=DEFAULT_RUN)
    args=parser.parse_args(); print(build(args.data) if args.command=='build' else plan(args.data,args.run))
