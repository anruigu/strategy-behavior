"""Freeze post-pilot secondary baselines before future outcomes. No API calls."""
import argparse
from collections import Counter
import fcntl
from pathlib import Path
import time

from prediction import after_matrix as driver
from prediction.io_utils import now, read_json, write_json


def before_rollouts(root, stage):
    if any((root/stage/name).exists() for name in ('episodes','process.json','status.json')):
        raise RuntimeError('Secondary forecasts must precede every player rollout: '+stage)


def verify_plan(root, plan):
    for name,expected in plan['source_sha256'].items():
        if driver.file_hash(driver.pipeline.ROOT/'prediction'/name)!=expected:
            raise ValueError('Secondary source changed: '+name)
    for field,filename in (('metadata_sha256','metadata.json'),('manifest_sha256','manifest.json')):
        for stage,expected in plan[field].items():
            if driver.file_hash(root/stage/filename)!=expected:
                raise ValueError('Secondary '+filename+' changed: '+stage)
    if driver.file_hash(root/'training-records.json')!=plan['training_sha256']:
        raise ValueError('Secondary training snapshot changed')


def freeze(root):
    output=root/'secondary-baselines'
    output.mkdir(exist_ok=True)
    status_path=output/'status.json'
    if (output/'forecast-freeze.json').exists():
        evidence=read_json(output/'forecast-freeze.json')
        plan=read_json(output/'plan.json')
        if driver.file_hash(output/'plan.json')!=evidence['plan_sha256']:
            raise ValueError('Completed secondary plan changed')
        for path,expected in evidence['forecasts_sha256'].items():
            if driver.file_hash(path)!=expected:
                raise ValueError('Completed secondary forecast changed: '+path)
        verify_plan(root,plan)
        write_json(status_path,evidence)
        return
    write_json(status_path,dict(status='waiting_for_fixed_training',updated=now(),api_calls=False))
    while not (root/'training-records.json').exists():
        status=read_json(root/'pipeline-status.json').get('status','')
        if status=='error' or status.startswith('stopped') or status=='informative_negative':
            write_json(status_path,dict(status='upstream_stopped',updated=now(),upstream_status=status,api_calls=False))
            return
        time.sleep(10)
    primary=read_json(root/'primary-pilot-manifest.json')
    training,kimi,unknown=driver.validate_training(root,primary)
    pair='|'.join(sorted((kimi,unknown)))
    before_rollouts(root,'prospective')
    before_rollouts(root,'controls')
    plan=dict(version='secondary-freeze-v1',secondary_post_pilot=True,primary_methods_unchanged=True,
        explanation='Payoff-dominant equilibrium selection and scoring-weight-matched ordered context; motivated after observing pilot results.',
        training_sha256=driver.file_hash(root/'training-records.json'),pair_exclusion=pair,model_exclusion=unknown,
        metadata_sha256={stage:driver.file_hash(root/stage/'metadata.json') for stage in ('prospective','controls')},
        manifest_sha256={stage:driver.file_hash(root/stage/'manifest.json') for stage in ('prospective','controls')},
        source_sha256={name:driver.file_hash(driver.pipeline.ROOT/'prediction'/name) for name in
                      ('secondary_freeze.py','secondary_baselines.py','after_matrix.py','pipeline.py','prospective.py','modeling.py','analysis.py')})
    driver.immutable_json(output/'plan.json',plan)
    write_json(status_path,dict(status='freezing',updated=now(),api_calls=False))
    predicates=dict(full=lambda row:True,
        excluded_pair=lambda row:'|'.join(sorted((row['model'],row['opponent'])))!=pair,
        excluded_model=lambda row:unknown not in (row['model'],row['opponent']))
    frozen={}
    def track(paths):
        for path in paths:
            frozen[str(path)]=driver.file_hash(path)
    for name,predicate in predicates.items():
        folder=output/name
        rows=[row for row in training if predicate(row)]
        assert rows and set(Counter(row['episode_id'] for row in rows).values())=={2}
        records=folder/'training.json';artifact=folder/'fit.json'
        driver.immutable_json(records,rows)
        driver.immutable_json(folder/'training-audit.json',dict(filter=name,source_sha256=plan['training_sha256'],
            filtered_sha256=driver.file_hash(records),rows=len(rows),episodes=len(rows)//2,
            held_pair=pair if name=='excluded_pair' else None,held_model=unknown if name=='excluded_model' else None))
        track([records,folder/'training-audit.json'])
        driver.checked_step(root,'secondary-fit-'+name,['-m','prediction.secondary_baselines','fit',
            '--artifact',str(artifact),'--training-records',str(records)],[artifact])
        track([artifact])
        for stage in (('prospective','controls') if name=='full' else ('prospective',)):
            forecasts=folder/(stage+'.jsonl')
            before_rollouts(root,stage)
            driver.checked_step(root,'secondary-forecast-'+name+'-'+stage,
                ['-m','prediction.secondary_baselines','forecast','--artifact',str(artifact),
                 '--input',str(root/stage/'metadata.json'),'--output',str(forecasts),'--stage-root',str(root/stage)],
                [forecasts,forecasts.with_suffix('.manifest.json')])
            before_rollouts(root,stage)
            track([forecasts,forecasts.with_suffix('.manifest.json')])
    before_rollouts(root,'prospective')
    before_rollouts(root,'controls')
    verify_plan(root,plan)
    driver.immutable_json(output/'plan.json',plan)
    for path,expected in frozen.items():
        if driver.file_hash(path)!=expected:
            raise ValueError('Secondary artifact changed during freezing: '+path)
    evidence=dict(status='forecasts_frozen_before_rollouts',finished=now(),api_calls=False,secondary_post_pilot=True,
        forecasts_sha256=frozen,plan_sha256=driver.file_hash(output/'plan.json'),
        interpretation='Outcome joins must independently pass the existing prospective timestamp/hash audit. Planned controls may remain unrun.')
    driver.immutable_json(output/'forecast-freeze.json',evidence)
    write_json(status_path,evidence)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root',type=Path,required=True)
    args=parser.parse_args();root=args.run_root.resolve()
    if not root.is_relative_to(Path('/shared/allie')) or not root.is_dir():
        parser.error('run-root must exist under /shared/allie')
    with (root/'secondary-freeze.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:
            freeze(root)
        except Exception as exc:
            write_json(root/'secondary-baselines/status.json',dict(status='error',updated=now(),api_calls=False,
                error=type(exc).__name__+': '+str(exc)))
            raise


if __name__=='__main__':
    main()
