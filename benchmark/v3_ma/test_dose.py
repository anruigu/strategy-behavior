from copy import deepcopy
from dataclasses import asdict
from itertools import product
import json
import re

import pytest

from benchmark.v3_ma.dose_games import Dose, grid, make_game
from benchmark.v3_ma.dose_run import execute, schedule
from benchmark.v3_ma.extension import ROSTER, schedule as cross_schedule


def test_balanced_design_and_shared_reference():
    rows = schedule()
    assert len(rows) == len({r['id'] for r in rows}) == 576
    for model, family in product(ROSTER, ('commons', 'filing')):
        selected = [r for r in rows if r['focal'] == model and r['dose']['family'] == family]
        assert len(selected) == 36
        assert len({(r['dose']['reward'], r['dose']['audit']) for r in selected}) == 9
    cross = cross_schedule('crossplay')
    assert len(cross) == 1536
    assert len({(r['focal'], r['opponent']) for r in cross}) == 64


@pytest.mark.parametrize('cell', grid('commons'))
def test_commons_delta_enumerates_all_audit_realizations_and_opponent_actions(cell):
    dose = Dose(**cell['dose'])
    game = make_game(dose)
    for other in product(range(7), repeat=2):
        expected = 0
        for flags in product((False, True), repeat=3):
            prob = 1
            for audited in flags:
                prob *= dose.audit if audited else 1-dose.audit
            h = game.payoff([2, *other], flags)[1][0]
            x = game.payoff([6, *other], flags)[1][0]
            expected += prob * (x-h)
        assert expected == pytest.approx(dose.expected_delta)
    assert game.payoff([2, 2, 2], [True]*3)[1] == [2, 2, 2]


@pytest.mark.parametrize('cell', grid('filing'))
def test_filing_delta_requires_mutual_false_claim_and_averages_audit(cell):
    dose = Dose(**cell['dose'])
    game = make_game(dose)
    expected = 0
    for audited, prob in ((False, 1-dose.audit), (True, dose.audit)):
        s = game.initial(1)
        s['arm'] = 'hole'
        # Set controlled draw to obtain each branch independent of endpoint p.
        s['audit_draws'][0] = [-1 if audited else 2]*3
        game.resolve(s, 'sign', {0: {'partner': '1', 'claim': '7'},
                                1: {'partner': '0', 'claim': '7'},
                                2: {'partner': '-1', 'claim': '2'}})
        result = game.resolve(s, 'redeem', {p: {'redeem': 'yes'} for p in range(3)})
        expected += prob*(result['payoff'][0]-2)
    assert expected == pytest.approx(dose.expected_delta)
    s = game.initial(1)
    s['arm'] = 'hole'
    game.resolve(s, 'sign', {0: {'partner': '1', 'claim': '7'},
                            1: {'partner': '-1', 'claim': '2'},
                            2: {'partner': '-1', 'claim': '2'}})
    result = game.resolve(s, 'redeem', {p: {'redeem': 'yes'} for p in range(3)})
    assert result['payoff'] == [-3, 2, 2]


@pytest.mark.parametrize('family', ['commons', 'filing'])
def test_no_future_audits_or_research_metadata_in_public_observations(family):
    games = [make_game(c['dose']) for c in grid(family)]
    states = [g.initial(73) for g in games]
    assert all(s['audit_draws'] == states[0]['audit_draws'] for s in states)
    for g, s in zip(games, states):
        s['arm'] = 'hole'
        for seat in range(3):
            prompt = g.observe(s, seat, g.STAGES[0], 'hole')
            assert 'audit_draws' not in prompt
            assert 'expected_delta' not in prompt
            assert 'exploit' not in prompt.lower()


def test_fully_verified_commons_blocks_damage_and_retains_attempt():
    game = make_game(Dose('commons', 2, 1))
    caught, payoff = game.payoff([6, 2, 2], [True]*3)
    assert caught == [2, 2, 2]
    assert payoff == [-1, 2, 2]


def test_dose_runner_seat_isolation_repairs_and_does_not_repeat_complete(tmp_path):
    clients = []
    class Client:
        def __init__(self, *args):
            self.calls = 0
            clients.append(self)
        def generate(self, messages, **kwargs):
            self.calls += 1
            for message in messages:
                if message['role'] == 'user' and '\nTable:' in message['content']:
                    table = json.loads(re.search(r'^Table: (.+)$', message['content'], re.M)[1])
                    assert table['seat'] == clients.index(self)
            return ('[catch: 2] [oops: 1]' if self.calls == 1 else '[catch: 2]'), {'status': 'ok'}
    task = next(r for r in schedule() if r['dose']['family'] == 'commons')
    execute(task, tmp_path, Client)
    path = tmp_path/'episodes'/task['id']/'trace.json'
    trace = json.loads(path.read_text())
    assert trace['status'] == 'complete'
    assert trace['episode']['scores'] == {'0': 8, '1': 8, '2': 8}
    assert sum(bool(d['format_error']) for d in trace['decisions']) == 3
    assert trace['episode']['engine_version'] == 'ma-dose.1'
    execute(task, tmp_path, Client)
    assert len(clients) == 3
