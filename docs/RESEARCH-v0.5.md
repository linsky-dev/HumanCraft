---
name: research-v05
description: "Research basis and methodological limitations for the HumanCraft outcome benchmark."
---

# Research rationale — v0.5

- [SkillsBench](https://arxiv.org/abs/2602.12670) and [SkillsBench 1.1](https://www.skillsbench.ai/blogs/skillsbench-1-1): paired skill/no-skill runs, executable verifiers, explicit skill invocation measurement. Our four-arm pilot separates generic guidance and prior version. It is not the SkillsBench dataset.
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401): translate requirements into execution-based acceptance criteria, rather than model opinions. The pilot has a normal path plus an adverse path per task, with user-visible checks and mocked state.
- [Playwright best practices](https://playwright.dev/docs/best-practices): isolated contexts, user-facing locators and observable behavior. Retain evidence and distinguish app failure from infrastructure failure.
- [NN/g Usability 101](https://www.nngroup.com/articles/usability-101-introduction-to-usability/) and [Success Rate](https://www.nngroup.com/articles/success-rate-the-simplest-usability-metric/): measure real task success and errors, not merely visual impression. Our human study is an unexecuted protocol with an empty observation file.
- [Signal or Noise? A Benchmark Study of Agent Skills in Web Development](https://arxiv.org/abs/2608.23067): skill impact depends on model/project and skill matching; motivates additional length-matched and activation controls. Not yet implemented in the current four-arm pilot.
- [SkillBuffBench](https://arxiv.org/abs/2611.22017): paired uncertainty and explicit skill access/memory factors. Our task-cluster bootstrap is descriptive and public-task-limited; no claim of external validity.

These sources inform experimental design, not HumanCraft-specific uplift. Norman-derived theory remains in the original skill references. No copyrighted book text or illustrations are redistributed.
