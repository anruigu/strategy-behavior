"""Prepare an uncollected full-catalog plan, crossing seeds and focal seats."""
import argparse
from pathlib import Path

from prediction.io_utils import read_json,write_json,digest,now
from prediction.scaleup.providers import configurations
from . import VERSION
from .dataset import DEFAULT_DATA,source_hashes
from .native import environment_record


def full_plan(data,run,budget=50):
    data=Path(data).resolve(); run=Path(run).resolve(); catalog=read_json(data/'catalog.json'); manifest=read_json(data/'manifest.json')
    instances=read_json(data/'instances.evaluator.json'); games={g['configuration_id']:g for g in catalog['configurations']}
    episodes=[]
    for instance in instances:
        game=games[instance['configuration_id']]
        for seat in range(game['num_players']):
            block=manifest['seeds'].index(instance['seed'])*game['num_players']+seat
            for model in ('qwen-3.8-27b','glm'):
                for condition in ('normal','active_exploration'):
                    item=dict(game=game,seed=instance['seed'],seat=seat,model=model,condition=condition,
                        instance_id=instance['instance_id'],opening_group=instance['opening_group'],seed_seat_block=block)
                    item['episode_id']='ep-'+digest(item)[:20]; episodes.append(item)
    plan=dict(version=VERSION,created=now(),data_dir=str(data),data_manifest_sha256=digest(manifest),
        environment=environment_record(),source_hashes=source_hashes(),models=configurations(['qwen-3.8-27b','glm']),
        max_tokens=16384,max_attempts_per_decision=3,max_steps=128,max_focal_actions=64,budget_usd=budget,
        protocol='full native parameter catalog; all four seeds independently crossed with all focal seats; two models and two prompt conditions',
        episodes=episodes)
    path=run/'plan.json'
    if path.exists(): raise FileExistsError(path)
    write_json(path,plan)
    return dict(planned_episodes=len(episodes),collected_episodes=0,path=str(path))


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--data',type=Path,default=DEFAULT_DATA)
    parser.add_argument('--run',type=Path,default=Path('prediction/general_games/runs/full-catalog-v1'))
    parser.add_argument('--budget',type=float,default=50); args=parser.parse_args()
    print(full_plan(args.data,args.run,args.budget))
