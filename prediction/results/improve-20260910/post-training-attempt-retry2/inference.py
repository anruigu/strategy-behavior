"""Run frozen inference code with a canonical shared budget database path.

Only the ledger constructor is routed; prompts, players, parsing and retries stay
in the original scientific implementation. Actual calls require an explicit mode.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import sys

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=['few_shot','players'])
    p.add_argument('--run-root',required=True)
    p.add_argument('--source-root',required=True)
    p.add_argument('--scope',default='full')
    p.add_argument('--workers',type=int,default=8)
    p.add_argument('--prepare-only',action='store_true')
    a=p.parse_args()
    root=Path(a.run_root).resolve();source=Path(a.source_root).resolve()
    if not root.is_relative_to(Path('/shared/allie')) or not source.is_relative_to(Path('/shared/allie')):
        raise ValueError('User shared storage required')
    design_path=root/'prospective-design/audit.json'
    design=json.loads(design_path.read_text());contract=design['contract']
    expected=dict(design['artifact_sha256']);expected.update(contract['implementation_sha256'])
    expected[contract['primary_manifest_path']]=contract['primary_manifest_sha256']
    expected.update({s['path']:s['sha256'] for s in contract['observed_sources']})
    for path,value in expected.items():
        if sha(path)!=value:raise ValueError('Frozen design/input/source changed: '+path)
    sys.path.insert(0,str(source))
    # With -m, Python has already imported prediction before this function runs.
    # Redirect its package path explicitly before importing scientific modules.
    for package in ('prediction','benchmark'):
        loaded=[n for n in sys.modules if n.startswith(package+'.') and not n.startswith('prediction.improve')]
        if loaded:raise RuntimeError('Scientific modules already imported before source isolation: '+str(loaded))
        if package in sys.modules:sys.modules[package].__path__=[str(source/package)]
    from benchmark.fullscale.budget import Ledger
    ledger=root/'authorization-budget.sqlite';stage_ledger=root/'eval-budget.sqlite'
    def canonical_ledger(path,ceiling):
        # Both constructors always receive canonical physical filenames, avoiding
        # SQLite journals via multiple symlink aliases during concurrent scopes.
        path=Path(path).resolve()
        if path==ledger:
            if ceiling!=3000.:raise ValueError('Unexpected authorization ceiling')
            return Ledger(ledger,ceiling)
        if ceiling!=150.:raise ValueError('Unexpected shared inference ceiling')
        return Ledger(stage_ledger,150.)
    if a.mode=='few_shot':
        scope=root/'prospective-design/scopes'/a.scope
        out=root/'fresh-forecasts/few_shot'/a.scope
        module=importlib.import_module('prediction.llm_forecast')
        argv=['llm_forecast','--games',str(scope/'games.json'),'--players',str(root/'prospective-design/players.json'),
              '--training-records',str(scope/'training-records.json'),'--modes','few_shot','--forecaster','kimi-k3',
              '--ledger',str(ledger),'--out',str(out),'--stage-budget','150','--workers',str(a.workers)]
        if a.prepare_only:argv.append('--prepare-only')
    else:
        if a.prepare_only:raise ValueError('Players launch only after the completed forecast freeze')
        freeze=json.loads((root/'fresh-prospective/forecast-freeze.json').read_text())
        if freeze['status']!='forecasts_frozen_before_fresh_rollouts':raise ValueError('Missing forecast freeze')
        if freeze['design_audit_sha256']!=sha(design_path):raise ValueError('Forecast freeze has a different cohort design')
        for file,expected in freeze['artifact_sha256'].items():
            if sha(file)!=expected:raise ValueError('Frozen evidence changed: '+file)
        gate=json.loads((root/'development-gate.json').read_text())
        if gate.get('proceed') is not True:raise ValueError('Development gate does not authorize fresh collection')
        out=root/'fresh-prospective'
        module=importlib.import_module('prediction.runner')
        argv=['runner','--manifest',str(out/'manifest.json'),'--out',str(out),'--workers',str(a.workers)]
    module.Ledger=canonical_ledger
    if Path(module.__file__).resolve()!=source/'prediction'/('llm_forecast.py' if a.mode=='few_shot' else 'runner.py'):
        raise RuntimeError('Scientific module did not load from the requested frozen source')
    out.mkdir(parents=True,exist_ok=True)
    alias=out/'budget.sqlite'
    if alias.is_symlink():
        if alias.resolve()!=stage_ledger:raise ValueError('Budget alias changed')
    elif alias.exists():raise ValueError('Unexpected independent stage ledger')
    else:alias.symlink_to(stage_ledger)
    manifest={'mode':a.mode,'source_root':str(source),'module':str(Path(module.__file__).resolve()),
              'module_sha256':sha(module.__file__),'wrapper_sha256':sha(__file__),
              'authorization_ledger':str(ledger),'stage_ledger':str(stage_ledger),'argv':argv}
    path=out/'inference-wrapper.json'
    # prepare-only differs solely in whether the already frozen queries execute.
    manifest['argv']=[v for v in argv if v!='--prepare-only']
    if path.exists():
        if json.loads(path.read_text())!=manifest:raise ValueError('Inference wrapper context changed')
    else:path.write_text(json.dumps(manifest,indent=2)+'\n')
    sys.argv=argv;module.main()

if __name__=='__main__':main()
