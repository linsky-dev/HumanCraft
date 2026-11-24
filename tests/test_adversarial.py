import unittest,sys,copy,subprocess, json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root/'evals'),str(root/'skills/humancraft/scripts'),str(root/'tests')]
from audit_score import score
from check_trace import check
from paired import analyze
from activation_score import score as activation
from test_score import sample
from test_paired import row
from test_trace import events
class AdversarialTests(unittest.TestCase):
    def test_all_na_blocks(self):
        x=sample();x['dimensions']={k:{'score':None,'evidence_type':'na','reason':'not relevant'} for k in x['dimensions']};x['gates']={k:{'status':'na','reason':'not relevant'} for k in x['gates']};self.assertEqual(score(x)['gate_status'],'blocked')
    def test_no_evidence_blocks(self):
        x=sample();x['dimensions']={k:{'score':None} for k in x['dimensions']};self.assertEqual(score(x)['gate_status'],'blocked')
    def test_fake_evidence_whitespace(self):
        x=sample();x['gates']['integrity']['evidence']=['  '];self.assertRaises(ValueError,score,x)
    def test_fake_evidence_number(self):
        x=sample();x['dimensions']['outcome']['evidence']=123;self.assertRaises(ValueError,score,x)
    def test_unpaired_critical_visible(self):
        x=analyze([row('candidate',critical_failure=True)]);self.assertEqual(x['status'],'PARTIAL');self.assertEqual(x['candidate_critical_failures'],1);self.assertEqual(x['strata'][0]['arms']['candidate']['critical_failures'],1)
    def test_invalid_trial(self): self.assertRaises(ValueError,analyze,[row('baseline',trial=True)])
    def test_empty_identity(self): self.assertRaises(ValueError,analyze,[row('baseline',model=' ')])
    def test_optimized_python(self):
        code='from paired import analyze; analyze('+repr([row('candidate',True,critical_failure=True)])+')';p=subprocess.run([sys.executable,'-O','-c',code],cwd=root/'evals',capture_output=True);self.assertNotEqual(p.returncode,0)
    def test_validator_optimized(self):
        p=subprocess.run([sys.executable,'-O',str(root/'scripts/validate.py')],capture_output=True);self.assertNotEqual(p.returncode,0)
    def test_malformed_activation_truth(self): self.assertRaises(ValueError,activation,[{'id':'a','should_trigger':'false'}],{'a':True})
    def test_empty_activation(self): self.assertRaises(ValueError,activation,[],{})
    def test_space_id(self):
        x=events(['start','authorize','commit','success']);x['events'][2]['write_id']=' w ';self.assertRaises(ValueError,check,x)
    def test_space_scope(self):
        x=events(['start','cancel']);x['events'][1]['scope']='r ';self.assertRaises(ValueError,check,x)
