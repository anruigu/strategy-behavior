"""Actual artifact writers -> continuation audit/scorer/gate, synthetic data only.

The baseline optimizer and its Fleet authority check are mocked: no fitting,
model loading, subprocesses, API calls, or empirical files are used.
"""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from prediction.improve import baselines, evaluate, gate, transformer
from prediction.improve.data import TARGETS, aggregate_records, build_folds, metadata_examples, write_new
from prediction.improve.integrate import immutable, prompted, read
from prediction.improve.post_training import Work, hashes, record_evidence, save, sha
from prediction.improve.test_data import PROTOCOL, synthetic_records

TMP = '/shared/allie/home/.codex/tmp'


def constant_fits(*args):
    return {method: dict(kind='constant', prediction=.5) for method in baselines.METHODS}


def fixture(root):
    """Write exact current worker schemas without executing an optimizer."""
    train = aggregate_records(synthetic_records(42), PROTOCOL)
    development = aggregate_records(synthetic_records(7, 5678), PROTOCOL)
    fresh = metadata_examples(synthetic_records(7, 9999), PROTOCOL)
    data = dict(targets=list(TARGETS), train_examples=train, development_examples=development)
    folds = build_folds(train, development)
    (root/'data').mkdir()
    data_path, folds_path = root/'data/data.json', root/'data/folds.json'
    write_new(data_path, data); write_new(folds_path, folds)
    inputs = hashes([data_path, folds_path])
    job = 'synthetic-job-never-submitted'
    save(root/'fleet-runtime/training-status.json', dict(status='complete', fleet_run_id=job))
    with patch.object(baselines, 'fleet_guard'), patch.object(baselines, 'fit_methods', side_effect=constant_fits) as fitter:
        baselines.run_worker(data_path, folds_path, root/'baselines', job)
        assert fitter.call_count == 30
    fitted = dict(mean=np.zeros(2), scale=np.ones(2), weight=np.zeros((3, 2)),
                  bias=np.zeros(3), supported=np.ones(3, dtype=bool))
    for kind, method in transformer.METHODS.items():
        for fold in folds:
            folder = root/'transformer'/kind/fold['fold_id']
            contract = dict(method=method, fold=fold, input_sha256=inputs)
            transformer.prepare_fit_folder(folder, contract, False)
            selected_train = [train[i] for i in fold['train']]
            dataset = train if fold['test_dataset'] == 'train' else development
            query = [dataset[i] for i in fold['test']]
            transformer.finish_fit(folder, fitted,
                dict(fleet=dict(fleet_run_id=job), optimization_success=True), contract, inputs, selected_train)
            transformer.export_forecasts(folder, query, np.full((len(query), 3), .5), fitted['supported'],
                method, fold['split'], fold['fold_id'], contract, inputs)
            transformer.complete_fit(folder, inputs)
    scopes = [fold['fold_id'] for fold in folds if fold['split'] in ('family', 'development')]
    for sid in scopes:
        query = fresh if sid == 'full' else [r for r in fresh if r['family'] == sid[len('family_'):]]
        split = 'fresh_full' if sid == 'full' else 'fresh_family_excluded'
        query_path = root/'queries'/f'{sid}.json'
        save(query_path, query)
        baselines.forecast(root/'baselines/fits.json', query_path,
            root/'fresh-forecasts/baselines'/sid/'forecasts.jsonl', split, sid)
        for kind, method in transformer.METHODS.items():
            fit_folder = root/'transformer'/kind/sid
            forecast_inputs = {**inputs, **hashes([query_path, fit_folder/'artifact.json', fit_folder/'complete.json']),
                               **read(fit_folder/'complete.json')['output_sha256']}
            # The actual fresh writer puts artifact identity inside contract,
            # while its input map binds all fitted checkpoint bytes.
            contract = dict(fit_artifact_sha256=sha(fit_folder/'artifact.json'),
                            fit_method=method, fit_fold_id=sid, fleet=dict(fleet_run_id=job))
            transformer.export_forecasts(root/'fresh-forecasts'/kind/sid, query,
                np.full((len(query), 3), .5), fitted['supported'], method, split, sid, contract, forecast_inputs)
    original_prompted = root/'synthetic-original-prompted.jsonl'
    source_rows = [dict(game_id=e['game_id'], model=e['model'], opponent=e['opponent'],
        method='llm_few_shot', target=t, prediction=.5 if t == 'action0' or e['applicability'][t] else None,
        prediction_created_utc='2026-09-10T00:00:00+00:00') for e in development for t in TARGETS]
    immutable(original_prompted, source_rows, jsonl=True)
    prompted(original_prompted, development, root/'development-few-shot/forecasts.jsonl', 'development', 'full')
    write_new(root/'gate-protocol.json', gate.protocol())
    work = Work(root, 0)
    work.plan = dict(existing_fleet_run_id=job, scopes=scopes, input_sha256=inputs)
    save(work.folder/'plan.json', work.plan)
    return work, data, folds


class SchemaIntegrationTests(unittest.TestCase):
    def test_actual_writers_pass_training_audit_development_score_and_gate(self):
        with tempfile.TemporaryDirectory(dir=TMP, prefix='improve-schema-synthetic-') as temporary:
            root = Path(temporary); work, data, folds = fixture(root)
            work.audit_training()
            audit = read(work.folder/'training-audit.json')
            self.assertEqual(audit['transformer_fits'], 20)
            self.assertEqual(audit['status'], 'verified')
            record_evidence(work.folder/'training-audit.json')
            # Exercise original Kimi sidecar's scalar hashes, both call forms.
            prompt = root/'development-few-shot/forecasts.manifest.json'
            self.assertEqual(record_evidence(prompt),
                             record_evidence(prompt, root/'development-few-shot/forecasts.jsonl'))
            original_score = evaluate.score_files
            def small_synthetic_score(data_path, folds_path, paths, out):
                return original_score(data_path, folds_path, paths, out, 20)
            with patch.object(evaluate, 'score_files', side_effect=small_synthetic_score) as scorer:
                work.score_development()
                work.score_development()  # Resume verifies nested score outputs.
                self.assertEqual(scorer.call_count, 1)
            scores = read(root/'development-evaluation/scores.json')
            self.assertEqual(set(scores['available_methods_by_split']['development']),
                set(baselines.METHODS) | set(transformer.METHODS.values()) | {'llm_few_shot'})
            self.assertNotIn('llm_few_shot', scores['available_methods_by_split']['family'])
            self.assertTrue(work.apply_gate())  # Equal fixed .5 forecasts are inconclusive.
            self.assertTrue(work.apply_gate())
            decision = read(root/'development-gate.json')
            self.assertEqual(len(decision['cells']), 12)
            self.assertEqual(len(decision['verified_transformer_fits']), 20)
            for cell in decision['cells']:
                self.assertAlmostEqual(cell['improvement'], 0)
            (root/'transformer/frozen/full/head.npz').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'changed'):
                work.audit_training()


if __name__ == '__main__':
    unittest.main()
