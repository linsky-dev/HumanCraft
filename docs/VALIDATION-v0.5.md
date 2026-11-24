---
name: validation-v05
description: "Actual observed benchmark calibration, engineering tests and limits."
---

# Actual v0.5 validation

- Final Chromium calibration: 8 public synthetic tasks × 2 viewport widths × 2 paths × 2 implementations = 64 outcomes. All 64 matched predeclared expectations. Starter normal: 16/16 passed; starter adverse: 0/16 passed. Handcrafted reference normal: 16/16; reference adverse: 16/16. Five critical tasks each at two viewports: starter 10 critical-check failures, reference zero. These are scenario checks, not people or model trials.
- Starter check completion 16/32, reference 32/32. This demonstrates verifier discrimination and repair feasibility, not causal skill uplift. Starter was intentionally defective and reference was written by the authoring agent.
- Experiment protocol: 192 packets prepared for two example configurations (8 tasks, 4 arms, 3 repetitions); NOT_RUN for independent model runs. Placeholder configurations are not actual model names. Sample plan and empty summary included.
- Grader smoke: stale-search starter yielded FAIL (2 failed checks), reference yielded PASS (0 failed checks); both are fixture submissions, not model output. Raw grades, submissions and partial summary included. The experiment is intentionally incomplete and blocked.
- Human observations: empty; no actual participant, preference, task time or satisfaction measured.
- Browser is real Chromium running DOM contents, not a live website or backend; in-memory state, no persistence. HTTP navigation was blocked by environment policy, including an intercepted test origin. Cross-browser CI is configured, not locally executed. No independent Codex/Claude/Gemini client or usable API credentials present.
- Local hashes detect unintended alteration, not malicious tampering by a privileged operator. Public state hooks are mock contracts and can be spoofed by deliberately malicious implementations. Keep grader isolated, independently review tests, and add private holdout tasks and actual server state before external claims.

Raw evidence: `bench/evidence-v05/calibration-final/results.json`, screenshots, `example-plan.json`, `example-empty-summary.json`, `smoke-grades`, `smoke-submissions`, `smoke-summary.json`, `unit-tests.log`. Historical v0.4 evidence is preserved separately.

Final repository verification: 73/73 unit tests passed; 36 Markdown YAML headers and the existing 44 behavior cases / 24 activation cases validated. See `bench/evidence-v05/final-validation.log`.
