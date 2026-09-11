"""Matched three-condition diagnostic, with resumable per-turn checkpoints.

Primary outcomes come exclusively from the deterministic engine evaluator.
The informed condition is an execution diagnostic, not spontaneous discovery.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import random
import time
import traceback
import uuid

import referee_games as RG
import referee_spartan as SP
from . import ROOT
from .clients import ModelClient, ModelConfig, MODELS, OPENROUTER, now, write_json
from .games import GAME_IDS
from .diagnostic_games import GAMES, HANABI_PROFILE, source_fingerprints, evaluate
from .specs import SPECS
from .prompts import reflection_prompt, REFLECTION_SYSTEM
from .diagnostic_prompts import CONDITIONS, GUIDES, PROBE_REFLECTION, intervention, parse_reflection

FRONTIER = {
 'claude-sonnet-5': ModelConfig('claude-sonnet-5', 'openrouter', 'anthropic/claude-sonnet-5', OPENROUTER, 'OPENROUTER_API_KEY', temperature=None, reasoning_effort='high'),
 'gpt-5': ModelConfig('gpt-5', 'openrouter', 'openai/gpt-5', OPENROUTER, 'OPENROUTER_API_KEY', temperature=None, reasoning_effort='high'),
 'gemini-3.1-pro': ModelConfig('gemini-3.1-pro', 'openrouter', 'google/gemini-3.1-pro-preview', OPENROUTER, 'OPENROUTER_API_KEY', temperature=0.0, reasoning_effort='high'),
}
REGISTRY = {**MODELS, **FRONTIER}


def run_chain(model, game_id, condition, args, out, client_factory=ModelClient):
    folder = out / condition / model
    folder.mkdir(parents=True, exist_ok=True)
    client = client_factory(REGISTRY[model], folder/'calls')
    prior = ''
    game = GAMES[game_id]
    for iteration in range(1, args.iterations+1):
        path = folder/'traces'/f'{game_id}-{iteration}.json'
        seed = args.seed*10000 + GAME_IDS.index(game_id)*100 + iteration
        t = json.loads(path.read_text()) if path.exists() else {
            'experiment_id': out.name, 'run_id': uuid.uuid4().hex, 'model_id': model,
            'model_config': asdict(REGISTRY[model]), 'game_id': game_id, 'condition': condition,
            'scope': 'within-game', 'iteration': iteration, 'sequence': iteration,
            'seed': seed, 'timestamp': now(), 'playbook_before': prior,
            'status': 'playing', 'turn_checkpoint': [], 'engine_version': game.ENGINE_VERSION}
        if t['playbook_before'] != prior or t['seed'] != seed or t['condition'] != condition:
            raise ValueError(f'Resume chain mismatch: {path}')
        if t['status'] == 'complete':
            prior = '' if condition == 'no_reflection' else json.dumps(t['playbook_after'], ensure_ascii=False)
            continue
        extra = intervention(condition, game_id, prior)
        base = RG.WINMAX_SYSTEM + extra
        incoming = SP.Playbook(0 if condition == 'no_reflection' else iteration-1, prior, (game_id,) if prior else ())
        actual_system = incoming.system(base)
        if 'system_prompt' in t and t['system_prompt'] != actual_system:
            raise ValueError(f'Resume system prompt changed: {path}')
        t.update(system_prompt=actual_system, intervention=extra)
        write_json(path, t)
        if 'episode' not in t or 'digest' not in t:
            def make_ask(system):
                assert system == actual_system
                messages = [{'role': 'system', 'content': system}]
                index = 0
                def ask(pid, phase, observation):
                    nonlocal index
                    messages.append({'role': 'user', 'content': observation})
                    if index < len(t['turn_checkpoint']):
                        saved = t['turn_checkpoint'][index]
                        if saved['prompt'] != observation or saved['pid'] != pid or saved['phase'] != phase:
                            raise ValueError('Checkpoint does not replay to the same observation')
                        reply, meta = saved['reply'], saved['meta']
                    else:
                        reply, meta = client.generate(messages, max_tokens=args.play_max_tokens, purpose='play')
                        t['turn_checkpoint'].append(dict(pid=pid, phase=phase, prompt=observation, reply=reply, meta=meta))
                        t['updated_at'] = now()
                        write_json(path, t)
                    messages.append({'role': 'assistant', 'content': reply})
                    index += 1
                    ask.last_meta = meta
                    return reply
                return ask
            def captured(g, ep, turns, pb, chain, rnd, epi, books=None):
                t.update(episode=asdict(ep), turns=[asdict(turn) for turn in turns], status='played')
                write_json(path, t)
            _, digests = SP.run_round(game, make_ask, [seed], incoming, max_chars=0,
                                     base_system=base, seed0=args.seed, on_episode=captured)
            t['digest'] = digests[0] + '\n\nFinal referee resolution: ' + t['episode']['extras']['final_state']['feedback']
            t['execution'] = evaluate(game_id, t['episode']['extras']['events'])
            write_json(path, t)
        if condition == 'no_reflection':
            t.update(status='complete', finished=now(), evaluation=t['execution'],
                     playbook_after=None, reflection_status='omitted_by_design',
                     discovery_status='not_scored',
                     discovery_note='No semantic judge; no post-game reflection or cross-episode memory.')
            write_json(path, t)
            print(f'{model} {condition} {game_id} {iteration}/{args.iterations}: complete', flush=True)
            continue
        if 'reflection_prompt' not in t:
            user = reflection_prompt(game_id, [t['digest']], prior)
            if condition == 'planned_test': user += PROBE_REFLECTION
            t['reflection_prompt'] = [{'role': 'system', 'content': REFLECTION_SYSTEM}, {'role': 'user', 'content': user}]
            write_json(path, t)
        messages = list(t.get('reflection_request', t['reflection_prompt']))
        for repair in range(3):
            # Reuse the saved response after interruption, rather than rerunning gameplay.
            if repair == 0 and t.get('reflection'):
                raw, meta = t['reflection'], t['reflection_meta']
            else:
                raw, meta = client.generate(messages, max_tokens=args.reflection_max_tokens, purpose='reflection')
                t.update(reflection=raw, reflection_meta=meta, reflection_request=messages)
                write_json(path, t)
            try:
                book = parse_reflection(raw, condition)
                break
            except (ValueError, TypeError, KeyError) as exc:
                if repair == 2: raise
                messages += [{'role': 'assistant', 'content': raw}, {'role': 'user', 'content': f'Return the complete playbook JSON, correcting this schema error: {exc}'}]
        t.update(status='complete', playbook_after=book, finished=now(), evaluation=t['execution'],
                 discovery_status='not_scored', discovery_note='No semantic judge in the primary diagnostic. Informed condition is not spontaneous discovery.')
        write_json(path, t)
        prior = json.dumps(book, ensure_ascii=False)
        print(f'{model} {condition} {game_id} {iteration}/{args.iterations}: score={t["episode"]["scores"]["0"] if "0" in t["episode"]["scores"] else t["episode"]["scores"][0]} attempted={sum(r["attempted"] for r in t["execution"])} executed={sum(r["executed"] for r in t["execution"])} successful={sum(r["successful"] for r in t["execution"])}', flush=True)
    return (model, game_id, condition)


def progress(out):
    traces = [json.loads(p.read_text()) for p in out.glob('*/*/traces/*.json')]
    return {'updated': now(), 'pid': os.getpid(), 'complete': sum(t['status']=='complete' for t in traces),
            'played': sum('episode' in t for t in traces), 'started': len(traces),
            'by_condition': {c: sum(t['status']=='complete' and t['condition']==c for t in traces) for c in (*CONDITIONS, 'no_reflection')}}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--models', nargs='+', choices=REGISTRY, default=list(FRONTIER))
    ap.add_argument('--conditions', nargs='+', choices=(*CONDITIONS, 'no_reflection'), default=['no_reflection'])
    ap.add_argument('--games', nargs='+', choices=GUIDES, default=['ref_exchange', 'ref_hanabi', 'ta_ipd'])
    ap.add_argument('--iterations', type=int, default=4)
    ap.add_argument('--seed', type=int, default=907)
    ap.add_argument('--workers', type=int, default=6)
    ap.add_argument('--play-max-tokens', type=int, default=16384)
    ap.add_argument('--reflection-max-tokens', type=int, default=16384)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--resume', action='store_true')
    args = ap.parse_args()
    if args.iterations < 1 or args.workers < 1: ap.error('iterations/workers must be positive')
    out = args.output.resolve()
    if args.resume:
        config = json.loads((out/'config.json').read_text())
        for key in ('models', 'games', 'iterations', 'seed', 'play_max_tokens', 'reflection_max_tokens'):
            if config['args'][key] != getattr(args, key): raise ValueError(f'Resume config mismatch: {key}')
        if config.get('conditions', list(CONDITIONS)) != args.conditions: raise ValueError('Resume conditions mismatch')
        for m in args.models:
            if config['model_configs'][m] != asdict(REGISTRY[m]): raise ValueError('Resume model settings changed')
        for name, fingerprint in config['source_fingerprints'].items():
            if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != fingerprint:
                raise ValueError(f'Source changed since launch: {name}; resume from the recorded source')
    else:
        out.mkdir(parents=True, exist_ok=False)
        config = {'experiment_id': out.name, 'started': now(), 'args': {**vars(args), 'output': str(out)},
                  'conditions': args.conditions, 'model_configs': {m: asdict(REGISTRY[m]) for m in args.models},
                  'source_fingerprints': source_fingerprints(), 'guides': GUIDES,
                  'hanabi_profile': HANABI_PROFILE,
                  'design': 'Matched environment seeds across conditions/models. Four within-game repetitions; one chain per cell. Independent condition memory. No sampling seeds; provider-default temperature where unsupported.',
                  'primary_metrics': 'Engine attempted, executed, successful and score; no judge dependency.',
                  'discovery': 'Not scored. Informed condition receives ground truth and cannot measure spontaneous discovery.'}
        write_json(out/'config.json', config)
        for relative in config['source_fingerprints']:
            dest = out/'source'/relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((ROOT/relative).read_bytes())
        write_json(out/'specs.json', [asdict(s) for s in SPECS if s.game_id in args.games])
    expected = len(args.models)*len(args.games)*len(args.conditions)*args.iterations
    write_json(out/'status.json', {**progress(out), 'state': 'running', 'expected': expected})
    tasks = [(m, g, c) for g in args.games for c in args.conditions for m in args.models]
    # Randomize scheduling to avoid always sampling one condition first.
    random.Random(args.seed).shuffle(tasks)
    failures = {}
    from .diagnostic_report import build_report
    for attempt in range(2):
        todo = tasks if attempt == 0 else list(failures)
        if not todo: break
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(run_chain, *task, args, out): task for task in todo}
            for future in as_completed(futures):
                task = futures[future]
                try:
                    future.result(); failures.pop(task, None)
                except Exception as exc:
                    failures[task] = str(exc)
                    print(f'CHAIN ERROR {task}: {exc}', flush=True)
                    write_json(out/'failures'/('-'.join(task)+'.json'), {'task': task, 'error': str(exc), 'traceback': traceback.format_exc(), 'at': now()})
                write_json(out/'status.json', {**progress(out), 'state': 'running', 'expected': expected, 'failures': [{'task': t, 'error': e} for t, e in failures.items()]})
                build_report(out, plots=False)
    final = progress(out)
    success = final['complete'] == expected and not failures
    write_json(out/'status.json', {**final, 'state': 'complete' if success else 'incomplete', 'expected': expected, 'failures': [{'task': t, 'error': e} for t, e in failures.items()]})
    build_report(out, plots=args.conditions != ['no_reflection'])
    if args.conditions == ['no_reflection']:
        from .fresh_profiles import read_traces, plot
        plot(out, out/'model_profiles', read_traces(out))
    print(f'Finished {final["complete"]}/{expected}: {out}', flush=True)
    return int(not success)

if __name__ == '__main__':
    raise SystemExit(main())
