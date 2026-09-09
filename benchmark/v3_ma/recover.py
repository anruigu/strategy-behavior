"""Recover transport failures by replaying the exact accepted episode prefix.

No completed choice is resampled. Incoming request messages must exactly match the
saved request before a reply may be replayed. First-pass reports are preserved.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import hashlib
from pathlib import Path
import shutil
import time

from benchmark.clients import ModelConfig, now, write_json
from benchmark.fullscale.budget import Ledger, BudgetExceeded
from benchmark.fullscale.client import StudyClient
from benchmark.v3_ma.run import execute


class Replay:
    def __init__(self, saved, calls, live):
        self.saved = list(saved)
        self.calls = calls
        self.live = live
        self.replayed = 0
    def generate(self, messages, **kwargs):
        if self.replayed < len(self.saved):
            decision = self.saved[self.replayed]
            original = json.loads((self.calls / (decision['metadata']['call_id'] + '.json')).read_text())
            if messages != original['request']['messages']:
                raise RuntimeError('Recovery request differs from saved prefix; refusing to resample earlier actions')
            self.replayed += 1
            return decision['reply'], decision['metadata']
        return self.live.generate(messages, **kwargs)


def recover_episode(task, out, configs, live_factory, suffix, attempts):
    path = out / 'episodes' / task['id'] / 'trace.json'
    old = json.loads(path.read_text())
    if old['status'] == 'complete':
        return 'complete'
    by_seat = {p: [d for d in old['decisions'] if d['pid'] == p] for p in range(3)}
    iterator = iter(range(3))
    clients = []
    def factory(config, calls):
        pid = next(iterator)
        client = Replay(by_seat[pid], calls, live_factory(config, calls))
        clients.append(client)
        return client
    execute(task, out, configs, 8192, factory, suffix, attempts)
    row = json.loads(path.read_text())
    row['recovery'] = dict(protocol='exact-prefix-recovery.1', previous_error=old.get('error'),
        previous_decisions=len(old['decisions']), replayed_decisions=sum(c.replayed for c in clients),
        earlier_replies_resampled=False, recovered_at=now())
    write_json(path, row)
    return row['status']


def recover(out, workers):
    from benchmark.v3_ma.report import report
    plan = json.loads((out/'plan.json').read_text())
    for relative in plan['source_hashes']:
        if hashlib.sha256(Path(relative).read_bytes()).hexdigest() != plan['source_hashes'][relative]:
            raise ValueError('Recovery engine or prompt differs from frozen main run: ' + relative)
    state = json.loads((out/'status.json').read_text())
    if not state['status'].startswith('finished'):
        raise ValueError('Wait for the original campaign to finish before recovery')
    configs = {m: ModelConfig(**c) for m, c in plan['models'].items()}
    ledger = Ledger(out/'budget.sqlite', ceiling=plan['budget_ceiling_usd'])
    selected = []
    for task in plan['tasks']:
        path = out/'episodes'/task['id']/'trace.json'
        row = json.loads(path.read_text())
        error = row.get('error', '')
        if row['status'] == 'failed' and not row.get('recovery') and any(s in error for s in ('transport failure', 'invalid_response', 'truncated')):
            selected.append(task)
    archive = out/'first-pass'
    archive.mkdir(exist_ok=True)
    for name in ('status.json', 'report.json', 'REPORT.md'):
        if (out/name).exists() and not (archive/name).exists():
            shutil.copyfile(out/name, archive/name)
    recovery = dict(protocol='exact-prefix-recovery.1', started=now(), tasks=selected,
        implementation_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        policy='One recovery pass for transport/completion errors only. Match and replay every saved request/reply; no earlier choices resampled.',
        results=[])
    write_json(out/'recovery.json', recovery)

    class Client(StudyClient):
        def __init__(self, config, calls):
            super().__init__(config, calls, ledger)
            self.client = self.client.with_options(timeout=180)
        def generate(self, messages, **kwargs):
            error = None
            for limit in (8192, 16384):
                try:
                    reply, meta = super().generate(messages, **{**kwargs, 'max_tokens': limit})
                    if meta['status'] == 'ok':
                        return reply, meta
                    error = RuntimeError(f'{self.config.model_id}: {meta["status"]}; call {meta["call_id"]}')
                except BudgetExceeded:
                    raise
                except Exception as exc:
                    error = exc
                if limit == 8192:
                    time.sleep(1)
            raise error
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(recover_episode, task, out, configs, Client,
                               plan['system_suffix'], plan['format_corrections']): task for task in selected}
        for f in as_completed(futures):
            task = futures[f]
            try:
                status = f.result()
                row = dict(id=task['id'], status=status)
            except Exception as exc:
                row = dict(id=task['id'], status='failed', error=str(exc))
            recovery['results'].append(row)
            write_json(out/'recovery.json', recovery)
            print(row, flush=True)
    result = report(out)
    recovery.update(finished=now(), outcomes=result['outcomes'], budget=ledger.summary())
    write_json(out/'recovery.json', recovery)
    write_json(out/'status.json', dict(status='finished_after_recovery', updated=now(),
        planned=len(plan['tasks']), processed=len(plan['tasks']), outcomes=result['outcomes'],
        first_pass_outcomes=state['outcomes'], budget=ledger.summary(), recovery='recovery.json'))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--workers', type=int, default=12)
    a = p.parse_args()
    recover(a.out, a.workers)
