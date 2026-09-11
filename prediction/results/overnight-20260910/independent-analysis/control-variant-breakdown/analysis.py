"""Read-only secondary variant breakdown of completed, audited saved forecasts.

Run from the project root. No refitting, inference, or writes to supervised paths.
"""
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from prediction.analysis import _prediction_key, _valid, score_rows


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TARGETS = ('action0', 'cooperation', 'coordination')
VARIANTS = ('scale3', 'offset10', 'abstract_text')


def main():
    captured = {}

    def read(path, lines=False):
        path = Path(path).resolve()
        raw = path.read_bytes()
        captured[str(path)] = hashlib.sha256(raw).hexdigest()
        return [json.loads(line) for line in raw.decode().splitlines() if line] if lines else json.loads(raw)

    if (OUT/'scores.json').exists():
        raise FileExistsError('Refusing to replace an existing derived breakdown')
    status = read(ROOT/'controls/status.json')
    if status['status'] not in ('complete', 'finished_with_errors'):
        raise ValueError('Control runner must have reached its normal terminal state')
    audit = read(ROOT/'controls/evaluation/audit.json')
    if audit.get('prospective_verified') is not True:
        raise ValueError('Primary control score timing/identity audit must pass')
    secondary_root = ROOT/'secondary-baselines/full/controls-comparison'
    supervisor = read(secondary_root/'supervisor-audit.json')
    if supervisor.get('status') != 'verified':
        raise ValueError('Secondary control comparison must be independently verified')
    for mapping in (supervisor['initial_sha256'], supervisor['output_sha256']):
        for name, expected in mapping.items():
            if hashlib.sha256(Path(name).read_bytes()).hexdigest() != expected:
                raise ValueError('Verified secondary input/output changed: '+name)
    manifest = read(ROOT/'controls/manifest.json')
    games = {game['id']: game for game in manifest['games']}
    primary = read(ROOT/'controls/evaluation/scores.json')
    joined_primary = read(ROOT/'controls/evaluation/joined-predictions.jsonl', lines=True)
    secondary = read(secondary_root/'scores.json')
    joined = read(secondary_root/'joined-predictions.jsonl', lines=True)
    primary_support = {(r['split'], r['target']): r['common_rows'] for r in primary['support']}
    secondary_support = {(r['split'], r['target']): r['common_rows'] for r in secondary['support']}
    original = defaultdict(lambda: defaultdict(dict))
    augmented = defaultdict(lambda: defaultdict(dict))
    for source, destination in ((joined_primary, original), (joined, augmented)):
        for row in source:
            if row['target'] not in TARGETS:
                continue
            bucket = destination[row['split'], row['target']][row['method']]
            if _valid(row):
                key = _prediction_key(row)
                if key in bucket:
                    raise ValueError('Duplicate saved prediction key')
                bucket[key] = row
    saved = {(r['split'], r['target'], r['method']): r for r in secondary['scores']}
    rows, support, derivation, reproduced = [], [], [], []
    for (split, target), methods in sorted(original.items()):
        common = set.intersection(*(set(values) for values in methods.values()))
        if len(common) != primary_support[split, target] or len(common) != secondary_support[split, target]:
            raise ValueError('Original all-method support does not match audited score support')
        buckets = augmented[split, target]
        if not all(common <= set(values) for values in buckets.values()):
            raise ValueError('Secondary methods do not retain original common support')
        for method, values in buckets.items():
            selected = [values[key] for key in sorted(common)]
            pooled = score_rows(selected)
            for metric in ('event_brier', 'event_log_loss', 'calibration_ece'):
                if abs(pooled[metric]-saved[split, target, method][metric]) > 1e-12:
                    raise ValueError('Pooled score reproduction failed: '+str((target, method, metric)))
            reproduced.append(dict(split=split, target=target, method=method, **pooled))
            for variant in VARIANTS:
                subset = [r for r in selected if games[r['game_id']]['control_variant'] == variant]
                rows.append(dict(split=split, variant=variant, target=target, method=method,
                                 **score_rows(subset), intervals={}))
        reference = methods[next(iter(methods))]
        for variant in VARIANTS:
            keys = [key for key in sorted(common) if games[reference[key]['game_id']]['control_variant'] == variant]
            subset = [reference[key] for key in keys]
            support.append(dict(split=split, variant=variant, target=target, common_rows=len(keys),
                                groups=len({r['group_id'] for r in subset}),
                                episodes=len({r['episode_id'] for r in subset}),
                                opportunities=sum(r['opportunities'] for r in subset)))
            derivation.append(dict(split=split, variant=variant, target=target,
                                   original_common_prediction_keys=[list(key) for key in keys]))
    for name, expected in captured.items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest() != expected:
            raise ValueError('Input changed during read-only breakdown: '+name)
    output = dict(classification='secondary_descriptive_control_variant_breakdown',
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  no_refitting=True, no_inference=True,
                  original_common_support_preserved=True,
                  weighting='Equal canonical source-game groups; event opportunities pooled within each group. Whole focal episode rows retained. No episode/round independence assumption or bootstrap intervals.',
                  reference='Pooled scores reproduced from the audited augmented comparison on exactly the original all-method support before splitting by manifest control_variant.',
                  limitations=['Descriptive per-variant points, not preregistered additional tests or method selection.',
                               'Variants reuse seven canonical source groups; they are not 21 independent shape clusters.',
                               'These forecast scores use completed forecast support, which differs from matched historical-pilot sensitivity support.'],
                  inputs_sha256=captured,
                  analysis_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  scores=rows, support=support, pooled_reproduced_scores=reproduced)
    for filename, content in [('scores.json', output), ('derivation.json', dict(inputs_sha256=captured, support=derivation))]:
        with (OUT/filename).open('x') as handle:
            json.dump(content, handle, indent=2, allow_nan=False)
            handle.write('\n')
    print(json.dumps(dict(output=str(OUT), variant_score_rows=len(rows), pooled_checks=len(reproduced), support_cells=len(support))))


if __name__ == '__main__':
    main()
