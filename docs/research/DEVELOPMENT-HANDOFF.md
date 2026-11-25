---
name: humancraft-development-handoff
description: 完整源码恢复记录、双基线和当前开发分支。
---

# 开发交接

| 对象 | 历史定位 |
| --- | --- |
| 完整 v0.6.0 源码 | `22077c0971d512eb5eb5fdfe5f2d3da44d8d2a15`，原有 408 项 |
| GitHub 公开导入 | `1d60e54099873ba0cb56b40c16d7b8f15689f3bf`，原有 30 项 |
| 合并恢复 | `cabc9ae8ce22f170f02d964b2027e1124fa1538c`，保留两父提交，融合两份 README |
| 图标 | `6055ebad1d5a682b5812345a8f1b8baecdb51c90`，原 PNG 在中英文 README 可见 |

原两条历史通过本地 `backup/v0.6.0-full` 和 `backup/v0.6.0-public-import` 保留。候选工作在 `feature/evidence-benchmark`。需要复现稳定基线时使用上表提交或从核验过的 Bundle 建新工作区。回滚公开变更采用新增还原提交并保留历史。

本地验证命令参见 [快速开始](../../README.zh-CN.md) 与 [原始评测协议](../../bench/README.md)。最后核验于 2026-11-25（香港时间）。
