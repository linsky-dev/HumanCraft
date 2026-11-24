import unittest, importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'skills/humancraft/scripts/audit_score.py'
s=importlib.util.spec_from_file_location('score',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def sample():
    return {'dimensions':{k:{'score':4,'evidence_type':'observed_test','evidence':['T1']} for k in m.WEIGHTS},'gates':{k:{'status':'pass','evidence_type':'observed_test','evidence':['T1']} for k in m.GATES}}
class ScoreTest(unittest.TestCase):
    def test_full(self): self.assertEqual(m.score(sample())['observed_score'],100)
    def test_unknown(self):
        d=sample(); d['dimensions']['resilience']={'score':None}; d['gates']['recovery']={'status':'unknown'}; r=m.score(d); self.assertEqual(r['observed_weight_coverage_pct'],80); self.assertEqual(r['gate_status'],'blocked')
    def test_fail(self):
        d=sample(); d['gates']['integrity']['status']='fail'; self.assertEqual(m.score(d)['gate_status'],'blocked')
    def test_reported(self):
        d=sample(); d['dimensions']['outcome']['evidence_type']='reported'; self.assertEqual(m.score(d)['observed_weight_coverage_pct'],85)
    def test_unverified_gate(self):
        d=sample(); d['gates']['integrity']['evidence_type']='reported'; self.assertRaises(ValueError,m.score,d)
    def test_na(self):
        d=sample(); d['dimensions']['control']={'score':None,'evidence_type':'na','reason':'static display'}; self.assertEqual(m.score(d)['observed_weight_coverage_pct'],100)
    def test_bad_score(self):
        d=sample(); d['dimensions']['outcome']['score']=True; self.assertRaises(ValueError,m.score,d)
    def test_no_evidence(self):
        d=sample(); d['dimensions']['outcome']['evidence']=[]; self.assertRaises(ValueError,m.score,d)
