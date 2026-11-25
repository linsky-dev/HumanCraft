---
name: international-benchmark
description: "截至 2026-11-24 的 Agent Skills 工程、实证评测、人本交互、无障碍和公开竞赛对标；区分外部证据、HumanCraft 已有证据与建议行动。"
---

# HumanCraft 国际对标与证据边界

访问日期：2026-11-24

## 目的与判读规则

本文查阅官方规范、项目文档、政府服务指南、原始研究预印本及主办方赛事结果。外部项目的成果只用于总结方法和建立对标，不构成 HumanCraft 已达到相同结果的证据。研究论文中的统计结论属于论文作者报告，研究版本和任务集的适用范围以原文为准。

本文将发现分为三种状态：

- **已核实的外部证据**：来源页面直接支持的规范、方法、赛事结果或论文报告。
- **HumanCraft 当前项目证据**：仅引用仓库中可定位的验证记录。历史测试或合成夹具结果不等同于模型增益、生产系统质量或真人体验。
- **建议行动**：从外部方法推导出的项目工作项，尚不表示已经实现或验证。

## Agent Skills 格式与实现实践

### Agent Skills 开放规范

Agent Skills 规范要求技能至少有一个 `SKILL.md`，以 YAML front matter 和 Markdown 正文构成。`name` 与父目录同名，`description` 同时说明能力和触发条件。`scripts/`、`references/` 和 `assets/` 是可选结构。规范允许渐进披露：发现时先呈现名称和描述，模型需要该技能时再读取正文和相关资源。[Agent Skills 规范](https://agentskills.io/specification)

**对 HumanCraft 的建议行动：**继续让入口文件承担路由与执行步骤，把深入知识放在被明确引用的参考文件中；为 name/description 建立格式、长度、目录一致性和触发边界检查。文件可解析只证明格式有效，需另行验证各客户端实际发现、加载和调用。

### OpenAI Skills 与 Codex

OpenAI 文档把 Skill 定义为可复用指令及支持文件目录，建议 description 交代“做什么”和“何时使用”，references 用于背景资料，scripts 用于可重复动作，assets 用于模板或资源。官方还提醒，Skill 内容会影响规划和工具执行，应按不可信输入审阅，尤其是联网工作流中的提示注入与数据外传风险。[OpenAI Skills API 指南](https://developers.openai.com/api/docs/guides/tools-skills) [OpenAI Build skills](https://developers.openai.com/plugins/build/skills)

OpenAI 面向 Codex 的技能评测文章建议准备可量化任务，运行技能版本并检查逐项输出，对结果迭代后扩大测试集。它还强调技能名称和描述是触发信号。该指南展示评测流程，不代表某一具体技能已有增益。[OpenAI Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)

**对 HumanCraft 的建议行动：**持续测试应触发和不应触发的任务，保存模型、客户端、提示、技能哈希和输出。仅凭当前会话读取了 `SKILL.md`，不能外推为 Codex、Responses API 或其他客户端均已安装成功。

### Anthropic Skills

Anthropic 开源 `skill-creator` 描述了一套迭代流程：写技能草案、构造测试提示、执行有技能任务、评估结果、根据反馈和量化评测修改，再扩大任务集。触发优化示例混合正例和负例，设置训练集和保留集，重复多轮调用以观察触发稳定性，并按保留集成绩选择描述。文档也提醒简单任务可能无需技能，因此触发样例应覆盖模型确实能从技能中获益的复杂任务。[Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)

**对 HumanCraft 的建议行动：**把触发测试集与行为增益评测分开，防止只优化触发率；保留未参与描述调优的触发测试样本；不能把描述优化分数当作技能完成任务质量。

### Google Gemini CLI

Google Gemini CLI 官方文档记载其支持 Agent Skills，并可通过项目或用户级 Skill 发现专业指令；扩展还可组合工具、MCP 服务、自定义命令、主题、hooks、子 Agent 和技能。扩展层可带来更广的能力，也意味着评测时必须记录实际启用的扩展、工具和配置，避免把扩展提供的能力误计为 HumanCraft 的贡献。[Gemini CLI 使用 Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md) [Gemini CLI 扩展](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/index.md)

**对 HumanCraft 的建议行动：**跨生态验证时为每个客户端记录版本、发现路径、加载轨迹、扩展和工具权限。当前仓库的本地验证记录未提供 Gemini CLI 实际导入或运行结果，因此兼容性仍待实测。

## 技能增益研究与评估设计

### SkillsBench

SkillsBench 论文预印本报告 86 个任务、11 个领域和确定性验证器，比较无技能、策展技能和模型自生成技能三种条件。作者报告 7 种 agent/model 配置、7,308 条轨迹；策展技能平均通过率提高 16.2 个百分点，但效果按领域差异很大，84 个任务中 16 个为负增益；聚焦且由 2–3 个模块构成的技能优于综合型文档。以上是该论文任务集和配置的结果，不可直接套用到 HumanCraft。[SkillsBench 论文](https://arxiv.org/abs/2602.12670) [SkillsBench 项目页](https://www.skillsbench.ai/)

**对 HumanCraft 的建议行动：**预先指定主要指标，以任务为配对单位计算有技能与无技能差值；保存负增益结果；按任务类别和模型配置报告异质性；考虑对入口和模块进行消融，检验知识拆分是否减少简单任务的上下文开销。论文展示的平均效应不能替代 HumanCraft 自身实验。

### SWE-Skills-Bench

SWE-Skills-Bench 2026 年 10 月修订版预印本评估 98 个公开 SWE 技能，每个技能配对真实 GitHub 仓库固定提交、仓库特定需求和可执行验证器。作者在四种 agent/model 配置中做有技能/无技能配对，合计 3,920 项评估。论文报告 92/98 个技能没有显著效果，平均通过率从 76.6% 到 76.9%；少数技能有正增益，也发现技能模板会锚定模型并覆盖任务明确要求而造成负增益。论文尚属预印本，数据集为软件工程任务，不能视为 HumanCraft 的结果。[SWE-Skills-Bench v2](https://arxiv.org/abs/2603.15401)

**对 HumanCraft 的建议行动：**每项实验采用独立工作区、相同初始提交和冻结验收程序；技能不得修改 verifier 或读取隐藏答案；用保留任务检验过拟合；记录指令冲突、回归和负增益，尤其关注技能模板覆盖用户明确要求的案例。

### NVIDIA SkillEvaluator

NVIDIA 在 2026 年公开的 SkillEvaluator 文章介绍三层流程：静态结构、安全、许可与脚本检查；技能之间的语义重复检查；最后在隔离环境中执行有技能和无技能的真实任务对照。作者描述的 Tier 3 在同一 harness 中固定提示、模型、任务输入、评分方式和隔离沙箱，只切换技能是否安装，并可使用 Harbor 执行任务与收集结果。文章报告其首轮评估覆盖 300 多个已核验技能和 30 多项产品。该集合及汇总分数为 NVIDIA 自述，任务领域、评分器和 harness 限制需在解释其数字时保留。[NVIDIA SkillEvaluator 方法](https://developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator)

**对 HumanCraft 的建议行动：**将格式与安全扫描、重复规则审查、任务运行三类结果分开报告。核心实验需冻结基线和任务输入，使用隔离目录，并保证判分器不受被测 Agent 修改。工程静态测试通过不能表述为模型提升。

## 人本交互、产品体验与研究方法

### Microsoft HAX Toolkit

Microsoft HAX Toolkit 面向用户型 AI 产品，包含人机交互指南、设计模式库、团队优先级工作簿和面向自然语言系统的失败模式 Playbook。它把 AI 的行为与交互作为产品设计对象，支持团队在开发前规划常见失败及缓解措施。[HAX Toolkit](https://www.microsoft.com/en-us/haxtoolkit/) [HAX Playbook](https://www.microsoft.com/en-us/haxtoolkit/playbook/) [Microsoft Research HAX 项目](https://www.microsoft.com/en-us/research/project/hax-toolkit/)

**对 HumanCraft 的建议行动：**把 HAX 作为 Human-AI 工作流和失败模式的补充参考，逐条映射现有 HumanCraft 合约与恢复行为，标明重复、缺失或不适用项。现有材料未证明 HumanCraft 与 HAX 已完成系统映射。

### Google HEART

Google 研究论文提出 HEART 作为大规模用户体验指标框架，分别关注 Happiness、Engagement、Adoption、Retention 和 Task Success，并以 Goals-Signals-Metrics 的过程把产品目标映射到可观察信号和指标。它强调指标要从目标推导，避免用通用指标替代具体用户结果。[Google HEART 原始论文](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36299.pdf)

**对 HumanCraft 的建议行动：**针对具体软件任务先定义任务成功、错误和恢复目标，再选择适当量化指标；只有在产品具有重复使用场景并能获取真实行为数据时，才使用留存或参与度指标。HEART 框架本身不能证明设计造成因果改善。

### Nielsen Norman Group 启发式

NN/g 将十项可用性启发式说明为广泛的经验规则，而非具体验收标准，包括系统状态可见、现实世界匹配、用户控制、错误预防、识别优于回忆、错误诊断和恢复等。[NN/g 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)

**对 HumanCraft 的建议行动：**用启发式生成审查问题和缺陷假设，随后通过真实流程、状态和可执行条件验证。专家启发式检查不能代替目标用户任务测试。

### GOV.UK Design System 与 Service Manual

GOV.UK 指南要求团队理解端到端用户需求，尽早测试假设并通过原型探索设计；代码原型适合验证更真实的交互。主持式可用性测试应观察真实或潜在用户完成清晰、中性、可信的任务，并纳入残障用户和需要协助的群体。具体设计系统是公共服务语境下的组件与模式资源，不是所有产品必须复制的统一视觉风格。[GOV.UK Service Standard：理解用户需求](https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs) [GOV.UK 原型指南](https://www.gov.uk/service-manual/design/making-prototypes) [GOV.UK 主持式可用性测试](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing) [GOV.UK 研究规划](https://www.gov.uk/service-manual/user-research/plan-user-research-for-your-service) [GOV.UK Design System](https://design-system.service.gov.uk/)

GOV.UK 服务评估指南提示演示全流程并说明异常路径，例如用户不符合资格或无法按时提供证明材料。服务研究还应纳入真实任务经验、合适的用户群和现实数据。[GOV.UK 服务评估](https://www.gov.uk/service-manual/service-assessments/how-service-assessments-work) [GOV.UK 政府用户服务设计](https://www.gov.uk/service-manual/design/services-for-government-users)

**对 HumanCraft 的建议行动：**为状态、失败和恢复路径设置任务验收；真人研究须单独招募、知情同意并记录完成率、耗时、错误与求助。AI 模拟结果只能作为探索，不应称作真人可用性证据。

## 无障碍标准与测试工具

### WCAG 2.2

W3C WCAG 2.2 是 W3C Recommendation，含面向不同设备的、可测试且技术无关的成功准则。W3C 建议制定或更新无障碍策略时考虑使用当前版本。它提供评价标准，不是自动扫描器，也不涵盖每一种残障用户需求。[W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/)

### Playwright 与 axe-core

Playwright 官方无障碍测试指南通过 `@axe-core/playwright` 把自动扫描嵌入浏览器测试，并明确自动化只能发现部分常见问题，仍需人工无障碍评估和包容性用户测试。[Playwright Accessibility Testing](https://playwright.dev/docs/accessibility-testing)

### Testing Library、Storybook 与 axe-core

Testing Library 的原则是优先从用户可见和可访问的方式查询及操作界面，使组件测试尽可能接近实际使用。[Testing Library 原则](https://testing-library.com/docs/guiding-principles/)

Storybook 官方测试文档提供组件测试、交互测试和可访问性测试流程；axe-core 文档说明其自动规则仅检测部分可自动化的 WCAG 相关问题。不同工具的扫描通过率不能代替键盘、焦点、读屏和真人参与的检查。[Storybook 测试](https://storybook.js.org/docs/writing-tests) [axe-core](https://github.com/dequelabs/axe-core)

**对 HumanCraft 的建议行动：**把自动扫描、键盘/焦点人工检查、屏幕阅读器检查和残障用户研究作为不同证据来源记录；报告工具版本、测试页面和状态，避免以单一 axe 结果宣称符合 WCAG 2.2 AA。

## 已核实的 Agent Skills 竞赛结果

竞赛项目可提供价值取舍和演示方式案例。获奖身份与主办方的评价属于外部事实，不等于对 HumanCraft 的认可，也不能代替其独立评测。

### MIT Media Lab / HCLTech NandaHack 2026

主办方页面说明活动于 2026 年 6 月至 7 月举行，超过 400 名注册者、230 多项独立提交、125 多项完整提交。决赛要求团队提供一个服务和 `SKILL.md`，评审用 stock agent 仅凭该文件调用服务。评判关注实用性、创意、易设置，以及 Agent 能否只靠技能文件成功使用。页面公布首奖 AgentPress，第二名 2036 Agentic Town: AI Constitution (Civil Ledger)，第三名 Litmus: secure NANDA。[NandaHack 官方活动与获奖结果](https://nandahack.media.mit.edu/)

**可借鉴方法：**冷启动的 skill-only 可用性评测、外部服务可达性验证、明确 setup 步骤和现场 demo。主办方公布的提交规模与成绩为活动信息，不构成独立模型增益研究。

### OpenSearch Agent Skills Hackathon 2026

OpenSearch Project 官方结果页记录赛事于 2026 年举办，要求 Apache 2.0 代码、README 和五分钟 demo。评审权重为技术创新 25%、社区创意与效用 25%、运营卓越 20%、厂商中立与可移植 15%、文档与赋能 15%。结果页公布三项获奖技能：第一名 `unclosed`、第二名 GDPR Forget-Me、第三名 `slow-query-doctor`。[OpenSearch 官方获奖结果](https://opensearch.org/blog/and-the-winners-are-announcing-the-results-of-the-opensearch-agent-skills-hackathon/) [赛事信息](https://opensearch.org/events/agent-skills-hackathon-us-2026/)

主办方对案例的技术说明包括：`unclosed` 在根因分析前验证异常是否真实，显式保留假设分支并做解释闭合检查，附有标注测试语料；GDPR 技能采用只读输出、法律保留拒绝、可审计脚本和合成数据验证；`slow-query-doctor` 比较原始及改写查询的实际延迟，并附单元测试、四个 Docker 场景和 11 项 LLM-as-judge 评估。此处为赛事主办方的项目介绍，未在本轮独立运行获奖仓库或复核其测试。[OpenSearch 获奖案例详情](https://opensearch.org/blog/and-the-winners-are-announcing-the-results-of-the-opensearch-agent-skills-hackathon/)

**可借鉴方法：**先验证问题前提；输出可追溯的推理证据；只读诊断，变更交给用户审批；用实际前后测量和包含负例的测试材料支持结论；优先采用标准接口与低依赖实现。尚未在 HumanCraft 独立复现这些案例。

## HumanCraft 已有证据与状态

本轮查看仓库记录 [docs/VALIDATION-v0.6.md](../VALIDATION-v0.6.md) 和 [docs/RELEASE-GATES.md](../RELEASE-GATES.md)。前者记录历史 v0.6.0 的 77/77 单元测试和 64/64 合成 Chromium 校准预期结果，并明确其不是生产服务器、持久化、用户满意度或技能因果增益证据。记录还将独立模型执行、真实客户端安装/激活、独立隐藏测试、真人研究列为 `NOT_RUN`，并说明远程 Actions 尚未观察到运行结果。此处是仓库记录的复述，本报告编写期间没有重跑这些测试。

因此，截至本报告编写时，现有记录能支持的是特定本地测试与合成校准结果；不能支持任务通过率因 HumanCraft 提升、真人认知负担降低、视觉盲评优势、跨模型兼容性或冠军竞争力等结论。项目的 release gates 将这些作为目标和后续验收条件，而非已取得成绩。[v0.6 验证记录](../VALIDATION-v0.6.md) [发布门禁](../RELEASE-GATES.md)

### 证据和工作项映射

| 领域 | 外部已核实依据 | HumanCraft 当前证据 | 建议行动与完成条件 |
|---|---|---|---|
| Skill 格式与触发 | Agent Skills、OpenAI、Anthropic 对元数据、触发、模块化的说明 | 仓库有技能及引用目录；本报告未审计完整兼容性 | 增加可重复的格式/引用/正负触发检查；逐个客户端实测发现、加载、调用 |
| 技能因果增益 | SkillsBench、SWE-Skills-Bench、SkillEvaluator 的配对对照范式 | 未运行独立模型对照 | 冻结版本、模型、工具、预算、任务和 grader；至少重复运行并报告置信区间、负增益及成本 |
| 异常与恢复 | HAX Playbook、GOV.UK 异常路径指南、OpenSearch 获奖实践 | v0.6 有合成校准记录和行为合约，仍非真实后端 | 加入权限变更、取消、网络中断、持久化和恢复真实路径测试，保持独立 verifier |
| 用户体验 | HEART、GOV.UK 用户研究实践 | 真人研究未执行 | 招募实际目标用户，记录中性任务成功率、错误、耗时、帮助、恢复及同意流程 |
| 无障碍 | WCAG 2.2、Playwright/axe、Testing Library/Storybook 文档 | 仓库含 accessibility 参考；未见完整真人/人工符合性证据 | 自动扫描加人工键盘、焦点、缩放、读屏和包容性用户测试，逐条映射适用成功准则 |
| 竞赛表现 | NandaHack 与 OpenSearch 官方获奖标准和结果 | HumanCraft 未参赛或经外部评审 | 采用冷启动演示、服务可用性、证据闭合与可移植性作为准备项；不推断获奖概率 |

## 本轮覆盖范围与未覆盖领域

已查阅本报告所列 Agent Skills 规范、OpenAI 和 Anthropic 技能指导、Google Gemini CLI 技能文档、Microsoft HAX、SkillsBench、SWE-Skills-Bench、NVIDIA SkillEvaluator、HEART、NN/g 启发式、WCAG 2.2、GOV.UK 用户研究与原型指南、Playwright、Testing Library、Storybook、axe-core，以及两个有官方获奖结果的 Skills 竞赛。

以下事项尚未在本轮核实或运行：

- 未逐项评估至少十个竞争技能的许可、安装体验、源码、模型表现、Token 成本和跨客户端兼容性。
- 未检查 SkillsBench 与 SWE-Skills-Bench 的完整论文方法、全部任务、评分器实现和复现代码，也未独立复跑其结果。SWE-Skills-Bench 此处采用 arXiv v2 摘要信息。
- 未核实 Anthropic Claude Code 黑客松、Google DeepMind/NVIDIA/MIT 其他竞赛的具体获奖项目和完整评分记录。本报告仅纳入检索到官方结果页、明确列出作品和规则的 NandaHack、OpenSearch 两项。
- 未独立运行 NandaHack 或 OpenSearch 获奖仓库，也未从主办方描述之外审计这些项目的代码与评测。
- 未独立评审 HumanCraft 的视觉产物、真实用户任务结果、跨模型技能增益或生产系统数据完整性。
- 未对设计心理学 PDF 作内容引用或版权复核。

## 来源记录

以下链接于 2026-11-24 通过公开网页检索或打开。对会变化的项目文档、论文版本和竞赛结果，访问日期仅说明本次查阅时间，不表示内容永久不变。

| 来源 | 类型与采用内容 |
|---|---|
| [Agent Skills Specification](https://agentskills.io/specification) | 格式规范、元数据和目录结构 |
| [OpenAI Skills API Guide](https://developers.openai.com/api/docs/guides/tools-skills) | Skill 格式、渐进知识、脚本资源及安全边界 |
| [OpenAI Build Skills](https://developers.openai.com/plugins/build/skills) | 工作流边界、辅助文件组织、入口聚焦 |
| [OpenAI Skill Evals](https://developers.openai.com/blog/eval-skills) | 评测迭代与触发设计 |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | 有/无技能评测、留出集和触发正负例 |
| [Gemini CLI Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md) | Google CLI 的技能发现与调用说明 |
| [Gemini CLI Extensions](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/index.md) | 扩展、工具与技能组合形式 |
| [Microsoft HAX Toolkit](https://www.microsoft.com/en-us/haxtoolkit/) | HAX 指南、设计库、工作簿和 Playbook |
| [SkillsBench paper](https://arxiv.org/abs/2602.12670) | 多领域技能对照研究摘要；论文作者报告 |
| [SWE-Skills-Bench v2](https://arxiv.org/abs/2603.15401) | 固定提交、需求、执行验证器和配对结果；预印本摘要 |
| [NVIDIA SkillEvaluator](https://developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator) | 静态、安全、去重、隔离任务对照评估 |
| [Google HEART paper](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36299.pdf) | HEART 类别和 Goals-Signals-Metrics |
| [NN/g usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | 专家审查启发式及适用边界 |
| [GOV.UK user needs](https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs) | 研究用户问题和早期测试假设 |
| [GOV.UK prototyping](https://www.gov.uk/service-manual/design/making-prototypes) | 互动原型和真实交互测试 |
| [GOV.UK usability testing](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing) | 真实参与者、任务、主持式观察 |
| [GOV.UK Design System](https://design-system.service.gov.uk/) | 公共服务组件、模式与指南 |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | 正式推荐标准与成功准则 |
| [Playwright accessibility tests](https://playwright.dev/docs/accessibility-testing) | axe 自动扫描以及人工/包容性测试边界 |
| [Testing Library principles](https://testing-library.com/docs/guiding-principles/) | 从用户可见方式测试组件的原则 |
| [Storybook testing](https://storybook.js.org/docs/writing-tests) | 组件、交互、可访问性测试文档 |
| [axe-core](https://github.com/dequelabs/axe-core) | 自动可访问性检查工具及代码库 |
| [NandaHack results](https://nandahack.media.mit.edu/) | 官方赛事、评测方式与前三名 |
| [OpenSearch Agent Skills Hackathon results](https://opensearch.org/blog/and-the-winners-are-announcing-the-results-of-the-opensearch-agent-skills-hackathon/) | 官方评分权重、前三名与案例说明 |
