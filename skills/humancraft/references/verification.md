---
name: skills-humancraft-references-verification
description: 'HumanCraft supporting resource: Verification: from design to observable
  behavior. Read only when relevant to the current task.'
---

# Verification: from design to observable behavior
For material changes establish baseline and independent acceptance criteria before implementation. Link issue → rule → test → evidence; do not weaken assertions to make a candidate pass. Use existing test stack and isolated synthetic data.
- Unit: state transitions, validation, permissions, idempotency.
- Component: render empty/loading/error/disabled/success/partial states; keyboard, accessible names, focus and live announcements. Reuse Storybook/Vitest/Testing Library where available.
- Integration: real API contract, stale responses, offline, timeout, conflict, retry, persistence. Never inject destructive faults into production.
- E2E: use user-facing roles/names and observable outcomes, isolated browser contexts and failure traces. Verify actual writes or absence of writes. Test supported engines, viewports and locales.
- Visual: deterministic captures, approved baselines and reviewed diffs; never auto-approve changes. A screenshot diff is not a quality judgment.
- Accessibility: axe or equivalent plus keyboard, focus, zoom/reflow and manual assistive testing. No full conformance claim from automation.
- Human research: neutral task prompts, representative participants, consent, task success, time, errors, assistance, perceived difficulty and comprehension. Keep qualitative findings separate from statistical comparisons.
Run known-good and deliberately broken versions when feasible; negative controls must fail for intended reasons. Setup errors are inconclusive. Record exact commands, environment, cases, artifacts, failures, skips and scope. Recheck fixes against unchanged assertions and related regression. A passing suite proves only its assertions.

## Skill impact is a separate experiment
Use identical task, model/version, settings, tools, budget and initial files for no-skill, generic UX checklist, frozen previous version and candidate. Randomize order, isolate sessions, repeat trials, hold out scenarios and blind independent reviewers. Report critical-check pass rates, introduced defects, tokens, runtime and uncertainty. Track activation precision/recall and irrelevant-task overhead. Mark unavailable models or participants NOT_RUN. Never present deliberately defective vs hand-fixed demos as causal evidence for skill uplift.
