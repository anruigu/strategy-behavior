"""Pure continuation decisions and manifest invariants; no API or empirical labels."""
from copy import deepcopy
from collections import Counter
import json
import tempfile
from pathlib import Path
import unittest

from prediction.after_matrix import (gate_signal, new_prospective_games, control_games,
                                     stage_manifest, checked_step, immutable_json, file_hash,
                                     expansion_decision, step_contract, score_stage)
from prediction.games import generate_games


class AfterMatrixTests(unittest.TestCase):
    def test_prespecified_gate_threshold_and_uncertainty(self):
        row = dict(split='family', target='action0', method='raw_logistic', baseline='pair',
                   improvement={'event_brier': .005}, intervals={'event_brier': {'lower': .0001, 'upper': .02}})
        scores = {'comparisons_to_pair': [row]}
        self.assertTrue(gate_signal(scores, ['family'])['passed'])
        for mutation in ({'method': 'family'}, {'baseline': 'marginal'}, {'target': 'forgiveness'},
                         {'split': 'model'}, {'improvement': {'event_brier': .00499}},
                         {'intervals': {'event_brier': {'lower': 0, 'upper': .02}}},
                         {'improvement': {'event_brier': float('nan')}}):
            self.assertFalse(gate_signal({'comparisons_to_pair': [{**row, **mutation}]}, ['family'])['passed'])
        prospective = {**row, 'split': 'prospective', 'intervals': {'event_brier': {'lower': -.02, 'upper': .03}}}
        self.assertTrue(gate_signal({'comparisons_to_pair': [prospective]}, ['prospective'], False)['passed'])
        self.assertFalse(gate_signal({'comparisons_to_pair': [prospective]}, ['prospective'], True)['passed'])
        self.assertTrue(expansion_decision({'comparisons_to_pair': [prospective]}, ['prospective'])['proceed'])
        negligible = [{**row, 'split': split, 'method': method, 'improvement': {'event_brier': .001},
                       'intervals': {'event_brier': {'lower': -.001, 'upper': .004}}}
                      for split in ('family', 'random_group')
                      for method in ('raw_logistic', 'combined_logistic_both', 'combined_mlp_both')]
        self.assertFalse(expansion_decision({'comparisons_to_pair': negligible}, ['family', 'random_group'])['proceed'])
        self.assertTrue(expansion_decision({'comparisons_to_pair': negligible[:-1]}, ['family', 'random_group'])['proceed'])
        negligible[0]['intervals']['event_brier']['upper'] = .005
        self.assertTrue(expansion_decision({'comparisons_to_pair': negligible}, ['family', 'random_group'])['proceed'])

    def test_disjoint_manifest_and_affine_presentation_controls(self):
        pilot, development = generate_games(20260910, 24), generate_games(20260911, 48)
        groups = {g['group_id'] for g in pilot+development}
        future = new_prospective_games(groups)
        self.assertEqual(len(future), 21)
        self.assertFalse({g['group_id'] for g in future} & groups)
        with self.assertRaisesRegex(ValueError, 'overlap'):
            new_prospective_games(groups | {future[0]['group_id']})
        primary = dict(models={key: {'model_id': key} for key in ('haiku', 'kimi-k3', 'qwen27', 'gpt-oss')},
                       protocol={'max_tokens': 4096, 'rounds': 8}, sources={'runner.py': 'hash'},
                       source_root='/shared/allie/test/source', ledger='/shared/allie/test/budget.sqlite')
        controls = control_games(pilot)
        manifest = stage_manifest(primary, 'controls', controls, 'test-created')
        self.assertEqual(len(manifest['episodes']), 420)
        self.assertEqual(Counter(g['control_variant'] for g in controls), {'scale3': 7, 'offset10': 7, 'abstract_text': 7})
        by_id = {game['id']: game for game in pilot}
        for game in controls:
            base = by_id[game['source_game_id']]
            self.assertEqual(game['group_id'], base['group_id'])
            for key, value in game['payoffs'].items():
                original = base['payoffs'][key]
                expected = round(original*3, 2) if game['control_variant'] == 'scale3' else round(original+10, 2) if game['control_variant'] == 'offset10' else original
                self.assertEqual(value, expected)
                self.assertAlmostEqual(value*100, round(value*100))
        game_map = {game['id']: game for game in controls}
        for episode in manifest['episodes']:
            variant = game_map[episode['game_id']]['control_variant']
            self.assertEqual(episode['representation'], 'text' if variant == 'abstract_text' else 'matrix')
            self.assertEqual(episode['swap'], bool(episode['trial_id']))
        for key in ('models', 'protocol', 'sources', 'source_root', 'ledger'):
            self.assertEqual(manifest[key], primary[key])
        manifest['protocol']['max_tokens'] = 1
        self.assertEqual(primary['protocol']['max_tokens'], 4096)
        prospective = stage_manifest(primary, 'prospective', future, 'test-created')
        self.assertEqual(len(prospective['episodes']), 420)
        self.assertEqual(len({episode['id'] for episode in prospective['episodes']}), 420)
        self.assertEqual(prospective['stage_budget_usd'], 250.)

    def test_completed_step_rejects_rewritten_outputs_and_changed_commands(self):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory)
            output = root/'forecast.json'
            source = root/'input.json'
            immutable_json(source, {'feature': 1})
            immutable_json(output, {'prediction': .25})
            marker = root/'steps'/'after-test.json'
            arguments = ['-m', 'prediction.after_matrix', '--input', str(source)]
            immutable_json(marker, {'status': 'complete', 'command': arguments, 'contract': step_contract(arguments),
                                    'output_sha256': {str(output): file_hash(output)}})
            checked_step(root, 'test', arguments, [output])
            with self.assertRaisesRegex(ValueError, 'command changed'):
                checked_step(root, 'test', arguments+['--changed'], [output])
            original = source.read_bytes()
            source.write_text('{"feature": 2}')
            with self.assertRaisesRegex(ValueError, 'inputs or computational sources changed'):
                checked_step(root, 'test', arguments, [output])
            source.write_bytes(original)
            output.write_text('{"prediction": 0.75}')
            with self.assertRaisesRegex(ValueError, 'outputs changed'):
                checked_step(root, 'test', arguments, [output])
            with self.assertRaisesRegex(ValueError, 'immutable artifact differs'):
                immutable_json(output, {'prediction': .25})

    def test_empty_common_support_scores_without_requiring_figures(self):
        from prediction.test_prospective import fixture
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory)
            _, _, rows, _, forecasts, records = fixture(directory)
            # One entirely missing method removes common support while another
            # method still has valid predictions, as a failed prompted mode can.
            for row in rows:
                if row['method'] == 'wrong':
                    row['prediction'] = None
            forecasts.write_text(''.join(json.dumps(row)+'\n' for row in rows))
            manifest_path = forecasts.with_suffix('.manifest.json')
            manifest = json.loads(manifest_path.read_text())
            manifest['forecast_sha256'] = file_hash(forecasts)
            manifest_path.write_text(json.dumps(manifest))
            result = score_stage(root, 'stage', 'evaluation', forecasts, records)
            self.assertTrue(result['audit']['prospective_verified'])
            self.assertEqual(result['comparisons_to_pair'], [])
            output = root/'stage'/'evaluation'
            summary = json.loads((output/'scores.json').read_text())
            self.assertTrue(all(row['common_rows'] == 0 for row in summary['support']))
            self.assertFalse((output/'comparison.png').exists())
            self.assertFalse((output/'calibration.png').exists())
            marker = json.loads((root/'steps'/'after-stage-evaluation.json').read_text())
            self.assertEqual(marker['status'], 'complete')
            self.assertEqual(len(marker['output_sha256']), 4)
            self.assertEqual(score_stage(root, 'stage', 'evaluation', forecasts, records), result)


if __name__ == '__main__':
    unittest.main()
