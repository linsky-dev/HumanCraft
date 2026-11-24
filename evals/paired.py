#!/usr/bin/env python3
"""Analyze independently scored paired runs; never call models or infer scores."""
import argparse, json, math, statistics
from pathlib import Path
ARMS=('baseline','generic','previous','candidate')

def require(condition, message):
    if not condition: raise ValueError(message)

def analyze(rows):
    require(isinstance(rows,list),"rows must be a list")
    groups={}
    for r in rows:
        key=tuple(r[k] for k in ('model','harness','config','task','trial'))
        arm=r['arm']; require(arm in ARMS,'invalid arm')
        require(all(isinstance(r[k],str) and r[k].strip() for k in ('model','harness','config','task')),'missing identity')
        require(type(r['trial']) is int and r['trial']>=1,'invalid trial')
        require(type(r['passed']) is bool and type(r['critical_failure']) is bool,'invalid result')
        require(not (r['passed'] and r['critical_failure']),'critical failure cannot pass')
        require(isinstance(r['evidence'],str) and r['evidence'].strip(),'missing independent evidence')
        for k in ('tokens','seconds'):
            require(type(r[k]) in (int,float) and math.isfinite(r[k]) and r[k]>=0,k)
        g=groups.setdefault(key,{})
        require(arm not in g,'duplicate arm');g[arm]=r
    strata={}
    for key,g in groups.items():
        strata.setdefault(key[:3],[]).append(g)
    report=[]
    for key,gs in sorted(strata.items()):
        complete=[g for g in gs if set(g)==set(ARMS)]
        comparisons={}
        for arm in ARMS[:-1]:
            wins=sum(g['candidate']['passed'] and not g[arm]['passed'] for g in complete)
            losses=sum(g[arm]['passed'] and not g['candidate']['passed'] for g in complete)
            n=len(complete)
            comparisons[arm]={'paired_n':n,'wins':wins,'losses':losses,'ties':n-wins-losses,'delta_pp':round(100*(wins-losses)/n,2) if n else None}
        report.append({'model':key[0],'harness':key[1],'config':key[2],'complete_pairs':len(complete),'incomplete_groups':len(gs)-len(complete),'comparisons':comparisons,'arms':{a:{'pass_rate':sum(g[a]['passed'] for g in complete)/len(complete) if complete else None,'critical_failures':sum(g[a]['critical_failure'] for g in gs if a in g),'observed_runs':sum(a in g for g in gs),'median_tokens':statistics.median(g[a]['tokens'] for g in complete) if complete else None,'median_seconds':statistics.median(g[a]['seconds'] for g in complete) if complete else None} for a in ARMS}})
    return {'scope':'independent observed runs only; descriptive paired statistics, no significance or causal claim from synthetic input','status':'PARTIAL' if any(r['incomplete_groups'] for r in report) else 'OBSERVED_INPUT' if report else 'NOT_RUN','candidate_critical_failures':sum(r['critical_failure'] for r in rows if r['arm']=='candidate'),'strata':report}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('json');a=p.parse_args();print(json.dumps(analyze(json.loads(Path(a.json).read_text())),indent=2))
