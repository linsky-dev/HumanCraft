---
name: skills-humancraft-references-diagnosis
description: 'HumanCraft supporting resource: Evidence-first design diagnosis. Read
  only when relevant to the current task.'
---

# Evidence-first design diagnosis

Use for material UX failures, contentious changes or audits. Do not force a lengthy process on obvious low-risk fixes.
1. Establish the premise: reproduce the user task under its real role, state, device and constraints; distinguish an actual defect from a report or assumption. Record the exact observation and expected outcome. If reproduction is impossible, mark it unknown.
2. Generate competing explanations: missing capability, misleading cue, incorrect mental model, inconsistent state, permissions, latency, data error or a cross-role handoff. For each, list supporting and disconfirming evidence and the cheapest discriminating test. Do not diagnose solely from a screenshot.
3. Link cause to harm: identify the affected user outcome, frequency and severity; distinguish root causes from symptoms. If evidence does not close the explanation, retain multiple hypotheses; don't manufacture certainty.
4. Specify a test independent of the proposed implementation. Include a known-good negative control and an intentionally defective variant when feasible. Freeze acceptance before edits. Record what would falsify your proposed fix.
5. Make the least disruptive effective change; verify the original failure and neighboring workflows. Record residual risk. No unsupported closure.

## Decision record
- Observed outcome / expected outcome / context / evidence
- Hypotheses and discriminating tests; unknowns
- Chosen change / alternatives / tradeoffs
- Contract ID / acceptance checks / exact test artifact / result / remaining uncertainty

## Product impact
Map each product goal to an observable signal and measurement before collecting metrics (HEART-inspired). For example, successful recovery → verified account recovered without support → completion rate, time, unauthorized attempts blocked. Record denominators, sampling, consent and baseline. Do not optimize engagement at the expense of the user's purpose. A synthetic pass is not a real-user satisfaction rating.
