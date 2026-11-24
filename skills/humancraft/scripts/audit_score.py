#!/usr/bin/env python3
"""Summarize explicitly supplied UX evidence, not inferred quality. No external dependencies."""
import json, sys
WEIGHTS = dict(outcome=15, interaction=15, complexity=15, resilience=20, accessibility=10, emotion=10, control=10, delivery=5)
GATES = ('authorization','integrity','recovery','accessible_core','control')
def evidence_ok(value):
    return isinstance(value, list) and bool(value) and all(isinstance(v,str) and v.strip() for v in value)
def reason_ok(value):
    return isinstance(value,str) and bool(value.strip())
def score(data):
    if not isinstance(data,dict): raise ValueError("audit must be an object")
    dims, gates = data['dimensions'], data['gates']
    if set(dims) != set(WEIGHTS) or set(gates) != set(GATES):
        raise ValueError('Supply all eight dimensions and five gates; use unknown when untested.')
    earned = observed = applicable = 0
    unknown = []
    for k,w in WEIGHTS.items():
        d = dims[k]; s = d.get('score'); kind = d.get('evidence_type','unknown')
        if kind not in ('observed_test','observed_inspection','reported','unknown','na'): raise ValueError(k+': invalid evidence type')
        if kind == 'na':
            if s is not None or not reason_ok(d.get('reason')): raise ValueError(k+': N/A needs reason and null score')
            continue
        applicable += w
        if s is None:
            unknown.append(k); continue
        if type(s) is not int or not 0 <= s <= 4 or kind not in ('observed_test','observed_inspection','reported') or not evidence_ok(d.get('evidence')):
            raise ValueError(k+': score needs integer 0–4 and evidence')
        if kind == 'reported':
            unknown.append(k); continue
        observed += w; earned += w*s/4
    blockers=[]
    if not observed: blockers.append('no-observed-dimensions')
    if all(g.get('status')=='na' for g in gates.values()): blockers.append('all-gates-na-requires-independent-scope-review')
    for k,g in gates.items():
        status=g.get('status')
        if status not in ('pass','fail','unknown','na'): raise ValueError(k+': invalid gate')
        if status=='na' and not reason_ok(g.get('reason')): raise ValueError(k+': N/A needs reason')
        if status in ('pass','fail') and (not evidence_ok(g.get('evidence')) or g.get('evidence_type') not in ('observed_test','observed_inspection')): raise ValueError(k+': gate needs observed evidence')
        if status in ('fail','unknown'): blockers.append(k+':'+status)
    return {'observed_score':round(100*earned/observed,2) if observed else None,'applicable_weight':applicable,'observed_weight':observed,'unknown_or_reported_weight':applicable-observed,'observed_weight_coverage_pct':round(100*observed/applicable,2) if applicable else None,'unknown_or_reported_dimensions':unknown,'critical_blockers':blockers,'gate_status':'blocked' if blockers else 'no_recorded_gate_blocker','warning':'Not a release certification; verify scope and evidence independently.'}
if __name__=='__main__':
    try:
        if len(sys.argv)!=2: raise ValueError('Usage: audit_score.py audit.json')
        with open(sys.argv[1],encoding='utf-8') as f: print(json.dumps(score(json.load(f)),ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as e:
        print(str(e),file=sys.stderr); sys.exit(1)
