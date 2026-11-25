#!/usr/bin/env python3
"""Frozen public development tasks; export independent packets and grade submitted code.
No model calls. Operator supplies independent fresh sessions; this is not a security sandbox."""
import argparse, hashlib, json, math, random, re, shutil, statistics, subprocess, sys, time, zipfile
from pathlib import PurePosixPath
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ARMS=('baseline','generic','previous','candidate')
V06_ARCHIVE=ROOT/'controls/v06.zip'
V06_ARCHIVE_SHA256='a216e4fe57716b63c7e1f5ad65e70023fcc54064e29f4716048844e67a14c27d'
def digest_bytes(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest_bytes(p.read_bytes())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,data):p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def require(ok,msg):
    if not ok:raise ValueError(msg)
def file_hashes(path):return {str(p.relative_to(path)).replace('\\','/'):sha(p) for p in sorted(path.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
def source_manifest(frozen_v06=False):
    manifest={'verifier':sha(ROOT/'verify.py'),'protocol':sha(Path(__file__)),
              'tasks':file_hashes(ROOT/'tasks'),'controls':file_hashes(ROOT/'controls'),
              'candidate':file_hashes(ROOT.parent/'skills/humancraft')}
    if frozen_v06:
        require(sha(V06_ARCHIVE)==V06_ARCHIVE_SHA256,'frozen v0.6 archive digest mismatch')
        manifest['frozen_v06_archive']=V06_ARCHIVE_SHA256
    return manifest
def prepare(dest,configs,trials,seed,frozen_v06=False):
    require(type(trials) is int and trials>0,'positive trials required')
    require(type(frozen_v06) is bool,'frozen_v06 must be boolean')
    require(isinstance(configs,list) and configs,'configuration list required')
    for c in configs:
        require(set(c)=={'model','harness','config'} and all(isinstance(v,str) and v.strip() for v in c.values()),'config fields')
    require(len({tuple(sorted(c.items())) for c in configs})==len(configs),'duplicate configuration')
    require(not dest.exists(),'destination must be new')
    dest.mkdir(parents=True);(dest/'packets').mkdir()
    manifest=source_manifest(frozen_v06)
    tasks=[read(x) for x in sorted((ROOT/'tasks').glob('*/task.json'))]
    runs=[dict(c,task=t['id'],trial=i,arm=a) for c in configs for t in tasks for i in range(1,trials+1) for a in ARMS]
    rng=random.Random(seed);rng.shuffle(runs)
    specs={t['id']:t for t in tasks}
    for i,r in enumerate(runs):
        packet=f'run-{i+1:05d}-{rng.getrandbits(48):012x}'
        r['packet']=packet
        d=dest/'packets'/packet;d.mkdir()
        shutil.copyfile(ROOT/'tasks'/r['task']/'starter.html',d/'app.html')
        if r['arm']=='candidate':shutil.copytree(ROOT.parent/'skills/humancraft',d/'skills/humancraft',ignore=shutil.ignore_patterns('__pycache__'))
        elif r['arm']=='generic':shutil.copytree(ROOT/'controls/generic-ux',d/'skills/generic-ux')
        elif r['arm']=='previous':
            control_archive=V06_ARCHIVE if frozen_v06 else ROOT/'controls/v05.zip'
            with zipfile.ZipFile(control_archive) as z:
                for item in z.infolist():
                    rel=PurePosixPath(item.filename)
                    require(not rel.is_absolute() and '..' not in rel.parts and rel.parts[0]=='humancraft' and '\\' not in item.filename,'invalid previous skill archive')
                    if frozen_v06:
                        mode=(item.external_attr>>16)&0o170000
                        require(not item.is_dir() and mode in (0,0o100000),'invalid frozen v0.6 archive member')
                if frozen_v06:
                    names=[item.filename for item in z.infolist()]
                    require(len(names)==25 and len(set(names))==25 and 'humancraft/SKILL.md' in names,'invalid frozen v0.6 archive contents')
                z.extractall(d/'skills')
        (d/'TASK.txt').write_text(specs[r['task']]['prompt']+'\n\nModify app.html in this workspace. If relevant guidance exists in skills/, use it. Keep the task self-contained, with no external services or dependencies. Do not change the state interface. Return the completed file; do not invent test results.\n',encoding='utf-8')
        r['input_hashes']=file_hashes(d)
    plan={'version':'0.6.0','configs':configs,'scope':'public development tasks; not held-out','seed':seed,'trials':trials,'sources':manifest,'runs':runs}
    if frozen_v06:plan['frozen_control']='v0.6.0'
    write(dest/'plan.json',plan);(dest/'plan.sha256').write_text(digest_bytes(canonical(plan))+'\n')
    return plan
def load_plan(dest):
    plan=read(dest/'plan.json')
    require(digest_bytes(canonical(plan))==(dest/'plan.sha256').read_text().strip(),'plan digest mismatch')
    frozen_control=plan.get('frozen_control')
    require(frozen_control in (None,'v0.6.0'),'unsupported frozen control')
    require(plan['sources']==source_manifest(frozen_control=='v0.6.0'),'frozen source changed')
    require(plan.get('version')=='0.6.0','unsupported plan version')
    configs=plan['configs'];trials=plan['trials']
    require(type(trials) is int and trials>0 and isinstance(configs,list) and bool(configs),'invalid matrix specification')
    require(all(isinstance(c,dict) and set(c)=={'model','harness','config'} and all(isinstance(v,str) and v.strip() for v in c.values()) for c in configs),'invalid configuration')
    keys=lambda r: (r['model'],r['harness'],r['config'],r['task'],r['trial'],r['arm'])
    task_ids=[read(p)['id'] for p in sorted((ROOT/'tasks').glob('*/task.json'))]
    expected={(c['model'],c['harness'],c['config'],t,i,a) for c in configs for t in task_ids for i in range(1,trials+1) for a in ARMS}
    rows=plan['runs']
    require(len(expected)==len(configs)*len(task_ids)*trials*len(ARMS) and len(rows)==len(expected) and {keys(r) for r in rows}==expected,'incomplete or duplicate experiment matrix')
    require(len({r['packet'] for r in rows})==len(rows) and all(re.fullmatch(r'run-[0-9]{5,}-[0-9a-f]{12}',r['packet']) for r in rows),'invalid or duplicate packets')
    return plan
def record(dest,packet,meta):
    plan=load_plan(dest);matches=[r for r in plan['runs'] if r['packet']==packet];require(len(matches)==1,'unknown packet')
    r=matches[0];d=dest/'packets'/packet;out=dest/'submissions'/packet
    require(not out.exists(),'submission already frozen')
    require(meta.get('status') in ('completed','agent_error','timeout'),'invalid status')
    for key in ('model','harness','config'):require(meta.get(key)==r[key],f'{key} differs from frozen plan')
    for key in ('seconds','tokens'):
        v=meta.get(key);require(v is None or type(v) in (int,float) and math.isfinite(v) and v>=0,'invalid '+key)
    require(type(meta.get('skill_invoked')) is bool or meta.get('skill_invoked') is None,'invalid invocation')
    require(isinstance(meta.get('operator'),str) and meta['operator'].strip(),'operator attribution required')
    # Only app.html may change. Refuse edits to prompt/skill, extra files allowed but not graded.
    for rel,digest in r['input_hashes'].items():
        if rel!='app.html':require((d/rel).is_file() and sha(d/rel)==digest,'task input changed: '+rel)
    require((d/'app.html').is_file() and not (d/'app.html').is_symlink(),'missing/invalid app')
    out.mkdir(parents=True)
    shutil.copyfile(d/'app.html',out/'app.html')
    meta=dict(meta,packet=packet,app_sha256=sha(out/'app.html'),plan_sha256=digest_bytes(canonical(plan)),provenance='operator-attested; not cryptographically verified agent identity')
    write(out/'run.json',meta)
def run_external(dest,packet,command,operator,timeout):
    plan=load_plan(dest);matches=[r for r in plan['runs'] if r['packet']==packet];require(len(matches)==1,'unknown packet')
    r=matches[0];d=dest/'packets'/packet
    require(not (dest/'submissions'/packet).exists(),'already recorded')
    require(file_hashes(d)==r['input_hashes'],'workspace differs from frozen input')
    require(isinstance(command,list) and command and all(isinstance(x,str) and x for x in command),'command must be a JSON argument array')
    prompt=(d/'TASK.txt').read_text(encoding='utf-8')
    cmd=[x.replace('{prompt}',prompt).replace('{workdir}',str(d.resolve())) for x in command]
    require(any('{prompt}' in x for x in command),'command must explicitly receive the task prompt')
    # Local trusted operator chooses the CLI, account/profile, budget and permissions.
    # No shell expansion. This is a fresh workspace, NOT an OS/security sandbox.
    logdir=dest/'execution-logs';logdir.mkdir(exist_ok=True);start=time.monotonic();status='completed';code=None
    with (logdir/(packet+'.stdout')).open('wb') as stdout,(logdir/(packet+'.stderr')).open('wb') as stderr:
        try:
            p=subprocess.run(cmd,cwd=d,stdout=stdout,stderr=stderr,timeout=timeout)
            code=p.returncode
            if code:status='agent_error'
        except subprocess.TimeoutExpired:status='timeout'
        except OSError as e:stderr.write(str(e).encode());status='agent_error'
    meta={k:r[k] for k in ('model','harness','config')}
    meta.update(status=status,operator=operator,seconds=round(time.monotonic()-start,3),tokens=None,skill_invoked=None,
                command_sha256=digest_bytes(canonical(command)),exit_code=code,execution_kind='local subprocess; identity/config operator-attested',
                stdout_sha256=sha(logdir/(packet+'.stdout')),stderr_sha256=sha(logdir/(packet+'.stderr')))
    record(dest,packet,meta)

def grade(dest,packet,executable=None):
    plan=load_plan(dest);matches=[r for r in plan['runs'] if r['packet']==packet];require(len(matches)==1,'unknown packet')
    r=matches[0];d=dest/'submissions'/packet;meta=read(d/'run.json')
    require(meta['packet']==packet and meta['plan_sha256']==digest_bytes(canonical(plan)) and meta['app_sha256']==sha(d/'app.html'),'submission digest mismatch')
    out=dest/'grades'/packet;require(not out.exists(),'grade already exists')
    out.mkdir(parents=True)
    if meta['status']!='completed':
        write(out/'grade.json',dict(packet=packet,result='AGENT_FAILURE',passed=False,critical_failure=None,failed_checks=None,run_sha256=sha(d/'run.json'),app_sha256=meta['app_sha256'],evidence=None));return
    cmd=[sys.executable,str(ROOT/'verify.py'),'--task',r['task'],'--app',str(d/'app.html'),'--output',str(out)]
    if executable:cmd+=['--executable',executable]
    try:
        result=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
        (out/'verifier.log').write_text(result.stdout+'\n'+result.stderr)
    except subprocess.TimeoutExpired:
        write(out/'grade.json',dict(packet=packet,result='ERROR',passed=False,critical_failure=None,failed_checks=None,run_sha256=sha(d/'run.json'),app_sha256=meta['app_sha256'],evidence=None));return
    if not (out/'results.json').is_file():
        write(out/'grade.json',dict(packet=packet,result='ERROR',passed=False,critical_failure=None,failed_checks=None,run_sha256=sha(d/'run.json'),app_sha256=meta['app_sha256'],evidence=None));return
    report=read(out/'results.json')
    outcome=grade_report(report,plan,r,meta['app_sha256'])
    write(out/'grade.json',dict(packet=packet,**outcome,run_sha256=sha(d/'run.json'),app_sha256=meta['app_sha256'],evidence=sha(out/'results.json')))
def grade_report(report,plan,r,app_hash):
    rows=report['results']
    require(report['verifier_sha256']==plan['sources']['verifier'],'verifier changed')
    require(len(rows)==4 and {(x['viewport'],x['scenario']) for x in rows}=={(v,s) for v in (1280,390) for s in ('normal','adverse')},'incomplete grade')
    critical=read(ROOT/'tasks'/r['task']/'task.json')['critical']
    require(all(x['task']==r['task'] and x['app_sha256']==app_hash and x['result'] in ('PASS','FAIL','ERROR') and type(x['critical']) is bool and x['critical']==(critical and x['scenario']=='adverse') for x in rows),'grade mismatch')
    error=any(x['result']=='ERROR' for x in rows)
    failed=sum(x['result']=='FAIL' for x in rows)
    known_critical=any(x['critical'] and x['result']=='FAIL' for x in rows)
    unknown_critical=any(x['critical'] and x['result']=='ERROR' for x in rows)
    return dict(result='ERROR' if error else 'PASS' if not failed else 'FAIL',passed=not error and not failed,
                critical_failure=True if known_critical else None if unknown_critical else False,
                failed_checks=failed if not error else None)
def bootstrap(ds,seed=437,n=4000):
    if len(ds)<2:return None
    rng=random.Random(seed);vals=sorted(statistics.mean(rng.choices(ds,k=len(ds))) for _ in range(n))
    return [round(100*vals[int(.025*n)],2),round(100*vals[int(.975*n)-1],2)]
def summarize(dest):
    plan=load_plan(dest);groups={};missing=[];errors=[];critical=[];unknown_critical=[];recorded=0
    for r in plan['runs']:
        pid=r['packet'];out=dest/'grades'/pid;d=dest/'submissions'/pid
        if not (out/'grade.json').exists():missing.append(pid);continue
        g=read(out/'grade.json');m=read(d/'run.json')
        require(g['packet']==pid and g['app_sha256']==sha(d/'app.html') and g['run_sha256']==sha(d/'run.json'),'altered grade input')
        require(m['plan_sha256']==digest_bytes(canonical(plan)) and all(m[k]==r[k] for k in ('model','harness','config')),'run metadata mismatch')
        if g['evidence'] is not None:require(g['evidence']==sha(out/'results.json'),'altered verifier evidence')
        require(g['result'] in ('PASS','FAIL','ERROR','AGENT_FAILURE') and g['passed']==(g['result']=='PASS'),'invalid grade')
        if g['evidence'] is not None:
            require(m['status']=='completed','noncompleted run has browser evidence')
            expected=grade_report(read(out/'results.json'),plan,r,g['app_sha256'])
            require(all(type(g[k]) is type(v) and g[k]==v for k,v in expected.items()),'grade inconsistent with evidence')
        else:
            require(g['result'] in ('ERROR','AGENT_FAILURE') and g['critical_failure'] is None and g['failed_checks'] is None,'missing outcome evidence')
            require((g['result']=='AGENT_FAILURE')==(m['status']!='completed'),'failure status inconsistent with run')
        recorded+=1
        if g['result']=='ERROR':errors.append(pid)
        if r['arm']=='candidate' and g['critical_failure'] is True:critical.append(pid)
        if r['arm']=='candidate' and g['critical_failure'] is None:unknown_critical.append(pid)
        key=(r['model'],r['harness'],r['config'],r['task'],r['trial'])
        groups.setdefault(key,{})[r['arm']]=(g,m)
    strata={}
    for key,arms in groups.items():strata.setdefault(key[:3],[]).append((key[3:],arms))
    reports=[]
    for key,sets in sorted(strata.items()):
        complete=[(task,trial,arms) for (task,trial),arms in sets if set(arms)==set(ARMS) and all(x[0]['result']!='ERROR' for x in arms.values())]
        def values(a,fn):return [fn(arms[a]) for _,_,arms in complete]
        def task_macro(a,fn):
            by={}
            for task,trial,arms in complete:by.setdefault(task,[]).append(fn(arms[a]))
            return {t:statistics.mean(v) for t,v in by.items()}
        metrics={}
        for a in ARMS:
            rates=task_macro(a,lambda x:int(x[0]['passed']))
            toks=[x for x in values(a,lambda x:x[1].get('tokens')) if x is not None]
            times=[x for x in values(a,lambda x:x[1].get('seconds')) if x is not None]
            inv=values(a,lambda x:x[1].get('skill_invoked'))
            checks=values(a,lambda x:x[0].get('failed_checks'))
            metrics[a]={'failed_check_total':sum(x for x in checks if x is not None),'failed_check_coverage':sum(x is not None for x in checks),'task_macro_pass_rate':statistics.mean(rates.values()) if rates else None,'token_median':statistics.median(toks) if toks else None,'token_coverage':len(toks),'seconds_median':statistics.median(times) if times else None,'seconds_coverage':len(times),'invocations_observed':sum(x is True for x in inv),'invocation_known':sum(x is not None for x in inv),'observed_critical_failures':sum(arms[a][0]['critical_failure'] is True for _,arms in sets if a in arms),'agent_failures':sum(arms[a][0]['result']=='AGENT_FAILURE' for _,arms in sets if a in arms)}
        comparisons={}
        for a in ARMS[:-1]:
            ca=task_macro('candidate',lambda x:int(x[0]['passed']));ba=task_macro(a,lambda x:int(x[0]['passed']))
            ds=[ca[t]-ba[t] for t in sorted(ca)]
            comparisons[a]={'tasks':len(ds),'paired_delta_pp':round(100*statistics.mean(ds),2) if ds else None,'task_cluster_bootstrap_95_pp':bootstrap(ds),'scope':'descriptive uncertainty across public tasks; not generalization'}
        reports.append({'model':key[0],'harness':key[1],'config':key[2],'complete_pairs':len(complete),'arms':metrics,'comparisons':comparisons})
    status='NOT_RUN' if not recorded else 'INCOMPLETE' if missing or errors else 'OBSERVED_OPERATOR_ATTESTED'
    thresholds=[{'model':x['model'],'harness':x['harness'],'config':x['config'],
                 'baseline_delta_target_met':x['comparisons']['baseline']['paired_delta_pp'] is not None and x['comparisons']['baseline']['paired_delta_pp']>=10,
                 'generic_delta_target_met':x['comparisons']['generic']['paired_delta_pp'] is not None and x['comparisons']['generic']['paired_delta_pp']>=5,
                 'baseline_interval_excludes_zero':(x['comparisons']['baseline']['task_cluster_bootstrap_95_pp'] or [0])[0]>0,
                 'generic_interval_excludes_zero':(x['comparisons']['generic']['task_cluster_bootstrap_95_pp'] or [0])[0]>0} for x in reports]
    return dict(status=status,descriptive_thresholds=thresholds,planned=len(plan['runs']),graded=recorded,missing=missing,infrastructure_errors=errors,candidate_critical_failures=critical,candidate_unknown_critical=unknown_critical,release_gate='BLOCKED' if missing or errors or critical or unknown_critical else 'COVERAGE_ONLY_NOT_CERTIFIED',strata=reports,scope='public development synthetic tasks; no holdout, no human usability evidence, operator-attested provenance')
def main():
    a=argparse.ArgumentParser(description=__doc__);s=a.add_subparsers(dest='cmd',required=True)
    p=s.add_parser('prepare');p.add_argument('destination',type=Path);p.add_argument('configs',type=Path);p.add_argument('--trials',type=int,default=3);p.add_argument('--seed',type=int,default=20261124);p.add_argument('--frozen-v06-control',action='store_true',help='use the frozen v0.6 skill as the previous arm instead of the historical v0.5 control')
    p=s.add_parser('record');p.add_argument('destination',type=Path);p.add_argument('packet');p.add_argument('metadata',type=Path)
    p=s.add_parser('run');p.add_argument('destination',type=Path);p.add_argument('packet');p.add_argument('command',type=Path);p.add_argument('--operator',required=True);p.add_argument('--timeout',type=int,default=600)
    p=s.add_parser('grade');p.add_argument('destination',type=Path);p.add_argument('packet');p.add_argument('--executable')
    p=s.add_parser('summary');p.add_argument('destination',type=Path)
    x=a.parse_args()
    try:
        if x.cmd=='prepare':
            p=prepare(x.destination,read(x.configs),x.trials,x.seed,x.frozen_v06_control);print(f'{len(p["runs"])} packets prepared, no model runs')
        elif x.cmd=='record':record(x.destination,x.packet,read(x.metadata));print('submission frozen')
        elif x.cmd=='run':run_external(x.destination,x.packet,read(x.command),x.operator,x.timeout);print('local execution recorded; inspect logs')
        elif x.cmd=='grade':grade(x.destination,x.packet,x.executable);print('grade recorded; inspect grade.json')
        else:print(json.dumps(summarize(x.destination),indent=2))
    except (OSError,ValueError,TypeError,KeyError) as e:print(str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
