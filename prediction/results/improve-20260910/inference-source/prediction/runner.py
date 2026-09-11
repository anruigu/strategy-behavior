"""Resumable autonomous simultaneous-play runner. No opponent action leaks."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from prediction.io_utils import digest, now, read_json, write_json
from prediction.client import Client, ModelConfig, Ledger, BudgetExceeded

SYSTEM = ('You are playing a repeated two-player game. Your objective is to maximize your own total points '
          'over all rounds. In each round choose one action simultaneously with the other player. '
          'Use the payoff table and the public history to choose. '
          'Reply with exactly A or B, with no explanation or extra text.')


def parse_action(reply):
    match = re.fullmatch(r'\s*([AB])\s*', reply)
    if not match:
        raise ValueError('Response must be exactly A or B')
    return 'AB'.index(match.group(1))


def messages_for(game, rounds, player, horizon, representation, swap):
    from prediction.games import render_game
    labels = ['B', 'A'] if swap else ['A', 'B']
    history = []
    for turn in rounds:
        history.append(f"Round {turn['round']}: you {labels[turn['actions'][player]]}, other {labels[turn['actions'][1-player]]}; "
                       f"your points {turn['payoffs'][player]:g}, other points {turn['payoffs'][1-player]:g}.")
    observation = (f'There are exactly {horizon} rounds. This is round {len(rounds)+1} of {horizon}. '
                   'The other player is an AI agent. Neither player sees the other current action before choosing.\n\n'
                   + render_game(game, representation=representation, swap=swap)
                   + '\n\nPublic history:\n' + ('\n'.join(history) if history else 'No rounds have been played.')
                   + '\n\nChoose A or B now.')
    return [dict(role='system', content=SYSTEM), dict(role='user', content=observation)]


def decision(client, messages, path, identity, max_attempts=2):
    expected = digest(dict(identity=identity, messages=messages))
    if path.exists():
        item = read_json(path)
        if item['context_sha256'] != expected or item['messages'] != messages:
            raise RuntimeError('Checkpoint context mismatch')
    else:
        item = dict(context_sha256=expected, messages=messages, attempts=[], status='pending')
    if item['status'] == 'complete':
        assert item['attempts'][-1]['meta']['status'] == 'ok'
        assert item['displayed_action'] == parse_action(item['attempts'][-1]['reply'])
        return item
    while len(item['attempts']) < max_attempts:
        reply, meta = client.generate(messages)
        attempt = dict(reply=reply, meta=meta)
        item['attempts'].append(attempt)
        if meta['status'] == 'ok':
            try:
                action = parse_action(reply)
                item.update(status='complete', displayed_action=action)
                write_json(path, item)
                return item
            except ValueError:
                attempt['parse_error'] = True
        write_json(path, item)
        if meta.get('http_status') in (401, 402, 403, 404):
            break
        if len(item['attempts']) < max_attempts:
            time.sleep(1)
    raise RuntimeError('No valid decision after bounded attempts: ' + str(path))


def episode(spec, game, manifest, out, clients, request_pool):
    from prediction.games import payoff
    path = out / 'episodes' / spec['id']
    identity = digest(dict(protocol=manifest['protocol'], game=game, spec=spec, configs=manifest['models'],
                           sources=manifest['sources']))
    trace_path = path / 'trace.json'
    if trace_path.exists():
        return verify_trace(trace_path, manifest)
    rounds = []
    trace = dict(id=spec['id'], identity_sha256=identity, game=game, models=spec['models'],
                 trial_id=spec['trial_id'], representation=spec['representation'], swap=spec['swap'],
                 status='incomplete', rounds=rounds, started=now())
    try:
        for round_no in range(1, manifest['protocol']['rounds']+1):
            # Build both prompts from the same completed public history before either request.
            messages = [messages_for(game, rounds, p, manifest['protocol']['rounds'], spec['representation'], spec['swap']) for p in range(2)]
            futures = [request_pool.submit(decision, clients[spec['models'][p]], messages[p],
                        path / f'round-{round_no:02}-player-{p}.json', identity,
                        manifest['protocol']['max_attempts']) for p in range(2)]
            items, failures = [], []
            for future in futures:
                try:
                    items.append(future.result())
                except Exception as exc:
                    items.append(None)
                    failures.append(exc)
            if failures:
                raise failures[0]
            actions = [item['displayed_action'] ^ int(spec['swap']) for item in items]
            scores = payoff(game, *actions)
            rounds.append(dict(round=round_no, actions=actions, payoffs=list(scores),
                               decisions=[f'round-{round_no:02}-player-{p}.json' for p in range(2)]))
            write_json(path / 'progress.json', trace)
    except Exception as exc:
        trace.update(error=type(exc).__name__ + ': ' + str(exc), updated=now())
        write_json(path / 'incomplete.json', trace)
        raise
    trace.update(status='complete', finished=now())
    write_json(trace_path, trace)
    return trace


def verify_trace(path, manifest):
    from prediction.games import payoff
    trace = read_json(path)
    games = {g['id']: g for g in manifest['games']}
    specs = {s['id']: s for s in manifest['episodes']}
    spec = specs[trace['id']]
    game = games[spec['game_id']]
    identity = digest(dict(protocol=manifest['protocol'], game=game, spec=spec, configs=manifest['models'], sources=manifest['sources']))
    assert trace['identity_sha256'] == identity and trace['game'] == game
    assert trace['models'] == spec['models'] and trace['status'] == 'complete'
    for field in ('trial_id', 'representation', 'swap'):
        assert trace[field] == spec[field]
    assert len(trace['rounds']) == manifest['protocol']['rounds']
    history = []
    for turn in trace['rounds']:
        assert turn['round'] == len(history)+1
        assert turn['payoffs'] == list(payoff(game, *turn['actions']))
        for player in range(2):
            item = read_json(path.parent / turn['decisions'][player])
            messages = messages_for(game, history, player, manifest['protocol']['rounds'], spec['representation'], spec['swap'])
            assert item['messages'] == messages
            assert item['context_sha256'] == digest(dict(identity=identity, messages=messages))
            assert item['status'] == 'complete'
            attempt = item['attempts'][-1]
            assert attempt['meta']['status'] == 'ok'
            assert parse_action(attempt['reply']) ^ int(spec['swap']) == turn['actions'][player]
            call = read_json(path.parents[2] / 'calls' / spec['models'][player] / (attempt['meta']['call_id']+'.json'))
            assert call['request']['messages'] == messages
            assert call['config'] == manifest['models'][spec['models'][player]]
            assert call['status'] == 'ok'
            assert call['request']['model'] == call['config']['provider_model']
            assert call['request']['max_tokens'] == manifest['protocol']['max_tokens']
            assert call['request'].get('temperature') == call['config']['temperature']
            assert call['request'].get('seed') == call['config']['seed']
            assert call['request']['extra_body']['reasoning'] == {'effort': call['config']['reasoning_effort']}
            if call['config']['provider'] == 'openrouter':
                assert call['request']['extra_body']['provider'] == {'max_price': {'prompt': 20, 'completion': 120, 'request': 0}}
            raw_choice = call['response']['choices'][0]
            assert raw_choice['finish_reason'] == 'stop'
            assert raw_choice['message']['content'] == attempt['reply']
            assert not raw_choice['message'].get('refusal')
            assert attempt['meta']['actual_model'] == call['response']['model']
            assert item['displayed_action'] == parse_action(attempt['reply'])
        history.append(turn)
    return trace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=32)
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    manifest = read_json(args.manifest)
    import hashlib
    for relative, expected in manifest['sources'].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative
    args.out.mkdir(parents=True, exist_ok=True)
    ledger = Ledger(manifest['ledger'], 3000.0)
    stage = Ledger(args.out / 'budget.sqlite', manifest['stage_budget_usd'])
    clients = {name: Client(ModelConfig(**config), args.out/'calls'/name, ledger, stage,
                            manifest['protocol']['max_tokens']) for name, config in manifest['models'].items()}
    games = {game['id']: game for game in manifest['games']}
    specs = manifest['episodes'][:args.limit] if args.limit else manifest['episodes']
    state = dict(status='running', started=now(), planned=len(specs), completed=0, errors=[], models=Counter())
    write_json(args.out/'status.json', state)
    stopping = threading.Event()
    def work(spec, pool):
        if stopping.is_set():
            raise RuntimeError('Stopped after budget guard')
        try:
            return episode(spec, games[spec['game_id']], manifest, args.out, clients, pool)
        except BudgetExceeded:
            stopping.set()
            raise
    with ThreadPoolExecutor(max_workers=64) as requests, ThreadPoolExecutor(max_workers=args.workers) as episodes:
        futures = {episodes.submit(work, spec, requests): spec for spec in specs}
        for future in as_completed(futures):
            spec = futures[future]
            try:
                future.result()
                state['completed'] += 1
                for model in spec['models']:
                    state['models'][model] += 1
            except Exception as exc:
                state['errors'].append(dict(episode=spec['id'], error=type(exc).__name__+': '+str(exc)))
            state.update(updated=now(), budget=stage.summary(), global_budget=ledger.summary())
            write_json(args.out/'status.json', state)
            print(json.dumps({k:state[k] for k in ('updated','completed','planned')}), flush=True)
    state.update(status='finished_with_errors' if state['errors'] else 'complete', finished=now())
    write_json(args.out/'status.json', state)


if __name__ == '__main__':
    main()
