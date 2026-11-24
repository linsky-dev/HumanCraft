---
name: readme
description: "HumanCraft installation and public preview import status."
---

# HumanCraft

**Design for humans, not just screens.** · [简体中文](README.zh-CN.md)

A human-centered design skill for AI agents, informed by Donald Norman's design psychology and modern UX engineering. Move beyond visual polish: design real user outcomes, clear workflows, recoverable mistakes, accessible controls and honest automation.

**v0.6.0 — core skill public preview.** All 25 files in the standard skill directory are imported from the original v0.6.0 source snapshot. The complete development repository (benchmark fixtures, raw evidence, tests and CI) has not yet been imported. Independent model uplift and actual human usability remain unmeasured. This is not a usability certification or a claim of competition placement.

## Quick start

Copy the entire [skills/humancraft](skills/humancraft/) directory into your client's supported Agent Skills folder. Compatible installers may support:

```sh
npx skills add linsky-dev/HumanCraft --skill humancraft
```

Client-specific discovery and import have not been independently verified. No network, Python runtime or third-party API is required for the core instructions; optional local scripts use Python's standard library.

Try: **“Use HumanCraft to audit and improve our batch import flow. Preserve existing features, identify the root causes, define unchanged acceptance tests, and verify actual state and recovery.”**

## What makes it different

- Task-appropriate depth: quick for small edits, standard for features, critical for consequential workflows.
- Human-centered discovery, visual craft, interaction, complexity management, resilience and human–AI control.
- Twelve behavior contracts, independent acceptance checks, evidence firewall and honest handoff.
- Eighteen reference files (including source notes), optional evidence scoring and trace checking.

## Evidence, not claims

The full local v0.6.0 snapshot recorded 77/77 unit tests and 64/64 expected Chromium calibration outcomes on seeded synthetic fixtures. These are not independent model or actual human usability results. The remote repository currently contains the core skill, not the full reproducibility suite. See [validation](docs/VALIDATION-v0.6.md) and [release gates](docs/RELEASE-GATES.md).

## License and attribution

MIT for original project code and documentation (maintainer to confirm before publication). Referenced research and third-party works retain their own rights. See [LICENSE](LICENSE) and [sources](skills/humancraft/references/sources.md). No book PDF, publisher material or endorsement is included. Candidate brand name has not undergone trademark clearance.
