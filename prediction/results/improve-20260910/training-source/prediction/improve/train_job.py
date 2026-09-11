"""Run the fixed training comparison and metadata-only forecasts in one Fleet job."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import traceback
import unittest
from types import SimpleNamespace

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while block:=f.read(4*1024*1024): h.update(block)
    return h.hexdigest()

def save(path, data):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,indent=2)+'\n');temp.replace(path)

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-root',required=True);p.add_argument('--resume',action='store_true');a=p.parse_args()
    root=Path(a.run_root).resolve()
    if not root.is_relative_to(Path('/mnt/sfs/allie')) or not os.environ.get('FLEET_RUN_NAME'):
        raise RuntimeError('Expected a Fleet job on user shared storage')
    name=os.environ['FLEET_RUN_NAME']
    os.environ.update(PREDICTION_FLEET_TRAINING_RUN='1',IMPROVE_TRAINING_AUTHORITY='fleet_api',IMPROVE_FLEET_RUN_ID=name)
    runtime=root/'fleet-runtime';runtime.mkdir(exist_ok=True)
    log=(runtime/'training.log').open('a',buffering=1)
    sys.stdout=log;sys.stderr=log
    deadline=datetime.fromisoformat(os.environ['PREDICTION_EXPERIMENT_DEADLINE']).timestamp()
    started=datetime.now(timezone.utc).isoformat()
    state={'fleet_run_id':name,'started_utc':started,'steps':[],'status':'running'}
    if (runtime/'training-status.json').exists():
        if not a.resume:raise FileExistsError('Existing job state requires explicit resume')
        state['prior_attempt']=json.loads((runtime/'training-status.json').read_text())
    def verify_record(path,output=None):
        record=json.loads(path.read_text())
        for table in ('input_sha256','source_sha256','output_sha256'):
            for file,expected in record.get(table,{}).items():
                if sha(file)!=expected:raise ValueError('Saved step artifact changed: '+file)
        if output is not None and sha(output)!=record['forecast_sha256']:
            raise ValueError('Saved forecast changed')
        return record
    def reuse_or_run(label,marker,fn,output=None,partial_folder=None):
        if a.resume and marker.exists():
            record=verify_record(marker,output)
            print('REUSE '+label,flush=True)
            return record
        if a.resume and partial_folder is not None and partial_folder.exists():
            partial_folder.rename(partial_folder.with_name(partial_folder.name+'.incomplete-'+name))
        return fn()
    def remaining():
        result=deadline-time.time()-120
        if result<=0: raise TimeoutError('Conservative total experiment deadline reached')
        return result
    def step(label, fn):
        remaining();stamp=datetime.now(timezone.utc).isoformat()
        print(stamp+' START '+label,flush=True)
        result=fn()
        state['steps'].append({'name':label,'started_utc':stamp,'finished_utc':datetime.now(timezone.utc).isoformat()})
        save(runtime/'training-status.json',state)
        print(state['steps'][-1]['finished_utc']+' COMPLETE '+label,flush=True)
        return result
    try:
        frozen=json.loads((root/'training-freeze.json').read_text())
        for relative,expected in frozen['relative_sha256'].items():
            if sha(root/relative)!=expected: raise ValueError('Frozen input/source changed: '+relative)
        from prediction.improve import transformer,baselines
        def synthetic_tests():
            suite=unittest.defaultTestLoader.loadTestsFromNames([
                'prediction.improve.test_data','prediction.improve.test_baselines','prediction.improve.test_transformer'])
            result=unittest.TextTestRunner(verbosity=2).run(suite)
            if not result.wasSuccessful() or result.skipped:
                raise RuntimeError('Fleet synthetic verification failed or skipped required Torch checks')
        step('synthetic_verification',synthetic_tests)
        common=dict(model_path=str(root/'model'/frozen['model_revision']),model_manifest=str(root/'model/manifest.json'),
                    fleet_run_id=name,data=str(root/'data/data.json'),protocol=str(root/'transformer-protocol.json'))
        step('transformer_technical_preflight',lambda:reuse_or_run('technical_preflight',runtime/'model-preflight.json',
            lambda:transformer.preflight(SimpleNamespace(**common,out=str(runtime/'model-preflight.json')))))
        step('baseline_training',lambda:reuse_or_run('baselines',root/'baselines/completion.json',
            lambda:baselines.run_worker(root/'data/data.json',root/'data/folds.json',root/'baselines',name),partial_folder=root/'baselines'))
        step('transformer_training',lambda:transformer.run(SimpleNamespace(**common,folds=str(root/'data/folds.json'),
             out=str(root/'transformer'),embedding_cache=str(root/'embedding-cache'),max_runtime_seconds=remaining(),
             methods='both',fold_ids=['all'],resume=a.resume)))
        scopes=json.loads((root/'prospective-design/scopes.json').read_text())
        for scope in scopes:
            sid=scope['scope_id'];setting='fresh_full' if sid=='full' else 'fresh_family_excluded'
            metadata=root/'prospective-design/scopes'/sid/'queries.json'
            baseline_out=root/'fresh-forecasts/baselines'/sid/'forecasts.jsonl'
            step('baseline_fresh_'+sid,lambda sid=sid,metadata=metadata,setting=setting,baseline_out=baseline_out:reuse_or_run(
                'baseline_fresh_'+sid,baseline_out.with_suffix('.manifest.json'),
                lambda:baselines.forecast(root/'baselines/fits.json',metadata,baseline_out,setting,sid),
                output=baseline_out,partial_folder=baseline_out.parent))
            for method in ('frozen','lora'):
                forecast_out=root/'fresh-forecasts'/method/sid
                step(method+'_fresh_'+sid,lambda sid=sid,metadata=metadata,setting=setting,method=method,forecast_out=forecast_out:reuse_or_run(
                    method+'_fresh_'+sid,forecast_out/'forecast-manifest.json',lambda:transformer.forecast(
                    SimpleNamespace(model_path=common['model_path'],model_manifest=common['model_manifest'],fleet_run_id=name,
                        fit=str(root/'transformer'/method/sid),metadata=str(metadata),split=setting,
                        out=str(forecast_out),embedding_cache=str(root/'embedding-cache'),max_runtime_seconds=remaining())),
                    output=forecast_out/'forecasts.jsonl',partial_folder=forecast_out))
        for relative,expected in frozen['relative_sha256'].items():
            if sha(root/relative)!=expected: raise ValueError('Frozen input/source changed during job: '+relative)
        state.update(status='complete',finished_utc=datetime.now(timezone.utc).isoformat())
        save(runtime/'training-status.json',state)
    except BaseException as e:
        state.update(status='error',error_type=type(e).__name__,message=str(e),finished_utc=datetime.now(timezone.utc).isoformat())
        save(runtime/'training-status.json',state);traceback.print_exc();raise

if __name__=='__main__':
    main()
