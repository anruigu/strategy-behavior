"""Game-weighted probability/rate scores and block uncertainty for saved forecasts."""
from __future__ import annotations

import argparse
from collections import defaultdict
import math
from pathlib import Path

from prediction.modeling import load_records, write_json, output_path, SEED
import numpy as np
from scipy.stats import rankdata


def _weights(rows, event=False):
    totals = defaultdict(float)
    for row in rows:
        totals[row['group_id']] += row['opportunities'] if event else 1.0
    values = np.asarray([(r['opportunities'] if event else 1.0) / totals[r['group_id']] for r in rows])
    return values / values.sum()


def _correlation(x, y, weights):
    x = np.asarray(x) - np.average(x, weights=weights)
    y = np.asarray(y) - np.average(y, weights=weights)
    denominator = math.sqrt(float(np.dot(weights, x*x) * np.dot(weights, y*y)))
    return float(np.dot(weights, x*y) / denominator) if denominator > 1e-12 else None


def score_rows(rows, bins=10):
    """Counts supply event scores; observed row rates supply rate error/correlation."""
    if not rows:
        return {'rows': 0, 'groups': 0, 'episodes': 0, 'opportunities': 0,
                'rate_mae': None, 'rate_rmse': None, 'event_brier': None,
                'event_log_loss': None, 'calibration_ece': None, 'pearson': None,
                'spearman': None, 'calibration': []}
    y = np.asarray([r['value'] for r in rows], dtype=float)
    p = np.asarray([r['prediction'] for r in rows], dtype=float)
    wr, we = _weights(rows), _weights(rows, event=True)
    p_safe = np.clip(p, 1e-6, 1-1e-6)
    brier = y * (1-p)**2 + (1-y) * p**2
    logloss = -(y * np.log(p_safe) + (1-y) * np.log(1-p_safe))
    bin_id = np.minimum((p * bins).astype(int), bins-1)
    calibration, ece = [], 0.0
    for b in range(bins):
        selected = bin_id == b
        if not np.any(selected):
            continue
        mass = float(we[selected].sum())
        predicted = float(np.average(p[selected], weights=we[selected]))
        observed = float(np.average(y[selected], weights=we[selected]))
        ece += mass * abs(predicted - observed)
        calibration.append({'bin': b, 'lower': b/bins, 'upper': (b+1)/bins,
                            'prediction': predicted, 'observed': observed,
                            'game_equal_event_mass': mass, 'rows': int(selected.sum()),
                            'opportunities': sum(r['opportunities'] for r, flag in zip(rows, selected) if flag)})
    return {'rows': len(rows), 'groups': len({r['group_id'] for r in rows}),
            'episodes': len({r['episode_id'] for r in rows}),
            'opportunities': sum(r['opportunities'] for r in rows),
            'rate_mae': float(np.dot(wr, np.abs(p-y))),
            'rate_rmse': math.sqrt(float(np.dot(wr, (p-y)**2))),
            'event_brier': float(np.dot(we, brier)), 'event_log_loss': float(np.dot(we, logloss)),
            'calibration_ece': float(ece), 'pearson': _correlation(p, y, wr),
            'spearman': _correlation(rankdata(p), rankdata(y), wr), 'calibration': calibration}


def _resample_blocks(rows, rng):
    """Hierarchical resampling preserves both focal players in an episode."""
    grouped = defaultdict(lambda: defaultdict(list))
    for row in rows:
        # Same row may occur in multiple model-holdout folds: retain all copies
        # inside its episode cluster rather than treating folds independently.
        grouped[row['group_id']][row['episode_id']].append(row)
    groups = sorted(grouped)
    sampled = []
    for position, group in enumerate(rng.choice(groups, size=len(groups), replace=True)):
        episodes = sorted(grouped[group], key=str)
        for epi_position, epi in enumerate(rng.choice(episodes, size=len(episodes), replace=True)):
            for row in grouped[group][epi]:
                sampled.append({**row, 'group_id': f'bootstrap_{position}',
                                'episode_id': f'bootstrap_{position}_{epi_position}'})
    return sampled


def bootstrap_intervals(rows, repetitions=300, seed=SEED):
    if repetitions <= 0 or len({r['group_id'] for r in rows}) < 2:
        return {}
    values = _bootstrap_metric_samples(rows, repetitions, seed)[0]
    return {key: {'lower': float(np.quantile(v, .025)), 'upper': float(np.quantile(v, .975))}
            for key, v in values.items()}


