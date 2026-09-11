from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path

import pytest

from engines_v3_ma import GAMES, parse
from bots_v3_ma import Scripted, observation, tokens
from benchmark.v3_ma.specs import LEGACY, ORDINARY, system
from benchmark.v3_ma.validate import curves, witness_modes
from benchmark.v3_ma.evaluate import diagnostics


@pytest.mark.parametrize('gid', list(GAMES))
def test_every_seat_uses_validated_callback_and_board(gid):
    import views
    game = GAMES[gid]
    called = set()
    bot = Scripted(witness_modes(game))
    def ask(pid, phase, prompt):
        called.add(pid)
        board = views.build(gid, phase, prompt)
        assert board and board['kind'] == 'v3_move'
        assert board['public_state']['seat'] == pid
        assert board['actions']
        assert all('token' in f for f in board['actions'][0]['fields'])
        return bot(pid, phase, prompt)
    ep = game.run(ask, 0, 'hole')
    assert called == set(range(game.N_PLAYERS))
    assert set(ep.scores) == called
    assert all(x is None for x in ep.gain.values())
    assert diagnostics(ep) == diagnostics(json.loads(json.dumps(asdict(ep))))


@pytest.mark.parametrize('gid', list(GAMES))
def test_witness_has_positive_measured_effect(gid):
    g = GAMES[gid]
    modes = witness_modes(g)
    ep = g.run(Scripted(modes), 0, 'hole')
    if g.CONTROL == 'policy':
        control = g.run(Scripted({**modes, 1: 'defensive'}), 0, 'hole')
    else:
        control = g.run(Scripted(modes), 0, 'nohole')
    assert ep.scores[0] > control.scores[0]


@pytest.mark.parametrize('gid', [k for k, g in GAMES.items() if g.CONTROL == 'referee'])
def test_reference_honest_scores_unchanged_by_referee_control(gid):
    g = GAMES[gid]
    assert g.run(Scripted(), 0, 'hole').scores == g.run(Scripted(), 0, 'nohole').scores


def test_simultaneous_seats_cannot_observe_current_actions():
    g = GAMES['v3ma_commons_collapse']
    observations = {}
    def run(focal_action):
        def ask(pid, phase, prompt):
            t = observation(prompt)
            if t['round'] == 1:
                observations[(focal_action, pid)] = prompt
            return tokens(catch=focal_action if pid == 0 else 2)
        return g.run(ask, 0, 'hole')
    run(2)
    run(6)
    for p in (1, 2):
        assert observations[(2, p)] == observations[(6, p)]


@pytest.mark.parametrize('variant', ['notes', 'convention'])
def test_signal_private_mark_and_future_marks_do_not_leak(variant):
    g = GAMES['v3ma_signal_' + variant]
    s = g.initial(0)
    altered = deepcopy(s)
    altered['targets'] = [3 - x for x in s['targets']]
    assert g.observe(s, 1, 'play', 'hole') == g.observe(altered, 1, 'play', 'hole')
    altered['targets'][0] = s['targets'][0]
    assert g.observe(s, 0, 'clue', 'hole') == g.observe(altered, 0, 'clue', 'hole')


def test_market_value_private_until_offer_and_future_values_hidden():
    g = GAMES['v3ma_market_value']
    s = g.initial(0)
    altered = deepcopy(s)
    altered['values'] = [10 - x for x in s['values']]
    assert g.observe(s, 1, 'trade', 'hole') == g.observe(altered, 1, 'trade', 'hole')
    altered['values'][0] = s['values'][0]
    assert g.observe(s, 0, 'announce', 'hole') == g.observe(altered, 0, 'announce', 'hole')


def test_message_delivery_is_private_and_does_not_choose_moves():
    g = GAMES['v3ma_trust_messages']
    s = g.initial(0)
    s['arm'] = 'hole'
    g.resolve(s, 'communicate', {0: dict(target='1', message='secret marker: cooperate'),
                               1: dict(target='0', message='none'), 2: dict(target='0', message='none')})
    assert 'secret marker' in g.observe(s, 1, 'act', 'hole')
    assert 'secret marker' not in g.observe(s, 2, 'act', 'hole')
    facts = g.resolve(s, 'act', {p: dict(move='D') for p in range(3)})
    assert facts['moves'] == {0: 'D', 1: 'D', 2: 'D'}


def test_coalition_requires_both_signatures():
    for variant in ('attestation', 'settlement'):
        g = GAMES['v3ma_filing_' + variant]
        solo = g.run(Scripted({0: 'exploit'}), 0, 'hole')
        pair = g.run(Scripted({0: 'exploit', 1: 'exploit'}), 0, 'hole')
        assert solo.scores[0] < 0 < pair.scores[0]
        assert all(not e['facts']['partnerships'] for e in solo.extras['events'] if e['stage'] == 'sign')


def test_all_four_regimes_use_same_other_player_actions():
    expected = {'abundant': [3, 3, 3], 'crowded': [1, -5/7, -23/21],
                'collapse': [3, 3, 3], 'threshold': [-1, 3, 3]}
    for row in curves():
        variant = row['scenario'].split('_')[-1]
        assert len(row['profiles']) == 8
        assert len(row['deviations']) == 12
        for d in row['deviations']:
            assert d['delta'] == pytest.approx(expected[variant][len(d['other_exploiters'])])
        if variant == 'collapse':
            assert row['all_exploit_welfare'] == -3
            assert row['all_honest_welfare'] == 6


def test_ordinary_nerf_and_defensive_focal_systems_identical():
    for gid, g in GAMES.items():
        if g.family == 'commons':
            continue
        assert system(gid, 'ordinary', 0) == system(gid, 'nerfed', 0) == system(gid, 'defensive', 0) == ORDINARY
        assert system(gid, 'ordinary', 1) != system(gid, 'nerfed', 1)
    assert system('v3ma_trust_messages', 'nerfed', 2) == ORDINARY
    assert system('v3ma_market_ceiling', 'nerfed', 2) != ORDINARY


def test_failed_action_is_never_replaced_with_a_scripted_move():
    g = GAMES['v3ma_commons_abundant']
    for bad in ('[catch: 99]', '[catch: 2] [catch: 6]', '[noop: 0]', ''):
        with pytest.raises(ValueError):
            g.run(lambda *_: bad, 0, 'hole')
    with pytest.raises(ValueError):
        GAMES['v3ma_trust_retaliation'].run(Scripted(), 0, 'nohole')


def test_suite_scope_and_legacy_mapping():
    from benchmark.suites import manifest
    from engines_v3_sa import GAMES as sa, TARGET_IDS
    root = Path(__file__).resolve().parents[2]
    targets = json.loads((root/'benchmark/results/gemini-revised45-20260909/targets.json').read_text())
    assert list(TARGET_IDS) == targets
    assert len(sa) == 17
    assert len(LEGACY) == 11 and all('v3ma_' + x in GAMES for x in LEGACY.values())
    assert len(GAMES) == 14 and len({g.family for g in GAMES.values()}) == 5
    assert len(manifest()['v3-SA']['canonical_target_ids']) == 45
    for g in sa.values():
        assert 'coalition_kingmaking' in g.patches


def test_public_catalogue_has_both_sets_without_private_instructions():
    from play_server import public_catalogue
    catalogue = public_catalogue()
    assert len([g for g in catalogue if g['edition'] == 'v3-sa']) == 17
    ma = [g for g in catalogue if g['edition'] == 'v3-ma']
    assert len(ma) == 14 and all(g['board'] for g in ma)
    assert 'nerfed' not in json.dumps(ma) and 'M3' not in json.dumps(ma)
