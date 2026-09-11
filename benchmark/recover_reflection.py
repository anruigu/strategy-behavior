"""Recover a completed game whose reflection response failed; never replay gameplay."""
import argparse
import json
from pathlib import Path
from types import SimpleNamespace
import referee_spartan as SP
from .clients import ModelClient, MODELS, write_json, now
from .games import GAMES
from .evaluator import evaluate
from .prompts import parse_playbook


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    ap.add_argument('--model',required=True)
    ap.add_argument('--max-tokens',type=int,default=16384)
    args=ap.parse_args()
    d=args.output/args.model
    staged=[(p,json.loads(p.read_text())) for p in d.glob('traces/*.json') if 'playbook_after' not in json.loads(p.read_text())]
    if len(staged)!=1:
        raise ValueError(f'Expected one completed game pending reflection, found {len(staged)}')
    path,t=staged[0]
    calls=[json.loads(p.read_text()) for p in (d/'calls').glob('*.json')]
    previous=max((c for c in calls if c['purpose']=='reflection'),key=lambda c:c['timestamp'])
    messages=previous['request']['messages']
    original_messages=json.loads(json.dumps(messages))
    client=ModelClient(MODELS[args.model],d/'calls')
    for repair in range(3):
        raw,meta=client.generate(messages,max_tokens=args.max_tokens,purpose='reflection_recovery')
        try:
            book=parse_playbook(raw)
            break
        except (ValueError,TypeError,KeyError) as exc:
            if repair==2:
                raise
            messages += [{'role':'assistant','content':raw},
                         {'role':'user','content':f'Return the complete playbook JSON, repairing this schema error: {exc}'}]
    meta['recovery']={'original_failed_call':previous['call_id'],'original_prompt_unchanged':messages[:len(original_messages)]==original_messages,
                      'max_tokens':args.max_tokens,'transport_timeout_seconds':600,'timestamp':now()}
    ep=SimpleNamespace(**t['episode']);ep.scores={int(k):v for k,v in ep.scores.items()}
    digest=SP.render_episode(GAMES[t['game_id']],ep,[SP.Turn(**r) for r in t['turns']],0,max_chars=0)
    digest+='\n\nFinal referee resolution: '+ep.extras['final_state']['feedback']
    evidence=digest+'\n\nIncoming playbook:\n'+t['playbook_before']+'\n\nReflection:\n'+raw
    t.update(status='judge_failed',judge_error='Recovered reflection awaiting uniform discovery scoring',
             reflection=raw,reflection_meta=meta,reflection_prompt=messages,playbook_after=book,
             execution=evaluate(t['game_id'],ep.extras['events']),discovery_evidence=evidence)
    write_json(path,t)
    write_json(d/'playbooks'/f'{t["sequence"]:02d}.json',
               {k:t[k] for k in ('experiment_id','run_id','game_id','model_id','iteration','sequence')}
               | {'playbook':book,'raw':raw,'meta':meta})
    print(f'Recovered {args.model} {path.name}; {len(book["discoveries"])} playbook entries; game not replayed',flush=True)
    return 0

if __name__=='__main__':
    raise SystemExit(main())
