---
name: skills-humancraft-references-sources
description: 'HumanCraft supporting resource: Sources and boundaries. Read only when
  relevant to the current task.'
---

# Sources and boundaries

HumanCraft is an independent, original operational synthesis, not an official adaptation or a replacement for reading the books. Donald A. Norman: The Design of Everyday Things (revised edition); Living with Complexity; Emotional Design; The Design of Future Things. Chinese edition supplied for private research: 《设计心理学》全四册, 中信出版社, 2015. Public distribution should not include that PDF, translated passages, illustrations or reconstructed chapter-by-chapter substitutes. Concept labels and bibliographic citations are used for attribution. No author or publisher endorsement implied.

Extensions (not attributed to Norman):
- Agent Skills specification: https://agentskills.io/specification
- OpenAI skill creation and evaluation: https://github.com/openai/skills ; https://developers.openai.com/blog/eval-skills
- Anthropic skill creator: https://github.com/anthropics/skills/tree/main/skills/skill-creator
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Microsoft HAX guidelines: https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/
- Comparison projects: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill ; https://github.com/anthropics/skills/tree/main/skills/frontend-design

Engineering constraints, rubric weights, gate semantics, examples and workflows are HumanCraft proposals. They are not quoted from, licensed by, or empirically validated by the sources above.

## Evaluation and product engineering extensions
- OpenSearch Agent Skills Hackathon winners, 2026-09-14: https://opensearch.org/blog/and-the-winners-are-announcing-the-results-of-the-opensearch-agent-skills-hackathon/ (evidence-gated diagnosis; original adaptation).
- MIT Media Lab NandaHack: https://nandahack.media.mit.edu/ (independent stock-agent use, ease of setup).
- Anthropic hackathon: https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon (acceptance-first and domain-grounded evaluation).
- NVIDIA SkillEvaluator: https://developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator/ (paired live skill evaluation).
- Playwright: https://playwright.dev/docs/best-practices; Storybook: https://storybook.js.org/docs/writing-tests/ (user-facing tests and CI).
- Rodden et al., HEART: https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/ (goal-signal-metric).

## v0.3 additional research
- Agent Skills specification and authoring guidance: https://agentskills.io/specification ; https://agentskills.io/skill-creation/best-practices . Use bounded entry instructions, load relevant references, capture concrete expert procedures and measure actual execution.
- Anthropic skill-creator: https://github.com/anthropics/skills/tree/main/skills/skill-creator . Use trigger-positive/negative cases and blind comparisons; never infer actual activation from the description text alone.
- SkillsBench: https://arxiv.org/abs/2602.12670 ; SWE-Skills-Bench: https://arxiv.org/abs/2603.15401 . These independent studies motivate controlled comparisons and compatibility checks; their findings are not HumanCraft results.
- GOV.UK Design System contribution and research criteria: https://design-system.service.gov.uk/community/contribution-criteria/ . Check the actual user need, context and representative accessibility evidence.
