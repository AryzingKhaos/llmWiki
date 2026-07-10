# doctor

目的：

对全仓（或指定 library）做**确定性体检**，发现结构缺失、死链、锚点失效、格式违规与索引污染。本命令由脚本执行，不消耗 LLM 阅读全库；Claude 只负责调用脚本并解读结果。

命令格式：

- `doctor`（体检所有 `*Wiki` 库）
- `doctor [libraryName]`（只体检指定库）

执行方式：

```
python3 script/bin/doctor.py [libraryName]
```

检查项：

| 级别 | 检查 | 对应规范来源 |
|---|---|---|
| E | 库缺 `wiki/` 目录或 `wiki/index.md` | AGENT.md 仓库结构 |
| E | `index.md` 与 `wiki/**/*.md` 中相对 md 链接目标文件不存在（死链） | lint |
| E | `wiki/sources/*.md` 各级标题内容含空格/Tab/全角空格 | ingest 硬性约束 |
| W | 链接 `#锚点` 在目标文件中找不到对应二级标题（宽容归一匹配后仍不中） | lint 锚点规范 |
| W | `wiki/sources/*.md` 存在但 `index.md` 无对应条目（未登记） | ingest 索引规范 |
| W | `index.md` 简短摘要超过 100 字 | ingest Index 格式说明（2026-07-03 修订：一律 ≤100 字） |
| W | `index.md` 残留 `ingest xxx "..."` 待入库清单行（索引污染） | — |
| W | `wiki/sources/*.md` 缺 `Source Path:` 字段 | ingest 执行要求 7 |
| W | 孤儿页：`wiki/sources|concepts/*.md` 除索引文件外无任何入链 | Karpathy lint（orphan pages） |

执行要求：

1. 直接运行脚本，将输出如实呈现给用户（可归纳同类项，但不得隐瞒任何 E 级问题）。
2. 「锚点失效」项特别值得人工跟进：实践中它多次暴露出**长文多 subagent 压缩汇总时丢失整个模块**的事故（如二级标题序列 G→I 缺 H），这不是链接写错，而是内容缺失。解读时必须区分这两种情况：
	- 链接一侧写错（部/章号笔误等）→ 修链接即可
	- 目标模块整体缺失 → 提示用户需要对该 source 重新执行 ingest 补齐模块
3. doctor 本身**不做任何修改**。修复动作需用户确认后另行执行，且修复方式必须遵循对应命令的规范（改链接遵循 lint、补内容遵循 ingest）。
4. 建议的执行时机：每次 ingest / batch_lint 之后；或定期全仓巡检。

硬性约束：

- doctor 只读，不修改任何文件。
- 不得因批量输出而省略 E 级问题。
- 修复建议必须区分「链接错误」与「内容缺失」两类，不得一律当作链接问题处理。
- 禁止执行复制、剪切、移动或重命名 raw 文件的操作。

输出结果：

- 库概览（raw/sources 数量、index 体积）
- E 级错误列表与 W 级警告列表
- 一份简短解读：问题归类、建议的修复顺序
