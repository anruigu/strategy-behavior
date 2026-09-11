import copy
import math
import os
import unittest
from unittest.mock import patch

from prediction.games import make_game
from prediction.improve.data import aggregate_records
from prediction.improve.baselines import (equilibrium,fit_methods,predict,prepared,
    encoder_fit,encode,logistic_fit,probability,fleet_guard,fit_logistic)
from prediction.improve.test_data import PROTOCOL,synthetic_records


class BaselineTests(unittest.TestCase):
    def test_joint_equilibrium_ties_and_masks(self):
        tied=make_game('tie',1,-.2,.4,1)
        self.assertEqual(equilibrium(tied,'action0'),.5)
        self.assertEqual(equilibrium(tied,'coordination'),1)
        self.assertLess(equilibrium(tied,'coordination',False),1)
        self.assertIsNone(equilibrium(tied,'cooperation'))
        pd=make_game('pd',1,-.2,1.4,0)
        self.assertEqual(equilibrium(pd,'cooperation'),0)
        self.assertEqual(equilibrium(pd,'action0'),0)

    def test_synthetic_methods_are_finite_and_keep_structural_masks(self):
        rows=aggregate_records(synthetic_records(21),PROTOCOL)
        for target in ('action0','cooperation','coordination'):
            fits=fit_methods(rows,target)
            for row in rows:
                for fit in fits.values():
                    value=predict(fit,row,target)
                    supported=target=='action0' or row['applicability'][target]
                    if supported:self.assertTrue(value is not None and math.isfinite(value) and 0<=value<=1)
                    else:self.assertIsNone(value)

    def test_normalized_features_invariant_and_train_only_scaling(self):
        rows=aggregate_records(synthetic_records(14),PROTOCOL)
        eligible,y,w=prepared(rows,'action0')
        encoder=encoder_fit(eligible,w,'normalized')
        affine=copy.deepcopy(eligible)
        for row in affine:row['payoffs']={k:3*v+10 for k,v in row['payoffs'].items()}
        import numpy as np
        self.assertTrue(np.allclose(encode(encoder,eligible),encode(encoder,affine),atol=1e-9))
        query=copy.deepcopy(rows[0]);query['model']='unseen';query['opponent']='unseen'
        before=copy.deepcopy(encoder);encode(encoder,[query])
        self.assertEqual(before,encoder)

    def test_calibration_smooths_exceptions_monotonically(self):
        import numpy as np
        q=np.asarray([.01,.01,.99,.99]);x=np.column_stack([np.ones(4),np.log(q/(1-q))])
        y=np.asarray([.1,.2,.8,.9]);w=np.ones(4)
        fit=logistic_fit(x,y,w,.01,calibration=True)
        from scipy.special import expit
        p=expit(x@np.asarray(fit['coefficients']))
        self.assertGreater(p[0],.01);self.assertLess(p[-1],.99)
        self.assertLess(p[0],p[-1]);self.assertGreaterEqual(fit['coefficients'][1],0)

    def test_empirical_worker_guard_requires_fleet_submission_authority(self):
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaises(RuntimeError):fleet_guard('synthetic-unsubmitted')


if __name__ == '__main__':unittest.main()
