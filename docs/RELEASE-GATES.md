---
name: docs-release-gates
description: 'HumanCraft supporting resource: Competition-inspired release gates.
  Read only when relevant to the current task.'
---

# Competition-inspired release gates

These are proposed project targets, not observed results or guarantees of popularity.

| Gate | Target evidence |
|---|---|
| Real utility | At least 3 independent adopters complete a real design task and describe a verified benefit; document failures too. |
| Incremental skill value | Two or more agent families, four-arm paired comparison; ≥10 percentage points over no skill and ≥5 over a generic checklist on held-out task pass rates, with uncertainty intervals and no additional critical failures. If not achieved, investigate and narrow scope. |
| Efficiency | Report median tokens/time and quality trade-off. Target ≤20% median token overhead for matched simple tasks; do not trade away safety for tokens. |
| Independent setup | Clean profile, stock agent, no author assistance; installation and first successful task recorded per supported client. Target first usable result within 5 minutes under documented conditions. |
| Engineering | Unchanged behavioral tests, real persistence and backend integration where applicable, supported browser/device matrix, independent review. |
| User experience | Representative task participants, neutral prompts and consent, completion/error/time/assistance; record sampling limitations. |
| Distribution | Maintainer-approved license and name clearance, no book content or private data, reproducible demo, versioned artifacts, transparent limitations and community feedback. |

## 90-second demo storyboard
1. Start with a real failing task, not a beauty shot. Example: cancel an approved archive operation and observe a late commit in the synthetic fault fixture.
2. Show the expected behavior contract HC-B07 and unchanged test. Show the deliberate fault failing and reference passing with trace and authoritative state.
3. Once independent model runs exist, show blinded baseline vs candidate on the same problem; report time and token cost. Until then explicitly label the demo as handcrafted reference/mutant and no causal skill evidence.
4. Install on a clean supported agent, invoke on an unseen problem, show evidence and limitations. Do not stage or cherry-pick a purportedly live result.

## Durable advantage
Keep the skill lean; grow maintained test adapters, domain rules with exceptions, private holdout scenarios, independent outcome evidence and contributor workflows. Re-run baselines as models change. Retire instructions that become redundant or cause regressions. No artificial stars, reviews, telemetry or vendor lock-in.
