import pathlib
import sys
import unittest
import pandas as pd
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
from sensitivity_v2 import weighted_test

class MultiplicityTest(unittest.TestCase):
    def test_preserves_occurrences_and_conflicting_labels_not_ineligible_patterns(self):
        full=pd.DataFrame({'FLOW_START_MILLISECONDS':[0,10,11,12,13],'_row':[0,1,2,3,4],'x':[1.,1.,1.,2.,3.],'Label':[0,0,1,1,0]})
        unique=full.iloc[[1,3]].copy()
        unique['_hash']=pd.util.hash_pandas_object(unique[['x']],index=False).to_numpy()
        actual=weighted_test(full,unique,10,['x'])
        self.assertEqual(actual._row.tolist(),[1,2,3])
        self.assertEqual(actual.Label.tolist(),[0,1,1])

if __name__=='__main__': unittest.main()
