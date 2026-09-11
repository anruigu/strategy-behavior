"""Budgeted model-tier extension of the frozen v3-MA screen."""
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

from benchmark.clients import MODELS, ModelConfig, OPENROUTER, now, write_json
from benchmark.fullscale.budget import BudgetExceeded, Ledger
from benchmark.fullscale.client import StudyClient
from benchmark.v3_ma.campaign import FORMAT
from benchmark.v3_ma.run import execute
from engines_v3_ma import GAMES

VERSION = 'v3-MA-tier-extension.1'
TIERS = {
    'frontier': ('claude-opus-5', 'gpt-5.6-sol', 'gemini-3.1-pro'),
    'middle': ('claude-sonnet-5', 'gpt-5', 'gemini-3.7-flash'),
    'open': ('qwen-3.8-27b', 'glm'),
}
ROSTER = tuple(m for group in TIERS.values() for m in group)
ROUTES = {
    'claude-opus-5': 'anthropic/claude-opus-5',
    'gpt-5.6-sol': 'openai/gpt-5.6-sol',
    'gemini-3.1-pro': 'google/gemini-3.1-pro-preview',
    'claude-sonnet-5': 'anthropic/claude-sonnet-5',
    'gpt-5': 'openai/gpt-5',
}
CONFIGS = {m: replace(MODELS[m], temperature=None, reasoning_effort='low')
           if m in MODELS else ModelConfig(m, 'openrouter', ROUTES[m], OPENROUTER,
           'OPENROUTER_API_KEY', temperature=None, reasoning_effort='low') for m in ROSTER}


def task_id(row):
    return hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()[:20]


def schedule(stage):
    rows = []
    games = list(GAMES) if stage == 'crossplay' else ['v3ma_signal_notes', 'v3ma_trust_pledge']
    for gid, focal, opponent, condition in product(games, ROSTER, ROSTER, ['ordinary', 'nerfed']):
        if stage == 'pilot' and (focal != opponent or condition != 'ordinary'):
            continue
        if GAMES[gid].family == 'commons' and condition == 'nerfed':
            continue
        row = dict(game=gid, focal=focal, opponent=opponent, condition=condition,
                   seed=0 if stage == 'crossplay' else 1701, arm='hole')
        row['id'] = task_id(row)
        rows.append(row)
    random.Random(20260910).shuffle(rows)
    return rows


def prepare(root, stage):
    out = root / stage
    sources = [Path(__file__), Path('benchmark/v3_ma/run.py'),
               Path('benchmark/v3_ma/specs.py'), Path('benchmark/v3_ma/evaluate.py'),
               Path('benchmark/v3_ma/report.py'), Path('benchmark/v3_ma/campaign.py'),
               Path('benchmark/clients.py'), Path('benchmark/fullscale/client.py'),
               Path('benchmark/fullscale/budget.py'), Path('hole_exp/referee_games.py'),
               Path('hole_exp/hackable_games/engines_v3_ma.py')]
    hashes = {str(p.resolve().relative_to(Path.cwd())): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sources}
    plan = dict(protocol=VERSION, stage=stage, tasks=schedule(stage), tiers=TIERS,
        models={m: asdict(c) for m, c in CONFIGS.items()}, source_hashes=hashes,
        system_suffix=FORMAT, output_allowances=[8192, 16384], transport_attempts=2,
        format_corrections=1, budget_ceiling_usd=500,
        budget_ledger=str((root / 'budget.sqlite').resolve()),
        budget_scope='All paid OpenRouter calls across pilot, cross-play and dose. FLT is the configured internal unbilled gateway; usage retained separately.',
        context='Fresh separate seat contexts per episode. No reflection or hints. Provider-default temperature, low requested reasoning, no sampling seed.',
        estimand='Scenario-specific behavior by ordered model pairing and recipient condition. Tier labels are design strata, not measured capability.',
        limitations='One environment seed per ordered pairing/condition in the initial cross-play screen. No independent sampling replicates within a cell. Recipient-condition comparisons are not H/X policy deltas.')
    # Normalize tuples before immutable comparisons.
    plan = json.loads(json.dumps(plan))
    path = out / 'plan.json'
    if path.exists() and json.loads(path.read_text()) != plan:
        raise ValueError('Frozen plan changed; use a new directory')
    write_json(path, plan)
    for relative, digest in hashes.items():
        target = out / 'source' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copyfile(relative, target)
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError('Source snapshot mismatch: ' + relative)
    return plan


