from copy import deepcopy
from pathlib import Path
import json
import tempfile
import unittest

from prediction.prospective import build_rows
from prediction.improve.data import aggregate_records, metadata_examples
from prediction.improve.prospective_design import (
    FAMILIES, TARGETS, audit_manifest, build_scopes, digest, forecast_coverage,
    freeze_forecast_evidence, fresh_games, make_manifest, no_players_started, sha,
    verify_prepared,
)


TMP = Path('/shared/allie/home/.codex/tmp')


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, allow_nan=False)+'\n')


def primary_fixture():
    return dict(models={m: dict(model_id=m, temperature=.7) for m in ('a', 'b', 'c', 'd')},
                protocol=dict(rounds=8, temperature=.7, max_tokens=4096, max_attempts=2,
                              history='complete_public', objective='own_cumulative_points',
                              opponent_identity_disclosed=False), sources={},
                source_root='/shared/allie/frozen-fixture', ledger='/shared/allie/old-ledger.sqlite')


class ProspectiveDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.primary = primary_fixture()
        cls.old_games = fresh_games(set(), seed=123, per_family=1)
        cls.old_groups = {g['group_id'] for g in cls.old_games}
        old = make_manifest(cls.primary, cls.old_games, '2026-09-10T10:00:00+00:00')
        cls.training = build_rows(old)
        cls.games = fresh_games(cls.old_groups)
        cls.manifest = make_manifest(cls.primary, cls.games, '2026-09-10T10:00:00+00:00')
        cls.metadata = build_rows(cls.manifest)
        cls.scopes, cls.queries, cls.training_examples, cls.expansion = build_scopes(
            cls.training, cls.metadata, cls.primary['protocol'])
        cls.predictions = []
        qi = {q['row_id']: q for q in cls.queries}
        for scope in cls.scopes:
            for method in ('numeric', 'transformer'):
                for row_id in scope['query_row_ids']:
                    app = qi[row_id]['applicability']
                    for target in TARGETS:
                        valid = target == 'action0' or (app['cooperative_action'] is not None if target == 'cooperation' else app['coordination'])
                        cls.predictions.append(dict(scope_id=scope['scope_id'], method=method,
                                                    row_id=row_id, target=target,
                                                    prediction=.4 if valid else None))

    def coverage(self, rows=None, exclusions=()):
        return forecast_coverage(self.scopes, self.queries, self.predictions if rows is None else rows,
                                 ['numeric', 'transformer'], ['numeric'], exclusions)

    def test_exact_fresh_family_and_pair_label_design(self):
        result = audit_manifest(self.manifest, self.primary, self.old_groups)
        self.assertEqual((result['groups'], result['episodes'], result['focal_rows']), (28, 560, 1120))
        self.assertEqual(result['families'], {f: 4 for f in FAMILIES})
        self.assertEqual(result['self_play_episodes'], 224)
        self.assertEqual(result['label_episodes'], {'False': 280, 'True': 280})
        self.assertEqual(fresh_games(self.old_groups), self.games)

    def test_observed_collisions_are_skipped_without_changing_family_quotas(self):
        blocked = {g['group_id'] for g in self.games}
        other = fresh_games(blocked | self.old_groups)
        self.assertFalse(blocked & {g['group_id'] for g in other})
        self.assertEqual([sum(g['family'] == f for g in other) for f in FAMILIES], [4]*7)

    def test_manifest_rejects_display_pair_and_payoff_corruption(self):
        corruptions = [lambda m: m['episodes'][0].update(swap=not m['episodes'][0]['swap']),
                       lambda m: m['episodes'].pop(),
                       lambda m: m['games'][0]['payoffs'].update(R=999),
                       lambda m: m['protocol'].update(rounds=9)]
        for corrupt in corruptions:
            with self.subTest(corrupt=corrupt):
                changed = deepcopy(self.manifest); corrupt(changed)
                with self.assertRaises(ValueError):
                    audit_manifest(changed, self.primary, self.old_groups)

    def test_new_budget_ledger_does_not_mutate_original_manifest(self):
        before = deepcopy(self.primary)
        ledger = '/shared/allie/new-authorized/authorization-budget.sqlite'
        manifest = make_manifest(self.primary, self.games, '2026-09-10T10:00:00+00:00', ledger=ledger)
        self.assertEqual(self.primary, before)
        self.assertEqual(manifest['ledger'], ledger)
        self.assertEqual(manifest['stage_budget_usd'], 150)
        audit_manifest(manifest, self.primary, self.old_groups, ledger=ledger)
        with self.assertRaises(ValueError):
            make_manifest(self.primary, self.games, '2026-09-10T10:00:00+00:00', stage_budget_usd=151)

    def test_lofo_scopes_exclude_both_focal_roles_and_all_family_examples(self):
        self.assertEqual(len(self.scopes), 8)
        self.assertEqual(len(self.queries), 448)
        for scope in self.scopes[1:]:
            f = scope['excluded_family']
            self.assertEqual(len(scope['query_row_ids']), 64)
            self.assertTrue(all(self.training[i]['family'] != f for i in scope['train_original_row_indices']))
            self.assertTrue(all(self.metadata[i]['family'] == f for i in scope['query_original_row_indices']))
            selected = set(scope['train_original_row_indices'])
            for i in selected:
                same = {j for j, r in enumerate(self.training) if r['episode_id'] == self.training[i]['episode_id']}
                self.assertTrue(same <= selected)
        self.assertEqual(sorted(i for s in self.scopes[1:] for i in s['query_original_row_indices']), list(range(1120)))

    def test_context_expansion_preserves_self_play_duplicates_and_cross_play_roles(self):
        qi = {q['row_id']: q for q in self.queries}
        for item in self.expansion:
            q = qi[item['row_id']]
            self.assertEqual(len(item['outcomes']), 4 if q['model'] == q['opponent'] else 2)
            for outcome in item['outcomes']:
                raw = self.metadata[outcome['original_row_index']]
                self.assertEqual((raw['model'], raw['opponent']), (q['model'], q['opponent']))
        self.assertEqual(sorted(o['original_row_index'] for e in self.expansion for o in e['outcomes']), list(range(1120)))

    def test_scope_builder_rejects_query_training_group_leakage(self):
        with self.assertRaisesRegex(ValueError, 'leaks'):
            build_scopes(self.metadata, self.metadata, self.primary['protocol'])

    def test_metadata_omits_target_outcomes_and_visible_ids(self):
        modified = deepcopy(self.metadata)
        for r in modified:
            r['targets'] = {'leaked': 'SECRET_FRESH_OUTCOME'}
        examples = metadata_examples(modified, self.primary['protocol'])
        self.assertEqual(examples, self.queries)
        for row in examples:
            self.assertNotIn(row['game_id'], row['input_text'])
            self.assertNotIn(row['group_id'], row['input_text'])
            self.assertNotIn('SECRET_FRESH_OUTCOME', row['input_text'])

    def test_complete_forecasts_and_missing_method_support(self):
        coverage = self.coverage()
        self.assertTrue(coverage['ready'])
        self.assertEqual(len(coverage['support']), 24)
        absent = next(r for r in self.predictions if r['scope_id'] == 'full' and r['method'] == 'transformer' and r['target'] == 'action0')
        rows = [r for r in self.predictions if r is not absent]
        incomplete = self.coverage(rows)
        self.assertFalse(incomplete['ready'])
        cell = next(c for c in incomplete['support'] if c['scope_id'] == 'full' and c['target'] == 'action0')
        self.assertEqual(len(cell['numerical_common_row_ids'])-len(cell['all_method_common_row_ids']), 1)
        excluded = self.coverage(rows, [dict(scope_id='full', method='transformer', reason='Documented technical failure', created_utc='2026-09-10T10:01:00+00:00')])
        self.assertTrue(excluded['ready'])
        self.assertEqual(excluded['support'], incomplete['support'])

    def test_forecast_rows_reject_invalid_probabilities_leakage_and_duplicates(self):
        for change in ({'prediction': float('nan')}, {'prediction': True}, {'prediction': 1.1},
                       {'successes': 1}, {'scope_id': 'undeclared'}):
            rows = [dict(self.predictions[0], **change), *self.predictions[1:]]
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.coverage(rows)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.coverage([*self.predictions, self.predictions[0]])

    def test_structurally_unsupported_numeric_forecast_rejected(self):
        rows = deepcopy(self.predictions)
        next(row for row in rows if row['prediction'] is None)['prediction'] = .5
        with self.assertRaisesRegex(ValueError, 'unsupported'):
            self.coverage(rows)

    def prepared_fixture(self, root):
        design = root/'prospective-design'
        source = root/'frozen-source.json'; write(source, {'frozen': True})
        files = {design/'scopes.json': self.scopes, design/'queries.json': self.queries}
        for p, d in files.items(): write(p, d)
        audit = dict(created_utc='2026-09-10T10:00:00+00:00', artifact_sha256={str(p): sha(p) for p in files},
                     contract=dict(implementation_sha256={str(source): sha(source)},
                                   primary_manifest_path=str(source), primary_manifest_sha256=sha(source), observed_sources=[]))
        write(design/'audit.json', audit)
        predictions = root/'normalized-predictions.json'; write(predictions, self.predictions)
        return source, predictions

    def test_freeze_guard_resume_and_source_input_mutations(self):
        with tempfile.TemporaryDirectory(dir=TMP) as tmp:
            root = Path(tmp)
            source, predictions = self.prepared_fixture(root)
            coverage = self.coverage()
            value = freeze_forecast_evidence(root, [source], coverage, predictions, '2026-09-10T10:02:00+00:00')
            write(root/'fresh-prospective/status.json', {'status': 'running'})
            self.assertEqual(value, freeze_forecast_evidence(root, [source], coverage, predictions))
            with self.assertRaisesRegex(ValueError, 'begun'):
                verify_prepared(root, require_unstarted=True)
            write(predictions, self.predictions[:-1])
            with self.assertRaises(ValueError):
                freeze_forecast_evidence(root, [source], coverage, predictions)
            write(predictions, self.predictions)
            write(source, {'frozen': False})
            with self.assertRaisesRegex(ValueError, 'changed'):
                verify_prepared(root)

    def test_all_startup_markers_block_first_freeze(self):
        for marker in ('process.json', 'status.json', 'episodes', 'calls'):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory(dir=TMP) as tmp:
                root = Path(tmp); source, predictions = self.prepared_fixture(root)
                path = root/'fresh-prospective'/marker;path.parent.mkdir(parents=True)
                path.mkdir() if marker in ('episodes', 'calls') else write(path, {})
                with self.assertRaisesRegex(ValueError, 'begun'):
                    freeze_forecast_evidence(root, [source], self.coverage(), predictions)

    def test_forged_coverage_or_late_exclusion_cannot_freeze(self):
        with tempfile.TemporaryDirectory(dir=TMP) as tmp:
            root = Path(tmp);source,predictions=self.prepared_fixture(root)
            coverage=self.coverage();coverage['normalized_prediction_sha256']='forged'
            with self.assertRaisesRegex(ValueError, 'coverage'):
                freeze_forecast_evidence(root,[source],coverage,predictions)
            coverage=self.coverage(exclusions=[dict(scope_id='full',method='transformer',reason='technical',created_utc='2026-09-10T10:03:00+00:00')])
            with self.assertRaisesRegex(ValueError, 'before'):
                freeze_forecast_evidence(root,[source],coverage,predictions,'2026-09-10T10:02:00+00:00')


if __name__ == '__main__':
    unittest.main()
