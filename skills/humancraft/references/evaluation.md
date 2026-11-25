---
name: skills-humancraft-references-evaluation
description: 'HumanCraft supporting resource: Evidence-based evaluation. Read only
  when relevant to the current task.'
---

# Evidence-based evaluation

For a substantial audit, use eight dimensions and explicit evidence. Weights are a HumanCraft proposal, not a scientifically validated score.

| ID | Dimension | Weight | Evidence to collect |
|---|---|---:|---|
| outcome | User outcome and task fit | 15 | Representative task and completion criteria |
| interaction | Discoverability, mapping, feedback | 15 | Walkthrough and task observations |
| complexity | Comprehensible workflow | 15 | Task steps, handoffs, rework |
| resilience | Prevention, recovery, integrity | 20 | Negative and recovery tests |
| accessibility | Inclusive operation | 10 | Keyboard, zoom, assistive checks as relevant |
| emotion | Contextual visual quality and trust | 10 | Screens and feedback; user research if available |
| control | Autonomy, permissions and agency | 10 | Scope, intervention and authorization tests |
| delivery | Feasible implementation and continuity | 5 | Tests, migration, constraints |

Each score 0–4: 0 observed complete failure; 1 major deficiencies; 2 partial; 3 meets specified representative checks; 4 meets specified checks plus relevant adverse conditions. A rating needs evidence identifiers. Evidence can be observed test, observed inspection, or reported (not verified); untested is null, never zero or a passing score. N/A requires a reason. Report coverage, observed score, and unknowns; no comparability claim across different scope/conditions. Critical defects override numeric scores. Critical checks: authorization, unintended irreversible loss, core task recovery, accessible core path and user control when applicable. Unknown critical check blocks readiness; N/A needs rationale.

Issue record: ID, task/role, reproduction, observed vs expected, user harm, severity, proposed remedy, acceptance test, evidence. P0 critical harm/blocked essential task without safe alternative; P1 major recurring task impediment or substantial risk; P2 moderate friction with workaround; P3 minor polish. Prioritize by impact, frequency, reversibility and certainty, not appearance alone.

Evaluation modes: inspection (hypotheses), executable interaction tests (observed), representative human task testing (observed for sampled users), and longitudinal outcomes. Keep these separate. Do not claim measured outcomes from hypothetical personas or LLM judges. For skill benchmarking use identical prompts and environment with and without skill, repeat trials, blinded review, report completion, severe failures, tokens and runtime. Hold out scenarios; never optimize only for the public examples.

Evidence IDs must be nonempty strings in a list. All gates marked N/A require independent scope review; no observed dimensions blocks a readiness claim. For critical pass claims, require relevant executed tests in addition to inspection.

`audit_score.py` records an `executed-test-required` blocker when a gate is marked pass with inspection evidence alone. An observed failure remains a blocker even when found during inspection. Fix duplicate JSON fields or non-finite numbers before scoring. Run the script from the complete skill directory so its shared parser is available.
