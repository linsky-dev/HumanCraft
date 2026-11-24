---
name: skills-humancraft-references-decision-playbook
description: 'HumanCraft supporting resource: Decision playbook: translate friction
  into a specific remedy. Read only when relevant to the current task.'
---

# Decision playbook: translate friction into a specific remedy

Start with the task, not the visual symptom. In Norman's model, execution and evaluation fail differently. Determine where the user cannot proceed or cannot know what happened. Treat the following as conditional hypotheses, not universal UI laws.

| Evidence pattern | Candidate cause | First intervention | Countercheck |
|---|---|---|---|
| User selects wrong action despite knowing goal | action slip, similar target | distinguish action/object, preview target for high impact | repeated routine then rare action; verify no wrong target |
| User abandons despite correct controls | wrong conceptual model or missing capability | use domain vocabulary, expose prerequisites, test comprehension | ask what will happen before clicking, not whether UI is pretty |
| User forgets after interruption | memory lapse | durable draft, last action, safe resume | interrupt, restart, check draft and no duplicate commit |
| User follows outdated process | rule-based mistake | contextual policy, version and exception path | experienced operator with old habit |
| User lacks information to decide | knowledge-based mistake | disclose relevant facts, uncertainty and consequences | distinguish informed choice from guessing |
| Minimal UI adds navigation | displaced complexity | keep frequent controls discoverable; use progressive disclosure for rare detail | compare task steps AND error recovery; expert shortcuts optional |
| Different teams cannot reconcile progress | mismatched concepts/ownership | map handoff, state owner and source of truth | absent reviewer, retry, conflict, escalation |
| Automation looks easy but control is fake | shared context/control gap | show scope, stage, authority and cancellation semantics | late completion, concurrent changes, actual side effects |

## Resolve tradeoffs
1. Eliminate preventable harm and preserve rights first. Do not weaken authorization or data integrity to save a click.
2. Keep real task requirements, distinguish necessary domain complexity from accidental interaction complexity.
3. Prefer reversible changes and familiar patterns; compare alternatives by observed task outcomes, not counts of rules.
4. Match disclosure to decision timing. Keep consequential limits visible before commitment. Do not hide controls solely for visual minimalism.
5. Preserve expert speed without forcing new users to memorize commands. Add assistance in context; avoid forced tours for everyone.
6. Verify context and culture: dates, sorting, names, directional conventions, keyboard shortcuts, text expansion, locale and platform semantics. Natural mapping is not necessarily universal.
7. If constraints conflict, record the rejected option, risk and validation method. Do not substitute artificial user personas for observation.

## Design from past, present, future
For complex tasks give a useful trace of completed steps, current mode/object/owner and what remains. Display history with privacy boundaries. Teach in context and permit discovery without requiring a manual. For handoffs connect the visible user journey to backstage state and responsibility; do not expose unnecessary internal machinery.

Source basis: Norman volume 1 ch. 2–5 (action and error models), volume 2 ch. 6–8 (service, waiting and complexity), volume 3 ch. 3/5 (experience and trust), volume 4 ch. 2/5/6 (shared context, automation and communication). This table and procedure are original engineering applications, not quotations or validated laws.
