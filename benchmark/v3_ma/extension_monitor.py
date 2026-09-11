"""Durable local status, one recovery pass, then final figures and verification."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import time

from benchmark.clients import now, write_json
from benchmark.fullscale.budget import Ledger
from benchmark.v3_ma.extension_report import summary
from benchmark.v3_ma.extension_recovery import recover
from benchmark.v3_ma.extension_verify import verify


def status(root):
    stages = {stage: json.loads((root/stage/'status.json').read_text())
              for stage in ('pilot', 'crossplay', 'dose')}
    budget = Ledger(root/'budget.sqlite', 500).summary()
    state = dict(updated=now(), stages=stages, budget=budget)
    write_json(root/'status.json', state)
    lines = ['# Cross-play and dose study status', '', f'Updated {state["updated"]}.', '',
        '| Stage | Processed / planned | Outcomes | State |', '|---|---:|---|---|']
    for stage, s in stages.items():
        lines.append(f'| {stage} | {s["processed"]}/{s["planned"]} | {s["outcomes"]} | {s["status"]} |')
    lines += ['', f'Reported paid usage: **${budget["reported_usd"]:.2f}**. Committed including '
              f'outstanding/unknown reservations: **${budget["committed_usd"]:.2f} / $500**.', '',
        '[Figures and exact data](plots/README.md) · '
        '[Protocol](../../../research_logs/sep/0910-ma-extension-protocol.md) · '
        '[Verification](verification.json).', '',
        'The monitor refreshes this file every 30 seconds and the figures periodically. '
        'After each main stage finishes, it performs at most one exact-prefix recovery '
        'for transport/completion failures. Refusals and malformed game submissions are '
        'not retried by recovery. Final figures and exact replays run automatically.', '']
    (root/'STATUS.md').write_text('\n'.join(lines))
    return state


def monitor(root):
    sources = ['extension_monitor.py', 'extension_report.py', 'extension_verify.py', 'extension_recovery.py']
    hashes = {}
    for name in sources:
        source = Path(__file__).with_name(name)
        hashes[name] = hashlib.sha256(source.read_bytes()).hexdigest()
        target = root/'analysis-source'/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    write_json(root/'analysis-manifest.json', dict(created=now(), source_hashes=hashes))
    write_json(root/'monitor.json', dict(status='running', started=now()))
    last_plot = time.monotonic()
    jobs = {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        while True:
            state = status(root)
            for stage in ('crossplay', 'dose'):
                s = state['stages'][stage]['status']
                if s in ('complete', 'finished_with_errors') and stage not in jobs:
                    if (root/stage/'recovery.json').exists():
                        raise ValueError('Existing recovery requires inspection before restarting monitor')
                    jobs[stage] = pool.submit(recover, root, stage, 32)
                if stage in jobs and jobs[stage].done():
                    jobs[stage].result()
            final = all(state['stages'][s]['status'] == 'finished_after_recovery' for s in ('crossplay', 'dose'))
            if final or time.monotonic()-last_plot > 600:
                for name, digest in hashes.items():
                    if hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() != digest:
                        raise ValueError('Analysis source changed while monitor was running: '+name)
                summary(root)
                last_plot = time.monotonic()
            if final:
                # The inherited reporter has a historical four-model heading;
                # only update that display label for this eight-model campaign.
                p = root/'crossplay'/'REPORT.md'
                if p.exists():
                    p.write_text(p.read_text().replace('# v3-MA four-model cross-play', '# v3-MA eight-model cross-play', 1))
                passed = verify(root)
                write_json(root/'monitor.json', dict(status='complete' if passed else 'verification_failed',
                    finished=now(), verification_passed=passed))
                status(root)
                return
            time.sleep(30)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--once', action='store_true')
    a = p.parse_args()
    if a.once:
        print(json.dumps(status(a.out), indent=2))
    else:
        try:
            monitor(a.out)
        except Exception as exc:
            write_json(a.out/'monitor.json', dict(status='failed', updated=now(),
                error=type(exc).__name__+': '+str(exc)))
            raise
