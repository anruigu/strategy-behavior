from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

import pytest

from benchmark.clients import write_json
from benchmark.fullscale.budget import BudgetExceeded
from benchmark.v3_sa_dose.client import billed_cost
from benchmark.v3_sa_dose.run import CONFIGS, execute, file_hash, read, verify_trace
from benchmark.v3_sa_dose.specs import SYSTEM, digest, schedule
from benchmark.v3_sa_dose.plot import collect, report, wilson
from benchmark.v3_sa_dose.calibrate import calibrate


@pytest.fixture
def design(tmp_path):
    model = 'gpt-5.6-sol'
    tasks = schedule((model,), (19,), 'reward')
    calibration = calibrate((19,), 'reward')
    write_json(tmp_path / 'calibration.json', calibration)
    plan = dict(protocol='v3-SA-dose.1', stage='reward', models={model: asdict(CONFIGS[model])},
                tasks=tasks, system=SYSTEM, max_tokens=16384, max_decisions=8, source_hashes={},
                calibration_sha256=file_hash(tmp_path / 'calibration.json'))
    plan['identity'] = digest(plan)
    write_json(tmp_path / 'plan.json', plan)
    return tmp_path, plan, next(t for t in tasks if t['family'] == 'commons')


class Fake:
    def __init__(self, action='[catch: 6]', fail_at=None, status='ok', budget=False):
        self.action, self.fail_at, self.status, self.budget = action, fail_at, status, budget
        self.calls = []

    def generate(self, messages, **kwargs):
        self.calls.append(deepcopy(messages))
        if self.fail_at == len(self.calls):
            if self.budget:
                raise BudgetExceeded('test reservation denied')
            raise RuntimeError('test transport failure')
        return self.action, dict(status=self.status)


def test_complete_episode_replays_and_never_resamples(design):
    out, plan, task = design
    client = Fake()
    trace = execute(task, out, plan, lambda *args: client)
    assert trace['status'] == 'complete' and len(client.calls) == 8
    assert trace['metrics']['attempted']
    verify_trace(trace, task, plan)
    def no_call(*args):
        pytest.fail('Completed episode was resampled')
    assert execute(task, out, plan, no_call) == trace
    assert len(client.calls[-1]) == 16
    assert all(m['content'] != 'hint' for m in client.calls[-1])


def test_transport_recovery_preserves_accepted_context_and_is_bounded(design):
    out, plan, task = design
    first = Fake(fail_at=3)
    failed = execute(task, out, plan, lambda *args: first)
    assert failed['status'] == 'failed' and len(failed['turns']) == 2
    second = Fake(fail_at=1)
    assert execute(task, out, plan, lambda *args: second)['status'] == 'failed'
    assert not second.calls
    failed_again = execute(task, out, plan, lambda *args: second, recover=True)
    assert failed_again['recovery_count'] == 1
    assert second.calls[0] == first.calls[2]
    final = Fake()
    assert execute(task, out, plan, lambda *args: final, recover=True)['status'] == 'failed'
    assert not final.calls


def test_budget_pause_can_resume_without_spending_recovery_allowance(design):
    out, plan, task = design
    first = Fake(fail_at=3, budget=True)
    paused = execute(task, out, plan, lambda *args: first)
    assert paused['status'] == 'budget_paused'
    second = Fake()
    trace = execute(task, out, plan, lambda *args: second)
    assert trace['status'] == 'complete' and trace['recovery_count'] == 0
    assert len(second.calls) == 6 and second.calls[0] == first.calls[2]


def test_refusals_are_missing_and_not_retried(design):
    out, plan, task = design
    client = Fake(status='refusal')
    failed = execute(task, out, plan, lambda *args: client)
    assert failed['status'] == 'failed' and 'metrics' not in failed
    execute(task, out, plan, lambda *args: client, recover=True)
    assert len(client.calls) == 1
    data, _ = collect(out)
    assert all(c['n'] == 0 and c['rate'] is None for c in data['cells'])


def test_changed_context_or_dose_cannot_reuse_checkpoint(design):
    out, plan, task = design
    execute(task, out, plan, lambda *args: Fake(fail_at=3))
    altered = deepcopy(task)
    altered['dose']['reward'] += 1
    with pytest.raises(ValueError, match='identity'):
        execute(altered, out, plan, lambda *args: Fake(), recover=True)
    path = out / 'episodes' / task['id'] / 'decision-01.json'
    item = read(path)
    item['reply'] = '[catch: 0]'
    write_json(path, item)
    with pytest.raises(ValueError, match='prefix'):
        execute(task, out, plan, lambda *args: Fake(), recover=True)


def test_plot_handles_partial_and_zero_observations_and_exports(design):
    out, plan, task = design
    no_data = report(out)
    assert no_data['completion'] == {'not_started': 10}
    execute(task, out, plan, lambda *args: Fake(action='[catch: 3]'))
    data = report(out)
    observed = [c for c in data['cells'] if c['n']]
    assert len(observed) == 1 and observed[0]['rate'] == 0
    assert all(c['rate'] is None for c in data['cells'] if not c['n'])
    for name in ('reward_response', 'payoff_calibration'):
        for extension in ('png', 'svg', 'pdf'):
            assert (out / 'plots' / f'{name}.{extension}').stat().st_size > 100
    assert (out / 'plots' / 'dose-cells.csv').exists()
    assert wilson(0, 0) == (None, None)
    assert wilson(0, 5)[1] > 0


def test_cost_accounting_includes_byok_and_preserves_unknown_costs():
    raw = {'usage': {'cost': .01, 'cost_details': {'upstream_inference_cost': .05}}}
    assert billed_cost(raw, 'openrouter') == .05
    assert billed_cost(raw, 'flt') == 0
    assert billed_cost({'usage': {}}, 'openrouter') is None
    assert billed_cost({'usage': {'cost': float('nan')}}, 'openrouter') is None


def test_wilson_error_bars_enclose_observed_rate_at_every_pilot_count():
    for n in range(1, 201):
        for k in range(n + 1):
            low, high = wilson(k, n)
            assert 0 <= low <= k / n <= high <= 1
    assert wilson(0, 3)[0] == 0
    assert wilson(3, 3)[1] == 1
