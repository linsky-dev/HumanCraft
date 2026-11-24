---
name: skills-humancraft-references-interaction
description: 'HumanCraft supporting resource: Interaction: close the action and interpretation
  gaps. Read only when relevant to the current task.'
---

# Interaction: close the action and interpretation gaps

For each critical task, walk the seven phases: goal → plan → specify → perform → perceive → interpret → compare. At each phase ask what the user knows, what the system exposes, what might be misunderstood, and how the user recovers.

| Lens | Design action | Verification |
|---|---|---|
| Discoverability | Put the next meaningful action in the relevant context | First-time user locates action without coaching |
| Affordance | Ensure the action actually works for the role, device and input method | Exercise the action using real permissions and supported input |
| Signifier | Use clear visible labels, shapes, state and accessible names | Predict action and outcome before activation |
| Mapping | Align controls, scope, objects and result; respect platform and cultural conventions | Change target A and verify only A changes |
| Constraints | Prevent invalid combinations, clarify required conditions; enforce rules server-side | Attempt invalid and unauthorized requests |
| Feedback | Acknowledge input; describe state and outcome, including partial completion | Delay, repeat and fail the operation |
| Conceptual model | Use a consistent user-facing model of objects, actions and lifecycle | Ask users to explain what happened and predict the next step |

Prefer recognition over recall: searchable lists, recent items, visible examples, saved context and meaningful defaults. Use real-world terminology. An icon alone is suitable only when familiar in the target context and accessible; unfamiliar or high-risk actions need labels. Use a clear primary action without hiding secondary actions that are genuinely needed. Don't blindly enforce one button per screen or arbitrary click limits.

Design states: initial/empty, ready, loading, success, partial success, invalid input, dependency failure, no permission, interruption/resume, cancellation, and stale data when relevant. Explain disabled actions near the control. Keep field inputs on validation errors, identify the field and correction. In complex forms, group by user activity, disclose requirements before submission, and make review/edit possible. For visual implementation, inspect actual viewport sizes and keyboard focus, not screenshots alone.
