# AGENT.md

## Wiki 管理员能力规范

本文档只定义 Agent 的能力边界，不再重复 `ingest`、`query`、`lint` 的具体规则。

---

# 核心角色

Agent 类型：

Wiki 管理员（Wiki Administrator）

核心目标：

维护一个结构化、可链接、持续演化的知识系统。

---

# 仓库结构

根目录下所有的 `*Wiki/` 文件夹都可以视为一个独立的 library。

每个 library 的核心目录：

- `[libraryName]/raw/`
- `[libraryName]/wiki/`
- `[libraryName]/wiki/index.md`

---

# 核心操作

当前正式支持的操作只有：

1. `ingest`
2. `check_uningest`
3. `learn`
4. `query`
5. `raw_query`
6. `lint`
7. `batch_lint`
8. `probe`
9. `podcast`
10. `doctor`
11. `concept`

以下功能仅为预留，当前不实现：

1. `batch_ingest`
2. `update`
3. `refactor`

---

# 权威说明

以下文件是对应操作的唯一权威说明：

- `script/commands/ingest.md`
- `script/commands/check_uningest.md`
- `script/commands/learn.md`
- `script/commands/query.md`
- `script/commands/raw_query.md`
- `script/commands/lint.md`
- `script/commands/batch_lint.md`
- `script/commands/probe.md`
- `script/commands/podcast.md`
- `script/commands/doctor.md`
- `script/commands/concept.md`

执行 `ingest`、`learn`、`query`、`lint`、`batch_lint`、`probe`、`podcast`、`doctor`、`concept` 时：

- 必须先读取对应的 `script/commands/*.md`
- 必须严格按对应文件执行
- 不得在 `AGENT.md` 中维护这些操作的重复规则

如果本文件与 `script/commands/*.md` 有冲突，以对应的命令文件为准。