def _bootstrap_metric_samples(rows, repetitions, seed, comparison=None):
    """Vectorized exact game/episode bootstrap using episode sufficient statistics."""
    # Each stream stores row count, event count, two rate losses, two event
    # losses and ten calibration-bin triples. No fitted models are refit.
    streams = [rows] if comparison is None else [rows, comparison]
    grouped = defaultdict(lambda: defaultdict(list))
    for i, row in enumerate(rows):
        grouped[row['group_id']][row['episode_id']].append(i)
    groups = sorted(grouped)
    rng = np.random.default_rng(seed)
    selected = rng.integers(0, len(groups), size=(repetitions, len(groups)))
    samples = np.zeros((len(streams), repetitions, len(groups), 34))
    for group_index, group in enumerate(groups):
        positions = np.where(selected == group_index)
        if not len(positions[0]):
            continue
        episodes = list(grouped[group].values())
        multiplicities = rng.multinomial(len(episodes), np.full(len(episodes), 1/len(episodes)), size=len(positions[0]))
        for stream_index, stream in enumerate(streams):
            statistics = np.zeros((len(episodes), 36))
            for e, indices in enumerate(episodes):
                for index in indices:
                    row = stream[index]
                    n, y, p = row['opportunities'], row['value'], row['prediction']
                    safe = min(max(p, 1e-6), 1-1e-6)
                    statistics[e, :6] += [1, n, abs(p-y), (p-y)**2,
                                           n*(y*(1-p)**2+(1-y)*p**2),
                                           -n*(y*math.log(safe)+(1-y)*math.log(1-safe))]
                    b = min(int(p*10), 9)
                    statistics[e, 6+3*b:9+3*b] += [n, n*p, n*y]
            total = multiplicities @ statistics
            normalized = np.column_stack((total[:, 2:4]/total[:, :1], total[:, 4:]/total[:, 1:2]))
            samples[stream_index, positions[0], positions[1], :] = normalized
    output = []
    for sample in samples:
        mean = sample.mean(axis=1)
        calibration = mean[:, 4:].reshape((repetitions, 10, 3))
        output.append({'rate_mae': mean[:, 0], 'rate_rmse': np.sqrt(mean[:, 1]),
                       'event_brier': mean[:, 2], 'event_log_loss': mean[:, 3],
                       'calibration_ece': np.abs(calibration[:, :, 1]-calibration[:, :, 2]).sum(axis=1)})
    return output


def _prediction_key(row):
    return row['fold'], row['row_index']


def _valid(row):
    p = row.get('prediction')
    return (row.get('eligible') is True and row.get('value') is not None and
            row.get('opportunities') is not None and row['opportunities'] > 0 and
            p is not None and math.isfinite(p) and 0 <= p <= 1)


