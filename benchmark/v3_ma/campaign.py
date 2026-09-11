"""Prespecified four-model MA screen with bounded retries and durable accounting."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, replace
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import shutil
import threading
import time

from benchmark.clients import MODELS, now, write_json
from benchmark.fullscale.budget import BudgetExceeded, Ledger
from benchmark.fullscale.client import StudyClient
from benchmark.v3_ma.run import execute
from benchmark.v3_ma.specs import manifest
from engines_v3_ma import GAMES

ROSTER = ('claude-haiku-4.5', 'gpt-5-mini', 'qwen-3.8-27b', 'glm')
CONFIGS = {m: replace(MODELS[m], temperature=None) for m in ROSTER}
FORMAT = ('\nReturn only the required bracketed action tokens, once per field. '
          'Use only fields listed in Actions for the current stage; do not submit later stages. '
          'Do not include analysis, alternatives, or a copy of the action menu. '
          'Message fields must be at most 300 characters; use none for no message.')
VERSION = 'v3-MA-four-model-screen.2'


def schedule(stage):
    games = list(GAMES) if stage == 'main' else ['v3ma_trust_memory', 'v3ma_signal_notes']
    rows = []
    for gid, focal, opponent, seed, condition in product(games, ROSTER, ROSTER,
            [0, 1] if stage == 'main' else [0], ['ordinary', 'nerfed']):
        if stage == 'pilot' and focal != opponent:
            continue
        if GAMES[gid].family == 'commons' and condition == 'nerfed':
            continue
        row = dict(game=gid, focal=focal, opponent=opponent, seed=seed, condition=condition, arm='hole')
        row['id'] = hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()[:20]
        rows.append(row)
    random.Random(20260909).shuffle(rows)
    return rows


def prepare(out, stage, ceiling):
    rows = schedule(stage)
    sources = [Path(__file__), Path('benchmark/v3_ma/run.py'), Path('benchmark/v3_ma/specs.py'),
        Path('benchmark/v3_ma/evaluate.py'), Path('benchmark/v3_ma/report.py'),
        Path('hole_exp/hackable_games/engines_v3_ma.py'), Path('hole_exp/referee_games.py'),
        Path('benchmark/clients.py'), Path('benchmark/fullscale/client.py'), Path('benchmark/fullscale/budget.py')]
    root = Path.cwd()
    hashes = {str(p.resolve().relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    plan = dict(protocol=VERSION, stage=stage, suite=manifest(), tasks=rows,
        models={m: asdict(c) for m, c in CONFIGS.items()}, source_hashes=hashes,
        system_suffix=FORMAT, output_allowances=[8192, 16384], max_transport_attempts_per_submission=2,
        format_corrections=1, correction_feedback='Public action schema only; every invalid reply retained',
        budget_ceiling_usd=ceiling, budget_scope='OpenRouter requests; FLT transport reports no dollar charge',
        context='Fresh per-seat memory per episode; no reflection or training between episodes',
        comparison='Ordinary vs privately nerfed recipients, open referee arm only. Commons ordinary only.',
        estimand='Paired seed/game/model-lineup differences in behavioral markers and focal payoff; no claim of learning.')
    path = out / 'plan.json'
    if path.exists() and json.loads(path.read_text()) != plan:
        raise ValueError('Immutable campaign plan changed; use a new output directory')
    write_json(path, plan)
    for relative in hashes:
        target = out / 'source' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copyfile(relative, target)
        assert hashlib.sha256(target.read_bytes()).hexdigest() == hashes[relative]
    return plan


def launch(out, stage, workers, ceiling):
    from benchmark.v3_ma.report import report
    plan = prepare(out, stage, ceiling)
    ledger = Ledger(out / 'budget.sqlite', ceiling=ceiling)
    # Limit per-model requests even when episode scheduling is wide.
    limits = {m: threading.BoundedSemaphore(32) for m in ROSTER}

    class Client(StudyClient):
        def __init__(self, config, log_dir):
            super().__init__(config, log_dir, ledger)
            self.client = self.client.with_options(timeout=180)
        def generate(self, messages, **kwargs):
            last_error = None
            for limit in (8192, 16384):
                try:
                    with limits[self.config.model_id]:
                        reply, meta = super().generate(messages, **{**kwargs, 'max_tokens': limit})
                    if meta['status'] == 'ok':
                        return reply, meta
                    last_error = RuntimeError(f'{self.config.model_id}: {meta["status"]}; call {meta["call_id"]}')
                except BudgetExceeded:
                    raise
                except Exception as exc:
                    last_error = exc
                if limit == 8192:
                    time.sleep(1)
            raise last_error

    outcomes = {}
    errors = []
    def status(state):
        write_json(out / 'status.json', dict(status=state, updated=now(), planned=len(plan['tasks']),
            processed=len(outcomes), outcomes=dict(Counter(outcomes.values())),
            errors=errors, budget=ledger.summary()))
    status('running')
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(execute, row, out, CONFIGS, 8192, Client, FORMAT, 1): row for row in plan['tasks']}
        for future in as_completed(futures):
            row = futures[future]
            try:
                future.result()
                trace = json.loads((out / 'episodes' / row['id'] / 'trace.json').read_text())
                outcomes[row['id']] = trace['status']
                if trace['status'] != 'complete':
                    errors.append(dict(id=row['id'], error=trace.get('error')))
            except Exception as exc:
                outcomes[row['id']] = 'failed'
                errors.append(dict(id=row['id'], error=type(exc).__name__ + ': ' + str(exc)))
            print(len(outcomes), len(plan['tasks']), outcomes[row['id']], row['game'], row['focal'], row['opponent'], row['condition'], flush=True)
            status('running')
    report(out)
    status('finished' if all(x == 'complete' for x in outcomes.values()) else 'finished_with_errors')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--stage', choices=['pilot', 'main'], required=True)
    p.add_argument('--workers', type=int, default=48)
    p.add_argument('--ceiling', type=float, default=200.)
    p.add_argument('--execute', action='store_true')
    a = p.parse_args()
    if a.workers < 1 or a.ceiling <= 0:
        p.error('workers and ceiling must be positive')
    if a.execute:
        launch(a.out, a.stage, a.workers, a.ceiling)
    else:
        plan = prepare(a.out, a.stage, a.ceiling)
        print(len(plan['tasks']), 'episodes planned')
