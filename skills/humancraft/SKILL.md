---
name: humancraft
description: >-
  Design, redesign, implement or audit human-centered products, software systems, features, user journeys, interfaces, forms, dashboards, onboarding, recovery flows, service workflows and AI interactions. Diagnose usability, confusing complexity, cognitive load, errors, accessibility and automation risks; produce testable design decisions and practical fixes, not merely attractive screens. Use for UX reviews, product requirements, interaction design, and user-facing changes. 适用于产品设计、系统功能设计、交互与界面、易用性审查、业务流程、异常恢复及人机协作。Do not activate for unrelated backend refactors or pure calculations; use quick depth for localized visual changes when they affect users.
license: MIT
metadata:
  version: "0.6.0"
---
# HumanCraft

Design for the person doing the work, not the implementation's internal structure. Make the next action understandable, the outcome verifiable, and mistakes recoverable. Apply only the depth the task warrants. Preserve existing working conventions and user requirements unless evidence supports a change. Respond in the user's language. Do not treat simulated users as real research.

## Route the task

- Product or feature discovery: [discovery](references/discovery.md).
- Interface, navigation, interaction, form, onboarding: [interaction](references/interaction.md).
- Complex workflow, desktop, enterprise, service, waiting: [complexity](references/complexity.md).
- Visual craft, look, feel, emotional experience, trust: [emotion](references/emotion.md).
- Errors, permissions, destructive operations, account or data recovery: [resilience](references/resilience.md).
- AI agents, automation, recommendations, delegation: [human-ai](references/human-ai.md).
- Accessibility or interface implementation: [accessibility](references/accessibility.md).
- Unclear root cause or contested audit: [evidence-first diagnosis](references/diagnosis.md).
- Review, release readiness or verification: [evaluation](references/evaluation.md) and [verification](references/verification.md).
- Complex or consequential interactions: [behavior contracts](references/behavior-contracts.md); select applicable IDs and link to tests.
- Domain-specific tradeoffs: [contexts](references/contexts.md).

Read only relevant modules; cross-cutting high-risk, accessibility and evaluation checks apply when relevant even if not the main task. For a tiny change, use a short reasoning and validation pass, not a report. For full product work, cover all applicable modules. When another visual design or coding skill is available, use it for visual craft or implementation, and use HumanCraft for human-facing decisions and acceptance. Do not assume other skills are installed.

## Choose depth before work
- **Quick**: localized low-risk UI change; inspect conventions, improve the action and verify its observable outcome. Do not generate a ceremony or score.
- **Standard**: new feature or multi-screen journey; select applicable contracts, map states and test the critical path plus one adverse path.
- **Critical**: permissions, data loss, money, consequential automation, irreversible action or migration; establish an independent acceptance oracle, verify actual state changes and recoverability. Do not release with unresolved critical checks.
- Read [decision playbook](references/decision-playbook.md) when requirements conflict, and [event evidence](references/event-evidence.md) for asynchronous, consequential or batch operations. Use [frontend delivery](references/frontend-delivery.md) for actual UI implementation and validation.
- Prefer installed project conventions, real data contracts and existing tools over generic recipes. Do not install new dependencies, call external services, or upload screenshots/data without need and permission. If a tool is unavailable, deliver the best supported specification and mark missing tests honestly.

## Workflow

