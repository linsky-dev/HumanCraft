#!/usr/bin/env python3
"""Compute activation metrics from observed results only."""
import json,sys
from pathlib import Path
def score(cases,observed):
    if not isinstance(cases,list) or not cases or any(not isinstance(x,dict) or not isinstance(x.get('id'),str) or not x['id'].strip() or type(x.get('should_trigger')) is not bool for x in cases): raise ValueError('invalid expected cases')
    if len({x['id'] for x in cases})!=len(cases): raise ValueError('duplicate case')
    expected={x['id']:x['should_trigger'] for x in cases}
    if not isinstance(observed,dict) or set(observed)-set(expected) or any(type(v) is not bool for v in observed.values()): raise ValueError('invalid observation')
    tp=fp=tn=fn=0
    for k,v in observed.items():
        t=expected[k]
        if t and v: tp+=1
        elif v: fp+=1
        elif t: fn+=1
        else: tn+=1
    return {'status':'COMPLETE' if len(observed)==len(expected) else 'PARTIAL' if observed else 'NOT_RUN','coverage':len(observed)/len(expected),'observed':len(observed),'total':len(expected),'tp':tp,'fp':fp,'tn':tn,'fn':fn,'precision':tp/(tp+fp) if tp+fp else None,'recall':tp/(tp+fn) if tp+fn else None}
if __name__=='__main__': print(json.dumps(score(*[json.loads(Path(x).read_text(encoding='utf-8')) for x in sys.argv[1:3]]),indent=2))
