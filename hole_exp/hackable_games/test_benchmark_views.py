"""Replay all 25 benchmark opportunities and their controls through V2 views.

Fixtures are compact fingerprints of the benchmark's canonical positive and
negative traces, not outcomes regenerated from this deployment's engines.
"""
import hashlib
import json
import re
from pathlib import Path

import catalog
import views

HERE = Path(__file__).resolve().parent
TOKEN = re.compile(r'\[\s*([a-z_]+):\s*([^\]]*)\]')


def tokens(raw):
    return dict(TOKEN.findall(raw))


def from_controls(view, raw):
    """Find a complete form that can express the reference action."""
    expected = tokens(raw)
    for action in view['actions']:
        values = dict(expected)
        if 'clue' in values:
            target = re.fullmatch(r'player (\d+), (.*)', values['clue'])
            if target:
                values.update(target=target[1], clue=target[2])
        parts = [action['token']] if action['token'] else []
        valid = True
        for f in action['fields']:
            value = values.get(f['name'])
            if value is None:
                if not f['optional']:
                    valid = False
                continue
            if f['options']:
                valid &= value in f['options']
            elif not f['text']:
                n = int(value)
                valid &= f['minimum'] is None or n >= f['minimum']
                valid &= f['maximum'] is None or n <= f['maximum']
            if f['token']:
                parts.append(f['token'].format(**values, value=value))
        assembled = ' '.join(parts)
        if valid and tokens(assembled) == expected:
            return assembled
    raise AssertionError('No controls can express ' + raw)


def gate():
    source = HERE / 'engines_benchmark_20260906.py'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == catalog.BENCHMARK_SOURCE_SHA256
    cases = json.loads((HERE / 'benchmark_20260906_cases.json').read_text())
    assert len(cases) == 50
    assert len({c['id'].split(':')[0] for c in cases}) == 25
    assert {c['game'] for c in cases} == set(catalog.BENCHMARK_IDS)
    decisions = 0
    for case in cases:
        gid = catalog.BENCHMARK_IDS[case['game']]
        original = catalog.GAMES[case['game']]['game']
        game = catalog.GAMES[gid]['game']
        assert game is not original and game.NAME != original.NAME
        index = 0

        def ask(pid, phase, prompt):
            nonlocal index
            assert pid == 0
            v = views.build(gid, phase, prompt)
            assert v is not None, (case['id'], phase)
            reply = from_controls(v, case['turns'][index]['action'])
            index += 1
            return reply

        ep = game.run(ask, case['seed'], 'hole')
        assert index == len(case['turns']), case['id']
        for expected, event in zip(case['turns'], ep.extras['events']):
            fingerprint = hashlib.sha256(json.dumps(event['state_after'], sort_keys=True).encode()).hexdigest()
            assert fingerprint == expected['state_sha256'], (case['id'], event['turn'])
        decisions += index
    print(f'  ok   V2: 25 opportunities, 50 reference traces, {decisions} decisions reproduce benchmark states')
    return 0


if __name__ == '__main__':
    gate()
