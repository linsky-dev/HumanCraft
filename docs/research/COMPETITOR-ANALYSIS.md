---
name: humancraft-competitor-analysis
description: 基于官方公开资料梳理 HumanCraft 的设计技能、设计系统与验证工具对照对象，并标记尚未实测的指标。
---

# HumanCraft 竞品与相邻工具分析

访问日期：2026-11-24

## 范围与判读方式

本清单包含可直接比较的 Agent Skills，也包含设计规范、生成式设计产品和验证工具。不同产品形态解决的问题不同，表中“公开覆盖”仅表示其官方资料明确描述了相关能力，不表示本项目已独立运行或验证这些能力。公开宣传、规则数量、下载量和项目受欢迎程度均不作为效果证据。

截至访问日期，以下工具的任务完成率、用户认知负担变化、视觉质量提升幅度、触发准确率、跨模型增益、Token 消耗和运行时间均未在统一条件下实测。相关指标统一标为“未测”。本轮未执行竞品安装、模型调用或用户测试。

## 对照对象

| 项目 | 产品形态 | 官方资料明确覆盖的能力 | 与 HumanCraft 的主要比较面 | 证据与限制 |
|---|---|---|---|---|
| UI UX Pro Max | Agent Skill 与本地搜索脚本 | 描述了按行业、风格、配色、页面模式、字体和技术栈检索设计建议的流程，并提供交付清单 | 视觉方向、设计系统生成、知识检索、脚本辅助 | 上游 README 与模板说明这些能力。其 README 描述的目录数量属于项目自述，不代表质量或增益已被独立验证。[上游仓库](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| Anthropic frontend-design | Agent Skill | 官方技能仓库提供面向前端设计与实现的技能入口 | 视觉质量、设计指导、前端交付流程 | 本次浏览器检索无法直接读取该目录的完整源码，需在进一步比较前固定仓库提交并复核实际文件。[上游技能目录](https://github.com/anthropics/skills/tree/main/skills/frontend-design) |
| Vercel React Best Practices | Agent Skill | React 与 Next.js 性能规则按类别和影响优先级组织，包含具体实现示例 | 前端工程、性能、规则可执行性 | 官方目录和规则文件描述其覆盖范围，不提供与 HumanCraft 同任务的独立用户价值对照。[官方技能目录](https://vercel.com/docs/agent-resources/skills)、[规则文件](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices) |
| OpenAI frontend-app-builder | Agent Skill | 面向新建或改造前端应用，包含视觉概念、实现、浏览器检查与响应式要求 | 视觉设计、工程实现、浏览器验证 | 上游技能要求使用图像生成形成设计概念。比较时应记录此依赖及其带来的额外时间和资源开销。[技能文件](https://github.com/openai/plugins/blob/main/plugins/build-web-apps/skills/frontend-app-builder/SKILL.md) |
| Google Stitch | 生成式设计产品 | Google Labs 将其描述为以自然语言创建、迭代高保真 UI 的 AI 设计画布 | 视觉探索、原型生成、设计迭代 | 它是设计产品，不是 Agent Skill。其产品介绍不能证明生成结果适用于真实工作流或优于其他组。[Google Labs 介绍](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/)、[产品页](https://stitch.withgoogle.com/) |
| Microsoft HAX Toolkit | 人机交互指南与工作坊工具 | 18 条人机交互指南，以及设计库、工作簿和 Playbook，涵盖初始交互、运行中、系统出错时和长期使用 | AI 自动化控制、失败恢复、团队需求规划 | 微软将指南描述为基于研究的实践资料。本清单未复核原始研究，也未评价其对当前模型输出的直接效果。[交互指南](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/)、[工具包](https://www.microsoft.com/en-us/haxtoolkit/) |
| GOV.UK Design System | 设计系统与组件库 | 提供组件、使用指导、代码示例和常见任务模式，聚焦政府服务 | 复杂表单、错误提示、流程模式、可复用组件 | 适用范围与 GOV.UK 服务相关。其模式应按产品和用户情境评估，不能无条件套用到其他领域。[组件](https://design-system.service.gov.uk/components/)、[设计系统](https://design-system.service.gov.uk/) |
| Playwright | 浏览器 E2E 测试框架 | 支持 Chromium、Firefox、WebKit，提供隔离测试、并发执行、断言、报告及调试工具 | 真实浏览器行为、关键流程验收、跨浏览器回归 | 是工程验证基础设施，不负责设计决策或用户体验评分。[官方文档](https://playwright.dev/docs/intro) |
| Playwright + axe-core | 浏览器无障碍自动化检查 | 可将 axe 扫描接入 Playwright 测试，检查部分可自动发现的无障碍问题 | 无障碍门禁、重复运行、缺陷回归 | Playwright 文档明确指出自动化只能发现部分问题，仍需人工检查及包容性用户测试。[无障碍测试指南](https://playwright.dev/docs/accessibility-testing) |
| Storybook Accessibility addon | 组件开发与测试插件 | 基于 axe-core 检查组件，并可与 Vitest 测试集成 | 组件级无障碍检查、组件状态验证 | 适合组件层反馈，不等于完成任务路径的无障碍验证。[Storybook 文档](https://storybook.js.org/docs/writing-tests/accessibility-testing/) |
| Deque axe | 无障碍规则引擎与测试产品 | 提供自动扫描、辅助式检查和人工测试工具，支持在测试中调用 axe-core | 缺陷扫描、无障碍测试流程 | Deque 明确区分自动、半自动和人工测试。单次自动扫描不能证明符合全部 WCAG 要求。[axe 产品说明](https://www.deque.com/axe/) |

## 能力覆盖矩阵

符号只描述官方资料中可见的功能范围。`有` 表示文档明确提供相关能力或工具，`部分` 表示覆盖面较窄或属于配套工具，`—` 表示该项目类型或已查资料没有足够依据。它不代表能力强弱或测试结果。

| 项目 | 视觉生成或指导 | 功能与交互设计 | 复杂工作流与恢复 | 前端工程 | 浏览器或自动测试 | 无障碍工具 | 真人用户证据 |
|---|---|---|---|---|---|---|---|
| UI UX Pro Max | 有 | 部分 | — | 部分 | — | 部分 | 未测 |
| Anthropic frontend-design | 有 | 部分 | — | 有 | — | 未测 | 未测 |
| Vercel React Best Practices | — | — | — | 有 | — | — | 未测 |
| OpenAI frontend-app-builder | 有 | 部分 | — | 有 | 有 | 部分 | 未测 |
| Google Stitch | 有 | 部分 | 未知 | 部分 | 未知 | 未知 | 未测 |
| Microsoft HAX Toolkit | — | 有 | 有 | — | — | — | 未测 |
| GOV.UK Design System | — | 有 | 部分 | 有 | — | 部分 | 未测 |
| Playwright | — | — | 部分 | — | 有 | 部分 | — |
| Playwright + axe-core | — | — | — | — | 有 | 有 | — |
| Storybook Accessibility addon | — | — | — | 部分 | 有 | 有 | — |
| Deque axe | — | — | — | — | 有 | 有 | — |

HumanCraft 当前对应维度也应标为“未测”，直到在预注册实验、冻结任务、相同模型和工具预算下获得结果。已有测试夹具通过只能说明代码和验收程序按预期运行，不能代替技能增益、真实用户价值或真人研究结论。

## 统一实测指标

本轮没有产生可用于竞品排名的实测数据。后续如执行对照，建议至少记录以下字段，并保留每次运行的原始日志和失败状态：

| 指标 | 当前值 |
|---|---|
| 任务通过率及相对无技能基线的绝对百分点差 | 未测 |
| 任务级严重缺陷数及新增严重缺陷率 | 未测 |
| 功能发现、任务完成时间、错误次数与恢复成功率 | 未测 |
| 盲评视觉质量及评价者间一致性 | 未测 |
| 无障碍自动检查结果与人工检查结果 | 未测 |
| Skill 触发准确率和召回率 | 未测 |
| Token 中位数、执行时间中位数和调用成本 | 未测 |
| 按任务类型和模型生态分层的正、零、负增益 | 未测 |
| 安装成功率、首次可用时间和离线可用性 | 未测 |

## 后续比较边界

需要进行实际竞品运行时，应先固定各项目的版本、许可证、依赖、运行命令和来源哈希。实验组采用相同任务、初始代码、模型版本、工具权限、时间和 token 预算，工作区独立。无法按同一条件运行的结果应分层报告，不得直接合并成排名。真人偏好、可用性或信任结论需要真实参与者和适当知情同意，自动化或 AI 评审不能替代。
