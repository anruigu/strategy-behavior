"""Prespecified ex-ante numerical predictors. Run ``python -m prediction.modeling --help``.

All numerical fitting is local. ``fit`` reads training labels, ``forecast`` needs only
game/model metadata, and ``evaluate`` is an explicitly requested grouped validation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import pickle
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
import warnings

ROOT = Path(__file__).resolve().parent
TEMP = Path('/shared/allie/home/.codex/tmp')
os.environ.setdefault('TMPDIR', str(TEMP))
os.environ.setdefault('MPLCONFIGDIR', str(TEMP / 'matplotlib-prediction'))
os.environ.setdefault('JOBLIB_TEMP_FOLDER', str(TEMP / 'joblib-prediction'))
if (ROOT / 'vendor').exists():
    sys.path.insert(0, str(ROOT / 'vendor'))

import numpy as np
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.neural_network import MLPRegressor
from sklearn.exceptions import ConvergenceWarning
import sklearn
from threadpoolctl import threadpool_limits

VERSION = '1.1'
TARGETS = ('action0', 'first_action0', 'cooperation', 'retaliation',
           'forgiveness', 'coordination', 'exploitation')
SEED = 20260910


@dataclass(frozen=True)
class ModelSpec:
    name: str
    estimator: str
    representation: str = 'none'
    identity: str = 'none'


NASH_TARGETS = ('action0', 'first_action0', 'cooperation', 'individual_cooperation', 'coordination')
SPECS = [ModelSpec('marginal', 'marginal'), ModelSpec('pair', 'pair'),
         ModelSpec('nash', 'nash'),
         ModelSpec('family', 'family')]
SPECS += [ModelSpec(f'{rep}_{est}', est, rep)
          for est in ('ridge', 'logistic') for rep in ('raw', 'structural', 'combined')]
SPECS += [ModelSpec('combined_mlp', 'mlp', 'combined'),
          ModelSpec('combined_mlp_both', 'mlp', 'combined', 'both')]
SPECS += [ModelSpec(f'combined_logistic_{identity}', 'logistic', 'combined', identity)
          for identity in ('model', 'opponent', 'both')]


def specification() -> dict:
    return {
        'version': VERSION, 'seed': SEED, 'models': [s.__dict__ for s in SPECS],
        'targets': TARGETS, 'primary_split': 'family',
        'ridge_alpha_grid': [0.1, 1.0, 10.0], 'logistic_C_grid': [0.1, 1.0, 10.0],
        'inner_validation': 'up to 3 canonical-game-group folds; train-only scaling/encoding',
        'tuning_tie_break': 'stronger regularization',
        'minimum_training_support': '4 eligible rows and 2 canonical game groups',
        'minimum_tuning_groups': 4,
        'mlp': {'hidden_layer_sizes': [16], 'activation': 'tanh', 'solver': 'lbfgs',
                'alpha': 1.0, 'max_iter': 300, 'early_stopping': False},
        'training_weighting': {
            'ridge_mlp_baselines': 'equal game groups, equal eligible focal rows within group',
            'logistic': 'success/failure pseudo-observations; equal groups and event weight within group',
            'regularization_scale': 'total training weight equals number of eligible game groups'},
        'unknown_identity': 'all-zero identity indicator; fitted game/intercept pathway, no learned unseen-model embedding (MLP nonlinear output is not guaranteed to equal a population mean)',
        'unknown_pair_family': 'training population mean',
        'pair_baseline_context': 'ordered (focal model, opponent model); split grouping remains unordered',
        'baseline_comparisons': 'paired improvements against both marginal and ordered model/opponent context',
        'artifact_write_policy': 'fit/forecast artifacts and companion manifests refuse existing paths',
        'no_training_support': 'null forecast; never invent zero for missing labels',
        'probability_clip': 'clip regressor outputs to [0,1]; log scoring clips to [1e-6,1-1e-6]',
        'parameter_split': 'canonical_t=(T-P)/(R-P) after R>P orientation, group mean; undefined groups excluded; interpolation middle tercile, upper extrapolation top tercile; canonical_s explicit secondary',
        'dependence': 'entire episode always retained together; game splits purge equivalent-game groups; pair/model/representation transfer intentionally reuses known games',
        'metrics': 'common supported held-out rows; game-equal rate MAE/RMSE/correlation and event Brier/logloss/ECE',
        'inference_input': 'payoffs, deterministic game features, declared model/opponent identity only',
        'structural_feature_exclusions': 'raw_*, normalized_R/S/T/P, payoff_offset/scale/mean/variance; structural means derived affine-normalized incentives/equilibrium/dominance/welfare statistics',
        'nash_comparator': 'memoryless independent symmetric play: unique pure equilibrium; else symmetric interior mixed; else first symmetric boundary in order action0/action1; all-indifferent uniform. Universal action, mutual/individual cooperation, coordination only; no conditional-target forecasts.',
    }


def output_path(value) -> Path:
    path = Path(value).resolve()
    if not path.is_relative_to(Path('/shared/allie')):
        raise ValueError('Created artifacts must be under /shared/allie')
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path, obj):
    path = output_path(path)
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')


def write_jsonl(path, rows):
    path = output_path(path)
    with path.open('w') as handle:
        for row in rows:
            handle.write(json.dumps(row, allow_nan=False) + '\n')


def load_records(path) -> list[dict]:
    path = Path(path)
    if path.suffix == '.jsonl':
        return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    data = json.loads(path.read_text())
    if isinstance(data, dict):
        data = data.get('records', data.get('measurements'))
    if not isinstance(data, list):
        raise ValueError('Input must be a JSON list, JSONL, or {records: [...]}')
    return data


def group_id(row):
    value = row.get('group_id')
    if value is None:
        raise ValueError('Every row requires a canonical group_id')
    return str(value)


def pair_id(row):
    return '|'.join(sorted((str(row['model']), str(row['opponent']))))


def ordered_context(row):
    """Behavior baseline preserves focal roles; pair_id is only a split key."""
    return str(row['model']), str(row['opponent'])


def require_new_paths(*paths):
    resolved = [output_path(path) for path in paths]
    for path in resolved:
        if path.exists():
            raise FileExistsError(f'Refusing to overwrite frozen artifact: {path}')
    return resolved


def write_new_json(path, obj):
    with output_path(path).open('x') as handle:
        handle.write(json.dumps(obj, indent=2, allow_nan=False) + '\n')


def supported_target(row, target):
    cell = row.get('targets', {}).get(target)
    if not cell or cell.get('applicable') is not True:
        return None
    value, successes, opportunities = (cell.get(k) for k in ('value', 'successes', 'opportunities'))
    if opportunities is None or value is None or successes is None:
        return None
    if not isinstance(opportunities, (int, float)) or not math.isfinite(opportunities):
        raise ValueError(f'Invalid opportunity count for {target}')
    if opportunities <= 0:
        return None
    if not 0 <= successes <= opportunities or not 0 <= value <= 1:
        raise ValueError(f'Invalid counts/rate for {target}')
    if int(opportunities) != opportunities or int(successes) != successes:
        raise ValueError('Binomial target counts must be integers')
    if abs(value - successes / opportunities) > 1e-7:
        raise ValueError(f'Rate and counts disagree for {target}')
    return {'value': float(value), 'successes': int(successes), 'opportunities': int(opportunities)}


def row_weights(rows, target=None, events=False):
    """Unit total mass per game, optionally event-weighted within each game."""
    base = np.asarray([supported_target(r, target)['opportunities'] if events else 1.0
                       for r in rows], dtype=float)
    totals = defaultdict(float)
    for row, value in zip(rows, base):
        totals[group_id(row)] += value
    weights = np.asarray([v / totals[group_id(r)] for r, v in zip(rows, base)])
    return weights


def population_mean(rows, target):
    if not rows:
        return None
    y = [supported_target(r, target)['value'] for r in rows]
    return float(np.average(y, weights=row_weights(rows)))


class FeatureEncoder:
    """Fit numeric scaling and identity vocabularies on training metadata only."""
    def __init__(self, representation='combined', identity='none'):
        self.representation, self.identity = representation, identity

    def fit(self, rows, weights):
        self.feature_keys = []
        if self.representation in ('raw', 'combined'):
            self.feature_keys += [('payoffs', k) for k in ('R', 'S', 'T', 'P')]
        if self.representation in ('structural', 'combined'):
            keys = sorted({k for r in rows for k, v in r.get('features', {}).items()
                           if isinstance(v, (int, float)) and not k.startswith('raw_')
                           and k not in ('payoff_offset', 'payoff_scale', 'payoff_mean', 'payoff_variance',
                                         'normalized_R', 'normalized_S', 'normalized_T', 'normalized_P')})
            self.feature_keys += [('features', k) for k in keys]
        self.identity_fields = {'none': [], 'model': ['model'], 'opponent': ['opponent'],
                                'both': ['model', 'opponent']}[self.identity]
        self.categories = {k: sorted({str(r[k]) for r in rows}) for k in self.identity_fields}
        raw = self._numeric(rows)
        self.mean = np.average(raw, weights=weights, axis=0) if raw.shape[1] else np.zeros(0)
        self.scale = np.sqrt(np.average((raw - self.mean) ** 2, weights=weights, axis=0)) if raw.shape[1] else np.ones(0)
        self.scale[self.scale < 1e-10] = 1.0
        return self

    def _numeric(self, rows):
        values = []
        for row in rows:
            vector = []
            for source, key in self.feature_keys:
                val = row.get(source, {}).get(key)
                if val is None or not isinstance(val, (int, float)) or not math.isfinite(val):
                    raise ValueError(f'Missing/nonfinite ex-ante feature {source}.{key}')
                vector.append(float(val))
            values.append(vector)
        return np.asarray(values, dtype=float).reshape((len(rows), len(self.feature_keys)))

    def transform(self, rows):
        blocks = [(self._numeric(rows) - self.mean) / self.scale]
        for field in self.identity_fields:
            blocks.append(np.asarray([[float(str(r[field]) == category) for category in self.categories[field]]
                                      for r in rows]))
        matrix = np.concatenate(blocks, axis=1)
        # A constant column supports an empty deterministic feature schema.
        return matrix if matrix.shape[1] else np.zeros((len(rows), 1))

    def unknown(self, row):
        return [field for field in self.identity_fields if str(row[field]) not in self.categories[field]]


def _random_group_folds(rows, seed, n_splits=3):
    groups = np.asarray(sorted({group_id(r) for r in rows}))
    np.random.default_rng(seed).shuffle(groups)
    for chunk in np.array_split(groups, min(n_splits, len(groups))):
        if len(chunk):
            selected = set(chunk)
            yield [i for i, r in enumerate(rows) if group_id(r) not in selected], [i for i, r in enumerate(rows) if group_id(r) in selected]


def _fit_estimator(spec, rows, target, parameter, seed):
    weighted_events = spec.estimator == 'logistic'
    weights = row_weights(rows, target, weighted_events)
    encoder = FeatureEncoder(spec.representation, spec.identity).fit(rows, weights)
    x = encoder.transform(rows)
    cells = [supported_target(r, target) for r in rows]
    y = np.asarray([v['value'] for v in cells])
    warning_messages = []
    if spec.estimator == 'logistic':
        n = np.asarray([v['opportunities'] for v in cells])
        s = np.asarray([v['successes'] for v in cells])
        # Fractional trial counts are represented exactly by two weighted classes.
        expanded_weights = np.concatenate((weights * s / n, weights * (n - s) / n))
        keep = expanded_weights > 0
        expanded_x = np.concatenate((x, x), axis=0)[keep]
        expanded_y = np.concatenate((np.ones(len(x)), np.zeros(len(x))))[keep]
        if len(np.unique(expanded_y)) < 2:
            return encoder, None, ['single observed event class']
        estimator = LogisticRegression(C=parameter, solver='lbfgs', max_iter=500, random_state=seed)
        fit_x, fit_y, fit_weights = expanded_x, expanded_y, expanded_weights[keep]
    elif spec.estimator == 'ridge':
        estimator = Ridge(alpha=parameter)
        fit_x, fit_y, fit_weights = x, y, weights
    elif spec.estimator == 'mlp':
        estimator = MLPRegressor(hidden_layer_sizes=(16,), activation='tanh', solver='lbfgs',
                                 alpha=1.0, max_iter=300, random_state=seed, early_stopping=False)
        fit_x, fit_y, fit_weights = x, y, weights
    else:
        raise ValueError(spec.estimator)
    with warnings.catch_warnings(record=True) as caught, threadpool_limits(limits=1):
        warnings.simplefilter('always', ConvergenceWarning)
        estimator.fit(fit_x, fit_y, sample_weight=fit_weights)
        warning_messages = [str(item.message) for item in caught]
    return encoder, estimator, warning_messages


def _predict_estimator(encoder, estimator, rows):
    x = encoder.transform(rows)
    with threadpool_limits(limits=1):
        if isinstance(estimator, LogisticRegression):
            return estimator.predict_proba(x)[:, list(estimator.classes_).index(1.0)]
        return np.clip(estimator.predict(x), 0.0, 1.0)


def nash_prediction(row, target):
    from prediction.games import make_game
    game = make_game('nash_comparator', **row['payoffs'])
    features, app = game['features'], game['applicability']
    pure = game['pure_nash']
    if features['all_indifferent']:
        q = .5
    elif len(pure) == 1 and pure[0][0] == pure[0][1]:
        q = float(pure[0][0] == 0)
    elif features['has_interior_mixed_equilibrium']:
        q = features['mixed_equilibrium_action0_probability']
    elif features['nash_00']:
        q = 1.0
    elif features['nash_11']:
        q = 0.0
    else:
        return None
    if target in ('action0', 'first_action0'):
        return q
    if target in ('cooperation', 'individual_cooperation'):
        c = app['cooperative_action']
        if c is None:
            return None
        cooperate = q if c == 0 else 1-q
        return cooperate**2 if target == 'cooperation' else cooperate
    if target == 'coordination' and app['coordination']:
        prob = {0: q, 1: 1-q}
        return sum(prob[a]*prob[b] for a, b in app['coordination_outcomes'])
    return None


class FittedPredictor:
    def __init__(self, spec, target, seed=SEED):
        self.spec, self.target, self.seed = spec, target, seed

    def fit(self, records, tune=True):
        rows = [] if self.spec.estimator == 'nash' else [r for r in records if supported_target(r, self.target) is not None]
        self.training_count = len(rows)
        self.training_groups = sorted({group_id(r) for r in rows})
        self.default = population_mean(rows, self.target)
        self.encoder, self.estimator = None, None
        self.lookup, self.tuning = {}, []
        self.warnings, self.fallback_reason = [], None
        self.parameter = None
        if self.spec.estimator == 'nash':
            return self
        if not rows:
            self.fallback_reason = 'no eligible training observations'
            return self
        if self.spec.estimator in ('pair', 'family'):
            grouped = defaultdict(list)
            for row in rows:
                key = ordered_context(row) if self.spec.estimator == 'pair' else str(row['family'])
                grouped[key].append(row)
            self.lookup = {k: population_mean(v, self.target) for k, v in grouped.items()}
            return self
        if self.spec.estimator == 'marginal':
            return self
        if len(rows) < 4 or len(self.training_groups) < 2:
            self.fallback_reason = 'fewer than 4 rows or 2 eligible game groups'
            return self
        values = [supported_target(r, self.target)['value'] for r in rows]
        if max(values) - min(values) < 1e-12:
            self.fallback_reason = 'constant training rate'
            return self
        grid = [0.1, 1.0, 10.0] if self.spec.estimator in ('ridge', 'logistic') else [1.0]
        self.parameter = 1.0
        if tune and len(grid) > 1 and len(self.training_groups) >= 4:
            inner_folds = list(_random_group_folds(rows, self.seed))
            for parameter in grid:
                squared, eval_rows = [], []
                for train, test in inner_folds:
                    inner_train, inner_test = [rows[i] for i in train], [rows[i] for i in test]
                    enc, est, _ = _fit_estimator(self.spec, inner_train, self.target, parameter, self.seed)
                    pred = _predict_estimator(enc, est, inner_test) if est is not None else np.full(len(test), population_mean(inner_train, self.target))
                    squared.extend((p - supported_target(r, self.target)['value']) ** 2 for p, r in zip(pred, inner_test))
                    eval_rows.extend(inner_test)
                score = float(np.average(squared, weights=row_weights(eval_rows, self.target, self.spec.estimator == 'logistic')))
                self.tuning.append({'parameter': parameter, 'inner_group_mse': score})
            self.parameter = min(self.tuning, key=lambda item: (item['inner_group_mse'],
                                 -item['parameter'] if self.spec.estimator == 'ridge' else item['parameter']))['parameter']
        self.encoder, self.estimator, self.warnings = _fit_estimator(self.spec, rows, self.target, self.parameter, self.seed)
        if self.estimator is None:
            self.fallback_reason = '; '.join(self.warnings)
        return self

    def predict(self, rows):
        if self.spec.estimator == 'nash':
            return [nash_prediction(r, self.target) for r in rows]
        if self.estimator is not None:
            return [float(v) for v in _predict_estimator(self.encoder, self.estimator, rows)]
        result = []
        for row in rows:
            key = ordered_context(row) if self.spec.estimator == 'pair' else str(row.get('family'))
            result.append(self.lookup.get(key, self.default))
        return result

    def metadata(self):
        return {'spec': self.spec.__dict__, 'target': self.target, 'training_count': self.training_count,
                'training_groups': self.training_groups, 'population_fallback': self.default,
                'fallback_reason': self.fallback_reason, 'parameter': self.parameter,
                'tuning': self.tuning, 'warnings': self.warnings,
                'feature_keys': self.encoder.feature_keys if self.encoder else [],
                'identity_categories': self.encoder.categories if self.encoder else {}}

    def row_fallback(self, row):
        if self.fallback_reason:
            return self.fallback_reason
        if self.spec.estimator == 'pair' and ordered_context(row) not in self.lookup:
            return 'unknown ordered model/opponent context: population mean'
        if self.spec.estimator == 'family' and str(row.get('family')) not in self.lookup:
            return 'unknown family: population mean'
        if self.encoder and self.encoder.unknown(row):
            return 'unknown identity: zero indicators for ' + ','.join(self.encoder.unknown(row))
        return None


def _parameter_value(row, parameter):
    val = row.get('split_metadata', {}).get(parameter)
    if val is None:
        return None
    if not isinstance(val, (int, float)) or not math.isfinite(val):
        raise ValueError(f'No finite label-independent split parameter {parameter}')
    return float(val)


def build_folds(records, kind='family', seed=SEED, n_splits=5, parameter='canonical_t'):
    """Split indices without touching targets; purge complete episodes in every split."""
    folds = []
    def append(name, test, detail=None, excluded=None):
        test = set(test)
        excluded = set(excluded or [])
        train = set(range(len(records))) - test - excluded
        if not train or not test:
            return
        episodes_train = {records[i].get('episode_id') for i in train} - {None}
        episodes_test = {records[i].get('episode_id') for i in test} - {None}
        if episodes_train & episodes_test:
            raise ValueError(f'{kind} would split the focal rows of an episode')
        folds.append({'name': str(name), 'kind': kind, 'train': sorted(train), 'test': sorted(test),
                      'excluded': sorted(excluded), 'detail': detail or {}, 'train_groups': sorted({group_id(records[i]) for i in train}),
                      'test_groups': sorted({group_id(records[i]) for i in test})})
    if kind == 'random_group':
        for number, (_, test) in enumerate(_random_group_folds(records, seed, n_splits)):
            append(f'random_{number}', test)
    elif kind == 'family':
        for family in sorted({str(r['family']) for r in records}):
            groups = {group_id(r) for r in records if str(r['family']) == family}
            append(f'family_{family}', [i for i, r in enumerate(records) if group_id(r) in groups], {'held_out_family': family})
    elif kind == 'pair':
        for pair in sorted({pair_id(r) for r in records}):
            append(f'pair_{pair}', [i for i, r in enumerate(records) if pair_id(r) == pair], {'held_out_pair': pair})
    elif kind == 'model':
        for model in sorted({str(r[k]) for r in records for k in ('model', 'opponent')}):
            append(f'model_{model}', [i for i, r in enumerate(records) if model in (str(r['model']), str(r['opponent']))], {'held_out_model': model})
    elif kind in ('interpolation', 'extrapolation'):
        grouped = defaultdict(list)
        undefined = set()
        for row in records:
            value = _parameter_value(row, parameter)
            if value is None:
                undefined.add(group_id(row))
            else:
                grouped[group_id(row)].append(value)
        for group in undefined:
            grouped.pop(group, None)
        coordinates = {g: float(np.mean(v)) for g, v in grouped.items()}
        unique = sorted(set(coordinates.values()))
        if len(unique) < 3:
            return []
        lo, hi = np.quantile(list(coordinates.values()), [1/3, 2/3])
        selected = {g for g, v in coordinates.items() if (lo < v <= hi if kind == 'interpolation' else v > hi)}
        append(kind, [i for i, r in enumerate(records) if group_id(r) in selected],
               {'parameter': parameter, 'undefined_groups': sorted(undefined), 'group_coordinates': coordinates,
                'lower_cut': float(lo), 'upper_cut': float(hi), 'test_region': 'middle' if kind == 'interpolation' else 'upper'},
               excluded=[i for i, r in enumerate(records) if group_id(r) in undefined])
    elif kind == 'representation':
        for representation in sorted({str(r.get('representation', 'matrix')) for r in records}):
            if representation == 'matrix':
                continue
            append(f'representation_{representation}', [i for i, r in enumerate(records) if r.get('representation') == representation],
                   {'training_representation': 'matrix', 'held_out_representation': representation},
                   excluded=[i for i, r in enumerate(records) if r.get('representation', 'matrix') not in ('matrix', representation)])
    else:
        raise ValueError(f'Unknown split {kind}')
    return folds


def prediction_rows(predictor, records, indices=None, split='prospective', fold='fitted'):
    if predictor.spec.estimator == 'nash' and predictor.target not in NASH_TARGETS:
        return []
    if indices is None:
        indices = range(len(records))
    result = []
    for index, row, prediction in zip(indices, records, predictor.predict(records)):
        cell = supported_target(row, predictor.target)
        result.append({
            'row_index': int(index), 'episode_id': row.get('episode_id'), 'game_id': row.get('game_id'),
            'player_index': row.get('player_index'), 'swap': row.get('swap'),
            'group_id': group_id(row), 'family': row.get('family'), 'model': row.get('model'),
            'opponent': row.get('opponent'), 'pair': pair_id(row), 'trial_id': row.get('trial_id'),
            'representation': row.get('representation', 'matrix'), 'target': predictor.target,
            'method': predictor.spec.name, 'split': split, 'fold': fold, 'prediction': prediction,
            'value': cell['value'] if cell else None, 'successes': cell['successes'] if cell else None,
            'opportunities': cell['opportunities'] if cell else None, 'eligible': cell is not None,
            'fallback': predictor.row_fallback(row), 'training_count': predictor.training_count})
    return result


def evaluate(records, outdir, specs=None, targets=TARGETS, splits=('family',), seed=SEED,
             n_splits=5, parameter='canonical_t', tune=True, bootstrap=300):
    from prediction.analysis import summarize_predictions, plot_comparisons
    outdir = output_path(Path(outdir) / 'placeholder').parent
    specs = SPECS if specs is None else specs
    write_json(outdir / 'specification.json', specification())
    write_json(outdir / 'run_config.json', {'created_utc': datetime.now(timezone.utc).isoformat(),
        'seed': seed, 'targets': list(targets), 'methods': [s.name for s in specs],
        'splits': list(splits), 'random_group_folds': n_splits, 'parameter': parameter,
        'tune': tune, 'bootstrap': bootstrap, 'record_count': len(records),
        'input_sha256': hashlib.sha256(json.dumps(records, sort_keys=True, allow_nan=False).encode()).hexdigest()})
    folds = [fold for split in splits for fold in build_folds(records, split, seed, n_splits, parameter)]
    write_json(outdir / 'folds.json', folds)
    all_predictions, fits = [], []
    for number, fold in enumerate(folds):
        training = [records[i] for i in fold['train']]
        test = [records[i] for i in fold['test']]
        print(json.dumps({'event': 'fold_start', 'fold': fold['name'], 'fold_number': number + 1,
                          'fold_count': len(folds), 'train_rows': len(training), 'test_rows': len(test)}), flush=True)
        for target in targets:
            for spec in specs:
                predictor = FittedPredictor(spec, target, seed).fit(training, tune=tune)
                all_predictions.extend(prediction_rows(predictor, test, fold['test'], fold['kind'], fold['name']))
                fits.append({'split': fold['kind'], 'fold': fold['name'], **predictor.metadata()})
    write_jsonl(outdir / 'predictions.jsonl', all_predictions)
    write_json(outdir / 'fit_audit.json', fits)
    summary = summarize_predictions(all_predictions, bootstrap=bootstrap, seed=seed)
    write_json(outdir / 'scores.json', summary)
    plot_comparisons(summary, outdir / 'comparison.png')
    return summary


def fit_bundle(records, artifact, specs=None, targets=TARGETS, seed=SEED, tune=True):
    path = output_path(artifact)
    sidecar = path.with_suffix(path.suffix + '.json')
    require_new_paths(path, sidecar)
    specs = SPECS if specs is None else specs
    predictors = [FittedPredictor(spec, target, seed).fit(records, tune=tune) for target in targets for spec in specs]
    metadata = {'version': VERSION, 'created_utc': datetime.now(timezone.utc).isoformat(),
                'sklearn_version': sklearn.__version__, 'numpy_version': np.__version__,
                'training_rows': len(records), 'training_sha256': hashlib.sha256(json.dumps(records, sort_keys=True, allow_nan=False).encode()).hexdigest(),
                'actual_configuration': {'seed': seed, 'tune': tune, 'targets': list(targets), 'methods': [s.name for s in specs]},
                'specification': specification(), 'fits': [p.metadata() for p in predictors]}
    with path.open('xb') as handle:
        handle.write(pickle.dumps({'metadata': metadata, 'predictors': predictors}, protocol=5))
    write_new_json(sidecar, metadata)
    return metadata


def forecast_bundle(artifact, records, output):
    output = output_path(output)
    manifest = output.with_suffix('.manifest.json')
    require_new_paths(output, manifest)
    bundle = pickle.loads(Path(artifact).read_bytes())
    forecasts = [row for p in bundle['predictors'] for row in prediction_rows(p, records)]
    with output.open('x') as handle:
        for row in forecasts:
            handle.write(json.dumps(row, allow_nan=False) + '\n')
    write_new_json(manifest, {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'artifact_sha256': hashlib.sha256(Path(artifact).read_bytes()).hexdigest(),
        'input_sha256': hashlib.sha256(json.dumps(records, sort_keys=True, allow_nan=False).encode()).hexdigest(),
        'forecast_sha256': hashlib.sha256(Path(output).read_bytes()).hexdigest(),
        'artifact_training_sha256': bundle['metadata']['training_sha256'], 'rows': len(forecasts)})
    return forecasts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    protocol = sub.add_parser('protocol', help='write prespecified methods without reading labels')
    protocol.add_argument('--output', required=True)
    for name in ('fit', 'evaluate'):
        p = sub.add_parser(name)
        p.add_argument('--input', required=True, help='measurement JSON/JSONL; training only for fit')
        p.add_argument('--targets', default=','.join(TARGETS))
        p.add_argument('--methods', default=','.join(s.name for s in SPECS))
        p.add_argument('--seed', type=int, default=SEED)
        p.add_argument('--no-tune', action='store_true', help='use fixed regularization=1; record explicitly')
        if name == 'fit':
            p.add_argument('--artifact', required=True)
        else:
            p.add_argument('--outdir', required=True)
            p.add_argument('--splits', default='family')
            p.add_argument('--folds', type=int, default=5)
            p.add_argument('--parameter', default='canonical_t')
            p.add_argument('--bootstrap', type=int, default=300)
    forecast = sub.add_parser('forecast', help='freeze predictions before target rollouts')
    forecast.add_argument('--artifact', required=True)
    forecast.add_argument('--input', required=True, help='feature/model/opponent rows; targets may be absent')
    forecast.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    if args.command == 'protocol':
        write_json(args.output, {'frozen_utc': datetime.now(timezone.utc).isoformat(), **specification()})
        return
    records = load_records(args.input)
    if args.command == 'forecast':
        forecast_bundle(args.artifact, records, args.output)
        return
    selected = args.methods.split(',')
    by_name = {s.name: s for s in SPECS}
    if set(selected) - set(by_name):
        parser.error('Unknown methods: ' + ','.join(set(selected) - set(by_name)))
    specs = [by_name[n] for n in selected]
    targets = args.targets.split(',')
    if args.command == 'fit':
        fit_bundle(records, args.artifact, specs, targets, args.seed, not args.no_tune)
    else:
        evaluate(records, args.outdir, specs, targets, args.splits.split(','), args.seed,
                 args.folds, args.parameter, not args.no_tune, args.bootstrap)


if __name__ == '__main__':
    # Keep pickled classes in the canonical package module across CLI/API usage.
    from prediction.modeling import main as package_main
    package_main()
