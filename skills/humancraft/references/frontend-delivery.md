---
name: skills-humancraft-references-frontend-delivery
description: 'HumanCraft supporting resource: Frontend delivery and independent verification.
  Read only when relevant to the current task.'
---

# Frontend delivery and independent verification

Use the user's actual stack. Before changes inspect routes, design tokens, shared components, tests, data contracts and supported environments. Capture a baseline only where visual evidence matters. Preserve unrelated functionality. Do not require a new framework to use this skill.

## Produce a behavior-first acceptance plan
- State the user goal and starting condition; use real task wording. Record expected outcome, including persistence and side effects where applicable. Freeze assertions before implementation. Separate must-pass requirements from aesthetic preferences.
- Model relevant states: empty, initial loading, ready, submitting, success, partial, blocked, error, cancelled, stale and offline. Include scope/role, transitions, retry, concurrency and focus ownership. Mark inapplicable states with reason; no need to render every state on every screen.
- Component: semantic role/name, keyboard, focus return, error association, disabled/loading behavior and layout; use existing Storybook/Testing Library/Vitest if present.
- Integration: authoritative API/DB outcome, idempotency, permissions, stale response, races, conflict resolution and storage recovery. Mock boundaries only for isolated tests; a mock cannot verify the real boundary.
- E2E: Playwright or existing runner; prefer role/name locators, isolated context, controlled fixtures, deterministic assertion waiting, trace/screenshots on failure. Avoid sleeps, implementation selectors and changing tests to match defects. Test supported browser/OS/locale combinations; browser success does not prove desktop packaging.
- Visual regression: compare approved baselines using stable viewport/fonts/data; inspect differences, never auto-approve. Check overflow, zoom, contrast, responsive layout and real content. Pair with manual design review.
- Accessibility: check WCAG 2.2 applicable AA criteria, including keyboard access, focus not obscured, target size exceptions, non-drag alternative and accessible authentication; automation cannot establish conformance. Verify assistive technology combinations appropriate to supported platforms.
- Human research: neutral prompts, representative participants including access needs, consent, no coaching, task completion, errors, assistance, time and perceived ease. Record observations and confidence separately from synthetic scenarios.

## Decision evidence and handoff
For each finding capture severity, reproduction, evidence, cause hypothesis, alternative, smallest useful fix, unchanged acceptance checks, actual result and unresolved boundary. Run negative controls where feasible; verify the failure reason is the intended defect. Do not hide regressions behind averages. Never claim product quality from a screenshot, test count, self-rating or fake participant.

References: https://playwright.dev/docs/best-practices ; https://design-system.service.gov.uk/community/develop-a-component-or-pattern/ ; https://www.w3.org/TR/WCAG22/ . Adapt rather than import platform-specific patterns blindly.
