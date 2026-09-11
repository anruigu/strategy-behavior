"""Synthetic signal recovery and leakage/eligibility tests; no API calls or real labels."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

from prediction.modeling import (FeatureEncoder, FittedPredictor, ModelSpec, SPECS,
                                 build_folds, fit_bundle, forecast_bundle,
                                 prediction_rows, supported_target, row_weights, nash_prediction)
from prediction.analysis import score_rows, summarize_predictions, _resample_blocks, paired_improvement_intervals


def synthetic(groups=24, repeats=3):
    rows = []
    rng = np.random.default_rng(81)
    for g in range(groups):
        x = -3 + 6*g/max(groups-1, 1)
        for trial in range(repeats):
            for a, b in [('a', 'a'), ('a', 'b'), ('b', 'c')]:
                episode = f'g{g}-{trial}-{a}-{b}'
                for model, opponent in [(a, b), (b, a)]:
                    probability = 1/(1+np.exp(-(1.6*x + {'a': -.5, 'b': .3, 'c': .8}[model])))
                    count = int(rng.binomial(100, probability))
                    rows.append({'episode_id': episode, 'game_id': f'g{g}', 'group_id': f'g{g}',
                                 'family': f'family_{g%3}', 'model': model, 'opponent': opponent,
                                 'trial_id': trial, 'representation': 'matrix',
                                 'payoffs': {'R': x, 'S': 0., 'T': 1., 'P': -1.},
                                 'features': {'gap_against_0': x, 'raw_R': x, 'normalized_R': x,
                                              'payoff_scale': 1.},
                                 'split_metadata': {'canonical_t': x},
                                 'targets': {'action0': {'value': count/100, 'successes': count,
                                                        'opportunities': 100, 'applicable': True}}})
    return rows


class PredictionTests(unittest.TestCase):
    def test_synthetic_structure_predicts_held_out_families(self):
        rows = synthetic()
        model_error, baseline_error = [], []
        for fold in build_folds(rows, 'family'):
            train, test = [rows[i] for i in fold['train']], [rows[i] for i in fold['test']]
            predictor = FittedPredictor(ModelSpec('signal', 'logistic', 'structural', 'both'), 'action0').fit(train)
            baseline = FittedPredictor(ModelSpec('marginal', 'marginal'), 'action0').fit(train)
            model_error.append(score_rows(prediction_rows(predictor, test))['rate_mae'])
            baseline_error.append(score_rows(prediction_rows(baseline, test))['rate_mae'])
        self.assertLess(np.mean(model_error), .075)
        self.assertLess(np.mean(model_error), .3*np.mean(baseline_error))

    def test_group_and_episode_leakage_and_unseen_model_purge(self):
        rows = synthetic(12, 1)
        variants = copy.deepcopy(rows)
        for row in variants:
            row['game_id'] += '_affine'
            row['episode_id'] += '_affine'
            row['payoffs'] = {k: 7*v+10 for k, v in row['payoffs'].items()}
        rows += variants
        for kind in ('family', 'random_group', 'interpolation', 'extrapolation', 'pair', 'model'):
            for fold in build_folds(rows, kind):
                train = [rows[i] for i in fold['train']]
                test = [rows[i] for i in fold['test']]
                self.assertFalse({r['episode_id'] for r in train} & {r['episode_id'] for r in test})
                if kind in ('family', 'random_group', 'interpolation', 'extrapolation'):
                    self.assertFalse({r['group_id'] for r in train} & {r['group_id'] for r in test})
                if kind == 'model':
                    held = fold['detail']['held_out_model']
                    self.assertTrue(all(held not in (r['model'], r['opponent']) for r in train))

    def test_scaling_unknown_identity_and_feature_ablation(self):
        rows = synthetic(6, 1)
        encoder = FeatureEncoder('structural', 'both').fit(rows, row_weights(rows))
        self.assertEqual(encoder.feature_keys, [('features', 'gap_against_0')])
        mean, scale = encoder.mean.copy(), encoder.scale.copy()
        unseen = copy.deepcopy(rows[0])
        unseen['features']['gap_against_0'] = 10000.
        unseen['model'] = 'brand_new'
        unseen['opponent'] = 'also_new'
        x = encoder.transform([unseen])
        self.assertTrue(np.array_equal(mean, encoder.mean))
        self.assertTrue(np.array_equal(scale, encoder.scale))
        self.assertTrue(np.all(x[0, 1:] == 0))
        self.assertEqual(set(encoder.unknown(unseen)), {'model', 'opponent'})

    def test_missing_counts_remain_missing(self):
        rows = synthetic(6, 1)
        for row in rows:
            row['targets']['action0'] = {'value': None, 'successes': 0, 'opportunities': 0, 'applicable': True}
        model = FittedPredictor(ModelSpec('ridge', 'ridge', 'raw'), 'action0').fit(rows)
        self.assertIsNone(supported_target(rows[0], 'action0'))
        self.assertIsNone(model.predict(rows[:1])[0])
        forecasts = prediction_rows(model, rows[:2])
        self.assertIsNone(forecasts[0]['value'])
        self.assertIsNone(forecasts[0]['opportunities'])
        self.assertEqual(summarize_predictions(forecasts, bootstrap=0)['scores'][0]['rows'], 0)

    def test_undefined_parameter_is_excluded_not_zero(self):
        rows = synthetic(9, 1)
        for row in rows:
            if row['group_id'] == 'g0':
                row['split_metadata']['canonical_t'] = None
        fold = build_folds(rows, 'extrapolation')[0]
        self.assertTrue(fold['excluded'])
        self.assertTrue(all(rows[i]['group_id'] == 'g0' for i in fold['excluded']))
        self.assertFalse(set(fold['excluded']) & set(fold['train'] + fold['test']))
        train_values = [rows[i]['split_metadata']['canonical_t'] for i in fold['train']]
        test_values = [rows[i]['split_metadata']['canonical_t'] for i in fold['test']]
        self.assertLess(max(train_values), min(test_values))

    def test_count_brier_and_equal_game_weight(self):
        base = {'episode_id': 'e', 'prediction': .25, 'value': .5, 'successes': 1,
                'opportunities': 2, 'group_id': 'g0'}
        second = {**base, 'group_id': 'g1', 'episode_id': 'f', 'prediction': 1., 'value': 1.,
                  'successes': 100, 'opportunities': 100}
        one = score_rows([base, second])
        duplicated = score_rows([base]*10 + [second])
        self.assertAlmostEqual(one['event_brier'], .15625)
        self.assertAlmostEqual(one['rate_mae'], .125)
        self.assertAlmostEqual(one['event_brier'], duplicated['event_brier'])
        self.assertAlmostEqual(one['rate_mae'], duplicated['rate_mae'])
        rows = [{**base, 'row_index': 0}, {**base, 'row_index': 1}]
        resampled = _resample_blocks(rows, np.random.default_rng(5))
        self.assertEqual([r['row_index'] for r in resampled], [0, 1])

    def test_common_support_and_artifact_forecast_without_labels(self):
        rows = synthetic(8, 1)
        specs = [ModelSpec('marginal', 'marginal'), ModelSpec('logistic', 'logistic', 'raw')]
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            artifact = Path(directory) / 'model.pkl'
            fit_bundle(rows, artifact, specs, ['action0'])
            unlabeled = copy.deepcopy(rows[:2])
            for row in unlabeled:
                row.pop('targets')
            forecast_path = Path(directory) / 'forecast.jsonl'
            forecasts = forecast_bundle(artifact, unlabeled, forecast_path)
            self.assertTrue(all(r['prediction'] is not None for r in forecasts))
            self.assertTrue(all(r['value'] is None for r in forecasts))
            # Exercise independent process deserialization, not only in-memory use.
            input_path = Path(directory) / 'input.json'
            input_path.write_text(json.dumps(unlabeled))
            subprocess.run([sys.executable, '-B', '-m', 'prediction.modeling', 'forecast',
                            '--artifact', str(artifact), '--input', str(input_path),
                            '--output', str(Path(directory) / 'child.jsonl')], check=True,
                           cwd=Path(__file__).resolve().parents[1], capture_output=True)
        fitted = [FittedPredictor(s, 'action0').fit(rows) for s in specs]
        predictions = [r for p in fitted for r in prediction_rows(p, rows[:2])]
        predictions[-1]['prediction'] = None
        summary = summarize_predictions(predictions, bootstrap=0)
        self.assertTrue(all(r['rows'] == 1 for r in summary['scores']))

    def test_small_mlp_fits_finite_probabilities(self):
        rows = synthetic(8, 1)
        mlp = FittedPredictor(ModelSpec('mlp', 'mlp', 'raw'), 'action0').fit(rows, tune=False)
        predictions = mlp.predict(rows)
        self.assertTrue(all(0 <= v <= 1 for v in predictions))
        baseline = FittedPredictor(ModelSpec('marginal', 'marginal'), 'action0').fit(rows)
        self.assertLess(score_rows(prediction_rows(mlp, rows))['rate_mae'],
                        .6*score_rows(prediction_rows(baseline, rows))['rate_mae'])

    def test_nash_selection_and_conditional_availability(self):
        pd = {'payoffs': {'R': 3, 'S': 0, 'T': 5, 'P': 1}}
        self.assertEqual(nash_prediction(pd, 'action0'), 0.)
        self.assertEqual(nash_prediction(pd, 'cooperation'), 0.)
        stag = {'payoffs': {'R': 4, 'S': 0, 'T': 3, 'P': 2}}
        self.assertAlmostEqual(nash_prediction(stag, 'action0'), 2/3)
        self.assertAlmostEqual(nash_prediction(stag, 'cooperation'), 4/9)
        self.assertAlmostEqual(nash_prediction(stag, 'coordination'), 5/9)
        model = FittedPredictor(ModelSpec('nash', 'nash'), 'forgiveness').fit([])
        self.assertEqual(prediction_rows(model, synthetic(3, 1)), [])

    def test_paired_block_intervals_exact_known_improvement(self):
        baseline, improved = [], []
        for i in range(8):
            y = float(i%2)
            row = {'episode_id': f'e{i}', 'group_id': f'g{i//2}', 'row_index': i, 'fold': 'f',
                   'prediction': .5, 'value': y, 'successes': int(8*y), 'opportunities': 8}
            baseline.append(row)
            improved.append({**row, 'prediction': y})
        intervals = paired_improvement_intervals(baseline, improved, repetitions=50)
        self.assertAlmostEqual(intervals['event_brier']['lower'], .25)
        self.assertAlmostEqual(intervals['event_brier']['upper'], .25)
        self.assertAlmostEqual(intervals['rate_mae']['lower'], .5)

    def test_ordered_context_controls_directional_model_differences(self):
        rows = [r for r in synthetic(6, 1) if {r['model'], r['opponent']} == {'a', 'b'}]
        for row in rows:
            successes = 90 if row['model'] == 'a' else 10
            row['targets']['action0'] = {'value': successes/100, 'successes': successes,
                                        'opportunities': 100, 'applicable': True}
        specs = [ModelSpec('marginal', 'marginal'), ModelSpec('pair', 'pair'),
                 ModelSpec('identity_only_copy', 'pair')]
        predictors = [FittedPredictor(spec, 'action0').fit(rows) for spec in specs]
        ordered = predictors[1]
        forward = next(r for r in rows if r['model'] == 'a')
        reverse = next(r for r in rows if r['model'] == 'b')
        self.assertAlmostEqual(ordered.predict([forward])[0], .9)
        self.assertAlmostEqual(ordered.predict([reverse])[0], .1)
        summary = summarize_predictions([r for p in predictors for r in prediction_rows(p, rows)], bootstrap=20)
        global_comparison = next(r for r in summary['comparisons_to_marginal'] if r['method'] == 'identity_only_copy')
        context_comparison = next(r for r in summary['comparisons_to_pair'] if r['method'] == 'identity_only_copy')
        self.assertGreater(global_comparison['improvement']['event_brier'], .1)
        self.assertAlmostEqual(context_comparison['improvement']['event_brier'], 0.)
        self.assertAlmostEqual(context_comparison['intervals']['event_brier']['lower'], 0.)
        # Withholding a pair still removes both directed contexts together.
        for fold in build_folds(synthetic(4, 1), 'pair'):
            if fold['detail']['held_out_pair'] == 'a|b':
                test = [synthetic(4, 1)[i] for i in fold['test']]
                self.assertEqual({r['model'] for r in test}, {'a', 'b'})

    def test_fit_and_forecast_preserve_existing_artifacts_and_sidecars(self):
        rows = synthetic(4, 1)
        specs = [ModelSpec('marginal', 'marginal')]
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            artifact = Path(directory) / 'frozen.pkl'
            fit_bundle(rows, artifact, specs, ['action0'])
            original = artifact.read_bytes()
            with self.assertRaises(FileExistsError):
                fit_bundle(rows, artifact, specs, ['action0'])
            self.assertEqual(artifact.read_bytes(), original)
            sidecar_only = Path(directory) / 'sidecar-only.pkl'
            sidecar_only.with_suffix('.pkl.json').write_text('existing manifest')
            with self.assertRaises(FileExistsError):
                fit_bundle(rows, sidecar_only, specs, ['action0'])
            self.assertFalse(sidecar_only.exists())
            forecast = Path(directory) / 'frozen.jsonl'
            forecast_bundle(artifact, rows[:1], forecast)
            original = forecast.read_bytes()
            with self.assertRaises(FileExistsError):
                forecast_bundle(artifact, rows[:1], forecast)
            self.assertEqual(forecast.read_bytes(), original)
            manifest_only = Path(directory) / 'manifest-only.jsonl'
            manifest_only.with_suffix('.manifest.json').write_text('existing forecast manifest')
            with self.assertRaises(FileExistsError):
                forecast_bundle(artifact, rows[:1], manifest_only)
            self.assertFalse(manifest_only.exists())


if __name__ == '__main__':
    unittest.main()