def summarize_predictions(predictions, bootstrap=300, seed=SEED):
    buckets = defaultdict(lambda: defaultdict(list))
    for row in predictions:
        buckets[row['split'], row['target']][row['method']].append(row)
    scores, fold_scores, support = [], [], []
    comparisons = {'marginal': [], 'pair': []}
    for (split, target), methods in sorted(buckets.items()):
        valid = {method: {_prediction_key(r): r for r in rows if _valid(r)} for method, rows in methods.items()}
        common = set.intersection(*(set(v) for v in valid.values())) if valid else set()
        common_rows = {method: [rows[key] for key in sorted(common)] for method, rows in valid.items()}
        support.append({'split': split, 'target': target, 'common_rows': len(common),
                        'valid_rows_by_method': {m: len(v) for m, v in valid.items()},
                        'all_rows_by_method': {m: len(v) for m, v in methods.items()},
                        'missingness': {m: dict(_missing_reasons(v)) for m, v in methods.items()}})
        for method, rows in common_rows.items():
            scores.append({'split': split, 'target': target, 'method': method,
                           **score_rows(rows), 'intervals': bootstrap_intervals(rows, bootstrap, seed)})
            fold_buckets = defaultdict(list)
            for row in rows:
                fold_buckets[row['fold']].append(row)
            for fold, subset in sorted(fold_buckets.items()):
                fold_scores.append({'split': split, 'target': target, 'method': method, 'fold': fold,
                                    **score_rows(subset)})
        # Pair preserves focal/opponent direction, controlling identity context.
        for baseline_name in ('marginal', 'pair'):
            if baseline_name not in common_rows or not common:
                continue
            baseline = common_rows[baseline_name]
            base_metrics = score_rows(baseline)
            for method, rows in common_rows.items():
                if method == baseline_name:
                    continue
                metric = score_rows(rows)
                delta = {k: base_metrics[k] - metric[k] for k in ('rate_mae', 'event_brier', 'event_log_loss')}
                intervals = paired_improvement_intervals(baseline, rows, bootstrap, seed)
                comparisons[baseline_name].append({'split': split, 'target': target, 'method': method,
                                    'baseline': baseline_name, 'positive_means_improvement': True,
                                    'improvement': delta, 'intervals': intervals})
    return {'schema_version': '1.1', 'weighting': 'equal canonical game groups; rates equal rows within group; binomial scores equal events within group',
            'uncertainty': {'method': 'hierarchical game then episode bootstrap, fixed fitted forecasts',
                            'repetitions': bootstrap, 'seed': seed,
                            'limitation': 'does not refit models; not uncertainty over training-set resampling'},
            'scores': scores, 'fold_scores': fold_scores, 'support': support,
            'comparisons_to_marginal': comparisons['marginal'],
            'comparisons_to_pair': comparisons['pair'],
            'pair_baseline_context': 'ordered (focal model, opponent model); held-pair splits remain unordered'}


def _missing_reasons(rows):
    result = defaultdict(int)
    for row in rows:
        if not row.get('eligible'):
            result['unsupported_target'] += 1
        elif row.get('prediction') is None:
            result['no_supported_training_forecast'] += 1
        elif not _valid(row):
            result['invalid_forecast_or_count'] += 1
    return result


def paired_improvement_intervals(baseline, method, repetitions=300, seed=SEED):
    if repetitions <= 0 or len({r['group_id'] for r in baseline}) < 2:
        return {}
    metrics = ('rate_mae', 'event_brier', 'event_log_loss')
    by_key = {_prediction_key(row): row for row in method}
    aligned = [by_key[_prediction_key(row)] for row in baseline]
    before, after = _bootstrap_metric_samples(baseline, repetitions, seed, aligned)
    values = {key: before[key]-after[key] for key in metrics}
    return {key: {'lower': float(np.quantile(v, .025)), 'upper': float(np.quantile(v, .975))}
            for key, v in values.items()}


def plot_comparisons(summary, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    rows = [r for r in summary['scores'] if r['split'] == 'family' and r['event_brier'] is not None]
    if not rows:
        return
    targets = sorted({r['target'] for r in rows})
    fig, axes = plt.subplots(len(targets), 1, figsize=(11, max(3, 2.6*len(targets))), squeeze=False)
    for target, axis in zip(targets, axes[:, 0]):
        target_rows = sorted([r for r in rows if r['target'] == target], key=lambda r: r['event_brier'])
        labels = [r['method'] for r in target_rows]
        value = np.asarray([r['event_brier'] for r in target_rows])
        error = np.asarray([[max(0., r['event_brier'] - r['intervals'].get('event_brier', {}).get('lower', r['event_brier'])) for r in target_rows],
                            [max(0., r['intervals'].get('event_brier', {}).get('upper', r['event_brier']) - r['event_brier']) for r in target_rows]])
        axis.errorbar(range(len(value)), value, yerr=error, fmt='o', capsize=3, color='#126B87')
        axis.set_xticks(range(len(value)), labels, rotation=30, ha='right', fontsize=8)
        axis.set_title(target, loc='left')
        axis.set_ylabel('Brier score')
        axis.grid(axis='y', alpha=.2)
    fig.suptitle('Held-out structural families: game-weighted probability prediction\nLower is better; game/episode bootstrap intervals')
    fig.tight_layout()
    fig.savefig(output_path(output), dpi=160)
    plt.close(fig)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--predictions', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--bootstrap', type=int, default=300)
    parser.add_argument('--plot')
    args = parser.parse_args(argv)
    summary = summarize_predictions(load_records(args.predictions), args.bootstrap)
    write_json(args.output, summary)
    if args.plot:
        plot_comparisons(summary, args.plot)


if __name__ == '__main__':
    main()
