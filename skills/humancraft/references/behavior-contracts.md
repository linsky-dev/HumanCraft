---
name: skills-humancraft-references-behavior-contracts
description: 'HumanCraft supporting resource: Behavioral contracts. Read only when
  relevant to the current task.'
---

# Behavioral contracts
Original operational extensions of design theory. Apply only relevant IDs; labels or buttons alone do not satisfy a contract.

| ID | Trigger | Required behavior | Adverse acceptance test |
|---|---|---|---|
| HC-B01 | Similar targets or routines | Distinguish target and scope at action; diverge hazardous vs routine paths early | Alternate routine and rare action; verify only intended object changes |
| HC-B02 | Shared control with modes | Persistently show active mode and units | Interrupt after mode switch; resume and verify target and units |
| HC-B03 | Multi-step work | Externalize prerequisites and unfinished state; preserve draft with privacy limits | Reload and resume without duplicate effects |
| HC-B04 | Async operation | Truthful phase, known/unknown progress, next action and fair queue policy where relevant | Stall or late response; no false success, progress or loss of control |
| HC-B05 | Cross-role service | Visible state, accountable owner, handoff, escalation | Owner absent; replacement receives context and status remains correct |
| HC-B06 | Partial batch | Reconcile completed/failed/pending; scoped retry | Retry failures; verify stored totals and no duplicates |
| HC-B07 | AI/automation | Shared task/scope/limits, meaningful approval and actual intervention | Cancel before commit; wait for late result; no cancelled write |
| HC-B08 | Trust-sensitive use | Align promise, behavior and receipt; disclose uncertainty | Fail after apparent success; receipt must match authoritative state |
| HC-B09 | Multi-reviewer workflow | Accountable owner, independent checks, escalation and dissent | Reviewer absent/disagrees; no silent approval |
| HC-B10 | Degraded service | Diagnose impact and recovery without blame; preserve safe context | Isolated fault and restoration; no fake success |
| HC-B11 | Feedback | Quiet persistent state for routine events; urgent accessible alert when warranted | Burst routine events and one urgent alert; focus and urgency preserved |
| HC-B12 | User preferences | Reversible settings and safe defaults; optional setup | Reset preference without unrelated loss; check novice and expert paths |

For applicable contracts record actor, task, evidence, harm, alternative, expected outcome, test ID, observed result and uncertainty. Real applications need integration/backend tests as well as UI checks.