1. **Ground.** Inspect supplied screenshots, code, current product, task context and constraints when accessible. Identify user roles, desired outcomes, frequency, environment, skill variation, dependencies and risks. Distinguish observed facts, reported facts, assumptions and unknowns. Ask only for material missing constraints; otherwise proceed with explicit assumptions.
2. **Frame.** Write a user outcome and observable success condition. Map current workflow including interruptions, mistakes and recovery. Identify whether the problem is a missing capability, weak cue, mental-model mismatch, excess complexity, delayed feedback or service boundary. Do not assume the requested solution is the root cause. For material failures, reproduce the premise, compare competing explanations, and only close findings with evidence.
3. **Explore.** For material design choices, compare at least two feasible approaches, including improving the current flow if one exists. Evaluate benefit, effort, risk, learnability, expert speed and migration cost. Choose the smallest useful change; do not force artificial alternatives for trivial edits.
4. **Specify.** Define entry points, user actions, labels, expected outcomes and state transitions. Include applicable empty, loading, success, partial success, error, cancellation, offline, permission and resume states. Keep essential information available at the point of action. Specify frontend and backend contracts for consequential behavior; visual affordance cannot replace authorization.
5. **Build or advise.** Implement when requested and tools allow; otherwise provide a concrete specification or review. Reuse the existing design system. Do not remove essential features for minimalism, invent user research, or silently change business rules. Avoid fake controls and unverified integrations.
6. **Challenge.** Walk the task as a newcomer, an experienced operator, a distracted user, and relevant accessibility or adverse conditions. Try wrong input, repeated action, interruption, permissions, unavailable dependencies and recovery. Classify evidence; record what remains untested.
7. **Verify and hand off.** For material user-facing changes, read [verification](references/verification.md); establish independent behavioral acceptance checks and baseline before edits where feasible. Run available real tests and report observations, defects, and evidence. For broad work, provide priorities, acceptance criteria and unresolved risks. Never claim a usability study, accessibility conformance, platform support, or measured improvement without appropriate evidence. Report whether evidence is code inspection, synthetic behavior, live integration, independent agent comparison or actual human observation.

## Evidence firewall

- Before changing a material flow, freeze acceptance criteria and the baseline. Separate implementation from verification; do not weaken checks to fit a patch. If the agent performs both roles, disclose self-review.
- Test repeated actions, stale responses, role/scope switches, refresh, restart and existing-data preservation where applicable. A visible success message is not an authoritative outcome.
- Treat missing, malformed, incomplete or out-of-scope evidence as unknown; never erase a serious failure because a comparison run is missing. For high-risk gates require relevant executable evidence, not just an attractive screenshot or code inspection. See [regression and evidence firewall](references/regression-firewall.md).

- For claims of improved UX or design quality, distinguish deterministic task completion from human usability. Use pre-change task scripts, compare the same task under both versions, and record critical mistakes, completion, assistance, and actual user time separately. See [outcome measurement](references/outcome-measurement.md). Do not equate screenshot preference or automated test duration with user satisfaction.

## Non-negotiable release checks

- No known path to irreversible unintended loss, unauthorized access or silent wrong-target action. High-impact actions must have scoped authorization and proportionate preview/confirmation/recovery.
- Status, impact, next step and recovery must be intelligible when a core action fails. Preserve input and drafts where feasible.
- Critical tasks must not depend solely on color, hidden gestures, or undocumented memory; support appropriate keyboard and assistive access.
- Automation must be bounded, honest about uncertainty, interruptible where feasible, and genuinely under appropriate user control. Never simulate control that does not exist.
- No fake success/progress, dark patterns, fabricated tests or blocked exits.

## Output contract

For a local edit, deliver the change and a short verification note. For substantial tasks: user outcome; evidence and assumptions; task flow; selected design and tradeoffs; state/permission/recovery behavior; implementation or prioritized findings; acceptance tests and evidence status. Use [design brief](assets/design-brief.md) or [audit template](assets/audit.md) as needed. For structured audit, [rubric](references/evaluation.md) and optional `scripts/audit_score.py` can summarize supplied evidence. For critical workflows optionally run `scripts/check_trace.py` on a sanitized, independently collected event trace; its output is limited to the modeled invariants. A score is not proof of usability. Stop at known critical defects; unknown critical checks prevent release-ready claims.

## Provenance

Original operational framework informed by human-centered design research, including Donald Norman's work. See [sources](references/sources.md). Not affiliated with the authors, publishers, or AI platforms.
