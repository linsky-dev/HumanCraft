---
name: research-v04
description: Research synthesis, direct tests, competition-readiness limitations and release priorities for HumanCraft v0.4.0.
---
# v0.4.0 — evidence firewall / 2026-11-24

## Research and implementation
- [OpenSearch Agent Skills Hackathon winners](https://opensearch.org/blog/and-the-winners-are-announcing-the-results-of-the-opensearch-agent-skills-hackathon/), 2026-09-14: verify diagnosis rather than assume it, preserve authority boundaries and ship evidence. HumanCraft uses independently observable effects and blocks unsupported readiness claims; it is not an OpenSearch entry and has not been judged.
- [SkillsBench 1.1](https://www.skillsbench.ai/blogs/skillsbench-1-1), 2026-06-16: paired runs, isolated environment and withheld oracles. The published aggregate uplift (+16.6 percentage points) is for their own benchmark, not HumanCraft. Added frozen randomized experiment schedule and completeness gate.
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401): requirement-specific executable acceptance tests. Separate acceptance oracle and implementation.
- [Anthropic Skill Creator](https://claude.com/plugins/skill-creator): executor, grader, blind comparator and analyzer. Separate roles in planned model evaluation; same-agent review in this round is not independent.
- [Playwright best practices](https://playwright.dev/docs/best-practices), [accessibility testing](https://playwright.dev/docs/accessibility-testing): user-observable outcomes, isolation, traces and combined manual/automated assessments. Replayed actual Chromium component tests; added unchanged before/after test suite.
- [Stryker mutation testing](https://stryker-mutator.io/docs/): seeded faults must be detected. Existing and added fixtures remain handcrafted rather than automated mutation coverage.
- [Agent Skills standard](https://agentskills.io/specification): concise entry and progressive disclosure, YAML and relative paths. Client-specific support still needs clean-install verification.

## Evidence
Baseline v0.3: 31 unit tests passed, then 13 additional adversarial tests exposed permissive evidence checks, all-N/A release loophole, incomplete critical failures, optimized-mode assertion bypass, ambiguous whitespace IDs and malformed activation data. All 13 reproduced as failures against frozen v0.3; all pass against v0.4. Seven additional matrix unit tests cover missing entire tasks, missing arms, unexpected rows and critical failure. Full 51 tests passed.

A self-application of HumanCraft to the synthetic workflow lab found two defects not caught by its seven original scenarios: repeat import deleted the previously stored C; completed archive could be initiated again, including after component rerender. Fixed with idempotent merge and state-derived disabled action/handler guard. Same three checks at two viewports: 6 old failures, 6 patched passes. Original 28 component tests also returned all expected outcomes. These were authored by the same assistant, with memory storage. No real model uplift, independent human evaluation, persistent storage or security certification follows. HTTP navigation was blocked by environment policy; actual E2E and cross-browser CI are unrun. No model CLI/API configuration was available.

## Competition gate (project targets, not measured ranking)
Before stable release: independent blind four-arm eval using at least two actual agent families, 3+ trials per held-out task, preregistered model/config/budget/skill and verifier hashes; task success lift >=10pp vs no skill and >=5pp vs generic checklist, report uncertainty and critical failures; clean install on supported clients; real backend/HTTP E2E, visual/a11y review and representative user tasks; public reproducible demo and maintainer-approved license/name. Report all errors and exclusions. Treat incomplete experiments as blockers, not successful results. See RELEASE-GATES.md. No score or rank can establish winning potential without comparative external evidence.

## Demo
Show old vs new import and archive behavior, the frozen tests, failure evidence, and patch. Then show an unseen independent agent task only after actually collecting model results. Never substitute the synthetic before/after demonstration for skill uplift.
