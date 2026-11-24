#!/usr/bin/env python3
"""Freeze a randomized experiment matrix and audit its completeness; no model calls."""
import argparse,hashlib,json,random,sys
from pathlib import Path
from paired import ARMS, analyze
KEY=('model','harness','config','task','trial','arm')
def make_plan(configs,tasks,trials,seed):
    if not configs or not tasks or type(trials) is not int or trials<1 or type(seed) is not int: raise ValueError('nonempty configurations/tasks, positive trials, integer seed required')
    if any(not isinstance(t,str) or not t.strip() for t in tasks) or len(set(tasks))!=len(tasks): raise ValueError('invalid tasks')
    rows=[]
    for c in configs:
        if set(c)!={'model','harness','config'} or not all(isinstance(v,str) and v.strip() for v in c.values()):raise ValueError('invalid config')
        for task in tasks:
            for trial in range(1,trials+1):
                for arm in ARMS:rows.append(dict(c,task=task,trial=trial,arm=arm))
    if len({tuple(r[k] for k in KEY) for r in rows})!=len(rows):raise ValueError('duplicate planned run')
    random.Random(seed).shuffle(rows)
    return {'seed':seed,'runs':rows}
def digest(plan):return hashlib.sha256(json.dumps(plan,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def audit(plan,rows):
    expected=plan.get('runs')
    if not isinstance(expected,list) or not expected:raise ValueError('empty plan')
    def key(r):return tuple(r[k] for k in KEY)
    planned={key(r) for r in expected}
    if len(planned)!=len(expected):raise ValueError('duplicate plan keys')
    if any(r['arm'] not in ARMS for r in expected):raise ValueError('invalid plan arm')
    groups={}
    for k in planned:groups.setdefault(k[:-1],set()).add(k[-1])
    if any(v!=set(ARMS) for v in groups.values()):raise ValueError('plan missing arm')
    report=analyze(rows);actual={key(r) for r in rows}
    missing=planned-actual;extra=actual-planned
    status='INCOMPLETE' if missing or extra else 'COMPLETE'
    return {'status':status,'plan_sha256':digest(plan),'planned':len(planned),'observed':len(actual),'missing':[dict(zip(KEY,k)) for k in sorted(missing)],'unexpected':[dict(zip(KEY,k)) for k in sorted(extra)],'candidate_critical_failures':report['candidate_critical_failures'],'gate':'BLOCKED' if missing or extra or report['candidate_critical_failures'] else 'COVERAGE_COMPLETE_NOT_CERTIFICATION','analysis':report}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True);a=sub.add_parser('plan');a.add_argument('config');a.add_argument('output');a=sub.add_parser('audit');a.add_argument('plan');a.add_argument('runs');a=p.parse_args()
    read=lambda path:json.loads(Path(path).read_text(encoding='utf-8'))
    try:
        if a.cmd=='plan':
            plan=make_plan(**read(a.config));Path(a.output).write_text(json.dumps(plan,indent=2));print(digest(plan))
        else:
            result=audit(read(a.plan),read(a.runs));print(json.dumps(result,indent=2));sys.exit(int(result['gate']=='BLOCKED'))
    except (ValueError,KeyError,TypeError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(2)
