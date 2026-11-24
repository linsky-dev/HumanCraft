import unittest,copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/humancraft/scripts'))
from check_trace import check

def events(kinds):
    return {'events':[dict(seq=i+1,op='a',scope='r',kind=k,**({'allowed':True} if k=='authorize' else {'write_id':'w'} if k=='commit' else {})) for i,k in enumerate(kinds)]}
class TraceTests(unittest.TestCase):
    def codes(self,x): return {v['code'] for v in check(x)['violations']}
    def test_good(self): self.assertEqual(check(events(['start','authorize','commit','success']))['status'],'PASS')
    def test_cancel(self): self.assertEqual(check(events(['start','authorize','cancel']))['status'],'PASS')
    def test_late(self): self.assertIn('after-terminal',self.codes(events(['start','authorize','cancel','commit'])))
    def test_unauthorized(self): self.assertIn('unauthorized-commit',self.codes(events(['start','commit','success'])))
    def test_denied(self):
        x=events(['start','authorize','commit','success']);x['events'][1]['allowed']=False;self.assertIn('unauthorized-commit',self.codes(x))
    def test_duplicate(self): self.assertIn('duplicate-effect',self.codes(events(['start','authorize','commit','commit','success'])))
    def test_false_success(self): self.assertIn('success-without-commit',self.codes(events(['start','success'])))
    def test_wrong_target(self):
        x=events(['start','authorize','commit','success']);x['events'][2]['scope']='other';self.assertIn('scope-changed',self.codes(x))
    def test_incomplete(self): self.assertIn('incomplete-operation',self.codes(events(['start','authorize'])))
    def test_failure_after_commit(self): self.assertIn('committed-effect-needs-reconciliation',self.codes(events(['start','authorize','commit','fail'])))
    def test_invalid(self):
        with self.assertRaises(ValueError): check({'events':[]})
    def test_order(self):
        x=events(['start','cancel']);x['events'][1]['seq']=1
        with self.assertRaises(ValueError): check(x)
    def test_retry_duplicate(self):
        x=events(['start','authorize','commit','success']);y=copy.deepcopy(x['events']);
        for e in y: e['op']='b';e['seq']+=4
        x['events']+=y;self.assertIn('duplicate-effect',self.codes(x))
