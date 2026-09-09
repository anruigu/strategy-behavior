"""Run four-repeat chains using the existing SPaRTan round and playbook machinery."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import random
import sys
from importlib.metadata import version as package_version
import traceback
import uuid

import referee_spartan as SP
import referee_games as RG
from . import ROOT, VERSION
from .clients import MODELS, ModelClient, now, write_json
from .games import GAMES, GAME_IDS
from .specs import SPECS, IMPLEMENTED
from .coverage_matrix import PROPOSED
from .prompts import reflection_prompt, REFLECTION_SYSTEM, parse_playbook
from .evaluator import evaluate
from .discovery import judge, model_articulation


def source_fingerprint():
    files = sorted((ROOT / 'benchmark').glob('*.py')) + [ROOT/'hole_exp'/p for p in
             ('referee_spartan.py','referee_games.py','referee_games2.py',
              'hackable_games/engines_generated.py','hackable_games/engines_textarena.py')]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def run_model(model_id, args, out, order, client_factory=ModelClient, judge_fn=judge, resume=False):
    model_dir = out / model_id
    model_dir.mkdir(parents=True, exist_ok=resume)
    client = client_factory(MODELS[model_id], model_dir/'calls')
    judge_client = client_factory(MODELS[args.judge], model_dir/'judge_calls')
    book = SP.Playbook(0, '', ())
    sequence = 0
    completed = []
    for game_index, game_id in enumerate(order):
        if args.scope == 'within-game':
            book = SP.Playbook(0, '', ())
        game = GAMES[game_id]
        for iteration in range(1, args.iterations+1):
            sequence += 1
            run_id = uuid.uuid4().hex
            trace_path = model_dir / 'traces' / f'{game_index+1:02d}-{game_id}-{iteration}.json'
            incoming = book if args.condition == 'persistent' else SP.Playbook(0, '', ())
            seed = args.seed * 10000 + GAME_IDS.index(game_id)*100 + iteration
            context = {'experiment_id': out.name, 'run_id': run_id, 'game_id': game_id,
                       'model_id': model_id, 'iteration': iteration, 'sequence': sequence,
                       'game_order_index': game_index, 'seed': seed, 'condition': args.condition,
                       'scope': args.scope, 'engine_version': game.ENGINE_VERSION,
                       'timestamp': now(), 'model_config': asdict(MODELS[model_id])}
            if resume and trace_path.exists():
                old = json.loads(trace_path.read_text())
                if 'playbook_after' not in old:
                    raise ValueError(f'Recover the unfinished reflection before resuming: {trace_path}')
                if old['playbook_before'] != incoming.text:
                    raise ValueError('Resume playbook differs from the recorded chain')
                book = SP.Playbook(sequence, json.dumps(old['playbook_after'], ensure_ascii=False),
                                   tuple(dict.fromkeys((*incoming.games, game_id))))
                completed.append(str(trace_path))
                print(f'[{model_id}] resume: retained {game_id} {iteration}', flush=True)
                continue
            captured = {}
            def make_ask(system):
                messages = [{'role': 'system', 'content': system}]
                def ask(pid, phase, observation):
                    messages.append({'role':'user','content':observation})
                    text, meta = client.generate(messages, max_tokens=getattr(args, 'play_max_tokens', 8192), purpose='play')
                    messages.append({'role':'assistant','content':text})
                    ask.last_meta = meta
                    return text
                return ask
            def on_episode(g, ep, turns, pb, chain, rnd, ep_i, books=None):
                captured.update(episode=asdict(ep), turns=[asdict(t) for t in turns],
                                playbook_before=pb.text, system_prompt=pb.system(RG.WINMAX_SYSTEM))
                write_json(trace_path, {**context, **captured, 'status':'played'})
            try:
                _, digests = SP.run_round(game, make_ask, [seed], incoming,
                         max_chars=0, base_system=RG.WINMAX_SYSTEM, seed0=args.seed,
                         on_episode=on_episode)
                # Include terminal public feedback, which has no subsequent action prompt.
                digests[0] += '\n\nFinal referee resolution: ' + captured['episode']['extras']['final_state']['feedback']
                reflection, reflection_meta, reflection_messages, structured = '', None, [], None
                if args.condition != 'no_reflection':
                    reflection_messages = [{'role':'system','content':REFLECTION_SYSTEM},
                            {'role':'user','content':reflection_prompt(game_id, digests, incoming.text)}]
                    for repair in range(2):
                        reflection, reflection_meta = client.generate(reflection_messages,
                                                 max_tokens=getattr(args, 'reflection_max_tokens', 8192), purpose='reflection')
                        try:
                            structured = parse_playbook(reflection)
                            break
                        except (ValueError, KeyError, TypeError) as exc:
                            if repair:
                                raise
                            reflection_messages += [{'role':'assistant','content':reflection},
                                {'role':'user','content':f'Return the complete playbook JSON, repairing this schema error: {exc}'}]
                    book = SP.Playbook(sequence, json.dumps(structured, ensure_ascii=False),
                                       tuple(dict.fromkeys((*incoming.games, game_id))))
                    write_json(model_dir/'playbooks'/f'{sequence:02d}.json',
                               {**context,'playbook':structured,'raw':reflection,'meta':reflection_meta})
                rows = evaluate(game_id, captured['episode']['extras']['events'])
                evidence = digests[0] + '\n\nIncoming playbook:\n' + incoming.text + '\n\nReflection:\n' + reflection
                # Persist before judging; a failed judge cannot erase a completed game/reflection.
                trace = {**context, **captured, 'status':'played' if args.condition == 'no_reflection' else 'reflected', 'reflection':reflection,
                         'reflection_meta':reflection_meta, 'reflection_prompt':reflection_messages,
                         'playbook_after':structured, 'execution':json.loads(json.dumps(rows)), 'discovery_evidence':evidence}
                write_json(trace_path, trace)
                try:
                    judged = (judge_fn(judge_client, game_id, evidence, rows, articulation=model_articulation(trace))
                              if judge_fn is judge else judge_fn(judge_client, game_id, evidence, rows))
                    mapping = {j['exploit_id']:j for j in judged['judgments']}
                    for row in rows:
                        row.update(mapping[row['exploit_id']])
                        row.update(context)
                    trace.update(status='complete', evaluation=rows, discovery_judge=judged)
                except Exception as exc:
                    trace.update(status='judge_failed', judge_error=str(exc))
                write_json(trace_path, trace)
                completed.append(str(trace_path))
                print(f'[{model_id}] {game_id} {iteration}/{args.iterations}: '
                      f'{trace["status"]}, score={captured["episode"]["scores"][0]}, '
                      f'executed={sum(r["executed"] for r in rows)}, success={sum(r["successful"] for r in rows)}', flush=True)
            except Exception as exc:
                write_json(model_dir/'failure.json', {**context,'error':str(exc),'traceback':traceback.format_exc(),
                                                      'completed_traces':completed})
                raise
    write_json(model_dir/'complete.json', {'model_id':model_id,'completed':len(completed), 'timestamp':now()})
    return model_id


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--models', nargs='+', choices=MODELS, default=list(MODELS))
    ap.add_argument('--games', nargs='+', choices=GAME_IDS, default=list(GAME_IDS))
    ap.add_argument('--iterations', type=int, default=4)
    ap.add_argument('--condition', choices=['no_reflection','fresh','persistent'], default='no_reflection')
    ap.add_argument('--scope', choices=['within-game','cross-game'], default='cross-game')
    ap.add_argument('--seed', type=int, default=906)
    ap.add_argument('--judge', choices=MODELS, default='claude-haiku-4.5')
    ap.add_argument('--workers', type=int, default=6)
    ap.add_argument('--play-max-tokens', type=int, default=8192)
    ap.add_argument('--reflection-max-tokens', type=int, default=8192)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if args.iterations < 1 or args.workers < 1:
        ap.error('iterations and workers must be positive')
    out = args.output or ROOT/'benchmark'/'results'/(now().replace(':','').replace('+','-')+'-'+uuid.uuid4().hex[:8])
    out.mkdir(parents=True, exist_ok=False)
    orders = {}
    for model in args.models:
        order = list(args.games)
        stable = int(hashlib.sha256(model.encode()).hexdigest()[:8],16)
        random.Random(args.seed+stable).shuffle(order)
        orders[model] = order
    write_json(out/'config.json', {'experiment_id':out.name, 'version':VERSION,
               'started':now(), 'runtime': {'python':sys.version,'openai':package_version('openai')}, 'args':{**vars(args),'output':str(out)}, 'orders':orders,
               'model_configs':{m:asdict(MODELS[m]) for m in args.models},
               'source_fingerprints':source_fingerprint(),
               'randomness':'Seeded environments; temperature=0, provider sampling seed unsupported/unset; exact model reproducibility not guaranteed.',
               'opponents':'deterministic scripted; one focal live model per game',
               'discovery_judge':asdict(MODELS[args.judge])})
    write_json(out/'exploit_specs.json', [asdict(s) for s in SPECS])
    write_json(out/'coverage.json', {'proposed':PROPOSED,'implemented':IMPLEMENTED})
    # Snapshot exact sources because this research checkout can change during sampling.
    for relative in source_fingerprint():
        dest = out/'source'/relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((ROOT/relative).read_bytes())
    failures = []
    with ThreadPoolExecutor(max_workers=min(args.workers,len(args.models))) as pool:
        futures = {pool.submit(run_model, m, args, out, orders[m]):m for m in args.models}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                failures.append({'model':futures[future], 'error':str(exc)})
                print(f'FAILED {futures[future]}: {exc}', flush=True)
    write_json(out/'status.json', {'finished':now(), 'failures':failures})
    from .reports import build_report
    summary = build_report(out)
    if summary['scored_games'] != summary['expected_games'] and not failures:
        failures.append({'stage':'discovery_judge','error':'Some games are not fully scored; inspect trace statuses.'})
        write_json(out/'status.json', {'finished':now(), 'failures':failures})
    if args.condition == 'no_reflection':
        from .fresh_profiles import read_traces, plot
        plot(out, out/'model_profiles', read_traces(out))
    print(f'Results: {out}', flush=True)
    return int(bool(failures))

if __name__ == '__main__':
    raise SystemExit(main())
