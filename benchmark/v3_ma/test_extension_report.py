from dataclasses import asdict

import pytest

from benchmark.v3_ma.dose_games import Dose, make_game
from benchmark.v3_ma.extension_report import aggregate_dose, dose_metrics, paired_cross


def test_attempts_are_not_silently_replaced_with_enforced_execution():
    game = make_game(Dose('commons', 2, 1))
    ep = game.run(lambda pid, phase, prompt: '[catch: 6]' if pid == 0 else '[catch: 2]', 19, 'hole')
    metrics = dose_metrics(asdict(ep))
    assert metrics['attempts'] == 4
    assert metrics['executions'] == metrics['positive_extra_payments'] == 0
    assert all(r['realized_delta'] == -3 for r in metrics['rounds'])


def test_filing_extraction_can_fail_despite_an_attempt_in_each_round():
    game = make_game(Dose('filing', 1.6, 0))
    def ask(pid, phase, prompt):
        if '"name": "partner"' in prompt:
            return '[partner: 1] [claim: 7]' if pid == 0 else '[partner: -1] [claim: 2]'
        return '[redeem: yes]'
    metrics = dose_metrics(asdict(game.run(ask, 19, 'hole')))
    assert metrics['attempts'] == 4
    assert metrics['executions'] == 0
    assert not any(r['paired'] for r in metrics['rounds'])


def test_opponent_weights_and_wholly_missing_anchor():
    def row(opponent, attempts, status='complete'):
        return dict(id=str(attempts)+opponent, focal='test', opponent=opponent,
                    dose=dict(family='commons', reward=1, audit=0), status=status,
                    dose_metrics=dict(attempts=attempts, executions=attempts, positive_extra_payments=attempts,
                        attempted_episode=bool(attempts), attempted_first=bool(attempts), attempted_last=bool(attempts)))
    rows = [row('qwen-3.8-27b', 4), row('glm', 0), row('glm', 0)]
    cell = aggregate_dose(rows)[0]
    assert cell['complete'] == 3 and cell['attempted_rounds'] == 4 and cell['rounds'] == 12
    assert cell['attempt_rate'] == .5  # Each opponent has half the target weight.
    cell = aggregate_dose([rows[0], row('glm', 0, 'failed')])[0]
    assert cell['attempt_rate'] is None
    assert cell['attempt_rate_by_opponent']['qwen-3.8-27b'] == 1


def test_crossplay_panels_use_identical_complete_pairs():
    def row(seed, condition, status):
        return dict(game='v3ma_trust_pledge', focal='a', opponent='b', seed=seed,
                    condition=condition, status=status)
    rows = [row(0, 'ordinary', 'complete'), row(0, 'nerfed', 'complete'),
            row(1, 'ordinary', 'complete'), row(1, 'nerfed', 'failed')]
    assert paired_cross(rows) == rows[:2]
