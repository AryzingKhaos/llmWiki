---
name: lint
description: 当用户要求检查 wiki 的结构、链接、命名和元数据时使用。先读取仓库中的命令规范，并严格按规范执行。
---

# lint

该 skill 的具体执行定义由 [`script/commands/lint.md`](../../../script/commands/lint.md) 提供。

执行要求：

1. 先阅读 [`script/commands/lint.md`](../../../script/commands/lint.md)。
2. 将该文件视为权威执行流程。
3. 输入格式必须是 `lint [libraryName]`。
4. `lint` 默认是非破坏性的。
5. 不得复制、剪切、移动 raw 文件。
6. 返回 `Lint Report`。
7. 涉及 wiki 更新建议时，内容必须使用简体中文。
