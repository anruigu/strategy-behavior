"""Prepare/calibrate without API calls; --execute requires a dedicated budget."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
import fcntl
import hashlib
import json
import math
from pathlib import Path
import shutil
import threading

from benchmark.clients import ModelConfig, now, write_json
from benchmark.fullscale.budget import BudgetExceeded, Ledger
from engines_v3_sa_dose import VERSION, make_game
from .calibrate import calibrate
from .client import Client
from .evaluate import evaluate
from .specs import ROSTER, SEEDS, SYSTEM, digest, schedule

ROOT = Path(__file__).resolve().parents[2]
CONFIGS = {
    'gpt-5.6-sol': ModelConfig('gpt-5.6-sol', 'openrouter', 'openai/gpt-5.6-sol',
                             'https://openrouter.ai/api/v1', 'OPENROUTER_API_KEY', None, None, 'high'),
    'gemini-3.1-pro': ModelConfig('gemini-3.1-pro', 'openrouter', 'google/gemini-3.1-pro-preview',
                                'https://openrouter.ai/api/v1', 'OPENROUTER_API_KEY', None, None, 'high'),
    'qwen-3.8-27b-medium': ModelConfig('qwen-3.8-27b-medium', 'flt', 'qwen3.8-27b',
                                    'https://inference.flt.build/v1', 'FLEET_API_KEY', None, None, 'medium'),
    'glm': ModelConfig('glm', 'flt', 'glm-5.3', 'https://inference.flt.build/v1',
                       'FLEET_API_KEY', None, None, 'high'),
}


def read(path):
    return json.loads(Path(path).read_text())


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_files():
    # Snapshot local dependencies conservatively, without traversing result archives.
    patterns = ('benchmark/*.py', 'benchmark/v3/*.py', 'benchmark/v3_sa_dose/*.py',
                'hole_exp/*.py', 'hole_exp/hackable_games/*.py', 'benchmark/fullscale/budget.py',
                'benchmark/fullscale/__init__.py', 'hole_exp/hackable_games/v3_sa_targets.json')
    return sorted({p for pattern in patterns for p in ROOT.glob(pattern)})


def verify_plan(out, plan, *, sources=True):
    payload = {k: v for k, v in plan.items() if k != 'identity'}
    if digest(payload) != plan['identity']:
        raise ValueError('Plan identity mismatch')
    if file_hash(out / 'calibration.json') != plan['calibration_sha256']:
        raise ValueError('Calibration changed')
    for relative, expected in plan['source_hashes'].items():
        if file_hash(out / 'source' / relative) != expected:
            raise ValueError('Source snapshot changed: ' + relative)
        if sources and file_hash(ROOT / relative) != expected:
            raise ValueError('Workspace source changed; execute from the frozen source directory: ' + relative)


def prepare(out, models=ROSTER, seeds=SEEDS, stage='full'):
    out = Path(out).resolve()
    if any(model not in CONFIGS for model in models):
        raise ValueError('Unsupported model')
    if any(type(seed) is not int for seed in seeds):
        raise ValueError('Invalid environment seed')
    if (out / 'plan.json').exists():
        plan = read(out / 'plan.json')
        if list(models) != list(plan['models']) or list(seeds) != plan['seeds'] or stage != plan['stage']:
            raise ValueError('Existing design differs; use a new output directory')
        verify_plan(out, plan)
        return plan
    tasks = schedule(models, seeds, stage)
    calibration = calibrate(seeds, stage)
    out.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for source in source_files():
        relative = str(source.relative_to(ROOT))
        target = out / 'source' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and file_hash(target) != file_hash(source):
            raise ValueError('Existing source snapshot differs: ' + relative)
        if not target.exists():
            shutil.copyfile(source, target)
        hashes[relative] = file_hash(target)
    write_json(out / 'calibration.json', calibration)
    plan = dict(protocol=VERSION, stage=stage, seeds=list(seeds), tasks=tasks,
                models={m: asdict(CONFIGS[m]) for m in models}, system=SYSTEM,
                max_tokens=16384, max_decisions=8, source_hashes=hashes,
                calibration_sha256=file_hash(out / 'calibration.json'),
                primary_outcome='Episode contains a target-exploit attempt, before enforcement.',
                sampling='Fresh independent contexts, fixed scripted rivals, doses interleaved within blocks; no provider sampling seed.',
                missingness='Provider failures/refusals are missing; invalid game actions consume a turn and are counted separately.',
                recovery='One explicit transport/truncation recovery pass, preserving accepted prefixes. Budget pauses may resume.',
                limits='Five episode replicates per cell in default design. No fitted threshold, causal discovery, or exploration-cost sensitivity.')
    plan['identity'] = digest(plan)
    write_json(out / 'plan.json', plan)
    verify_plan(out, plan)
    return plan


def episode_identity(plan, task):
    return digest(dict(plan=plan['identity'], task=task))


def verify_trace(trace, task, plan):
    if trace['identity'] != episode_identity(plan, task) or trace['task'] != task:
        raise ValueError('Episode identity differs')
    game = make_game(task['dose'], task['patched'])
    state = game.initial(task['seed'])
    history = [dict(role='system', content=plan['system'])]
    actions = []
    for turn in trace['turns']:
        obs = game.observe(state)
        history.append(dict(role='user', content=obs))
        if turn['before'] != state or turn['observation'] != obs:
            raise ValueError('Trace state/observation mismatch')
        context_hash = digest(dict(identity=trace['identity'], messages=history))
        if turn['context_sha256'] != context_hash or turn['meta']['status'] != 'ok':
            raise ValueError('Accepted context mismatch')
        state, facts = game.transition(state, turn['reply'])
        if facts != turn['facts'] or state != turn['after']:
            raise ValueError('Transition mismatch')
        history.append(dict(role='assistant', content=turn['reply']))
        actions.append(turn['reply'])
    if trace['status'] == 'complete':
        scores = evaluate(task['dose'], task['seed'], actions, task['patched'])
        if trace['metrics'] != scores:
            raise ValueError('Scoring mismatch')
    return history


class EpisodeFailure(RuntimeError):
    pass


def execute(task, out, plan, factory, *, recover=False):
    directory = Path(out) / 'episodes' / task['id']
    directory.mkdir(parents=True, exist_ok=True)
    # Protect both complete traces and accepted checkpoints against concurrent launchers.
    with (directory / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        return _execute(task, directory, plan, factory, recover)


def _execute(task, directory, plan, factory, recover):
    path = directory / 'trace.json'
    old = read(path) if path.exists() else None
    recovery_count = 0
    if old:
        verify_trace(old, task, plan)
        if old['status'] == 'complete':
            return old
        recovery_count = old.get('recovery_count', 0)
        if old['status'] == 'failed':
            if not recover or old['error_kind'] not in ('transport', 'truncated') or recovery_count >= 1:
                return old
            recovery_count += 1
        for i, turn in enumerate(old['turns'], 1):
            checkpoint = directory / f'decision-{i:02}.json'
            expected = {key: turn[key] for key in ('reply', 'meta', 'context_sha256')}
            if not checkpoint.exists() or read(checkpoint) != expected:
                raise ValueError('Accepted prefix checkpoint missing or changed')
    game = make_game(task['dose'], task['patched'])
    state = game.initial(task['seed'])
    history = [dict(role='system', content=plan['system'])]
    trace = dict(task=task, identity=episode_identity(plan, task), status='running', turns=[],
                 recovery_count=recovery_count, started=now(), inference_kind='model')
    write_json(path, trace)
    client = None
    error_kind = 'transport'
    try:
        while not state['done']:
            if len(trace['turns']) >= plan['max_decisions']:
                error_kind = 'protocol'
                raise EpisodeFailure('Decision limit exceeded')
            observation = game.observe(state)
            history.append(dict(role='user', content=observation))
            context_hash = digest(dict(identity=trace['identity'], messages=history))
            checkpoint = directory / f'decision-{len(trace["turns"]) + 1:02}.json'
            if checkpoint.exists():
                item = read(checkpoint)
                if item['context_sha256'] != context_hash or item['meta']['status'] != 'ok':
                    error_kind = 'integrity'
                    raise EpisodeFailure('Resume checkpoint context differs')
            else:
                if client is None:
                    client = factory(ModelConfig(**plan['models'][task['model']]), directory / 'calls')
                reply, meta = client.generate(history, max_tokens=plan['max_tokens'])
                if meta.get('status') != 'ok':
                    error_kind = meta.get('status', 'invalid_response')
                    raise EpisodeFailure(error_kind)
                item = dict(reply=reply, meta=meta, context_sha256=context_hash)
                write_json(checkpoint, item)
            before = state
            state, facts = game.transition(state, item['reply'])
            trace['turns'].append(dict(**item, observation=observation, before=before,
                                       after=state, facts=facts))
            history.append(dict(role='assistant', content=item['reply']))
            write_json(path, trace)
        trace['metrics'] = evaluate(task['dose'], task['seed'], [t['reply'] for t in trace['turns']], task['patched'])
        trace.update(status='complete', finished=now())
        verify_trace(trace, task, plan)
    except BudgetExceeded:
        trace.update(status='budget_paused', error_kind='budget', finished=now())
    except Exception as exc:
        trace.update(status='failed', error_kind=error_kind, error_type=type(exc).__name__, finished=now())
    write_json(path, trace)
    return trace


def launch(out, plan, budget, workers=4, recover=False, only='all'):
    if not math.isfinite(budget) or budget < 0 or workers < 1:
        raise ValueError('Invalid budget or worker count')
    verify_plan(out, plan)
    if only not in ('all', 'reward', 'audit', 'control'):
        raise ValueError('Unknown sweep selector')
    tasks = [t for t in plan['tasks'] if only == 'all' or t['sweep'] == only
             or (only == 'audit' and t['cell'] == 'reward-3')]
    if not tasks:
        raise ValueError('Requested sweep is absent from this plan')
    ledger = Ledger(out / 'budget.sqlite', ceiling=budget)
    limits = {model: threading.BoundedSemaphore(2) for model in plan['models']}
    def factory(config, calls):
        return Client(config, calls, ledger)
    def run_one(task):
        with limits[task['model']]:
            return execute(task, out, plan, factory, recover=recover)
    counts = Counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_one, task): task for task in tasks}
        for future in as_completed(futures):
            trace = future.result()
            counts[trace['status']] += 1
            write_json(out / 'status.json', dict(updated=now(), outcomes=counts, selected=len(tasks), planned=len(plan['tasks']),
                                                budget=ledger.summary()))
            print(sum(counts.values()), '/', len(tasks), trace['status'], trace['task']['model'],
                  trace['task']['family'], trace['task']['cell'], flush=True)
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--models', nargs='+', choices=ROSTER, default=ROSTER)
    parser.add_argument('--seeds', nargs='+', type=int, default=SEEDS)
    parser.add_argument('--stage', choices=('reward', 'full'), default='full')
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--budget-usd', type=float)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--recover', action='store_true')
    parser.add_argument('--only', choices=('all', 'reward', 'audit', 'control'), default='all')
    args = parser.parse_args()
    if args.execute and args.budget_usd is None:
        parser.error('--execute requires --budget-usd for this SA study')
    out = args.out.resolve()
    plan = prepare(out, args.models, args.seeds, args.stage)
    print(f'{len(plan["tasks"])} SA dose episodes prepared at {out}', flush=True)
    if args.execute:
        launch(out, plan, args.budget_usd, args.workers, args.recover, args.only)
    from .plot import report
    report(out)


if __name__ == '__main__':
    main()
