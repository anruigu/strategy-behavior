"""Verify frozen sources, accepted-call histories, and exact episode replays."""
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import re

from benchmark.clients import now, write_json
from benchmark.v3_ma.campaign import FORMAT
from benchmark.v3_ma.dose_games import make_game
from benchmark.v3_ma.specs import ORDINARY, system
from engines_v3_ma import GAMES, parse


def norm(value):
    return json.loads(json.dumps(value))


def verify(root):
    counts = Counter()
    errors = []
    outcomes = {}
    for stage in ('pilot', 'crossplay', 'dose'):
        plan_path = root/stage/'plan.json'
        if not plan_path.exists():
            continue
        plan = json.loads(plan_path.read_text())
        for path, digest in plan['source_hashes'].items():
            saved = root/stage/'source'/path
            for p in (Path(path), saved):
                if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
                    errors.append(f'Source mismatch: {p}')
                counts['source_hash_checks'] += 1
        statuses = Counter()
        for task in plan['tasks']:
            directory = root/stage/'episodes'/task['id']
            path = directory/'trace.json'
            if not path.exists():
                statuses['not_started'] += 1
                continue
            trace = json.loads(path.read_text())
            statuses[trace['status']] += 1
            if trace['status'] != 'complete':
                continue
            try:
                assert trace['task'] == task, 'Task identity changed'
                game = make_game(task['dose']) if stage == 'dose' else GAMES[task['game']]
                histories = {p: [] for p in range(game.N_PLAYERS)}
                valid = []
                for d in trace['decisions']:
                    pid = d['pid']
                    config = plan['models'][task['focal'] if pid == 0 else task['opponent']]
                    call = json.loads((directory/'calls'/(d['metadata']['call_id']+'.json')).read_text())
                    assert call['config'] == config, 'Call configuration mismatch'
                    expected_system = ORDINARY+FORMAT if stage == 'dose' else system(task['game'], task['condition'], pid)+FORMAT
                    assert trace['systems'][str(pid)] == expected_system, 'Wrong seat system'
                    request = call['request']
                    assert request['model'] == config['provider_model'], 'Requested route mismatch'
                    assert request['messages'][0] == dict(role='system', content=expected_system)
                    assert request['messages'][1:-1] == histories[pid], 'Seat history mismatch'
                    user = request['messages'][-1]
                    if d['correction_attempt'] == 0:
                        assert user == dict(role='user', content=d['observation'])
                    else:
                        assert 'No game action has occurred.' in user['content'], 'Wrong repair feedback'
                    histories[pid].extend([user, dict(role='assistant', content=d['reply'])])
                    response = call['attempts'][-1]['response']
                    assert response['choices'][0]['message']['content'] == d['reply'], 'Raw reply mismatch'
                    assert response['model'] == config['provider_model'], 'Unexpected actual model'
                    assert d['metadata']['status'] == 'ok', 'Nonaccepted provider response used'
                    forms = json.loads(re.search(r'^Actions: (.+)$', d['observation'], re.M)[1])
                    try:
                        parse(d['reply'], forms)
                        valid_format = True
                    except ValueError:
                        valid_format = False
                    assert valid_format == (not d['format_error']), 'Format classification mismatch'
                    if valid_format:
                        valid.append(d)
                    counts['accepted_call_history_checks'] += 1
                iterator = iter(valid)
                def replay(pid, phase, prompt):
                    d = next(iterator)
                    assert (pid, phase, prompt) == (d['pid'], d['phase'], d['observation']), 'Replayed observation mismatch'
                    return d['reply']
                episode = game.run(replay, task['seed'], task['arm'])
                assert next(iterator, None) is None, 'Unused recorded actions'
                assert norm(asdict(episode)) == trace['episode'], 'Episode replay differs'
                counts['exact_episode_replays'] += 1
            except Exception as exc:
                errors.append(f'{stage}/{task["id"]}: {type(exc).__name__}: {exc}')
        outcomes[stage] = dict(statuses)
    result = dict(updated=now(), passed=not errors, counts=dict(counts), outcomes=outcomes, errors=errors,
                  scope='Completed episodes only. Reconstruct isolated per-seat histories and replay every accepted game action without model calls.')
    write_json(root/'verification.json', result)
    print(json.dumps(result, indent=2))
    return not errors


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    raise SystemExit(0 if verify(args.out) else 1)
