from dataclasses import asdict
import json

import pytest

from benchmark.v3_ma.campaign import CONFIGS, ROSTER, schedule
from benchmark.v3_ma.report import marker, report
from benchmark.v3_ma.validate import witness_modes
from bots_v3_ma import Scripted
from engines_v3_ma import GAMES


def test_schedule_matches_approved_four_model_screen():
    rows = schedule('main')
    assert len(rows) == 768 and len({r['id'] for r in rows}) == 768
    assert len(schedule('pilot')) == 16
    assert {r['seed'] for r in rows} == {0, 1}
    assert {r['focal'] for r in rows} == set(ROSTER)
    assert all(r['arm'] == 'hole' for r in rows)
    assert all(c.temperature is None for c in CONFIGS.values())
    for r in rows:
        assert r['condition'] != 'nerfed' or GAMES[r['game']].family != 'commons'


@pytest.mark.parametrize('gid', list(GAMES))
def test_markers_reach_witness_and_do_not_flag_honest_policy(gid):
    game = GAMES[gid]
    witness = marker(asdict(game.run(Scripted(witness_modes(game)), 0, 'hole')))
    honest = marker(asdict(game.run(Scripted(), 0, 'hole')))
    assert witness['episode_marker'], witness
    assert not honest['episode_marker'], honest


def test_failed_pairs_do_not_enter_payoff_denominator(tmp_path):
    game = GAMES['v3ma_trust_memory']
    tasks = [dict(game=game.NAME, focal='a', opponent='b', seed=seed, condition=condition,
                  id=f'{seed}-{condition}', arm='hole') for seed in (0, 1) for condition in ('ordinary', 'nerfed')]
    (tmp_path/'plan.json').write_text(json.dumps(dict(protocol='test', tasks=tasks)))
    for task in tasks:
        directory = tmp_path/'episodes'/task['id']
        directory.mkdir(parents=True)
        if task['id'] == '1-nerfed':
            trace = dict(status='failed', decisions=[], error='test failure')
        else:
            modes = {0: 'exploit', 1: 'nerfed' if task['condition'] == 'nerfed' else 'defensive'}
            trace = dict(status='complete', decisions=[], episode=asdict(game.run(Scripted(modes), 0, 'hole')))
        (directory/'trace.json').write_text(json.dumps(trace))
    result = report(tmp_path)
    assert result['outcomes'] == {'complete': 3, 'failed': 1}
    assert result['games'][0]['matched_pairs'] == 1
    assert result['games'][0]['planned_pairs'] == 2
    assert result['games'][0]['paired_payoff_delta'] == 20
