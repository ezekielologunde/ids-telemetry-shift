import pathlib
import sys
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
from evaluate import counts, review_mask, partitions, families, corrupt

class EvaluationTests(unittest.TestCase):
    def test_hard_cap_and_ties(self):
        m=review_mask(np.ones(20),np.repeat([1,2],10),.1)
        self.assertEqual(np.flatnonzero(m).tolist(),[0,10])
    def test_error_accounting(self):
        c=counts(np.array([1,1,0,0]),np.array([0,1,1,0]),np.array([True,False,False,False]))
        self.assertEqual((c['errors'],c['reviewed_errors'],c['unreviewed_fn'],c['unreviewed_fp']),(2,1,0,1))
        self.assertAlmostEqual(c['accepted_risk'],1/3)
    def test_time_boundaries_and_overlap(self):
        d=pd.DataFrame({'FLOW_START_MILLISECONDS':np.arange(10)*10,'FLOW_END_MILLISECONDS':np.arange(10)*10+1,'_row':np.arange(10),'Label':[0,1]*5,'x':[1,2,3,4,5,6,1,8,2,10]})
        p,r=partitions(d,['x'])
        self.assertEqual(p['cal'].x.tolist(),[8])
        self.assertEqual(p['test'].x.tolist(),[10])
        self.assertTrue(p['train'].FLOW_END_MILLISECONDS.max()<r['boundaries_ms'][0])
    def test_masks_do_not_mutate_inputs(self):
        x=np.ones((5,3));g=families(['TCP_FLAGS','IN_BYTES','SRC_TO_DST_IAT_AVG'])
        a=corrupt(x,'temporal+tcp',g,17)
        self.assertTrue(np.isnan(a[:,[0,2]]).all())
        self.assertTrue((x==1).all())
        np.testing.assert_equal(corrupt(x,'random10',g,17),corrupt(x,'random10',g,17))

if __name__=='__main__': unittest.main()
