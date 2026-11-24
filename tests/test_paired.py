import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'evals'))
from paired import analyze,ARMS

def row(arm,passed=False,**kw):
    return dict(model='synthetic',harness='test',config='fixed',task='T1',trial=1,arm=arm,passed=passed,critical_failure=False,evidence='test fixture',tokens=10,seconds=1)|kw
class PairedTests(unittest.TestCase):
    def test_empty(self): self.assertEqual(analyze([])['status'],'NOT_RUN')
    def test_missing(self): self.assertEqual(analyze([row('candidate')])['strata'][0]['incomplete_groups'],1)
    def test_complete(self):
        r=analyze([row(a,a=='candidate') for a in ARMS])['strata'][0];self.assertEqual(r['comparisons']['baseline']['delta_pp'],100)
    def test_duplicate(self):
        with self.assertRaises(ValueError): analyze([row('baseline'),row('baseline')])
    def test_gate(self):
        with self.assertRaises(ValueError): analyze([row('candidate',True,critical_failure=True)])
    def test_evidence(self):
        with self.assertRaises(ValueError): analyze([row('candidate',evidence='')])
