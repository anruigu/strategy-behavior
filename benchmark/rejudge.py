"""Uniform v3 rescoring. Can follow a live run; no gameplay or playbook is changed."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time
import traceback
from .clients import ModelClient, MODELS, write_json, now
from .discovery import judge, model_articulation
from .reports import build_report
from .evaluator import evaluate

VERSION='discovery-v3-model-articulation'


def rescore(path, out, model):
    t=json.loads(path.read_text())
    if t.get('discovery_judge',{}).get('evaluator_version')==VERSION:
        return False
    client=ModelClient(MODELS[model],out/t['model_id']/'judge_v3_calls')
    evidence=t['discovery_evidence']
    deterministic=evaluate(t['game_id'],t['episode']['extras']['events'])
    result=judge(client,t['game_id'],evidence,deterministic,articulation=model_articulation(t))
    # Keep the original judge decision/error, including its raw call provenance.
    original=out/'evaluation_v1'/path.relative_to(out)
    if not original.exists():
        write_json(original,t)
    mapping={j['exploit_id']:j for j in result['judgments']}
    keys=('experiment_id','run_id','game_id','model_id','iteration','sequence',
          'game_order_index','seed','condition','scope','engine_version','timestamp','model_config')
    rows=[]
    for raw in deterministic:
        row={**raw,**mapping[raw['exploit_id']],**{k:t[k] for k in keys}}
        rows.append(row)
    result['source_sha256']=hashlib.sha256(Path(__file__).with_name('discovery.py').read_bytes()).hexdigest()
    result['rescored_at']=now()
    t.update(status='complete',execution=deterministic,evaluation=rows,discovery_judge=result)
    t.pop('judge_error',None)
    write_json(path,t)
    return True


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    ap.add_argument('--follow',action='store_true')
    ap.add_argument('--workers',type=int,default=6)
    args=ap.parse_args()
    out=args.output
    config=json.loads((out/'config.json').read_text())
    expected=len(config['args']['models'])*len(config['args']['games'])*config['args']['iterations']
    # Snapshot revised scoring implementation; the original run snapshot remains immutable.
    write_json(out/'evaluation_v3_config.json',{'version':VERSION,'started':now(),
              'judge':asdict(MODELS[config['args']['judge']]),
              'reason':'Require model-authored mechanism articulation; referee-only quotations cannot establish discovery.',
              'scope':'Every episode, not a selected subset; gameplay unchanged. Judge receives recomputed deterministic execution only, never previous discovery judgments.'})
    (out/'discovery_v3.py').write_bytes(Path(__file__).with_name('discovery.py').read_bytes())
    errors={}
    while True:
        todo=[]
        done=0
        for p in out.glob('*/traces/*.json'):
            t=json.loads(p.read_text())
            if t.get('discovery_judge',{}).get('evaluator_version')==VERSION:
                done+=1
            elif t['status'] in ('complete','judge_failed'):
                todo.append(p)
        if done==expected:
            break
        if todo:
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                fs={pool.submit(rescore,p,out,config['args']['judge']):p for p in todo}
                for future in as_completed(fs):
                    p=fs[future]
                    try:
                        if future.result():
                            done+=1
                            print(f'v3 {done}/{expected}: {p.parent.parent.name} {p.name}',flush=True)
                        errors.pop(str(p),None)
                    except Exception as exc:
                        errors[str(p)]=str(exc)
                        print(f'v3 ERROR {p.name}: {exc}',flush=True)
            build_report(out)
        if not args.follow or ((out/'status.json').exists() and not todo):
            break
        if errors and all(errors.get(str(p)) for p in todo) and (out/'status.json').exists():
            break
        time.sleep(10)
    summary=build_report(out)
    write_json(out/'evaluation_v3_status.json',{'finished':now(),'version':VERSION,
                'fully_rescored':done==expected,'rescored_games':done,'expected_games':expected,'errors':errors})
    print(f'v3 complete: {done}/{expected}',flush=True)
    return int(done!=expected)

if __name__=='__main__':
    raise SystemExit(main())
