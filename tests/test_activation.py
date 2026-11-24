import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'evals'))
from activation_score import score
class ActivationTests(unittest.TestCase):
    cases=[{'id':'a','should_trigger':True},{'id':'b','should_trigger':False}]
    def test_empty(self): self.assertEqual(score(self.cases,{})['status'],'NOT_RUN')
    def test_full(self): self.assertEqual(score(self.cases,{'a':True,'b':False})['precision'],1)
    def test_partial(self): self.assertEqual(score(self.cases,{'a':False})['recall'],0)
    def test_invalid(self):
        with self.assertRaises(ValueError): score(self.cases,{'c':True})
