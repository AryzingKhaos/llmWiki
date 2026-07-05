---
name: query
description: 当用户提出应基于已编译 wiki 回答的知识问题时使用。先读取仓库中的命令规范，并严格按规范执行。
---

# query

该 skill 的具体执行定义由 [`script/commands/query.md`](../../../script/commands/query.md) 提供。

执行要求：

1. 先阅读 [`script/commands/query.md`](../../../script/commands/query.md)。
2. 将该文件视为权威执行流程。
3. 输入格式必须是 `query [libraryName] [问题]`。
4. 优先使用 `[libraryName]/wiki/`，不要默认读取 `[libraryName]/raw/`。
5. 不得复制、剪切、移动 raw 文件。
6. 如果发现知识缺失，必须写出 `需要创建新 Wiki 页面（New Wiki Page Needed）`。
7. 涉及 wiki 新增或更新建议时，内容必须使用简体中文。
