---
name: docs-roadmap
description: 'HumanCraft supporting resource: Roadmap and release gates. Read only
  when relevant to the current task.'
---

# Roadmap and release gates

## 0.1 preview
Single portable skill, modular references, structured audit and test seeds. Verify structure, scorer behavior and repository contents. No claims of behavioral uplift.

## 0.2 evidence release
Run the evaluation protocol on at least two different agent families, with and without skill; include Chinese and English, novel tasks, hard negatives and repeated trials. Track trigger precision/recall, completion, severe defects, subjective blinded preference, time and tokens. Publish raw sanitized outputs, model/version and environment. Suggested project targets (not measured): no new severe failures, ≥85% precision and recall, materially improved acceptance check rate without disproportionate overhead. Use representative human testers for selected tasks. Investigate regressions before release.

## 0.3 distribution
Check candidate name availability/trademarks and confirm license (MIT is a candidate for original content only). Add a maintainer-approved license, contribution guide, security reporting and versioned release. Publish GitHub with concise bilingual README, topics agent-skills/ux/human-centered-design/product-design/accessibility, 3 reproducible before/after demos, actual screenshots and eval summary. Verify marketplace-specific packaging, policies and installation on clean profiles; use skills.sh discovery/install if supported; do not claim marketplace approval without evidence. Consider separate plugin wrappers only where needed; keep portable skill canonical.

## 1.0
Expand tested scenarios, independent reviewer/human tests, reliable installation matrix, stable schema, changelog and feedback-driven updates. Maintain a held-out regression suite. Prioritize meaningful user success over download counts. Publish transparent negative findings; avoid spam or artificial stars.

## Current v0.2 preview status
Evidence infrastructure and component mutation tests exist; the original v0.2 model impact gates remain open. See VALIDATION.md and RELEASE-GATES.md. Do not confuse a prepared CI workflow with a successful CI run.

## v0.6 public preview candidate

Engineering and distribution checks are prepared; actual publication, independent client setup, held-out model comparisons and representative users remain gates. Public release should be explicitly marked preview until these are observed. Keep the development cases public and independent holdout cases separate.
