"""One exact-prefix recovery pass; never retry refusals or format failures."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import shutil
import threading

from benchmark.clients import now, write_json
from benchmark.fullscale.budget import Ledger
from benchmark.v3_ma.dose_run import execute as execute_dose
from benchmark.v3_ma.extension import CONFIGS, ROSTER, client_factory
from benchmark.v3_ma.recover import Replay, recover_episode


def recover_dose(task, out, factory):
    path = out/'episodes'/task['id']/'trace.json'
    old = json.loads(path.read_text())
    by_seat = {p: [d for d in old['decisions'] if d['pid'] == p] for p in range(3)}
    sequence = iter(range(3))
    clients = []
    def replay_factory(config, calls):
        pid = next(sequence)
        client = Replay(by_seat[pid], calls, factory(config, calls))
        clients.append(client)
        return client
    archive = path.parent/'previous-attempts'
    archive.mkdir(exist_ok=True)
    previous = archive/'first-pass.json'
    if previous.exists():
        raise ValueError('Dose recovery already attempted')
    path.replace(previous)
    execute_dose(task, out, replay_factory)
    trace = json.loads(path.read_text())
    trace['recovery'] = dict(protocol='exact-prefix-recovery.1', previous_error=old.get('error'),
        previous_decisions=len(old['decisions']), replayed_decisions=sum(c.replayed for c in clients),
        earlier_replies_resampled=False, recovered_at=now())
    write_json(path, trace)
    return trace['status']


def recover(root, stage, workers=32):
    out = root/stage
    manifest_path = out/'recovery.json'
    if manifest_path.exists():
        raise ValueError('The single recovery pass has already been recorded')
    state = json.loads((out/'status.json').read_text())
    if state['status'] not in ('complete', 'finished_with_errors'):
        raise ValueError('Wait for the original stage to finish')
    plan = json.loads((out/'plan.json').read_text())
    for name, digest in plan['source_hashes'].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest() != digest:
            raise ValueError('Source differs from frozen plan: '+name)
    selected = []
    for task in plan['tasks']:
        trace = json.loads((out/'episodes'/task['id']/'trace.json').read_text())
        error = trace.get('error', '')
        if trace['status'] == 'failed' and any(x in error for x in ('transport failure', 'invalid_response', 'truncated')):
            selected.append(task)
    archive = out/'first-pass'
    archive.mkdir(exist_ok=True)
    for filename in ('status.json', 'report.json', 'REPORT.md'):
        if (out/filename).exists() and not (archive/filename).exists():
            shutil.copyfile(out/filename, archive/filename)
    sources = [Path(__file__), Path('benchmark/v3_ma/recover.py')]
    recovery = dict(protocol='exact-prefix-recovery.1', started=now(), tasks=selected,
        policy='One additional pass for transport/completion failures only. Replay every stored request and reply exactly; no prior accepted action is resampled. Refusal, budget and game-format failures remain final.',
        request_settings='Same model routes, low requested reasoning, 8192/16384 allowances, schema correction and 600-second transport wait.',
        source_hashes={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}, results=[])
    for p in sources:
        target = out/'recovery-source'/p.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
    write_json(manifest_path, recovery)
    ledger = Ledger(root/'budget.sqlite', 500)
    factory = client_factory(ledger, {m: threading.BoundedSemaphore(16) for m in ROSTER})
    write_json(out/'status.json', dict(state, status='recovering', updated=now()))
    def one(task):
        if stage == 'dose':
            return recover_dose(task, out, factory)
        return recover_episode(task, out, CONFIGS, factory, plan['system_suffix'], plan['format_corrections'])
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(one, task): task for task in selected}
        for f in as_completed(futures):
            task = futures[f]
            try:
                outcome = dict(id=task['id'], status=f.result())
            except Exception as exc:
                outcome = dict(id=task['id'], status='failed', error=type(exc).__name__+': '+str(exc))
            recovery['results'].append(outcome)
            write_json(manifest_path, recovery)
    from collections import Counter
    outcomes = Counter(json.loads((out/'episodes'/t['id']/'trace.json').read_text())['status'] for t in plan['tasks'])
    recovery.update(finished=now(), outcomes=dict(outcomes), budget=ledger.summary())
    write_json(manifest_path, recovery)
    if stage == 'crossplay':
        from benchmark.v3_ma.report import report
        report(out)
    write_json(out/'status.json', dict(status='finished_after_recovery', updated=now(),
        planned=len(plan['tasks']), processed=len(plan['tasks']), outcomes=dict(outcomes), budget=ledger.summary()))
    return recovery


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--stage', choices=['crossplay', 'dose'], required=True)
    p.add_argument('--workers', type=int, default=32)
    args = p.parse_args()
    print(json.dumps(recover(args.out, args.stage, args.workers), indent=2))
