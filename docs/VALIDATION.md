---
name: docs-validation
description: 'HumanCraft supporting resource: Validation — v0.2.0 preview (2026-11-24).
  Read only when relevant to the current task.'
---

# Validation — v0.2.0 preview (2026-11-24)

| Check | Result | Scope |
|---|---|---|
| Local structure | PASS | 44 unique cases, metadata, main relative references, publication file types |
| Python unit tests | 14/14 PASS | 8 score tests + 6 paired analyzer tests; synthetic inputs |
| Chromium DOM component | 28/28 expected | 14 reference passes + 14 intended fault detections, 1280×900 and 390×844; memory adapter, not E2E |
| Browser navigation / actual localStorage reload | BLOCKED | Environment browser administration denies file and loopback navigation; original error evidence retained |
| Firefox / WebKit / GitHub Actions | NOT_RUN | Workflow added, not executed |
| Real model A/B, activation, actual user studies | NOT_RUN | no raw observations yet |
| Official skill validator, clean client installs, market publication | NOT_RUN | no release claim |

Commands actually executed: `python scripts/validate.py`, `python -m unittest discover -s tests -v`, `python benchmark/run.py --component --executable /usr/bin/chromium`, `python evals/paired.py evals/observed-runs.json`. Chromium 144.0.7559.96, Python 3.13.5, Playwright 1.57.0. See `benchmark/evidence/results.json`, PNG screenshots and Playwright trace archives. The file `navigation-blocked.json` is the original failed navigation run, not counted as mutation detection. The fixture's draft test in component mode re-renders with memory-backed storage; it does not verify actual disk persistence. All mutants are handcrafted, not AI output. All assertions cover synthetic data only; no full WCAG conformance or model improvement implied.

## v0.3.0 validation addendum

2026-11-24: `python scripts/validate.py` passed all 28 Markdown YAML headers, skill name/path/description and main reference checks; 44 behavior cases and 24 activation prompts verified structurally. `python -m unittest discover -s tests -v` passed 31/31 tests (14 retained, 13 trace checks, 4 activation-scoring checks). The trace example CLI returned PASS for 4 synthetic events. The activation analyzer returned NOT_RUN for 0/24 observed results. Actual client imports, live model experiments, new browser runs and human studies are NOT_RUN. Historical evidence above is from v0.2.0.

## v0.4.0 validation addendum (2026-11-24)
- Original 31/31 baseline tests passed. 13 new adversarial tests failed on original v0.3; all 13 passed on v0.4. The full revised suite including 7 matrix checks passed 51/51.
- The original seven component scenarios, two viewports and two variants: 28/28 expected (14 good, 14 faults detected). New repeat-action tests: 12/12 expected (6 original failures, 6 patched passes). These are author-created fixtures and self-applied design rules, not independent model output or persistence tests.
- Full HTTP navigation: 28/28 setup errors, `ERR_BLOCKED_BY_ADMINISTRATOR`; none counted as product defects or successful tests. See `benchmark/evidence-v04/http-blocked.json`.
- No local Codex/Claude/Gemini CLI or configured model API was found. Model comparison, automatic activation, clean client installation, full E2E, real backend, assistive technology and human usability studies are NOT_RUN.
- No official hackathon judgement, external review, or measured market reception.
