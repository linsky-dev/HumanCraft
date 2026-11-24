---
name: outcome-measurement
description: "Plan comparative UX outcomes, independent task acceptance, and honest evidence."
---

# Measure outcomes, not polish

- Freeze a user goal, realistic initial data, completion oracle, critical errors, and allowed assistance before editing. Include an easy normal path and an adverse path (interruption, change of target, stale response, permission revocation, duplicate action, or recovery).
- Observe both the visible UI and authoritative state. If a backend is simulated, say so. Use the same test across variants, isolated initial state, and stable accessible names or documented contracts. Avoid enforcing an exact internal implementation.
- A failed normal path is a regression even if the adverse path improves. An infrastructure error is not a detected design defect. A missing test is unknown, not success.
- For actual users: give a neutral outcome prompt, not click-by-click instructions. Record unassisted/assisted/failed completion, critical errors and recovery, actual elapsed time, and a post-task ease rating (1–7). Collect consent; do not use real personal data. Recruit representative users, including relevant access needs. Separate novices and experts where appropriate.
- For aesthetic evaluation: use comparable content, viewport, and blind randomized presentation; record human judgments of legibility, visual hierarchy, consistency and contextual fit independently from usability. Do not let visual preference compensate for data loss or inaccessible actions.
- For skill effectiveness: same model/version, tools, input, budget and agent harness; fresh sessions with no carryover. Compare no skill, generic guidance, prior version and candidate. Keep tests outside agent workspaces, freeze test/hash and record all runs, including errors. Document actual skill invocation, time and token usage; report unknown when missing.
- Report paired task-level effect, uncertainty, critical failures, coverage and cost separately. Public development tasks are not a hidden holdout; do not tune against a claimed held-out test. Avoid causal/generalized claims for self-authored fixes, small convenience samples or synthetic workflows. A score is not a usability certification.
