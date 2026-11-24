---
name: regression-firewall
description: Prevent false passes and regression in UX engineering; select independent oracles, adverse cases and evidence scope.
---
# Regression and evidence firewall

1. Freeze the task, intended behavior, test oracle, initial data and environment. Inspect the existing path and run the baseline before edits; a failing environment is ERROR, not a discovered design defect.
2. Choose evidence independent of UI claims: persisted data, authorized server outcomes, operation receipts and actual task completion. Keep a negative control (a deliberately broken implementation) and a positive control. For stateful actions verify repeat, retry, interruption, stale results, target changes and existing records. Distinguish local mock evidence from a real backend.
3. Run the unchanged oracle on the patch. Separate PASS, FAIL, ERROR, NOT_RUN and NOT_APPLICABLE. Missing coverage is not a pass. An unresolved severe failure remains visible even if a comparison arm is incomplete. Record observed versus expected and reproducible commands. Do not treat an assertion on a CSS class or an internal boolean as proof of successful human interaction.
4. When scoring, give evidence IDs and coverage; independently review applicability and provenance. Scores cannot certify safety or real usability. For authorization, data integrity, cancellation and recovery, inspect actual effects and require relevant executed tests before release-ready claims. Self-generated traces must be labeled synthetic.
5. For model comparisons, freeze model/configuration, budgets, tool access, fixtures, baseline version and criteria. Isolate sessions, randomize arms, repeat runs, blind reviewers and reserve holdouts. Record all attempts including infrastructure errors and unpaired failures. Report task-level uncertainty and distinguish execution quality from activation. Do not claim model uplift from handcrafted fixtures or the same author judging their own work.
6. In routine work keep this proportional: a small cosmetic repair needs no formal score. In critical workflows the release claim is blocked when critical evidence is absent. Do not replace human testing or accessibility review with automation alone.
