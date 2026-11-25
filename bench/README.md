---
name: humancraft-bench
description: "Reproduce development calibration and run independent agent and human task comparisons."
---

# HumanCraft Bench: v0.6 development pilot

The eight public synthetic workflows are **development cases**, not independent held-out tasks. Each has `starter.html`, a human-readable task contract, `reference.html` (handcrafted by the same authoring agent), and a separate browser verifier. Do not give reference solutions, grading scripts, or prior outputs to the evaluated agent. The state interface is a mock in-memory application contract, not production server state. The verifier is not a security sandbox; run untrusted submissions only in an appropriately isolated environment.

## Reproduce calibration

From the repository root, with Python 3.10+:

```sh
python -m pip install -r benchmark/requirements.txt
python -m playwright install chromium
python bench/verify.py --calibrate --output new-calibration
```

If using a system Chromium, add `--executable /path/to/chromium`. No HTTP navigation is used; screenshots and raw JSON are emitted. Browser cases check normal and adverse paths at 1280x900 and 390x844. Actual CI for other engines has not been run in the authoring environment.

## Independent model comparison (not yet run)

1. Copy `bench/configs.example.json`; replace placeholders with exact model ID, CLI/harness version and config/budget identifier. Freeze model versions, temperature if supported, tool permissions, profile, memory settings, and budget. Do not count two profiles of one model as two model families. Use a fresh isolated session and clean agent profile per run; do not allow access to the repository, grading code, plan mapping, earlier results, or unrelated installed skills.
2. 准备实验。运行 `python bench/experiment.py prepare /path/to/new-experiment configs.json --trials 3 --seed 20261124`。两个配置将生成 192 个任务包。分组映射保存在实验计划中，由评分方保管。默认对照继续使用历史 v0.5 包。若需按 A/B/C/D 四臂比较冻结版 v0.6.0 与当前候选版本，显式添加 `--frozen-v06-control`。此时 baseline 不加载技能，generic 使用通用清单，previous 使用冻结版 v0.6.0，candidate 使用当前技能源码。该选项为显式启用，以保留既有命令和 v0.5 记录原有含义。任务包提供的是显式文件指导，不代表客户端已自动触发或完成安装测试。
3. Send **only** the selected packet to a fresh agent. Use its existing CLI to edit app.html; no access to the oracle. If suitable, the operator may use `python bench/experiment.py run EXP PACKET command.json --operator operator-id`; command.json is an explicit argument array containing `{prompt}` and optionally `{workdir}`. It runs without a shell in the packet directory and records logs, elapsed time and exit status. This is not process isolation; provide an independent sandbox, network policy and fresh profile yourself. Do not store credentials in command files or publish raw logs before sanitizing. If an external tool is operated manually, copy only its app.html back to the packet.
4. For manual runs, supply metadata JSON: `{"model":"exact-model","harness":"exact-cli","config":"frozen-config","status":"completed","operator":"anonymous-operator-id","tokens":null,"seconds":null,"skill_invoked":null}`. Set status to `agent_error` or `timeout` for failures. Record actual token/time/invocation from provider logs where available, never estimate. `python bench/experiment.py record EXP PACKET metadata.json` freezes the artifact. Metadata is operator-attested, not cryptographic proof of model identity.
5. In an independent grader environment run `python bench/experiment.py grade EXP PACKET`; optionally add `--executable ...`. The evaluator compares unchanged user-visible behavior and mock state; independent graders should review verifier validity and cheating risks. The source digest is fixed by the plan but is not a digital signature. The reference files and checks are public; use a genuinely separate holdout before claiming real generalization.
6. `python bench/experiment.py summary EXP > results.json` computes paired task-macro pass rates, critical failures, failure checks, time/token coverage and task-level bootstrap uncertainty. Missing runs and unknown candidate critical results block coverage. Do not omit failures, change budgets per arm or modify the frozen plan. Save raw artifacts, hashes, actual model IDs, configurations, tool versions and logs. A complete run is not a release certification.

Generic control is a short checklist, not token-length matched. Before publication add a length-matched irrelevant control and an actual automatic-activation arm, freeze hidden tasks with an independent author and run both. Public test cases may be memorized by models; keep them for development/regression only.

## Human studies

See `../docs/HUMAN-STUDY.md`; `human_study.py` validates consented anonymized records and summarizes actual task outcomes. The included observation file is intentionally empty. Run `python bench/human_study.py bench/human-plan-example.json bench/human-observations.json`. The example IDs are not participants.

历史对照仍使用 v0.5 技能包。可选的 v0.6 对照包 `bench/controls/v06.zip` 是从 Git 提交 `22077c0971d512eb5eb5fdfe5f2d3da44d8d2a15` 中 25 个受版本控制的 `skills/humancraft` 文件确定性生成的。SHA-256 为 `a216e4fe57716b63c7e1f5ad65e70023fcc54064e29f4716048844e67a14c27d`。收到的 WorkBuddy 压缩包 SHA-256 为 `1a6195c6df8525c095a6cd993b739650d2189e2a3d0dc677523bdbaa5bfa5568`，与 Git 重建的包不同，因此没有作为冻结对照。启用 v0.6 后，冻结清单会保存压缩包哈希，每个任务包也会记录解压技能文件的哈希。

已有实验计划和原始结果保持为历史制品。新的 v0.6 计划会验证完整配置和矩阵，即使计划摘要经过重算也会校验完整性。新实验默认每个条件运行三次。报告时保留随机种子、精确模型标识、执行器版本、预算及全部失败记录。
