"""Build frozen manifests and collect independently verified completed episodes."""
import argparse
from collections import Counter, defaultdict
from itertools import combinations_with_replacement
import json
from pathlib import Path
import random
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from prediction.io_utils import digest, now, read_json, write_json


def freeze_source(out):
    import hashlib
    destination = out / 'source'
    if destination.exists():
        saved = read_json(out/'source-manifest.json')
        for relative, expected in saved.items():
            assert hashlib.sha256((destination/relative).read_bytes()).hexdigest() == expected
        return saved
    files = [ROOT/'prediction'/name for name in ('__init__.py','client.py','games.py','io_utils.py','measurements.py','runner.py','study.py')]
    files += [ROOT/'benchmark'/name for name in ('__init__.py','clients.py','fullscale/__init__.py','fullscale/budget.py')]
    files += list((ROOT/'hole_exp').glob('*.py'))
    hashes = {}
    for path in files:
        relative = path.relative_to(ROOT)
        target = destination/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        hashes[str(relative)] = hashlib.sha256(target.read_bytes()).hexdigest()
    write_json(out/'source-manifest.json', hashes)
    return hashes


def manifest(out, stage, games, configurations, trials=4, representations=('matrix',), budget=250.0):
    source_hashes = freeze_source(out)
    items = []
    for game in games:
        for pair in combinations_with_replacement(sorted(configurations), 2):
            for representation in representations:
                for trial in range(trials):
                    item = dict(game_id=game['id'], models=list(pair), trial_id=trial,
                                representation=representation, swap=bool(trial % 2))
                    item['id'] = f"{game['id']}--{pair[0]}--{pair[1]}--{representation}--t{trial}"
                    items.append(item)
    random.Random(20260910).shuffle(items)
    value = dict(stage=stage, created=now(), models=configurations, games=games, episodes=items,
                 sources=source_hashes, source_root=str((out/'source').resolve()),
                 protocol=dict(version='symmetric2x2-v1', rounds=8, temperature=.7,
                               max_tokens=4096, max_attempts=2, opponent_identity_disclosed=False,
                               history='complete_public', objective='own_cumulative_points',
                               trial_randomization='alternating_action_labels_independent_requests'),
                 ledger=str((out/'budget.sqlite').resolve()), stage_budget_usd=budget)
    target = out/stage/'manifest.json'
    if target.exists():
        raise FileExistsError('Do not overwrite a frozen stage manifest')
    write_json(target, value)
    return value


def collect(stage_root, output=None):
    from prediction.runner import verify_trace
    from prediction.measurements import measure_episode
    manifest_data = read_json(stage_root/'manifest.json')
    rows, traces, errors = [], [], []
    for spec in manifest_data['episodes']:
        path = stage_root/'episodes'/spec['id']/'trace.json'
        if not path.exists():
            continue
        try:
            trace = verify_trace(path, manifest_data)
            records = measure_episode(trace)
            for record in records:
                record['stage'] = manifest_data['stage']
            rows.extend(records)
            traces.append(dict(path=str(path.resolve()), sha256=digest(trace)))
        except Exception as exc:
            errors.append(dict(path=str(path), error=type(exc).__name__+': '+str(exc)))
    summary = dict(updated=now(), stage=manifest_data['stage'], complete_episodes=len(traces),
                   planned_episodes=len(manifest_data['episodes']), rows=len(rows),
                   games=len({r['game_id'] for r in rows}), families=Counter(r['family'] for r in rows),
                   models=Counter(r['model'] for r in rows), errors=errors,
                   measured_targets=Counter(k for r in rows for k,v in r['targets'].items() if v['value'] is not None))
    target = output or stage_root/'collected'
    target.mkdir(parents=True, exist_ok=True)
    write_json(target/'records.json', rows)
    write_json(target/'provenance.json', traces)
    write_json(target/'summary.json', summary)
    return summary


def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='action', required=True)
    create = subs.add_parser('create')
    create.add_argument('--out', type=Path, required=True)
    create.add_argument('--stage', default='pilot')
    create.add_argument('--games', type=int, default=24)
    create.add_argument('--trials', type=int, default=4)
    create.add_argument('--seed', type=int, default=20260910)
    gather = subs.add_parser('collect')
    gather.add_argument('--stage-root', type=Path, required=True)
    gather.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.action == 'collect':
        print(json.dumps(collect(args.stage_root, args.output), indent=2))
        return
    from prediction.games import generate_games
    from prediction.client import configurations
    games = generate_games(args.seed, args.games)
    for game in games:
        game['id'] = args.stage+'-'+game['id']
    configs = configurations(['claude-haiku-4.5','kimi-k3','qwen-3.8-27b','gemma-4-31b'])
    value = manifest(args.out, args.stage, games, configs, args.trials)
    print(json.dumps(dict(stage=args.stage, games=len(games), episodes=len(value['episodes']),
                          calls_without_retries=16*len(value['episodes']), families=Counter(g['family'] for g in games))))


if __name__ == '__main__':
    main()
