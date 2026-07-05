# query

目的：

从已编译的 wiki 知识中回答问题，而不是直接复述 raw 材料。

命令格式：

- `query [libraryName] [问题]`

示例：

- `query coreWiki tool calling loop 是什么？`

输入：

- 一个 `libraryName`
- 一个自然语言问题

输入要求：

- 必须显式提供 `libraryName`，不能省略。
- 问题默认在指定的 library 范围内检索与回答。

执行要求：

1. 先识别问题对应的 library 和主题范围。
2. 默认从 `[libraryName]/wiki/` 中检索答案。入口优先读 `index.md` 顶部的 `## 主题索引` 定位相关主题行，再跳转对应条目，不必逐条通读全部 index 条目。
3. 优先读取以下目录中的页面：`[libraryName]/wiki/sources/`、`[libraryName]/wiki/fragment/`。如果查询时发现某个`wiki/sources/`下的wiki文件的某部分内容符合，就需要到对应的raw文件的对应章节中去查看原文，可以根据原文做详细解答
4. 对于  `[libraryName]/wiki/query/` 下的内容，不要做参考
5. 先定位最相关的 wiki 页面。
6. 再沿交叉链接继续读取相关页面。
7. 综合多个 wiki 页面生成结构化回答。
8. 回答时优先引用 wiki 中已经存在的稳定知识。
9. 如果 wiki 中确实不足以回答问题，可以阅读 wiki 中对应的  raw 内容，用更详细的内容解答问题。
10. 如果发现知识缺失，必须明确提出：`需要创建新 Wiki 页面（New Wiki Page Needed）`
11. 如果 query 过程中需要补充或建议新增 wiki 内容，相关内容必须使用简体中文。
12. 如果询问的问题，整个 wiki 都没有直接答案，可以去互联网搜索问题的相关内容。但是分析问题使用的方法论必须是 wiki 内的。


硬性约束：

- 不能把 query 当成 ingest 使用，默认不直接改写 wiki。
- 禁止执行复制、剪切、移动或重命名 raw 文件的操作。
- 不能编造 wiki 中不存在的内容。
- 不能伪造来源或链接。
- 若结论存在不确定性，必须标注 `Confidence: Low`。
- 输出应结构化、清晰、可复用，不要变成闲聊式回答。
- 涉及 wiki 页面名称、页面摘要或新增页面建议时，应使用简体中文表述。

输出结果：

- 一份结构化回答
- 可选的已引用 wiki 页面列表
- 若发现知识空缺，附带 `New Wiki Page Needed` 提示
