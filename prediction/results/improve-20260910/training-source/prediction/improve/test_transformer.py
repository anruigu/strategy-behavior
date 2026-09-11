"""Synthetic checks only: no checkpoint downloads, real embeddings, or actual study fits."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from . import transformer as t


def row(name, group, k, n, family='family_a'):
    return dict(row_id=name, game_id=group, group_id=group, family=family, model='focal', opponent='opponent',
        input_text='Payoffs and fixed protocol only.', applicability=dict(cooperation=False, coordination=False),
        targets={'action0': dict(successes=k, opportunities=n, applicable=True),
                 'cooperation': dict(successes=None, opportunities=0, applicable=False),
                 'coordination': dict(successes=None, opportunities=None, applicable=False)})


class PureTransformerTests(unittest.TestCase):
    def test_global_event_weights_and_unsupported_targets(self):
        rows = [row('a','g1',100,100), row('b','g2',0,1), row('c','g2',0,99)]
        weights = t.supervision(rows)
        np.testing.assert_allclose(weights['normalized_weights'][:,0], [.5,.005,.495])
        np.testing.assert_array_equal(weights['supported'], [True,False,False])
        np.testing.assert_array_equal(weights['groups_per_target'], [2,0,0])
        # Correct constant forecast for context {a,b}; unlike equal-context/game means (.5).
        selected = [0,1]
        p = (weights['normalized_weights'][selected,0]*weights['y'][selected,0]).sum()/weights['normalized_weights'][selected,0].sum()
        self.assertAlmostEqual(float(p),100/101,places=6)
        malformed=copy.deepcopy(rows); malformed[0]['targets']['coordination']['successes']=1
        with self.assertRaisesRegex(ValueError,'without opportunities'):
            t.supervision(malformed)

    def test_duplicate_events_in_a_game_preserve_objective(self):
        examples = [row('a','g1',2,3),row('b','g1',1,4),row('c','g2',8,9)]
        doubled=copy.deepcopy(examples)
        for x in doubled:
            if x['group_id']=='g1':
                for field in ['successes','opportunities']:
                    x['targets']['action0'][field]*=7
        a,b=t.supervision(examples),t.supervision(doubled)
        np.testing.assert_allclose(a['y'],b['y'])
        np.testing.assert_allclose(a['normalized_weights'],b['normalized_weights'])

    def test_train_only_scaling_and_metadata_only_cache(self):
        train=np.array([[1.,3.],[3.,3.]],dtype=np.float32)
        mean,scale=t.standardize_fit(train)
        np.testing.assert_array_equal(mean,[2,3]);np.testing.assert_array_equal(scale,[1,1])
        held_out=np.array([[1000.,3000.]],dtype=np.float32)
        np.testing.assert_array_equal((held_out-mean)/scale,[[998.,2997.]])
        a=row('a','g1',1,2);b=copy.deepcopy(a)
        b['targets']['action0']['successes']=2;b['family']='hidden_family';b['row_id']='hidden_id'
        self.assertEqual(t.context_identity(a),t.context_identity(b))
        self.assertEqual(set(t.context_identity(a)),{'input_text'})

    def test_fold_integrity_and_family_leak(self):
        train=[row('a','g1',1,2,'A'),row('b','g2',1,2,'B')]
        fold=dict(train=[0],test=[1],train_row_ids=['a'],test_row_ids=['b'],split='family')
        t.validate_fold(fold,train,train)
        leaked=copy.deepcopy(train);leaked[1]['family']='A'
        with self.assertRaisesRegex(ValueError,'Family holdout'):
            t.validate_fold(fold,leaked,leaked)
        leaked=copy.deepcopy(train);leaked[1]['group_id']='g1'
        with self.assertRaisesRegex(ValueError,'Canonical payoff group'):
            t.validate_fold(fold,leaked,leaked)
        mismatch=copy.deepcopy(fold);mismatch['test_row_ids']=['wrong']
        with self.assertRaisesRegex(ValueError,'identifiers'):
            t.validate_fold(mismatch,train,train)

    def test_fixed_protocol_and_fleet_guard(self):
        protocol=t.protocol_spec('a'*40);t.validate_protocol(protocol)
        modified=copy.deepcopy(protocol);modified['lora']['epochs']=3
        with self.assertRaisesRegex(ValueError,'differs'):
            t.validate_protocol(modified)
        with self.assertRaisesRegex(ValueError,'exact'):
            t.protocol_spec('main')
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaisesRegex(RuntimeError,'Fleet'):
                t.fleet_guard('not-a-submission')

    def test_forecast_without_labels_masks_structure_and_refuses_rewrites(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR','/shared/allie/home/.codex/tmp')) as name:
            folder=Path(name)/'export'; example=row('a','g1',1,2)
            del example['targets']
            example['applicability']['cooperation']=True
            t.export_forecasts(folder,[example],np.array([[.2,.3,.4]]),[True,False,True],
                t.METHODS['frozen'],'fresh','full',{'test':'synthetic'},{})
            records=[json.loads(line) for line in (folder/'forecasts.jsonl').read_text().splitlines()]
            self.assertEqual([r['prediction'] for r in records],[.2,None,None])
            self.assertEqual([r['status'] for r in records],['ok','no_training_support','structurally_undefined'])
            before=(folder/'forecasts.jsonl').read_bytes()
            with self.assertRaises(FileExistsError):
                t.export_forecasts(folder,[example],np.array([[.9,.9,.9]]),[True]*3,
                    t.METHODS['frozen'],'fresh','full',{}, {})
            self.assertEqual(before,(folder/'forecasts.jsonl').read_bytes())

    def test_completed_fit_resume_binds_contract_and_outputs(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR','/shared/allie/home/.codex/tmp')) as name:
            folder=Path(name)/'fit';contract={'input_sha256':{},'fixed':'synthetic'}
            self.assertTrue(t.prepare_fit_folder(folder,contract,False))
            output=folder/'synthetic-output.json';t.write_json(output,{'value':1})
            t.write_json(folder/'complete.json',{'status':'complete','input_sha256':{},
                'output_sha256':{str(output):t.sha(output)}})
            self.assertFalse(t.prepare_fit_folder(folder,contract,True))
            with self.assertRaisesRegex(ValueError,'contract'):
                t.prepare_fit_folder(folder,dict(contract,fixed='changed'),True)
            output.write_text('{"value":2}')
            with self.assertRaisesRegex(ValueError,'changed'):
                t.prepare_fit_folder(folder,contract,True)


@unittest.skipUnless(importlib.util.find_spec('torch'),'Torch tensor checks run in Fleet runtime; local Torch is absent')
class TensorTransformerTests(unittest.TestCase):
    def test_last_pooling_handles_padding_and_empty(self):
        import torch
        hidden=torch.arange(2*4*3).reshape(2,4,3).float()
        mask=torch.tensor([[1,1,0,0],[0,1,1,1]])
        torch.testing.assert_close(t.pool_last_hidden(hidden,mask),torch.stack([hidden[0,1],hidden[1,3]]))
        with self.assertRaisesRegex(ValueError,'empty'):
            t.pool_last_hidden(hidden,torch.zeros_like(mask))

    def test_fractional_binomial_loss_and_masked_gradient(self):
        import torch
        logits=torch.tensor([[.3,-2.,8.]],requires_grad=True)
        y=torch.tensor([[.25,.7,0.]])
        weights=torch.tensor([[.6,.4,0.]])
        loss=t.fractional_loss(logits,y,weights)
        p=torch.sigmoid(logits)
        manual=-.6*(torch.log(p[0,0])+3*torch.log1p(-p[0,0]))/4-.4*(7*torch.log(p[0,1])+3*torch.log1p(-p[0,1]))/10
        torch.testing.assert_close(loss,manual)
        loss.backward();self.assertEqual(float(logits.grad[0,2]),0.)
        torch.testing.assert_close(logits.grad,weights*(p-y))

    def test_microbatch_accumulation_preserves_global_game_loss(self):
        import torch
        logits=torch.tensor([[.2,-.3,.4],[-.1,.7,-.4],[.8,.5,.2]],requires_grad=True)
        y=torch.tensor([[1.,0.,.2],[0.,1.,.5],[.7,.2,1.]])
        weights=torch.tensor([[.2,.1,0.],[.1,.1,.2],[.2,0.,.1]])
        full=t.fractional_loss(logits,y,weights);full.backward();want=logits.grad.clone()
        logits.grad.zero_()
        for ids in ([0,1],[2]):
            # Each microbatch contributes to the same macro loss without batchwise renormalization.
            t.fractional_loss(logits[ids],y[ids],weights[ids]).backward()
        torch.testing.assert_close(logits.grad,want)


if __name__=='__main__':
    unittest.main()