def client_factory(ledger, limits):
    class Client(StudyClient):
        def __init__(self, config, log_dir):
            super().__init__(config, log_dir, ledger)
            self.client = self.client.with_options(timeout=600)

        def generate(self, messages, **kwargs):
            last_error = None
            for cap in (8192, 16384):
                try:
                    with limits[self.config.model_id]:
                        reply, meta = super().generate(messages, **{**kwargs, 'max_tokens': cap})
                    if meta['status'] == 'ok':
                        return reply, meta
                    last_error = RuntimeError(f'{self.config.model_id}: {meta["status"]}; call {meta["call_id"]}')
                except BudgetExceeded:
                    raise
                except Exception as exc:
                    last_error = exc
            raise last_error
    return Client


def launch(root, stage, workers):
    from benchmark.v3_ma.report import report
    plan = prepare(root, stage)
    out = root / stage
    ledger = Ledger(root / 'budget.sqlite', ceiling=500)
    limits = {m: threading.BoundedSemaphore(12) for m in ROSTER}
    Client = client_factory(ledger, limits)
    outcomes = {}
    def status(state):
        write_json(out / 'status.json', dict(status=state, updated=now(), planned=len(plan['tasks']),
            processed=len(outcomes), outcomes=dict(Counter(outcomes.values())), budget=ledger.summary()))
    status('running')
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(execute, row, out, CONFIGS, 8192, Client, FORMAT, 1): row
                   for row in plan['tasks']}
        for future in as_completed(futures):
            row = futures[future]
            future.result()
            record = json.loads((out / 'episodes' / row['id'] / 'trace.json').read_text())
            outcomes[row['id']] = record['status']
            status('running')
            print(len(outcomes), '/', len(plan['tasks']), record['status'], row['game'],
                  row['focal'], row['opponent'], row['condition'], flush=True)
    report(out)
    status('complete' if all(v == 'complete' for v in outcomes.values()) else 'finished_with_errors')


def probe(root):
    """One cheap transport/format check per model, excluded from behavioral data."""
    ledger = Ledger(root / 'budget.sqlite', ceiling=500)
    def one(m):
        client = StudyClient(CONFIGS[m], root / 'probes' / m, ledger)
        try:
            reply, meta = client.generate([dict(role='user', content='Reply with exactly [catch: 2].')],
                                         max_tokens=8192, purpose='route_and_format_probe')
            return m, dict(ok=meta['status'] == 'ok' and reply.strip() == '[catch: 2]',
                           reply=reply, metadata=meta)
        except Exception as exc:
            return m, dict(ok=False, error=str(exc))
    with ThreadPoolExecutor(max_workers=8) as pool:
        result = dict(pool.map(one, ROSTER))
    write_json(root / 'probes.json', dict(timestamp=now(), results=result, budget=ledger.summary()))
    for m, r in result.items():
        print(m, r['ok'], r.get('metadata', {}).get('actual_model'), flush=True)
    return all(r['ok'] for r in result.values())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--stage', choices=['probe', 'pilot', 'crossplay'], required=True)
    p.add_argument('--workers', type=int, default=32)
    p.add_argument('--execute', action='store_true')
    a = p.parse_args()
    if a.workers < 1:
        p.error('workers must be positive')
    if a.stage == 'probe':
        if not a.execute:
            p.error('probe requires --execute')
        raise SystemExit(0 if probe(a.out) else 1)
    if a.execute:
        launch(a.out, a.stage, a.workers)
    else:
        print(len(prepare(a.out, a.stage)['tasks']), 'episodes planned')


if __name__ == '__main__':
    main()
