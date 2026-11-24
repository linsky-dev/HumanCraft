---
name: benchmark-readme
description: 'HumanCraft supporting resource: HumanCraft Workflow Lab. Read only when
  relevant to the current task.'
---

# HumanCraft Workflow Lab

An original synthetic UI with seven seeded single-fault variants; it tests the **test harness**, not agent skill efficacy. Each check runs against a reference and a defective variant at 1280 and 390 CSS pixels. The defect must fail the intended assertion; setup errors are not detection. Screenshots and Playwright traces are emitted locally. Never use production data.

```sh
python -m pip install -r benchmark/requirements.txt
python -m playwright install chromium
python benchmark/run.py --output /tmp/hc-e2e
```

Optional `--engine firefox` or `--engine webkit` after installation; `--executable` selects a locally installed browser. Normal mode uses a loopback HTTP server and browser localStorage. In restricted environments use `--component` to run offline DOM interaction tests with an injected memory adapter. This exercises component behavior but cannot prove actual navigation, persistence, API integration or end-to-end behavior. The draft case re-renders with the same adapter rather than reloading.

The seven cases cover target scope, draft state, partial imports, cancellation with late commit, honest waiting, service handoff and keyboard/accessibility names. Use the same tests against candidate implementations with unchanged assertions. For actual skill impact use `evals/README.md` and independent holdouts.

## v0.4 regression
`python benchmark/regression.py --executable /usr/bin/chromium --output /tmp/hc-regression` compares the frozen v0.3 fixture and patched v0.4 fixture with identical checks for repeat import, already-completed archive and rerender. It is offline DOM testing using memory storage. See `evidence-v04/`.
