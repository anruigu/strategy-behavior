"""Synthetic forecast-freeze, identity, coverage and probability-scoring checks."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from prediction.games import make_game
from prediction.prospective import (build_rows, build_rows_file, canonical_hash, sha, score,
                                   join_forecasts, _frozen_identity)


def fixture(directory):
    stage = Path(directory)/'stage'
    stage.mkdir()
    games = [make_game('g0', 3, 0, 5, 1), make_game('g1', 4, 0, 3, 2)]
    manifest = {'games': games, 'models': {'a': {'model_id': 'a'}, 'b': {'model_id': 'b'}},
                'episodes': [], 'protocol': {'rounds': 8, 'temperature': .7, 'max_tokens': 16384, 'max_attempts': 2}}
    for game in games:
        for trial in range(2):
            for pair in (['a', 'b'], ['a', 'a']):
                manifest['episodes'].append({'id': f"{game['id']}-{trial}-{'-'.join(pair)}", 'game_id': game['id'],
                    'models': pair, 'trial_id': trial, 'representation': 'matrix', 'swap': bool(trial)})
    (stage/'manifest.json').write_text(json.dumps(manifest))
    planned = build_rows(manifest)
    forecasts, records = [], []
    for index, row in enumerate(planned):
        y = float(row['player_index'] == 0)
        observation = copy.deepcopy(row)
        observation['targets'] = {'action0': {'value': y, 'successes': int(8*y), 'opportunities': 8, 'applicable': True},
            'forgiveness': {'value': None, 'successes': 0, 'opportunities': 0, 'applicable': True}}
        records.append(observation)
        for method in ('perfect', 'wrong'):
            for target in ('action0', 'forgiveness'):
                forecasts.append({**row, 'row_index': index, 'method': method, 'target': target,
                    'prediction': (y if method == 'perfect' else 1-y) if target == 'action0' else .7,
                    'value': None, 'successes': None, 'opportunities': None, 'eligible': False,
                    'split': 'prospective', 'fold': 'fitted'})
    for spec in manifest['episodes']:
        path = stage/'episodes'/spec['id']
        path.mkdir(parents=True)
        (path/'trace.json').write_text(json.dumps({'id': spec['id'], 'started': '2026-06-03T12:00:00+00:00'}))
    forecast_path = Path(directory)/'forecasts.jsonl'
    forecast_path.write_text(''.join(json.dumps(row)+'\n' for row in forecasts))
    freeze = {'created_utc': '2026-06-01T12:00:00+00:00', 'forecast_sha256': sha(forecast_path.read_bytes()),
              'input_sha256': canonical_hash(planned), 'rows': len(forecasts)}
    forecast_path.with_suffix('.manifest.json').write_text(json.dumps(freeze))
    record_path = Path(directory)/'records.json'
    record_path.write_text(json.dumps(records))
    return stage, planned, forecasts, records, forecast_path, record_path


class ProspectiveTests(unittest.TestCase):
    def test_build_rows_is_label_free_and_focal_roles_exact(self):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            stage, planned, *_ = fixture(directory)
            output = Path(directory)/'metadata.json'
            rows = build_rows_file(stage/'manifest.json', output)
            self.assertEqual(rows, planned)
            self.assertTrue(all('targets' not in row for row in rows))
            self.assertEqual({row['player_index'] for row in rows}, {0, 1})
            self.assertEqual(rows[0]['model'], rows[1]['opponent'])
            with self.assertRaises(FileExistsError):
                build_rows_file(stage/'manifest.json', output)

    @patch('prediction.prospective.plot_scores')
    def test_perfect_wrong_scores_and_forecast_bytes_preserved(self, _plot):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            stage, _, _, _, forecasts, records = fixture(directory)
            original = forecasts.read_bytes()
            result = score(forecasts, records, Path(directory)/'score', stage_root=stage, bootstrap=20)
            self.assertTrue(result['audit']['prospective_verified'])
            rows = [row for row in result['scores']['scores'] if row['target'] == 'action0']
            self.assertEqual(next(row for row in rows if row['method'] == 'perfect')['event_brier'], 0.)
            self.assertEqual(next(row for row in rows if row['method'] == 'wrong')['event_brier'], 1.)
            self.assertEqual(forecasts.read_bytes(), original)
            self.assertEqual(result['coverage']['missing_planned_outcomes'], [])

    @patch('prediction.prospective.plot_scores')
    def test_missing_outcomes_and_zero_unknown_opportunities(self, _plot):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            stage, planned, numerical, records, forecasts, record_path = fixture(directory)
            records = records[2:]
            records[0]['targets']['forgiveness']['successes'] = None
            records[0]['targets']['forgiveness']['opportunities'] = None
            record_path.write_text(json.dumps(records))
            result = score(forecasts, record_path, Path(directory)/'score', stage_root=stage, bootstrap=0)
            self.assertEqual(len(result['coverage']['missing_planned_outcomes']), 2)
            joined, _, _ = join_forecasts(numerical, [], records, planned)
            self.assertTrue(all(not r['eligible'] and r['value'] is None for r in joined if r['target'] == 'forgiveness'))
            unknown = [r for r in joined if r['episode_id'] == records[0]['episode_id'] and r['player_index'] == records[0]['player_index'] and r['target'] == 'forgiveness']
            self.assertTrue(all(r['opportunities'] is None for r in unknown))
            self.assertTrue(any(r['opportunities'] == 0 for r in joined if r['target'] == 'forgiveness'))

    def test_duplicate_unexpected_and_conflicting_identities_rejected(self):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            _, planned, numerical, records, *_ = fixture(directory)
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                join_forecasts(numerical+[numerical[0]], [], records, planned)
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                join_forecasts(numerical, [], records+[records[0]], planned)
            bad = copy.deepcopy(records)
            bad[0]['payoffs']['R'] += 1
            with self.assertRaisesRegex(ValueError, 'payoffs'):
                join_forecasts(numerical, [], bad, planned)
            bad = copy.deepcopy(records)
            bad[0]['episode_id'] = 'unexpected'
            with self.assertRaisesRegex(ValueError, 'Unexpected'):
                join_forecasts(numerical, [], bad, planned)

    @patch('prediction.prospective.plot_scores')
    def test_late_forecasts_are_explicitly_unverified(self, _plot):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            stage, _, _, _, forecasts, records = fixture(directory)
            sidecar = forecasts.with_suffix('.manifest.json')
            manifest = json.loads(sidecar.read_text())
            manifest['created_utc'] = '2026-06-04T12:00:00+00:00'
            sidecar.write_text(json.dumps(manifest))
            result = score(forecasts, records, Path(directory)/'score', stage_root=stage, bootstrap=0)
            self.assertFalse(result['audit']['prospective_verified'])
            self.assertEqual(result['audit']['effective_split'], 'unverified_prospective')
            self.assertTrue(all(r['split'].startswith('unverified_') for r in result['scores']['scores']))

    def test_rewritten_forecast_and_changed_plan_rejected(self):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            stage, _, _, _, forecasts, records = fixture(directory)
            original = forecasts.read_bytes()
            forecasts.write_bytes(original+b'\n')
            with self.assertRaisesRegex(ValueError, 'frozen manifest hash'):
                score(forecasts, records, Path(directory)/'score', stage_root=stage, bootstrap=0)
            forecasts.write_bytes(original)
            path = stage/'manifest.json'
            manifest = json.loads(path.read_text())
            manifest['protocol']['max_tokens'] = 4096
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'input hash'):
                score(forecasts, records, Path(directory)/'score', stage_root=stage, bootstrap=0)

    @patch('prediction.prospective.plot_scores')
    def test_llm_probability_broadcast_and_frozen_input_audit(self, _plot):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            stage, planned, _, _, forecasts, records = fixture(directory)
            manifest = json.loads((stage/'manifest.json').read_text())
            payload = {'games': manifest['games'], 'players': manifest['models'],
                       'protocol': {'rounds': 8, 'player_temperature': .7,
                                    'player_max_completion_tokens': 16384, 'player_max_attempts': 2}}
            identity = _frozen_identity(payload)
            root = Path(directory)/'llm'; root.mkdir()
            (root/'inputs.json').write_text(json.dumps({'payload': payload, 'identity_sha256': identity}))
            contexts = {(r['game_id'], r['model'], r['opponent']): r for r in planned}
            rows = [dict(game_id=r['game_id'], group_id=r['group_id'], family=r['family'],
                         model=r['model'], opponent=r['opponent'], target='action0', method='llm_zero_shot',
                         representation='matrix', prediction=.25, value=None, successes=None, opportunities=None,
                         input_identity_sha256=identity, status='complete', prediction_created_utc='2026-06-02T12:00:00+00:00')
                    for r in contexts.values()]
            path = root/'forecasts.jsonl'
            path.write_text(''.join(json.dumps(row)+'\n' for row in rows))
            (root/'status.json').write_text(json.dumps({'finished_utc': '2026-06-02T12:01:00+00:00',
                                                      'forecast_sha256': sha(path.read_bytes())}))
            result = score(forecasts, records, Path(directory)/'score', path, stage_root=stage,
                           bootstrap=0, focus_model='a')
            self.assertTrue(result['audit']['prospective_verified'])
            joined = [json.loads(line) for line in (Path(directory)/'score'/'joined-predictions.jsonl').read_text().splitlines()]
            llm = [r for r in joined if r['method'] == 'llm_zero_shot']
            self.assertEqual(len(llm), len(planned))
            self.assertTrue(all(r['prediction'] == .25 for r in llm))
            self.assertEqual({r['player_index'] for r in llm}, {0, 1})

    @patch('prediction.prospective.plot_scores')
    def test_focus_does_not_hide_unexpected_actual_rows(self, _plot):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            stage, _, _, records, forecasts, record_path = fixture(directory)
            records[0]['model'] = 'unexpected'
            record_path.write_text(json.dumps(records))
            with self.assertRaisesRegex(ValueError, 'model'):
                score(forecasts, record_path, Path(directory)/'score', stage_root=stage,
                      bootstrap=0, focus_pair='a|b')

    @patch('prediction.prospective.plot_scores')
    def test_pair_focus_keeps_both_roles_and_validates_full_stage(self, _plot):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            stage, planned, _, _, forecasts, records = fixture(directory)
            result = score(forecasts, records, Path(directory)/'score', stage_root=stage,
                           bootstrap=0, focus_pair='b|a', split='prospective_pair')
            self.assertTrue(result['audit']['prospective_verified'])
            self.assertEqual(result['coverage']['planned_focal_rows'], len(planned))
            self.assertEqual(result['coverage']['scoring_planned_focal_rows'], len(planned)//2)
            joined = [json.loads(line) for line in (Path(directory)/'score'/'joined-predictions.jsonl').read_text().splitlines()]
            self.assertEqual({r['pair'] for r in joined}, {'a|b'})
            self.assertEqual({r['player_index'] for r in joined}, {0, 1})

    def test_source_edit_during_scoring_is_detected_before_export(self):
        from prediction.analysis import summarize_predictions
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            stage, _, _, _, forecasts, records = fixture(directory)
            def edit_then_summarize(*args, **kwargs):
                forecasts.write_bytes(forecasts.read_bytes()+b'\n')
                return summarize_predictions(*args, **kwargs)
            with patch('prediction.prospective.summarize_predictions', side_effect=edit_then_summarize):
                with self.assertRaisesRegex(ValueError, 'changed while scoring'):
                    score(forecasts, records, Path(directory)/'score', stage_root=stage, bootstrap=0)
            self.assertFalse((Path(directory)/'score').exists())


if __name__ == '__main__':
    unittest.main()
