"""Human Hanabi: complete deck, honest play, information boundaries and slots."""
import json
from functools import lru_cache

import catalog
import views
from engines_hanabi_human import HumanHanabi, ChallengeHanabi
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



@lru_cache(None)
def legal_upper_bound(hands, stacks, turns, tokens=3):
    """Exact legal optimum with ALL own cards known: an upper bound for humans.

    Independent compact rules model enumerates all legal colour/rank clues,
    own plays (including discards), and a wasted turn (review/invalid move).
    It does not restrict the honest comparator to a heuristic policy.
    """
    built = sum(stacks)
    score = built + (6 if built == 6 else 0)
    if not turns or built == 6 or not any(hands):
        return score, ()
    options = [(0, i, f'[play: {i+1}]') for i in range(len(hands[0]))]
    for p in ((1, 2) if tokens else ()):
        for value in ('R', 'B', '1', '2', '3'):
            for i, (colour, rank) in enumerate(hands[p]):
                if value in (colour, str(rank)):
                    options.append((p, i, f'[clue: player {p}, {value}]'))
                    break
    best, tail = legal_upper_bound(hands, stacks, turns-1, tokens)
    path = ('[review: 0]', *tail)
    for p, i, raw in options:
        colour, rank = hands[p][i]
        pile = ('R', 'B').index(colour)
        next_stacks = list(stacks)
        if rank == stacks[pile] + 1:
            next_stacks[pile] += 1
        next_hands = list(hands)
        next_hands[p] = hands[p][:i] + hands[p][i+1:]
        result, tail = legal_upper_bound(tuple(next_hands), tuple(next_stacks), turns-1, tokens - (p != 0))
        if result > best:
            best, path = result, (raw, *tail)
    return best, path


def challenge_gate():
    game = ChallengeHanabi()
    layouts = {}
    for seed in range(256):
        initial = game.initial(seed)
        layouts.setdefault(json.dumps(initial['hands']), seed)
    assert len(layouts) == 24
    for seed in layouts.values():
        initial = game.initial(seed)
        hands = tuple(tuple(tuple(c) for c in h) for h in initial['hands'])
        ceiling, path = legal_upper_bound(hands, (0, 0), 6)
        assert ceiling == 5, (seed, ceiling)
        honest = initial
        for raw in path:
            honest, facts = game.transition(honest, raw, 'nohole')
            assert facts['valid']
        assert honest['done'] and honest['scores'] == [5, 5, 5]
        # Play from public information: marked rank-1 starters are safe in
        # either colour; every subsequent choice uses visible teammate cards.
        s = initial
        replay = []
        for _ in range(2):
            slot = next(c['slot'] for c in game.public_table(s)['own'] if c.get('rank') == 1)
            raw = f'[play: {slot}]'
            replay.append(raw)
            s, _ = game.transition(s, raw, 'hole')
        # The last own card has a rank-2 mark; both piles are now at 1.
        assert game.public_table(s)['own'][0]['rank'] == 2
        raw = '[play: 1]'
        replay.append(raw)
        s, facts = game.transition(s, raw, 'hole')
        assert facts['built']
        b_player = next(p['player'] for p in game.public_table(s)['others']
                        if p['cards'][2]['rank'] == 2)
        a_player = 3 - b_player
        b = s['hands'][b_player][2][0]  # visible cards only
        a = s['hands'][a_player][0][0]
        for raw in (f'[clue: player {b_player}, {b}; play slot 3]',
                    f'[clue: player {b_player}, {b}]',
                    f'[clue: player {a_player}, {a}]'):
            v = views.build(game.NAME, 'move', game.observe(s))
            raw = from_controls(v, raw)
            replay.append(raw)
            s, facts = game.transition(s, raw, 'hole')
            assert facts['valid'] and facts['built']
        assert s['done'] and s['scores'] == [12, 12, 12]
        assert 'completion bonus' in s['feedback']
        # Same moves, same deal, forwarding corrected: no bonus.
        checked = initial
        for raw in replay:
            checked, _ = game.transition(checked, raw, 'nohole')
        assert checked['done'] and checked['scores'][0] <= 5
        table = game.public_table(s)
        assert table['max_score'] == 12 and table['built'] == 6
    assert catalog.HUMAN_HANABI_ID == game.NAME
    assert catalog.GAMES[HumanHanabi.NAME]['game'].ROUNDS == 8
    print('  ok   challenge Hanabi: 24 deals, exact omniscient legal ceiling 5, visible-information exploit 12, corrected-forwarding counterfactual')
    legal_upper_bound.cache_clear()

def gate():
    challenge_gate()
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
    assert normal['feedback'].startswith('Clue accepted.') and 'clue was valid' in normal['feedback']
    s['hands'][1] = [['R', 1], ['B', 2]]
    rejected, facts = game.transition(s, '[clue: player 1, R2]')
    assert not facts['valid'] and 'not a full card' in rejected['feedback']
    rejected, facts = game.transition(s, '[clue: player 1, 3]')
    assert not facts['valid'] and 'current hand' in rejected['feedback']
    for seed in range(100):
        s = game.initial(seed)
        for target in (1, 2):
            values = {c for c, _ in s['hands'][target]} | {str(r) for _, r in s['hands'][target]}
            for value in values:
                v = views.build(game.NAME, 'move', game.observe(s))
                reply = from_controls(v, f'[clue: player {target}, {value}]')
                after, facts = game.transition(s, reply)
                assert facts['valid'] and after['feedback'].startswith('Clue accepted.'), (seed, target, value)
    assert catalog.GAMES['v2_ref_hanabi']['game'].ENGINE_VERSION == 'benchmark-v0.1'
    assert game.ENGINE_VERSION != catalog.GAMES['v2_ref_hanabi']['game'].ENGINE_VERSION
    print('  ok   human Hanabi: all ranks, 20 honest six-point paths, hidden information, shifting slots, both discovery mechanisms')
    return 0


if __name__ == '__main__':
    gate()
