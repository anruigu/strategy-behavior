"""Synthetic secondary controls; no API calls or empirical outcomes."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from prediction.games import make_game, payoff
from prediction.prospective import build_rows, score
from prediction.secondary_baselines import (EQUILIBRIUM_METHOD, CONTEXT_METHOD, EQUILIBRIUM_TARGETS,
    equilibrium_distribution, equilibrium_prediction, fit_contexts, context_prediction,
    fit_bundle, forecast_bundle, sha, compare, retrospective)


class SecondaryBaselineTests(unittest.TestCase):
    def test_unique_pure_and_payoff_dominant_stag(self):
        cases = [('pd', (3, 0, 5, 1), 0., 0.),
                 ('harmony', (3, 2, 1, 0), 1., 1.),
                 ('stag', (4, 0, 3, 2), 1., 1.)]
        for name, values, action0, cooperation in cases:
            game = make_game(name, *values)
            distribution = equilibrium_distribution(game)
            self.assertEqual(distribution['rule'], 'payoff_dominant_symmetric_pure')
            self.assertEqual(equilibrium_prediction(game, 'action0'), action0)
            self.assertEqual(equilibrium_prediction(game, 'first_action0'), action0)
            self.assertEqual(equilibrium_prediction(game, 'cooperation'), cooperation)
            if name == 'stag':
                self.assertTrue(game['features']['has_interior_mixed_equilibrium'])
                self.assertEqual(equilibrium_prediction(game, 'coordination'), 1.)
            for target in EQUILIBRIUM_TARGETS:
                self.assertEqual(equilibrium_prediction(game, target, 0), equilibrium_prediction(game, target, 1))
        self.assertIsNone(equilibrium_prediction(game, 'retaliation'))

    def test_tied_pures_are_joint_conventions_and_label_marginal(self):
        game = make_game('tie', 3, 0, 1, 3)
        distribution = equilibrium_distribution(game)
        self.assertEqual(distribution['profiles'], [dict(actions=[0, 0], probability=.5), dict(actions=[1, 1], probability=.5)])
        self.assertFalse(distribution['independent'])
        self.assertEqual(equilibrium_prediction(game, 'action0'), .5)
        self.assertEqual(equilibrium_prediction(game, 'coordination'), 1.)
        self.assertIsNone(equilibrium_prediction(game, 'cooperation'))
        self.assertEqual(sum((1-int(swap))/2 for swap in (False, True)), .5)
        self.assertEqual(sum(row['probability']*payoff(game, *row['actions'])[0] for row in distribution['profiles']), 3.)
        for profile in distribution['profiles']:
            self.assertEqual(*payoff(game, *profile['actions']))
        indifferent = make_game('all-tied', 1, 1, 1, 1)
        self.assertEqual(equilibrium_prediction(indifferent, 'action0'), .5)
        self.assertIsNone(equilibrium_prediction(indifferent, 'coordination'))

    def test_no_symmetric_pure_keeps_independent_mixed_and_action_swap(self):
        for values in ((0, 1, 3, 0), (3, 2, 5, 1)):
            game = make_game('mixed', *values)
            distribution = equilibrium_distribution(game)
            self.assertTrue(distribution['independent'])
            q = game['features']['mixed_equilibrium_action0_probability']
            self.assertAlmostEqual(sum(p['probability'] for p in distribution['profiles']), 1.)
            self.assertAlmostEqual(equilibrium_prediction(game, 'action0'), q)
            self.assertAlmostEqual(equilibrium_prediction(game, 'coordination'), 2*q*(1-q))
            swapped = make_game('swap', values[3], values[2], values[1], values[0])
            self.assertAlmostEqual(equilibrium_prediction(swapped, 'action0'), 1-q)
            self.assertAlmostEqual(equilibrium_prediction(swapped, 'coordination'), equilibrium_prediction(game, 'coordination'))
            if game['applicability']['cooperative_action'] is not None:
                c = game['applicability']['cooperative_action']
                self.assertAlmostEqual(equilibrium_prediction(game, 'cooperation'), (q if c == 0 else 1-q)**2)

    def test_context_event_objective_uses_global_game_mass_and_ordered_roles(self):
        def row(group, model, opponent, s, n):
            return dict(group_id=group, model=model, opponent=opponent,
                        targets={'retaliation': dict(value=s/n if n else None, successes=s,
                                                    opportunities=n, applicable=True)})
        rows = [row('g1', 'a', 'b', 100, 100), row('g2', 'a', 'b', 0, 1), row('g2', 'b', 'a', 0, 99)]
        rows.append(dict(group_id='g2', model='a', opponent='b', targets={'retaliation':
                         dict(value=None, successes=None, opportunities=None, applicable=True)}))
        fits = fit_contexts(rows)
        self.assertAlmostEqual(context_prediction(fits, {'model': 'a', 'opponent': 'b'}, 'retaliation')[0], 100/101)
        self.assertEqual(context_prediction(fits, {'model': 'b', 'opponent': 'a'}, 'retaliation')[0], 0.)
        probability, fallback, count = context_prediction(fits, {'model': 'new', 'opponent': 'b'}, 'retaliation')
        self.assertEqual(probability, .5)
        self.assertIn('population mean', fallback)
        self.assertEqual(count, 3)
        self.assertIsNone(context_prediction(fits, {'model': 'a', 'opponent': 'b'}, 'forgiveness')[0])
        self.assertEqual(fits['retaliation']['contexts'][0]['eligible_rows'], 2)

    @patch('prediction.prospective.plot_scores')
    def test_frozen_artifact_and_full_metadata_score_without_primary_changes(self, _plot):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory); stage = root/'stage'; stage.mkdir()
            game = make_game('tie', 3, 0, 1, 3)
            manifest = dict(models={'a': {}, 'b': {}}, games=[game], episodes=[dict(
                id=f'episode-{trial}', game_id='tie', models=['a', 'b'], trial_id=trial,
                representation='matrix', swap=bool(trial)) for trial in range(2)])
            (stage/'manifest.json').write_text(json.dumps(manifest))
            metadata = build_rows(manifest)
            artifact, forecasts = root/'fit.json', root/'secondary.jsonl'
            fitted = fit_bundle(None, artifact)
            rows = forecast_bundle(artifact, metadata, forecasts, stage_root=stage)
            self.assertEqual(len(rows), len(metadata)*4)
            self.assertTrue(all(r['method'] == EQUILIBRIUM_METHOD and r['secondary_post_pilot'] for r in rows))
            self.assertEqual({r['prediction'] for r in rows if r['target'] == 'coordination'}, {1.})
            self.assertEqual({r['prediction'] for r in rows if r['target'] == 'action0'}, {.5})
            original = forecasts.read_bytes()
            with self.assertRaises(FileExistsError):
                forecast_bundle(artifact, metadata, forecasts)
            records = []
            for row in metadata:
                records.append(dict(row, targets={'action0': dict(value=.5, successes=4, opportunities=8, applicable=True),
                    'coordination': dict(value=1., successes=8, opportunities=8, applicable=True)}))
            record_path = root/'records.json'; record_path.write_text(json.dumps(records))
            starts = (datetime.now(timezone.utc)+timedelta(seconds=1)).isoformat()
            for episode in manifest['episodes']:
                folder = stage/'episodes'/episode['id']; folder.mkdir(parents=True)
                (folder/'trace.json').write_text(json.dumps(dict(id=episode['id'], started=starts)))
            result = score(forecasts, record_path, root/'evaluation', stage_root=stage, bootstrap=0)
            self.assertTrue(result['audit']['prospective_verified'])
            self.assertEqual(forecasts.read_bytes(), original)
            with self.assertRaisesRegex(ValueError, 'before any target stage'):
                forecast_bundle(artifact, metadata, root/'late.jsonl', stage_root=stage)

    def test_combined_export_binds_primary_and_rejects_labels(self):
        from prediction.test_prospective import fixture
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory)
            _, metadata, primary_rows, training, primary, _ = fixture(directory)
            artifact = root/'fit.json'
            fit_bundle(training, artifact)
            original = primary.read_bytes()
            output = root/'combined.jsonl'
            rows = forecast_bundle(artifact, metadata, output, primary_forecasts=primary)
            self.assertEqual(len(rows), len(primary_rows)+len(metadata)*11)
            self.assertEqual(primary.read_bytes(), original)
            self.assertTrue(any(r['method'] == CONTEXT_METHOD for r in rows))
            manifest = json.loads(output.with_suffix('.manifest.json').read_text())
            self.assertEqual(manifest['source_forecast_and_artifact_sha256'][str(primary.resolve())], sha(original))
            with self.assertRaisesRegex(ValueError, 'no outcome labels'):
                forecast_bundle(artifact, training, root/'leaked.jsonl')
            primary.write_bytes(original+b'\n')
            with self.assertRaisesRegex(ValueError, 'hash/input identity'):
                forecast_bundle(artifact, metadata, root/'corrupt.jsonl', primary_forecasts=primary)

    @patch('prediction.prospective.plot_scores')
    def test_compare_requires_verified_audits_matching_original_probabilities_and_outcomes(self, _plot):
        from prediction.test_prospective import fixture
        from prediction.modeling import TARGETS
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory)
            stage, metadata, old, training, primary, records = fixture(directory)
            full = [dict(row, target=target) for row in old if row['target'] == 'action0' for target in TARGETS]
            primary.write_text(''.join(json.dumps(row)+'\n' for row in full))
            manifest_path = primary.with_suffix('.manifest.json')
            manifest = json.loads(manifest_path.read_text())
            manifest.update(forecast_sha256=sha(primary.read_bytes()), rows=len(full))
            manifest_path.write_text(json.dumps(manifest))
            artifact, secondary = root/'fit.json', root/'secondary.jsonl'
            fit_bundle(training, artifact)
            forecast_bundle(artifact, metadata, secondary)
            for trace in (stage/'episodes').glob('*/trace.json'):
                value = json.loads(trace.read_text())
                value['started'] = (datetime.now(timezone.utc)+timedelta(seconds=1)).isoformat()
                trace.write_text(json.dumps(value))
            pdir, sdir = root/'primary-evaluation', root/'secondary-evaluation'
            score(primary, records, pdir, stage_root=stage, bootstrap=0)
            score(secondary, records, sdir, stage_root=stage, bootstrap=0)
            result = compare(pdir, sdir, root/'comparison', bootstrap=0)
            self.assertTrue(result['comparisons_to_secondary'])
            self.assertIn('prospective', result['secondary_classification'])
            joined_path = sdir/'joined-predictions.jsonl'
            original_joined = joined_path.read_bytes()
            joined = [json.loads(line) for line in original_joined.splitlines()]
            joined[0]['prediction'] = .314159
            joined_path.write_text(''.join(json.dumps(row)+'\n' for row in joined))
            with self.assertRaisesRegex(ValueError, 'frozen source forecast'):
                compare(pdir, sdir, root/'bad-probability', bootstrap=0)
            joined_path.write_bytes(original_joined)
            joined_path.write_bytes(original_joined+original_joined.splitlines(keepends=True)[0])
            with self.assertRaisesRegex(ValueError, 'Duplicate method'):
                compare(pdir, sdir, root/'duplicate', bootstrap=0)
            joined_path.write_bytes(original_joined)
            audit_path = sdir/'audit.json'
            audit = json.loads(audit_path.read_text()); audit['prospective_verified'] = False
            audit_path.write_text(json.dumps(audit))
            with self.assertRaisesRegex(ValueError, 'verified prospective audits'):
                compare(pdir, sdir, root/'unverified', bootstrap=0)

    @patch('prediction.prospective.plot_scores')
    @patch('prediction.analysis.plot_comparisons')
    def test_retrospective_reuses_saved_folds_and_rejects_changed_input(self, _primary_plot, _plot):
        from prediction.test_prospective import fixture
        from prediction.modeling import evaluate, ModelSpec
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory)
            _, _, _, records, _, record_path = fixture(directory)
            evaluation = root/'original-evaluation'
            evaluate(records, evaluation, specs=[ModelSpec('pair', 'pair'), ModelSpec('nash', 'nash')],
                     splits=['family'], bootstrap=0)
            original = (evaluation/'predictions.jsonl').read_bytes()
            result = retrospective(record_path, evaluation, root/'posthoc', bootstrap=0)
            self.assertEqual(result['secondary_classification'], 'secondary_post_pilot_retrospective_sensitivity')
            self.assertEqual((evaluation/'predictions.jsonl').read_bytes(), original)
            audit = json.loads((root/'posthoc'/'audit.json').read_text())
            folds = json.loads((evaluation/'folds.json').read_text())
            self.assertEqual([(f['train'], f['test']) for f in audit['fold_fit_audit']],
                             [(f['train'], f['test']) for f in folds])
            records[0]['targets']['action0'].update(value=.5, successes=4)
            record_path.write_text(json.dumps(records))
            with self.assertRaisesRegex(ValueError, 'original numerical input'):
                retrospective(record_path, evaluation, root/'changed-input', bootstrap=0)


if __name__ == '__main__':
    unittest.main()
