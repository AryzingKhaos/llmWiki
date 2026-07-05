# batch_lint

目的：

针对指定 library 的 `wiki/sources/` 目录下全部 `sources` 文件，逐个执行 `lint`，完成链接检查与双向链接补充。

命令格式：

- `batch_lint [libraryName]`

示例：

- `batch_lint coreWiki`

输入：

- 一个 `libraryName`

输入要求：

- 必须显式提供 `libraryName`，不能省略。
- 必须只针对 `[libraryName]/wiki/sources/` 目录执行，不得扩展到 `wiki/practice/`、`wiki/query/` 或其他目录。

执行要求：

1. 必须先枚举 `[libraryName]/wiki/sources/` 下的所有 markdown 文件。
2. 必须对枚举到的每一个文件逐个执行完整的 `lint` 流程。
3. 每个文件的检查标准、链接判断标准、双向链接补充方式、输出要求与硬性约束，都必须完全遵循 `script/commands/lint.md`，不得自行简化。
4. 执行 `batch_lint` 时，不得因为是批量处理而跳过对单个目标文件的完整阅读，也不得跳过对候选旧 `sources` 文件的详细阅读。
5. 批量处理过程中，后续文件必须基于前面文件已经产生的最新 `wiki/` 内容继续执行；不得把所有文件都当作彼此隔离的静态快照处理。
6. 如果某个文件检查后无需新增链接，也必须在结果中明确记录该文件已检查但未改动。
7. 如果 `[libraryName]/wiki/sources/` 下没有任何文件，必须明确说明本次没有可执行的目标文件。
8. 检查完成后，应输出本次批量处理过的文件列表，以及每个文件最终新增或未新增链接的结果。

硬性约束：

- 只允许修改 `[libraryName]/wiki/` 下的文件。
- 只允许为了补充双向链接而修改。
- 禁止执行复制、剪切、移动或重命名 raw 文件的操作。
- 不允许伪造问题，也不允许忽略真实结构错误。
- 若判断不充分，必须标注 `Confidence: Low`。
- 涉及实际链接补充时，必须使用简体中文。

输出结果：

- 可能更新的相关 wiki 文件
- 一份简短批量检查结果
