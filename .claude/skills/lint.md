---
name: lint
description: 检查 wiki 的结构完整性并输出知识库问题报告。当用户要求 lint、审计或检查断链、重复页面、孤立页面或元数据问题时使用。
user_invocable: true
---

# lint

使用该 skill 时，将 [`script/commands/lint.md`](../../script/commands/lint.md) 视为唯一权威说明。

必须遵循：

1. 执行前先阅读 [`script/commands/lint.md`](../../script/commands/lint.md)。
2. 严格按照该文件中的流程与约束执行。
3. 输入格式必须是 `lint [libraryName]`。
4. `lint` 默认是非破坏性的。
5. 不得复制、剪切、移动 raw 文件。
6. 输出 `Lint Report`，不要静默修改页面。
7. 涉及 wiki 更新建议时，内容必须使用简体中文。
