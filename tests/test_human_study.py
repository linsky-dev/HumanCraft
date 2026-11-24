import importlib.util,unittest
from pathlib import Path
sp=importlib.util.spec_from_file_location('human_study',Path(__file__).resolve().parents[1]/'bench/human_study.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
class StudyTests(unittest.TestCase):
    def setUp(self):
        self.plan=[dict(participant='test-id',task='t',experience='novice',order=['A','B'])]
    def row(self,v,**k):
        r=dict(participant='test-id',task='t',variant=v,position=1 if v=='A' else 2,consent=True,outcome='unassisted',critical_errors=0,errors=0,seconds=3,ease=5);r.update(k);return r
    def test_empty(self):self.assertEqual(h.analyze(self.plan,[])['status'],'NOT_RUN')
    def test_missing(self):self.assertEqual(h.analyze(self.plan,[self.row('A')])['status'],'INCOMPLETE')
    def test_pair(self):
        x=h.analyze(self.plan,[self.row('A',outcome='failed',errors=1,critical_errors=1),self.row('B')])
        self.assertEqual(x['delta_unassisted_pp'],100)
        self.assertEqual(x['variant_A']['successful_time_n'],0)
    def test_consent(self):
        with self.assertRaises(ValueError):h.analyze(self.plan,[self.row('A',consent=False)])
    def test_order(self):
        with self.assertRaises(ValueError):h.analyze(self.plan,[self.row('A',position=2)])
    def test_duplicate(self):
        with self.assertRaises(ValueError):h.analyze(self.plan,[self.row('A'),self.row('A')])
    def test_withdrawal(self):
        x=h.analyze(self.plan,[self.row('A',outcome='withdrawn',seconds=None,ease=None),self.row('B')]);self.assertEqual(x['complete_nonwithdrawn_pairs'],0)
