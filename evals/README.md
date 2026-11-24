---
name: evals-readme
description: 'HumanCraft supporting resource: Behavioral evaluation (not yet run).
  Read only when relevant to the current task.'
---

# Behavioral evaluation (not yet run)

Use `cases.json` as original development seeds, not proof of improvement. Run each prompt in a fresh session with and without HumanCraft; same model, configuration, tools and task fixture. Allow ordinary activation (measure activation separately from output quality); use explicit invocation in a separate experiment. Repeat at least three times per configuration. Randomize output order and have blinded reviewers mark each assertion pass/fail/not assessable with evidence. For negatives, measure over-triggering. Compare task acceptance rates, critical failures, tokens and wall time; report variance and sample size. Build private held-out variants before tuning. Use actual UI/code fixtures and human task testing for conclusions about usability; an LLM review alone cannot establish them. No test claims in this repository refer to this protocol until raw results exist.

## Paired results
`observed-runs.json` intentionally starts empty. For each task/trial/model/harness/config collect all four arms (`baseline`, `generic`, `previous` (frozen v0.3.0), `candidate`). Keep the same task fixture, budget and evaluator; freeze generic checklist and skill versions. Each row has `model`, `harness`, `config` (version/settings hash), `task`, `trial`, `arm`, `passed`, `critical_failure`, `evidence` (independent artifact reference), `tokens`, `seconds`. A critical failure cannot pass. Run `python evals/paired.py evals/observed-runs.json`. Incomplete groups are excluded and reported, not assumed failed. Compare per-model/harness/config; do not pool incompatible runs. Descriptive uplift is not statistical significance; use task-cluster bootstrap confidence intervals and report independent review agreement before broad effectiveness claims. Track activation separately using all positive and negative cases. Keep holdouts private to avoid benchmark leakage.

Incomplete groups yield PARTIAL; all observed critical failures are counted even when their comparison arm is missing. The comparator is descriptive, not proof of independent execution or completeness of a planned matrix.

## Freeze the planned run matrix before experiments
`python evals/matrix.py plan evals/plan-example.json /tmp/plan.json` generates a deterministic shuffled schedule and SHA-256. Replace the placeholder config with actual pinned model/harness/settings and private holdout task IDs; freeze exact skill ZIP hashes, generic checklist, task fixtures and independent verifiers in the experiment log before execution. `python evals/matrix.py audit /tmp/plan.json evals/observed-runs.json` detects missing whole tasks, missing arms, unexpected results and critical failures. No external agent is invoked by this tool. An empty observation file remains blocked. Complete coverage is not a certification or statistical significance. Review all excluded/errored runs explicitly; do not mark infrastructure errors as product failures. 
