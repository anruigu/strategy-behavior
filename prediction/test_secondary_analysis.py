"""CPU-only supervisor race, resume, readiness and temporal-audit regression tests."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from prediction.io_utils import read_json
from prediction.secondary_analysis import (run_step, file_hash, ready_decision, verified_evaluation, job_specs,
                                           can_skip_unrun_job)


class SecondaryAnalysisTests(unittest.TestCase):
    def make_job(self, root, name):
        source = root/'input.json'; source.write_text('{"fixed": true}')
        job = dict(name=name, kind='retrospective', output=root/name, markers=[],
                   classification='secondary_post_pilot_retrospective_sensitivity',
                   arguments=['-m', 'prediction.secondary_baselines', 'retrospective', '--records', str(source)])
        return source, job

    def emit(self, job):
        output = job['output']; output.mkdir()
        for name, value in (('scores.json', {}), ('audit.json', {'classification': job['classification'], 'prospective_verified': False}),
                            ('secondary-comparisons.json', [])):
            (output/name).write_text(json.dumps(value))
        (output/'joined-predictions.jsonl').write_text('')

    def test_before_after_race_cannot_receive_report_eligible_audit(self):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory); source, job = self.make_job(root, 'race')
            def mutate(*args, **kwargs):
                self.emit(job)
                source.write_text('{"fixed": false}')
                return SimpleNamespace(returncode=0)
            with patch('prediction.secondary_analysis.input_paths', return_value=[source]), \
                 patch('prediction.secondary_analysis.subprocess.run', side_effect=mutate):
                with self.assertRaisesRegex(ValueError, 'input/source/artifact changed'):
                    run_step(root, job)
            self.assertFalse((job['output']/'supervisor-audit.json').exists())
            marker = read_json(root/'steps/secondary-analysis-race.json')
            self.assertEqual(marker['status'], 'error')
            self.assertFalse(marker['report_eligible'])
            self.assertNotEqual(marker['contract']['initial_sha256'][str(source)], file_hash(source))

    def test_completed_step_resumes_without_rewrites_and_rejects_mutated_output(self):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory); source, job = self.make_job(root, 'complete')
            def complete(*args, **kwargs):
                self.emit(job)
                return SimpleNamespace(returncode=0)
            with patch('prediction.secondary_analysis.input_paths', return_value=[source]), \
                 patch('prediction.secondary_analysis.subprocess.run', side_effect=complete) as child:
                run_step(root, job)
                wrapper = job['output']/'supervisor-audit.json'
                original = wrapper.read_bytes()
                self.assertEqual(read_json(wrapper)['status'], 'verified')
                run_step(root, job)
                self.assertEqual(child.call_count, 1)
                self.assertEqual(wrapper.read_bytes(), original)
                (job['output']/'scores.json').write_text('{"altered": true}')
                with self.assertRaisesRegex(ValueError, 'input/source/artifact changed'):
                    run_step(root, job)
                self.assertEqual(child.call_count, 1)

    def test_terminal_readiness_and_exact_analysis_paths(self):
        self.assertEqual(ready_decision(True, 'complete_through_gate7'), 'ready')
        self.assertEqual(ready_decision(True, 'informative_negative'), 'ready')
        self.assertEqual(ready_decision(False, 'informative_negative', skip_authorized=True), 'skip_unavailable_terminal_stage')
        self.assertEqual(ready_decision(False, 'informative_negative'), 'missing_required_terminal_output')
        self.assertEqual(ready_decision(False, 'complete_through_gate7'), 'missing_required_terminal_output')
        self.assertEqual(ready_decision(False, 'error'), 'upstream_error')
        self.assertEqual(ready_decision(False, 'running', True, 'error'), 'freezer_error')
        self.assertEqual(ready_decision(False, 'running'), 'wait')
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory)
            jobs = {job['name']: job for job in job_specs(root)}
            self.assertEqual(len(jobs), 10)
            self.assertEqual(jobs['pilot-retrospective']['output'], root/'independent-analysis/pilot-secondary')
            self.assertEqual(jobs['development-retrospective']['output'], root/'independent-analysis/development-secondary')
            self.assertEqual(jobs['full-prospective-compare']['primary'], root/'prospective/evaluation')
            self.assertEqual(jobs['excluded_pair-prospective-compare']['primary'], root/'prospective/evaluation-pair')
            self.assertEqual(jobs['excluded_model-prospective-compare']['primary'], root/'prospective/evaluation-model')
            self.assertEqual(jobs['full-controls-score']['output'], root/'secondary-baselines/full/controls-evaluation')
            self.assertEqual(jobs['full-controls-compare']['output'], root/'secondary-baselines/full/controls-comparison')

    def test_only_gate_justified_unrun_future_stages_may_skip(self):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory)
            jobs = {job['name']: job for job in job_specs(root)}
            prospective = jobs['full-prospective-score']; controls = jobs['full-controls-score']
            self.assertFalse(can_skip_unrun_job(root, prospective))
            gates = {'decisions': [dict(continuation_key='expansion-screen', gate=5,
                                        decision='informative negative', screen={'decisive_negative': True})]}
            (root/'gates.json').write_text(json.dumps(gates))
            self.assertTrue(can_skip_unrun_job(root, prospective))
            self.assertTrue(can_skip_unrun_job(root, controls))
            self.assertFalse(can_skip_unrun_job(root, jobs['pilot-retrospective']))
            self.assertFalse(can_skip_unrun_job(root, jobs['development-retrospective']))
            (root/'prospective'/'episodes').mkdir(parents=True)
            self.assertFalse(can_skip_unrun_job(root, prospective))
            gates['decisions'].append(dict(continuation_key='controls-screen', gate=6,
                decision='inconclusive / controls unsupported', screen={'passed': False}))
            (root/'gates.json').write_text(json.dumps(gates))
            self.assertTrue(can_skip_unrun_job(root, controls))
            (root/'steps').mkdir()
            (root/'steps'/'after-controls-evaluation.json').write_text('{}')
            self.assertFalse(can_skip_unrun_job(root, controls))
            (root/'steps'/'after-controls-evaluation.json').unlink()
            gates['decisions'][-1].update(decision='proceed', screen={'passed': True})
            (root/'gates.json').write_text(json.dumps(gates))
            self.assertFalse(can_skip_unrun_job(root, controls))

    @patch('prediction.prospective.plot_scores')
    def test_temporal_verification_rejects_forged_true_flag_and_late_forecasts(self, _plot):
        from prediction.test_prospective import fixture
        from prediction.prospective import score
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as directory:
            root = Path(directory)
            stage, _, _, _, forecasts, records = fixture(directory)
            output = root/'evaluation'
            score(forecasts, records, output, stage_root=stage, bootstrap=0)
            self.assertTrue(verified_evaluation(output)['prospective_verified'])
            audit_path = output/'audit.json'
            original = audit_path.read_bytes()
            audit = json.loads(original)
            audit['sources'][0]['precedes_rollouts'] = False
            audit_path.write_text(json.dumps(audit))
            with self.assertRaisesRegex(ValueError, 'Source audit flags'):
                verified_evaluation(output)
            audit = json.loads(original)
            sidecar = forecasts.with_suffix('.manifest.json')
            manifest = read_json(sidecar); manifest['created_utc'] = '2026-06-04T12:00:00+00:00'
            sidecar.write_text(json.dumps(manifest))
            # Even a modified true flag plus updated hash cannot override the
            # independently recomputed forecast-versus-actual-trace chronology.
            audit['source_sha256'][str(sidecar)] = file_hash(sidecar)
            audit_path.write_text(json.dumps(audit))
            with self.assertRaisesRegex(ValueError, 'does not precede actual'):
                verified_evaluation(output)


if __name__ == '__main__':
    unittest.main()
