import json
from pathlib import Path
import tempfile
import unittest

from prediction.improve.data import write_new
from prediction.improve.test_evaluate import fixture
from prediction.improve.evaluate import score_files
from prediction.improve.report import render


class ReportTests(unittest.TestCase):
    def test_pending_report_never_invents_results_or_a_decision(self):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as tmp:
            root=Path(tmp);out=root/'REPORT.md'
            result=render(root,out)
            text=out.read_text()
            self.assertIn('Decision pending',text)
            self.assertIn('No comparative results are available yet',text)
            self.assertIn('Not yet available / unrun',text)
            self.assertEqual(result['figures'],0)

    def test_synthetic_figures_formats_decision_precedence_and_hash_guard(self):
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as tmp:
            root=Path(tmp);out=root/'REPORT.md';data,folds,rows=fixture()
            write_new(root/'data.json',data);write_new(root/'folds.json',folds)
            with (root/'forecasts.jsonl').open('x') as handle:
                for row in rows:handle.write(json.dumps(row)+'\n')
            score_files(root/'data.json',root/'folds.json',[root/'forecasts.jsonl'],root/'development-evaluation',20)
            write_new(root/'development-gate.json',dict(decision='Proceed',reason='Synthetic development screen'))
            write_new(root/'final-disposition.json',dict(status='Inconclusive',summary='SYNTHETIC fixture; no improvement claim.'))
            result=render(root,out)
            self.assertEqual(result['figures'],4)
            self.assertIn('Decision: Inconclusive',out.read_text())
            self.assertNotIn('Decision: Proceed',out.read_text())
            self.assertIn('Calibrated theory',out.read_text())
            self.assertIn('seven declared clusters',out.read_text().lower())
            for name in ('scores-event_brier','scores-log_loss','calibration','paired-gains'):
                for ext in ('png','svg','pdf'):
                    path=root/'report-figures'/(name+'.'+ext)
                    self.assertGreater(path.stat().st_size,1000)
            manifest=json.loads((root/'report-figures/report-artifacts.json').read_text())
            self.assertEqual(len(manifest['figure_sha256']),12)
            self.assertFalse(manifest['fitting_performed'])
            with (root/'development-evaluation/scores.json').open('a') as handle:handle.write(' ')
            with self.assertRaisesRegex(ValueError,'hash mismatch'):render(root,out)


if __name__=='__main__':unittest.main()
