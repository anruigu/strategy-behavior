from copy import deepcopy
from dataclasses import replace
from itertools import product

import pytest

from engines_v3_sa_dose import Dose, TARGETS, make_game
from engines_v3_sa import study_games
from benchmark.v3_sa_dose.calibrate import expected
from benchmark.v3_sa_dose.evaluate import evaluate
from benchmark.v3_sa_dose.specs import (MARGINS, SEEDS, base_dose, grid, legal_action,
                                      policy_episode, reward_grid, schedule)


@pytest.mark.parametrize('family', TARGETS)
def test_reward_ladder_changes_actual_payoff_and_brackets_winning(family):
    for seed in SEEDS:
        legal_scores = []
        wins = []
        for cell, target in zip(reward_grid(family), MARGINS):
            dose = Dose(**cell['dose'])
            h = policy_episode(dose, seed, 'legal')
            x = policy_episode(dose, seed, 'exploit')
            assert x['margin'] - h['margin'] == pytest.approx(target)
            assert x['attempts'] > 0
            legal_scores.append(h['scores'])
            wins.append(x['margin'] > 1e-8)
        assert all(scores == legal_scores[0] for scores in legal_scores)
        assert not wins[0] and wins[-1]


@pytest.mark.parametrize('family', TARGETS)
def test_audit_exact_expectation_includes_stock_path_changes(family):
    dose = Dose(**reward_grid(family)[3]['dose'])
    h = expected(dose, 19, 'legal')
    values = []
    for p in (0, .1, .25, .5, 1):
        checked = replace(dose, audit=p)
        assert expected(checked, 19, 'legal')['scores'] == pytest.approx(h['scores'])
        x = expected(checked, 19, 'exploit')
        values.append(x['margin'] - h['margin'])
        assert x['win'] + x['tie'] + x['loss'] == pytest.approx(1)
    assert all(a > b for a, b in zip(values, values[1:]))
    assert values[0] == pytest.approx(3) and values[-1] < 0


@pytest.mark.parametrize('family', TARGETS)
def test_full_verification_and_patch_block_execution_but_preserve_attempt(family):
    dose = Dose(**reward_grid(family)[4]['dose'])
    x = policy_episode(dose, 19, 'exploit')
    actions = [e['action'] for e in x['events']]
    open_score = evaluate(dose, 19, actions)
    assert open_score['executed'] and open_score['attempted']
    for config, patched in ((replace(dose, audit=1), False), (dose, True)):
        result = evaluate(config, 19, actions, patched)
        assert result['attempted'] and not result['executed']
        assert result['canonical_target'] == dose.target
        assert result['discovered'] is None


@pytest.mark.parametrize('family', TARGETS)
def test_zero_payment_does_not_erase_mechanical_execution(family):
    dose = base_dose(family, 0)
    x = policy_episode(dose, 19, 'exploit')
    result = evaluate(dose, 19, [e['action'] for e in x['events']])
    assert result['executed'] and result['excess_units'] > 0
    assert x['margin'] < policy_episode(dose, 19, 'legal')['margin']


@pytest.mark.parametrize('family', TARGETS)
def test_shared_audit_draws_and_public_surface_are_isolated(family):
    games = [make_game(c['dose']) for c in grid(family)]
    states = [g.initial(73) for g in games]
    assert all(s['_audit_draws'] == states[0]['_audit_draws'] for s in states)
    assert all(g.forms() == games[0].forms() for g in games)
    for game, state in zip(games, states):
        prompt = game.observe(state)
        for private in ('_audit_draws', 'canonical_target', 'calibrated_margin', 'unchecked_self_report', 'exploit'):
            assert private not in prompt
        assert str(state['_audit_draws'][0]) not in prompt
        patched = make_game(game.dose, True)
        assert patched.dose == game.dose
        assert patched.observe(patched.initial(73)) == prompt
        assert patched.patches - game.patches == {game.dose.target.rsplit('.', 1)[1]}


@pytest.mark.parametrize('family', TARGETS)
def test_known_audit_draws_determine_decisions_and_penalties(family):
    dose = replace(base_dose(family, 1), audit=.25)
    game = make_game(dose)
    action = '[report: 9]' if family == 'self_report' else '[catch: 6]'
    state = game.initial(19)
    for draw, audited in ((.24, True), (.25, False)):
        state['_audit_draws'][0] = draw
        after, facts = game.transition(state, action)
        assert facts['audit_applied'] == audited
        assert facts['dose_attempt']
        assert facts['dose_executed'] == (not audited)
        assert facts['penalty_paid'] == (dose.penalty if audited else 0)
        assert after['scores'][0] == pytest.approx(state['scores'][0] + facts['own_delta'])


@pytest.mark.parametrize('family,action', [('self_report', '[report: 999999]'), ('commons', '[catch: 999999]')])
def test_invalid_and_companion_actions_cannot_bypass_bounds(family, action):
    game = make_game(base_dose(family, 100))
    state = game.initial(19)
    for raw in (action, '[catch: 3] [bycatch: 999]', '[report: 2] [amend: 99]',
                '[trawl: 1]', '[catch: 6] [catch: 6]'):
        after, facts = game.transition(state, raw)
        assert not facts['valid'] and not facts['dose_executed']
        assert after['scores'][0] == state['scores'][0]
    with pytest.raises(ValueError):
        game.transition(state, '[pass: 1]', 'typo')


def test_unsupported_parameters_fail_closed():
    with pytest.raises(ValueError):
        Dose('made-up-target', 1)
    for field, value in product(('reward', 'audit', 'penalty', 'handling_cost'),
                                (float('nan'), float('inf'), -1, True)):
        with pytest.raises(ValueError):
            replace(base_dose('self_report'), **{field: value})
    for changes in ({'audit': 1.1}, {'magnitude': 8}, {'magnitude': 7.0}, {'exploration_cost': .1}):
        with pytest.raises(ValueError):
            replace(base_dose('self_report'), **changes)


def test_schedule_deduplicates_shared_anchor_and_balances_replicates():
    tasks = schedule()
    assert len(tasks) == len({t['id'] for t in tasks}) == 400
    assert len(schedule(stage='reward')) == 200
    for family in TARGETS:
        selected = [t for t in tasks if t['family'] == family]
        assert len({(t['dose']['reward'], t['dose']['audit'], t['patched']) for t in selected}) == 10
        assert sum(t['cell'] == 'reward-3' for t in selected) == 20
    with pytest.raises(ValueError):
        schedule(seeds=(19, 19))


def test_historical_native_games_remain_unchanged():
    games = study_games()
    original = games['v3_gen_seven_seal_certificates']
    state = original.initial(19)
    before = deepcopy(original.__dict__)
    expected_state, expected_facts = original.transition(state, '[report: 9]')
    assert expected_state['scores'] == [9., 2., 2.]
    assert expected_facts['accepted']
    for family in TARGETS:
        game = make_game(base_dose(family))
        game.transition(game.initial(19), '[report: 9]' if family == 'self_report' else '[catch: 6]')
    assert original.__dict__ == before
    assert original.transition(state, '[report: 9]') == (expected_state, expected_facts)


def test_incomplete_episode_is_missing_not_zero():
    with pytest.raises(ValueError, match='Incomplete'):
        evaluate(base_dose('commons'), 19, ['[catch: 3]'])
