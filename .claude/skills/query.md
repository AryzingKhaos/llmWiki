---
name: query
description: 基于已编译的 wiki 回答问题，而不是直接使用 raw 材料。当用户询问知识库中的内容时使用。
user_invocable: true
---

# query

使用该 skill 时，将 [`script/commands/query.md`](../../script/commands/query.md) 视为唯一权威说明。

必须遵循：

1. 执行前先阅读 [`script/commands/query.md`](../../script/commands/query.md)。
2. 严格按照该文件中的流程与约束执行。
3. 输入格式必须是 `query [libraryName] [问题]`。
4. 优先使用 `[libraryName]/wiki/`，不要默认读取 `[libraryName]/raw/`。
5. 不得复制、剪切、移动 raw 文件。
6. 如果发现知识缺失，必须明确写出 `需要创建新 Wiki 页面（New Wiki Page Needed）`。
7. 涉及 wiki 新增或更新建议时，内容必须使用简体中文。
