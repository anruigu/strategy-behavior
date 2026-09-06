"""Human Hanabi: complete deck, honest play, information boundaries and slots."""
import json
from functools import lru_cache

import catalog
import views
from engines_hanabi_human import HumanHanabi
from test_benchmark_views import from_controls


def honest_completion(game, initial):
    """Find a six-point path using only visible cards and legitimate marks."""
    @lru_cache(None)
    def search(encoded):
        s = json.loads(encoded)
        if sum(s['stacks'].values()) == 6:
            return True
        if s['done']:
            return False
        actions = []
        for i, known in enumerate(s['known']):
            if 'colour' in known and known.get('rank') == s['stacks'][known['colour']] + 1:
                actions.append(f'[play: {i+1}]')
        for p in (1, 2):
            for val in ('R', 'B', '1', '2', '3'):
                matches = [c for c in s['hands'][p] if val in (c[0], str(c[1]))]
                if matches and matches[0][1] == s['stacks'][matches[0][0]] + 1:
                    actions.append(f'[clue: player {p}, {val}]')
        # A normal review can consume a turn while a teammate supplies a clue.
        actions.append('[review: 0]')
        for raw in actions:
            v = views.build(game.NAME, 'move', game.observe(s))
            move = from_controls(v, raw)
            after, facts = game.transition(s, move, 'nohole')
            assert facts['valid']
            if search(json.dumps(after, sort_keys=True)):
                return True
        return False
    return search(json.dumps(initial, sort_keys=True))


def gate():
    game = HumanHanabi()
    required = {(c, r) for c in ('R', 'B') for r in (1, 2, 3)}
    for seed in range(20):
        s = game.initial(seed)
        assert required <= {tuple(c) for hand in s['hands'] for c in hand}
        table = game.public_table(s)
        assert all('rank' not in card for card in table['own'])
        assert len(table['own']) == 3
        assert honest_completion(game, s), ('No honest six-point path', seed)

    s = game.initial(0)
    leaked, _ = game.transition(s, '[review: 0]', 'hole')
    checked, _ = game.transition(s, '[review: 0]', 'nohole')
    assert all(k == dict(colour=c, rank=r) for k, (c, r) in zip(leaked['known'], s['hands'][0]))
    assert any('rank' not in k or 'colour' not in k for k in checked['known'])
    after, _ = game.transition(leaked, '[play: 1]')
    assert after['hands'][0] == leaked['hands'][0][1:]
    assert after['known'] == leaked['known'][1:]
    v = views.build(game.NAME, 'move', game.observe(after))
    assert v['actions'][0]['fields'][0]['options'] == ['1', '2']

    s['hands'][1] = [['R', 2], ['R', 1], ['B', 3]]
    raw = '[clue: player 1, R; play slot 2]'
    v = views.build(game.NAME, 'move', game.observe(s))
    assembled = from_controls(v, raw)
    normal, _ = game.transition(s, '[clue: player 1, R]')
    carried, _ = game.transition(s, assembled, 'hole')
    checked, _ = game.transition(s, assembled, 'nohole')
    assert carried['scores'][0] == 1 and normal['scores'][0] == checked['scores'][0] == 0
    assert catalog.GAMES['v2_ref_hanabi']['game'].ENGINE_VERSION == 'benchmark-v0.1'
    assert game.ENGINE_VERSION != catalog.GAMES['v2_ref_hanabi']['game'].ENGINE_VERSION
    print('  ok   human Hanabi: all ranks, 20 honest six-point paths, hidden information, shifting slots, both discovery mechanisms')
    return 0


if __name__ == '__main__':
    gate()
