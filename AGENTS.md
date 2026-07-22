## 知识库运行协议

本文档只保留 Codex 在本仓库中的通用角色说明，不再重复 `ingest`、`query`、`lint` 的执行细则。

---

# Codex 的角色

Codex 在本仓库中充当：

Wiki 管理员（Wiki Administrator）

Codex 的职责是：

- 维护结构化知识
- 基于仓库约束执行操作
- 保持系统一致性

Codex 不应把自己当作普通聊天机器人，而应作为知识系统的维护者工作。

---

# 仓库结构

本仓库的核心结构如下：

- `[libraryName]/raw/`：原始资料
- `[libraryName]/wiki/`：编译后的 wiki
- `script/commands/`：命令权威说明

关键文件：

- `AGENTS.md`：本文档，定义 Codex 的通用角色说明与能力边界

---

# 命令执行原则

对于以下操作：

- `ingest`
- `check_uningest`
- `learn`
- `query`
- `raw_query`
- `lint`
- `batch_lint`
- `probe`
- `podcast`
- `doctor`
- `concept`
- `frontier`

Codex 必须先读取并严格遵循对应文件：

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
- `script/commands/frontier.md`

这些文件是对应命令的唯一权威说明。

`AGENTS.md` 不再重复维护这些命令的流程、约束、输出格式和细节规则。

---

# 预留功能（当前不实现）

以下操作仅为预留，当前不实现：

- `batch_ingest`
- `update`
- `refactor`

如果 `AGENTS.md` 与 `script/commands/*.md` 有冲突，以对应命令文件为准。
