"""Independent orchestration checks using synthetic data and no transports."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from prediction import pipeline
from prediction.io_utils import read_json, write_json


class PipelineAuditTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory(prefix='pipeline-test-', dir='/shared/allie/home/.codex/tmp')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    @staticmethod
    def observation(group, model, opponent, successes, opportunities=8):
        return dict(group_id=group, model=model, opponent=opponent,
                    targets={'action0': dict(successes=successes, opportunities=opportunities,
                                             applicable=True, value=successes/opportunities if opportunities else None)})

    @staticmethod
    def primary():
        return dict(models={name: {'model': name, 'temperature': .7} for name in ('a','b','c','d')},
                    protocol=dict(rounds=8, temperature=.7, max_tokens=16384, max_attempts=3),
                    sources={'prediction/runner.py': 'synthetic-frozen-hash'},
                    source_root='/shared/allie/synthetic-frozen-source',
                    ledger='/shared/allie/synthetic-global-budget.sqlite',
                    games=[dict(id='primary', group_id='primary-group')])

    def test_opposing_ordered_contexts_do_not_cancel(self):
        rows = [self.observation('g0', 'a','b',0), self.observation('g0','b','a',8),
                self.observation('g1', 'a','b',8), self.observation('g1','b','a',0)]
        cells = pipeline.context_game_variances(rows, ['action0'])['action0']
        self.assertEqual({(r['model'],r['opponent']) for r in cells}, {('a','b'),('b','a')})
        self.assertEqual([r['between_game_variance'] for r in cells], [.25,.25])

    def test_counts_pool_within_group_before_equal_group_variance(self):
        rows = [self.observation('g0','a','b',0,2), self.observation('g0','a','b',6,6),
                self.observation('g1','a','b',0,8)]
        cell = pipeline.context_game_variances(rows, ['action0'])['action0'][0]
        self.assertEqual(cell['games'],2)
        self.assertAlmostEqual(cell['between_game_variance'],.140625)
        self.assertEqual(pipeline.context_game_variances(rows*2,['action0'])['action0'][0],cell)

    def test_zero_opportunities_and_one_group_do_not_mean_zero_variance(self):
        rows = [self.observation('g0','a','b',0,0), self.observation('g1','a','b',4,8)]
        self.assertEqual(pipeline.context_game_variances(rows,['action0','absent']),
                         {'action0': [], 'absent': []})

    def test_development_inherits_revised_protocol_before_save_and_resumes(self):
        primary = self.primary()
        original = deepcopy(primary)
        value = pipeline.development_manifest(self.root, primary)
        self.assertEqual(primary, original)
        self.assertEqual(value['protocol']['max_tokens'],16384)
        self.assertEqual(value['protocol']['max_attempts'],3)
        for field in ('models','protocol','sources','source_root','ledger'):
            self.assertEqual(value[field],primary[field])
        self.assertEqual(len(value['games']),48)
        self.assertEqual(len(value['episodes']),960)
        self.assertEqual({(s['trial_id'],s['swap']) for s in value['episodes']}, {(0,False),(1,True)})
        raw = (self.root/'development/manifest.json').read_bytes()
        self.assertEqual(pipeline.development_manifest(self.root,primary),value)
        self.assertEqual((self.root/'development/manifest.json').read_bytes(),raw)

    def test_existing_development_rejects_every_primary_contract_mismatch(self):
        primary = self.primary()
        value = pipeline.development_manifest(self.root,primary)
        mutations = dict(models={'changed':{}}, protocol={'rounds':99}, sources={'changed':'hash'},
                         source_root='/shared/allie/wrong-source', ledger='/shared/allie/wrong-ledger.sqlite')
        path=self.root/'development/manifest.json'
        for field, changed in mutations.items():
            with self.subTest(field=field):
                bad = deepcopy(value)
                bad[field] = changed
                write_json(path,bad)
                with self.assertRaisesRegex(ValueError,field):
                    pipeline.development_manifest(self.root,primary)
                self.assertEqual(read_json(path),bad)

    def test_overlap_is_rejected_before_creating_manifest(self):
        primary = self.primary()
        generated = [dict(id=f'g{i}', group_id='primary-group' if i==0 else f'new-{i}') for i in range(48)]
        with patch('prediction.games.generate_games',return_value=generated):
            with self.assertRaises(AssertionError):
                pipeline.development_manifest(self.root,primary)
        self.assertFalse((self.root/'development/manifest.json').exists())

    def test_completed_command_binds_command_input_source_and_output(self):
        for change in ('command','input','source','output','missing_output'):
            with self.subTest(change=change):
                root=self.root/change
                root.mkdir()
                source=root/'synthetic.py'
                source.write_text('# synthetic source\n')
                input_path=root/'input.json'
                input_path.write_text('[]\n')
                output=root/'out'
                arguments=[str(source),'--input',str(input_path),'--out',str(output)]
                def simulated_command(*args,**kwargs):
                    output.mkdir()
                    (output/'records.json').write_text('[1]\n')
                    from types import SimpleNamespace
                    return SimpleNamespace(returncode=0)
                with patch.object(pipeline.subprocess,'run',side_effect=simulated_command) as transport:
                    pipeline.command(root,'fixture',arguments)
                    pipeline.command(root,'fixture',arguments)
                    self.assertEqual(transport.call_count,1)
                    altered=list(arguments)
                    if change=='command':
                        altered.extend(['--seed','2'])
                    elif change=='input':
                        input_path.write_text('[2]\n')
                    elif change=='source':
                        source.write_text('# changed source\n')
                    elif change=='output':
                        (output/'records.json').write_text('[3]\n')
                    else:
                        (output/'records.json').unlink()
                    with self.assertRaises(RuntimeError):
                        pipeline.command(root,'fixture',altered)
                    self.assertEqual(transport.call_count,1)

    def test_prospective_freeze_requires_no_started_stage_and_rejects_mutation(self):
        from prediction.after_matrix import freeze_before_launch
        forecast=self.root/'forecast.json'
        forecast.write_text('{"prediction":0.4}\n')
        folder=self.root/'prospective'
        folder.mkdir()
        (folder/'episodes').mkdir()
        with self.assertRaisesRegex(ValueError,'after player stage has begun'):
            freeze_before_launch(self.root,'prospective',[forecast])
        self.assertFalse((folder/'forecast-freeze.json').exists())
        (folder/'episodes').rmdir()
        freeze_before_launch(self.root,'prospective',[forecast])
        original=(folder/'forecast-freeze.json').read_bytes()
        (folder/'episodes').mkdir()
        freeze_before_launch(self.root,'prospective',[forecast])
        self.assertEqual((folder/'forecast-freeze.json').read_bytes(),original)
        forecast.write_text('{"prediction":0.7}\n')
        with self.assertRaisesRegex(ValueError,'artifacts changed'):
            freeze_before_launch(self.root,'prospective',[forecast])

    def test_inconclusive_improvements_do_not_become_negative_findings(self):
        from prediction.after_matrix import expansion_decision, METHODS
        rows=[dict(split=split, method=method, target='action0', baseline='pair',
                   improvement={'event_brier':.10},
                   intervals={'event_brier':{'lower':-.01,'upper':.21}})
              for split in ('family','random_group') for method in METHODS]
        signal=expansion_decision({'comparisons_to_pair':rows},('family','random_group'))
        self.assertFalse(signal['passed'])
        self.assertFalse(signal['decisive_negative'])
        self.assertTrue(signal['proceed'])
        self.assertEqual(signal['decision'],'uncertainty_replication')


if __name__ == '__main__':
    unittest.main()
