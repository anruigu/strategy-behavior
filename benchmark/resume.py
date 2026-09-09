"""Resume a stopped model chain from its exact persisted playbook and game order.

A narrow, logged schema normalization handles the observed GLM top-level typo;
no hypothesis, evidence or strategy content is rewritten.
"""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
from types import SimpleNamespace
import uuid
import referee_spartan as SP
from .clients import write_json, now
from .prompts import parse_playbook
from .evaluator import evaluate
from .games import GAMES
from .experiment_runner import run_model, source_fingerprint


def recover_top_level_typo(out, model):
    model_dir=out/model
    staged=[]
    for p in model_dir.glob('traces/*.json'):
        t=json.loads(p.read_text())
        if 'playbook_after' not in t:
            staged.append((p,t))
    if not staged:
        return
    if len(staged)!=1:
        raise ValueError('Expected exactly one staged episode')
    path,t=staged[0]
    calls=[]
    for p in model_dir.glob('calls/*.json'):
        d=json.loads(p.read_text())
        if d['purpose']=='reflection' and d['attempts'] and 'response' in d['attempts'][-1]:
            calls.append((d['timestamp'],p,d))
    _,call_path,call=max(calls,key=lambda v:v[0])
    response=call['attempts'][-1]['response']
    raw=response['choices'][0]['message']['content']
    obj=json.loads(raw)
    if 'discoveries' in obj or 'discoverories' not in obj:
        raise ValueError('This recovery only handles the observed discoverories -> discoveries typo')
    obj['discoveries']=obj.pop('discoverories')
    structured=parse_playbook(json.dumps(obj,ensure_ascii=False))
    meta={'call_id':call_path.stem,'actual_model':response['model'],
          'timestamp':call['timestamp'],'finish_reason':response['choices'][0]['finish_reason'],
          'usage':response.get('usage'),
          'schema_normalization':{'discoverories':'discoveries'},'normalized_at':now()}
    game=GAMES[t['game_id']]
    ep=SimpleNamespace(**t['episode'])
    ep.scores={int(k):v for k,v in ep.scores.items()}
    turns=[SP.Turn(**turn) for turn in t['turns']]
    digest=SP.render_episode(game,ep,turns,0,max_chars=0)
    digest+='\n\nFinal referee resolution: '+t['episode']['extras']['final_state']['feedback']
    evidence=digest+'\n\nIncoming playbook:\n'+t['playbook_before']+'\n\nReflection:\n'+raw
    t.update(status='judge_failed',judge_error='Recovered reflection pending uniform discovery scoring',
             reflection=raw,reflection_meta=meta,reflection_prompt=call['request']['messages'],
             playbook_after=structured,execution=evaluate(t['game_id'],t['episode']['extras']['events']),
             discovery_evidence=evidence)
    write_json(path,t)
    write_json(model_dir/'playbooks'/f'{t["sequence"]:02d}.json',
               {k:v for k,v in t.items() if k in ('experiment_id','run_id','game_id','model_id','iteration','sequence')}
               | {'playbook':structured,'raw':raw,'meta':meta})
    print(f'Recovered reflection for {model}: {path.name}; hypothesis text unchanged',flush=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    ap.add_argument('--models',nargs='+',required=True)
    ap.add_argument('--recover-top-level-typo',action='store_true')
    ap.add_argument('--reflection-max-tokens',type=int)
    args=ap.parse_args()
    config=json.loads((args.output/'config.json').read_text())
    original=SimpleNamespace(**config['args'])
    if args.reflection_max_tokens:
        original.reflection_max_tokens=args.reflection_max_tokens
    for model in args.models:
        if model not in config['orders']:
            raise ValueError(model)
        if args.recover_top_level_typo:
            recover_top_level_typo(args.output,model)
        rec=args.output/model/'recovery'/uuid.uuid4().hex
        rec.mkdir(parents=True)
        failure=args.output/model/'failure.json'
        if failure.exists():
            failure.replace(rec/'original_failure.json')
        write_json(rec/'config.json',{'timestamp':now(),'source_fingerprints':source_fingerprint(),
                   'resume':'Retain completed episodes and exact playbooks; continue original order.',
                   'effective_args':vars(original), 'transport_timeout_seconds':600})
        run_model(model,original,args.output,config['orders'][model],resume=True)
    return 0

if __name__=='__main__':
    raise SystemExit(main())
