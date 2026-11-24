---
name: skills-humancraft-references-resilience
description: 'HumanCraft supporting resource: Resilience: design for ordinary human
  error. Read only when relevant to the current task.'
---

# Resilience: design for ordinary human error

Differentiate slips (right goal, wrong action), mistakes (wrong understanding or plan), memory lapses, and system faults. Use root-cause evidence rather than blame.

| Failure | Countermeasure | Test |
|---|---|---|
| Wrong adjacent target | Distinct labels, selection scope, preview | Select similar items and attempt change |
| Habit or mode error | Visible mode and target; consistent actions | Switch mode mid-task |
| Interruption/lapse | Save draft/checkpoint; resume cue | Exit, restart and resume |
| Wrong model | Explain consequences and prerequisites | Predict outcome before executing |
| Duplicate requests | Idempotency or explicit deduplication | Double-click/retry after timeout |
| Dependency failure | Preserve data; diagnosis and safe fallback | Kill dependency during write |
| Irreversible change | Scoped permissions, preview, backup/rollback as appropriate | Attempt unauthorized and wrong-target action |

Use a risk ladder: low-risk reversible changes may need only feedback/undo; serious impact needs deliberate review and authorization; unsafe states may require interlock. Do not use confirmation dialogs as a substitute for correct constraints. Error message: factual failure + impact + next step + whether input is preserved + diagnostic detail accessible if needed. Never claim data is preserved without verifying.

Account recovery: distinguish personal and managed accounts. Offer a visible recovery path before login. Use independent verified recovery proof or a properly authenticated local owner route appropriate to the threat model. No bypass based solely on a UI toggle or physical possession, no plaintext password display, no recovery secret leakage. Revoke affected sessions as appropriate; audit managed recovery without exposing secrets. Test legitimate lockout, stolen device, revoked proof, rate limits and offline conditions. If identity proof is unavailable, explain legitimate recovery limits rather than weakening security.

Data relocation/upgrades: discover configured paths, check permissions/free space/compatibility, preserve original data until verified migration, safely identify owned processes rather than kill by port alone, handle stale configuration and unavailable drives, and verify restart/rollback. Never automatically delete unknown data.

## Advanced behavioral checks
Distinguish habitual capture, target similarity and hidden modes. Expert speed is not safety; test common vs rare workflows, interruption and stale mode. Differentiate hazardous paths before commitment. See HC-B01–B03/B06/B10. [Contracts](behavior-contracts.md).
