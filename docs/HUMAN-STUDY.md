---
name: human-study-protocol
description: "Protocol for actual user testing of workflow changes and separate visual preference."
---

# Human usability and visual quality study

**Status: NOT_RUN.** No actual participants or ratings in this release.

Research question: can intended users complete the same task without assistance more often, with fewer critical mistakes, and with less effort? Visual appeal is a separate outcome, never a substitute for correct behavior.

1. Recruit representative users for one specific product/workflow, including relevant novices, expert operators and accessibility needs. Start a formative round with a small group to fix obvious problems; predefine sample size and analysis for a later confirmatory round based on expected effect, variability and the smallest meaningful benefit. Do not promise a universal sample size. Obtain informed consent, explain voluntary withdrawal, use dummy data, and do not collect identifying or sensitive data.
2. Freeze neutral prompts, time limit, assistance criteria, critical error definitions and completion conditions. Use realistic tasks rather than directions such as “click the Undo button.” Example: “You removed record A by mistake. Restore it without removing record B.”
3. Randomize or counterbalance order (A→B and B→A), hide product branding and evaluator preferences, and use equivalent but different task data to reduce learning. Include a between-subjects alternative when carryover is substantial. Keep browser, device, accessibility settings, data and time conditions comparable. Record technical failures separately and do not reclassify participant failures as infrastructure.
4. Observers record `unassisted`, `assisted`, `failed`, or `withdrawn` completion, critical errors, total errors, actual seconds and post-task ease (1–7). Record observed reasons qualitatively using anonymous IDs. Do not infer satisfaction from scripted browser timings. For visual preference use randomized screenshots with equal content and viewports; independently rate hierarchy, readability, consistency and product fit; include accessibility tests and aesthetic choice as secondary outcomes.
5. Keep signed-off plan before observing outcomes. Report unassisted completion, assisted completion, errors, successful-task time (and its denominator), and ease, together with incomplete/withdrawn cases and selection bias. Do not imply significance from an unpowered pilot. Confirmatory analysis should account for participant and task clusters and order.
6. Use `bench/human_study.py`. Plan is a JSON list with `participant` (anonymous study code), `task`, `experience` (`novice`, `experienced`, `other`) and `order` (`["A","B"]` or reversed). Observations contain `participant`, `task`, `variant`, `position`, `consent`, `outcome`, `critical_errors`, `errors`, `seconds`, `ease`. Unknown numbers use null where supported. Withdrawals do not retain timings or ease. The analyzer reports descriptive paired metrics only, and cannot verify that consent or data are authentic.

Do not publish private notes, identifying video or raw production records. Do not count internal testers as independent representative users without disclosure.
