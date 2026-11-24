#!/usr/bin/env python3
"""Analyze consented anonymized user task observations; never simulate participants."""
import argparse,json,math,statistics
from pathlib import Path
ARMS=('A','B')
def require(ok,msg):
    if not ok:raise ValueError(msg)
def analyze(plan,rows):
    require(isinstance(plan,list) and plan,'nonempty study plan required')
    expected={}
    for p in plan:
        require(all(isinstance(p[k],str) and p[k].strip() for k in ('participant','task','experience')),'missing study ID')
        require(p['experience'] in ('novice','experienced','other'),'invalid experience group')
        require(p['order'] in (['A','B'],['B','A']),'invalid order')
        key=(p['participant'],p['task']);require(key not in expected,'duplicate plan item');expected[key]=p
    seen={}
    for r in rows:
        k=(r['participant'],r['task']);require(k in expected,'unplanned participant/task')
        require(r['variant'] in ARMS and r['consent'] is True,'invalid variant or no consent')
        require(r['position']==expected[k]['order'].index(r['variant'])+1,'order differs from plan')
        require(r['outcome'] in ('unassisted','assisted','failed','withdrawn'),'invalid outcome')
        for f in ('critical_errors','errors'):
            require(type(r[f]) is int and r[f]>=0,'invalid '+f)
        require(r['critical_errors']<=r['errors'],'invalid error count')
        require(r['outcome']!='unassisted' or r['critical_errors']==0,'critical error cannot be unassisted success')
        v=r['seconds'];require(v is None or type(v) in (int,float) and math.isfinite(v) and v>=0,'invalid seconds')
        ease=r['ease'];require(ease is None or type(ease) is int and 1<=ease<=7,'invalid ease')
        require(r['outcome']!='withdrawn' or v is None and ease is None,'withdrawn must not retain measurements')
        key=k+(r['variant'],);require(key not in seen,'duplicate observation');seen[key]=r
    missing=[list(k+(a,)) for k in sorted(expected) for a in ARMS if k+(a,) not in seen]
    pairs=[(seen[k+('A',)],seen[k+('B',)]) for k in expected if all(k+(a,) in seen for a in ARMS) and all(seen[k+(a,)]['outcome']!='withdrawn' for a in ARMS)]
    def metrics(i):
        x=[p[i] for p in pairs];n=len(x);times=[r['seconds'] for r in x if r['outcome']=='unassisted' and r['seconds'] is not None];ease=[r['ease'] for r in x if r['ease'] is not None]
        return dict(n=n,unassisted_rate=sum(r['outcome']=='unassisted' for r in x)/n if n else None,assisted=sum(r['outcome']=='assisted' for r in x),failed=sum(r['outcome']=='failed' for r in x),critical_errors=sum(r['critical_errors'] for r in x),total_errors=sum(r['errors'] for r in x),successful_time_median=statistics.median(times) if times else None,successful_time_n=len(times),ease_median=statistics.median(ease) if ease else None,ease_n=len(ease))
    a,b=metrics(0),metrics(1)
    return dict(status='NOT_RUN' if not seen else 'INCOMPLETE' if missing else 'OBSERVED_INPUT',planned_pairs=len(expected),observed_rows=len(seen),complete_nonwithdrawn_pairs=len(pairs),withdrawn_rows=sum(r['outcome']=='withdrawn' for r in seen.values()),missing=missing,variant_A=a,variant_B=b,delta_unassisted_pp=round(100*(b['unassisted_rate']-a['unassisted_rate']),2) if pairs else None,scope='operator-supplied consented observations; convenience sample, repeated task learning and assignment effects may bias results; no significance or generalization')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('observations');a=p.parse_args()
    try:print(json.dumps(analyze(json.loads(Path(a.plan).read_text(encoding='utf-8')),json.loads(Path(a.observations).read_text(encoding='utf-8'))),indent=2))
    except (ValueError,TypeError,KeyError,OSError) as e:p.exit(2,str(e)+'\n')
