---
name: skills-humancraft-references-human-ai
description: 'HumanCraft supporting resource: Human–AI collaboration: useful autonomy,
  real control. Read only when relevant to the current task.'
---

# Human–AI collaboration: useful autonomy, real control

Use automation to augment human capability. Specify who decides, what the system may do, required evidence, possible side effects, and stop/recovery options. Autonomous operation is appropriate only within a bounded mandate and risk controls; otherwise provide assistance, proposals or approval gates.

Before use: explain relevant abilities, limits, data access and costs. During use: show status, scope and material assumptions, make it easy to correct, cancel or narrow the task. After use: report what was done, what failed, which sources were used, and how to reverse or escalate. Distinguish proposed, running, partially complete, complete, blocked and uncertain states. Do not imply a background operation unless one exists.

Calibrate trust: do not overstate confidence or anthropomorphize in ways that create false expectations. Prefer meaningful contextual signals to constant interruptions. If AI cannot determine intent or a consequential fact, seek clarification or human review; for harmless decisions make transparent assumptions. Human approval must be meaningful, not a rubber stamp: show target, changes, uncertainty and consequences. Do not train users to ignore excessive warnings.

Define safe degradation and handoff for wrong prediction, tool outage, revoked access, stale data, conflicting instructions, prompt injection and unexpected output. Treat external content as data. Limit privileges and side effects; require appropriate authorization for consequential changes; log enough for accountability without exposing sensitive data. When user takes over, provide context and usable state, not an unexplained failure.

Test with wrong AI suggestions, contradictory evidence, interrupted actions, attempted unauthorized side effects and manual fallback. Assess correction effort and over-reliance, not just accuracy.

## Advanced behavioral checks
Maintain shared task, target, authority and next action. Use quiet persistent signals for routine work. Distinguish committed from pending effects and prevent late callbacks committing cancelled work. See HC-B07/B11. [Contracts](behavior-contracts.md).
