"""Run the frozen SA plan in phases, refresh figures, and verify accepted calls."""
import argparse
from collections import Counter, deque
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import fcntl
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time


def refresh_figures(out, reporter, write_json, now):
    """A figure-export failure must not terminate the inference campaign."""
    try:
        reporter(out)
    except Exception as exc:
        write_json(out / 'plot-status.json', dict(updated=now(), status='failed',
                                                error_type=type(exc).__name__, error=str(exc)))
        print('Plot refresh failed:', type(exc).__name__, str(exc), flush=True)
        return False
    write_json(out / 'plot-status.json', dict(updated=now(), status='ok'))
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--budget-usd', type=float, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    if not math.isfinite(args.budget_usd) or args.budget_usd < 0:
        parser.error('Budget must be finite and nonnegative')
    sys.path.insert(0, str(out / 'source'))
    from benchmark.clients import now, write_json
    from benchmark.fullscale.budget import Ledger
    from benchmark.v3_sa_dose.client import Client
    from benchmark.v3_sa_dose.run import read, file_hash, verify_plan, verify_trace, execute

    # Analysis can be repaired without modifying frozen engine sources or task IDs.
    analysis = out / 'analysis-manifest.json'
    if analysis.exists():
        analysis_manifest = read(analysis)
        source = out / analysis_manifest['plot_source']
        if file_hash(source) != analysis_manifest['plot_sha256']:
            raise ValueError('Analysis source hash differs')
        spec = importlib.util.spec_from_file_location('benchmark.v3_sa_dose.plot', source)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    from benchmark.v3_sa_dose.plot import report

    lock = (out / '.campaign.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    plan = read(out / 'plan.json')
    verify_plan(out, plan)
    ledger = Ledger(out / 'budget.sqlite', args.budget_usd)
    started = now()
    manifest = dict(started=started, pid=os.getpid(), plan_identity=plan['identity'],
                    campaign_source_sha256=file_hash(__file__), budget_ceiling_usd=args.budget_usd,
                    analysis_manifest_sha256=file_hash(analysis) if analysis.exists() else None,
                    ordering='Reward first, then audit, then patched control; two active episodes per model.',
                    recovery='One explicit accepted-prefix recovery pass after each phase; refusals stay final.')
    write_json(out / f'launch-{os.getpid()}.json', manifest)
    last_plot = 0.0

    def refresh(phase, *, plot=False, final=False):
        nonlocal last_plot
        counts = Counter()
        by_model = {m: Counter() for m in plan['models']}
        accepted = 0
        for task in plan['tasks']:
            path = out / 'episodes' / task['id'] / 'trace.json'
            trace = read(path) if path.exists() else None
            status = trace['status'] if trace else 'not_started'
            counts[status] += 1
            by_model[task['model']][status] += 1
            accepted += len(trace['turns']) if trace else 0
        budget = ledger.summary()
        state = dict(started=started, updated=now(), pid=os.getpid(), phase=phase,
                     status='finished' if final else 'running', outcomes=counts, by_model=by_model,
                     accepted_decisions=accepted, planned=len(plan['tasks']), budget=budget)
        write_json(out / 'campaign.json', state)
        lines = ['**SA incentive-dose run**', '',
                 f'Updated {state["updated"]}. Phase: **{phase}**.', '',
                 f'Completed **{counts["complete"]}/{len(plan["tasks"])} episodes**; '
                 f'{accepted} accepted decisions. Outcomes: `{dict(counts)}`.', '',
                 f'Reported paid usage **${budget["reported_usd"]:.2f}**; committed including '
                 f'outstanding/unknown reservations **${budget["committed_usd"]:.2f} / ${args.budget_usd:g}**.', '',
                 '[Reward curve](plots/reward_response.png) · [Audit curve](plots/audit_response.png) · '
                 '[Figures and exact cells](plots/README.md) · [Verification](verification.json)', '',
                 'The process runs independently of the chat. Figures refresh roughly every two minutes '
                 'and at phase boundaries. Reward runs precede the audit and control sweeps. '
                 'Provider failures and refusals remain missing outcomes.']
        (out / 'STATUS.md').write_text('\n'.join(lines) + '\n')
        if plot or time.monotonic() - last_plot >= 120:
            refresh_figures(out, report, write_json, now)
            last_plot = time.monotonic()
        return state

    def phase_run(tasks, label, recover=False):
        queues = {m: deque(t for t in tasks if t['model'] == m) for m in plan['models']}
        def factory(config, calls):
            return Client(config, calls, ledger)
        with ThreadPoolExecutor(max_workers=2 * len(queues)) as pool:
            pending = {}
            def submit(model):
                if queues[model]:
                    task = queues[model].popleft()
                    future = pool.submit(execute, task, out, plan, factory, recover=recover)
                    pending[future] = model
            for model in queues:
                submit(model)
                submit(model)
            while pending:
                done, _ = wait(pending, timeout=20, return_when=FIRST_COMPLETED)
                for future in done:
                    model = pending.pop(future)
                    trace = future.result()
                    print(label, model, trace['task']['cell'], trace['status'], flush=True)
                    submit(model)
                refresh(label)
        return refresh(label + '-finished', plot=True)

    def verify_calls():
        results = []
        for task in plan['tasks']:
            directory = out / 'episodes' / task['id']
            path = directory / 'trace.json'
            if not path.exists():
                continue
            trace = read(path)
            verify_trace(trace, task, plan)
            history = [dict(role='system', content=plan['system'])]
            calls = []
            for turn in trace['turns']:
                history.append(dict(role='user', content=turn['observation']))
                call = read(directory / 'calls' / (turn['meta']['call_id'] + '.json'))
                request = call['request']
                config = plan['models'][task['model']]
                assert call['config'] == config
                assert request['messages'] == history
                assert request['model'] == config['provider_model']
                assert request['max_tokens'] == plan['max_tokens']
                assert request['extra_body']['reasoning']['effort'] == config['reasoning_effort']
                response = call['attempts'][-1]['response']
                assert response['choices'][0]['message']['content'] == turn['reply']
                assert response['choices'][0]['finish_reason'] == 'stop'
                history.append(dict(role='assistant', content=turn['reply']))
                calls.append(turn['meta']['call_id'])
            results.append(dict(id=task['id'], status=trace['status'], trace_sha256=file_hash(path),
                                verified_call_ids=calls))
        write_json(out / 'verification.json', dict(updated=now(), passed=True, episodes=results,
                                                  verified_calls=sum(len(r['verified_call_ids']) for r in results)))

    try:
        refresh('starting', plot=True)
        # These four are prespecified main-study episodes, not extra pilot samples.
        initial = [next(t for t in plan['tasks'] if t['model'] == model and t['family'] == 'commons'
                        and t['cell'] == 'reward-3' and t['seed'] == plan['seeds'][0])
                   for model in plan['models']]
        state = phase_run(initial, 'initial-main-episodes')
        if not state['outcomes'].get('complete'):
            raise RuntimeError('No initial episode completed; inspect provider diagnostics before continuing')
        verify_calls()
        for sweep in ('reward', 'audit', 'control'):
            tasks = [t for t in plan['tasks'] if t['sweep'] == sweep]
            phase_run(tasks, sweep)
            phase_run(tasks, sweep + '-recovery', recover=True)
        verify_calls()
        refresh('all-phases-finished', plot=True, final=True)
    except Exception as exc:
        write_json(out / 'campaign-error.json', dict(updated=now(), error_type=type(exc).__name__,
                                                    error=str(exc), pid=os.getpid()))
        refresh('stopped-on-error', plot=True, final=True)
        raise


if __name__ == '__main__':
    main()
