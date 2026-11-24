import importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('hc_experiment',ROOT/'bench/experiment.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
class TestBenchExperiment(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.dest=Path(self.temp.name)/'experiment'
        self.cfg=[dict(model='stub-not-ai',harness='test',config='unit')]
        self.plan=e.prepare(self.dest,self.cfg,1,13)
    def tearDown(self):self.temp.cleanup()
    def row(self,arm='candidate'):return next(x for x in self.plan['runs'] if x['arm']==arm)
    def meta(self,**kw):
        d=dict(self.cfg[0],status='completed',operator='unit test',tokens=None,seconds=None,skill_invoked=None)
        d.update(kw);return d
    def test_packet_count(self):
        self.assertEqual(len(self.plan['runs']),32)
    def test_identical_starter_four_arms(self):
        for task in {r['task'] for r in self.plan['runs']}:
            rows=[r for r in self.plan['runs'] if r['task']==task]
            self.assertEqual(len({r['input_hashes']['app.html'] for r in rows}),1)
            self.assertEqual(len({r['input_hashes']['TASK.txt'] for r in rows}),1)
    def test_no_verifier_in_packet(self):
        for r in self.plan['runs']:
            paths=r['input_hashes']
            self.assertFalse(any('verify.py' in x or 'reference.html' in x for x in paths))
    def test_previous_skill(self):
        r=self.row('previous')
        self.assertIn('version: "0.5.0"',(self.dest/'packets'/r['packet']/'skills/humancraft/SKILL.md').read_text())
    def test_missing_runs_block(self):
        s=e.summarize(self.dest)
        self.assertEqual(s['status'],'NOT_RUN');self.assertEqual(s['release_gate'],'BLOCKED');self.assertEqual(len(s['missing']),32)
    def test_plan_tamper(self):
        p=self.dest/'plan.json';a=e.read(p);a['seed']=99;e.write(p,a)
        with self.assertRaisesRegex(ValueError,'plan digest'):e.load_plan(self.dest)
    def test_prompt_tamper(self):
        r=self.row();(self.dest/'packets'/r['packet']/'TASK.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError,'task input changed'):e.record(self.dest,r['packet'],self.meta())
    def test_wrong_model(self):
        r=self.row()
        with self.assertRaisesRegex(ValueError,'model differs'):e.record(self.dest,r['packet'],self.meta(model='different'))
    def test_bad_usage(self):
        r=self.row()
        with self.assertRaisesRegex(ValueError,'invalid tokens'):e.record(self.dest,r['packet'],self.meta(tokens=-1))
    def test_record_immutable(self):
        r=self.row();e.record(self.dest,r['packet'],self.meta())
        with self.assertRaisesRegex(ValueError,'already frozen'):e.record(self.dest,r['packet'],self.meta())
    def test_agent_failure_is_not_critical_pass(self):
        r=self.row();e.record(self.dest,r['packet'],self.meta(status='agent_error'));e.grade(self.dest,r['packet'])
        g=e.read(self.dest/'grades'/r['packet']/'grade.json')
        self.assertEqual(g['result'],'AGENT_FAILURE');self.assertFalse(g['passed']);self.assertIsNone(g['critical_failure'])
        self.assertIn(r['packet'],e.summarize(self.dest)['candidate_unknown_critical'])
    def test_submission_tampering(self):
        r=self.row();e.record(self.dest,r['packet'],self.meta())
        (self.dest/'submissions'/r['packet']/'app.html').write_text('changed')
        with self.assertRaisesRegex(ValueError,'submission digest'):e.grade(self.dest,r['packet'])
    def test_bootstrap_deterministic(self):
        self.assertEqual(e.bootstrap([1,1,1]),[100,100]);self.assertIsNone(e.bootstrap([1]));self.assertEqual(e.bootstrap([0,1,-1]),e.bootstrap([0,1,-1]))
    def test_external_requires_clean_workspace(self):
        r=self.row();(self.dest/'packets'/r['packet']/'app.html').write_text('changed')
        with self.assertRaisesRegex(ValueError,'workspace differs'):e.run_external(self.dest,r['packet'],['python','{prompt}'],'unit',1)
    def test_no_fake_skill_invocation(self):
        r=self.row();e.record(self.dest,r['packet'],self.meta())
        self.assertIsNone(e.read(self.dest/'submissions'/r['packet']/'run.json')['skill_invoked'])
    def test_rehashed_truncated_plan_rejected(self):
        p=self.dest/'plan.json';a=e.read(p);a['runs'].pop();e.write(p,a)
        (self.dest/'plan.sha256').write_text(e.digest_bytes(e.canonical(a)))
        with self.assertRaisesRegex(ValueError,'incomplete or duplicate'):e.load_plan(self.dest)
    def test_invalid_packet_path_rejected(self):
        p=self.dest/'plan.json';a=e.read(p);a['runs'][0]['packet']='../../outside';e.write(p,a)
        (self.dest/'plan.sha256').write_text(e.digest_bytes(e.canonical(a)))
        with self.assertRaisesRegex(ValueError,'invalid or duplicate packets'):e.load_plan(self.dest)
    def test_error_does_not_mask_critical_failure(self):
        r=next(x for x in self.plan['runs'] if x['task']=='revoked-access')
        rows=[dict(viewport=v,scenario=s,task=r['task'],app_sha256='test',critical=s=='adverse',result='FAIL' if s=='adverse' else 'ERROR') for v in (1280,390) for s in ('normal','adverse')]
        g=e.grade_report(dict(verifier_sha256=self.plan['sources']['verifier'],results=rows),self.plan,r,'test')
        self.assertEqual(g['result'],'ERROR');self.assertIs(g['critical_failure'],True)
    def test_missing_critical_result_unknown(self):
        r=next(x for x in self.plan['runs'] if x['task']=='revoked-access')
        rows=[dict(viewport=v,scenario=s,task=r['task'],app_sha256='test',critical=s=='adverse',result='ERROR' if s=='adverse' else 'PASS') for v in (1280,390) for s in ('normal','adverse')]
        g=e.grade_report(dict(verifier_sha256=self.plan['sources']['verifier'],results=rows),self.plan,r,'test')
        self.assertEqual(g['result'],'ERROR');self.assertIsNone(g['critical_failure'])
if __name__=='__main__':unittest.main()
