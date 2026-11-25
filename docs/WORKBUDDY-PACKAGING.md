---
name: workbuddy-packaging
description: HumanCraft WorkBuddy 技能包的构建、元数据来源和验证说明。
---

# WorkBuddy 技能包

构建标准 Agent Skills 包、WorkBuddy 技能包、完整源码包及 SHA-256 清单：

```powershell
python scripts/package.py --output dist
```

输出包括 `HumanCraft-v0.6.1-skill.zip`、`HumanCraft-v0.6.1-WorkBuddy.zip`、`HumanCraft-v0.6.1-full.zip` 和 `SHA256SUMS.txt`。版本从 `skills/humancraft/SKILL.md` 的 `metadata.version` 读取，并写入 WorkBuddy 包顶层 `version` 字段，避免维护重复版本号。

标准包保留原始技能目录及其文件内容。WorkBuddy 包保留相同文件树，只在包内 `humancraft/SKILL.md` 的 YAML frontmatter 增加 WorkBuddy 元数据。技能 Markdown 正文和其他文件均逐字节保持一致。中文展示名及中英文介绍取自原始验证交接文件的 `workbuddy_extension` 对象，副本保存在 `scripts/workbuddy-extension.json` 以保证干净检出后仍可复现。

腾讯 WorkBuddy 技能文档描述了技能包基础目录和 frontmatter 字段。原始交接元数据未提供 `author`，默认构建会保留来源字段并省略作者，不宣称可直接通过开放平台元数据校验。官方技能文档将 `author` 列为必填。维护者确认作者后，可通过 `--workbuddy-author` 为 WorkBuddy 包补充该字段，标准技能包和完整源码包保持不变。未在 WorkBuddy 客户端实际导入验证。[WorkBuddy 技能包格式](https://open.workbuddy.cn/docs/skill)，访问日期：2026-11-25。

```powershell
python scripts/package.py --output dist --workbuddy-author "维护者名称"
```

完整开发包包含项目根目录 `assets/` 中通过文件类型门禁的公开资产，例如 `assets/humancraft-avatar.png`。标准技能包不包含根目录品牌资产。

打包回归测试：

```powershell
python -m unittest discover -s tests -p test_package.py -v
```

产品目录和 WorkBuddy 官方文档可能更新。打包器只验证 ZIP 完整性、版本一致性、文件集合和校验和，不代表客户端兼容认证或市场审核通过。
