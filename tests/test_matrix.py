import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'evals'))
from matrix import make_plan,audit,digest
from paired import ARMS
from test_paired import row
class MatrixTests(unittest.TestCase):
    def plan(self):return make_plan([dict(model='synthetic',harness='test',config='fixed')],['T1','T2'],1,42)
    def test_reproducible(self):self.assertEqual(digest(self.plan()),digest(self.plan()))
    def test_whole_missing_task(self):
        r=audit(self.plan(),[row(a) for a in ARMS]);self.assertEqual(len(r['missing']),4);self.assertEqual(r['gate'],'BLOCKED')
    def test_complete(self):
        r=audit(self.plan(),[row(a,task=t) for a in ARMS for t in ('T1','T2')]);self.assertEqual(r['status'],'COMPLETE')
    def test_complete_critical(self):
        r=audit(self.plan(),[row(a,task=t,critical_failure=a=='candidate') for a in ARMS for t in ('T1','T2')]);self.assertEqual(r['gate'],'BLOCKED')
    def test_extra(self):self.assertEqual(len(audit(self.plan(),[row('baseline',task='T3')])['unexpected']),1)
    def test_duplicate_config(self):
        c=dict(model='m',harness='h',config='c');self.assertRaises(ValueError,make_plan,[c,c],['T1'],1,1)
    def test_invalid_plan(self):
        p=self.plan();p['runs'].pop();self.assertRaises(ValueError,audit,p,[])
