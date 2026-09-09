"""Regression checks for coverage denominators and judge-independent behavior."""
import json
from types import SimpleNamespace

from benchmark.coverage_matrix import CATEGORIES
from benchmark.detailed_plots import Cube, GROUPS, cumulative, fixed_rate, load_data
from benchmark.references import play


def test_groups_are_exactly_the_requested_partition():
    categories = [c for group in GROUPS.values() for c in group]
    assert len(categories) == len(set(categories)) == 14
    assert set(categories) == set(CATEGORIES)
    assert 'rule_precedence' in GROUPS['A. RULE / ENFORCEMENT']
    assert 'terminal_condition_rushing' in GROUPS['C. STATE / TIME']
    assert 'commitment_exploit' in GROUPS['D. MULTIPLAYER / OBJECTIVE']


def test_cumulative_keeps_positive_but_does_not_treat_missing_as_negative():
    assert cumulative([False, True, False, False]) == [False, True, True, True]
    assert cumulative([False, None, False, True]) == [False, None, None, True]
    assert cumulative([True, None, False]) == [True, True, True]
    assert fixed_rate([True, False]) == .5
    assert fixed_rate([True, None]) is None
    assert fixed_rate([]) is None


def test_coverage_is_not_execution_conditioned_on_discovery():
    specs = [SimpleNamespace(exploit_id=k) for k in ('one', 'two')]
    rows = []
    for i in (1, 2):
        for key in ('one', 'two'):
            rows.append(dict(model_id='m', exploit_id=key, iteration=i,
                             attempted=key == 'one', executed=key == 'one', successful=key == 'one',
                             discovered=key == 'two' and i == 1))
    cube = Cube(['m'], specs, 2, rows)
    assert cube.curve('m', specs, 'executed', 'current') == [.5, .5]
    assert cube.curve('m', specs, 'discovered', 'current') == [.5, 0]
    assert cube.curve('m', specs, 'discovered', 'cumulative') == [.5, .5]


def test_engine_results_survive_failed_judge(tmp_path):
    config = {'args': {'models': ['m'], 'games': ['ref_commons'], 'iterations': 1}}
    (tmp_path/'config.json').write_text(json.dumps(config))
    traces = tmp_path/'m'/'traces'
    traces.mkdir(parents=True)
    events = play('ref_commons', lambda s, i: '[catch: 27]')
    trace = dict(model_id='m', game_id='ref_commons', iteration=1, status='judge_failed',
                 episode={'extras': {'events': events, 'final_state': events[-1]['state_after']}})
    (traces/'game.json').write_text(json.dumps(trace))
    _, _, rows, meta = load_data(tmp_path)
    quota = next(r for r in rows if r['category'] == 'unenforced_limit')
    assert quota['attempted'] and quota['executed'] and quota['successful']
    assert quota['discovered'] is None
    assert meta['engine_games'] == 1 and meta['judged_games'] == 0
