目的：
 - 方便之后逐个执行ingest

命令格式：
- `check_uningest [libraryName]`

输入要求：
- 必须显式提供 `libraryName`，不能省略。
- 必须在指定的 library 范围内检索。

执行要求：
- 到`[libraryName]/raw/`文件夹下确认所有的文件（包括所有子文件夹的文件）
- 排除 `*.ocr.md` 文件：它们是 OCR 成品、原始文件的衍生物（见 `ingest.md` 执行要求 16），不是独立资料，不得列入待入库清单
- 对比`[libraryName]/wiki/index.md`，确认是否完成入库
- 对于没有入库的文件，输出列表，写入（新建或覆盖更新）`[libraryName]/wiki/uningest.md`。文件名必须包含双引号，并带上`ingest [libraryName]`，比如`ingest [libraryName] "[文件名]"`。此举是为了方便之后逐个执行ingest。
- **待入库清单不得写入 `index.md`**（index 是全库入口，每个命令都会整个读取它，不能被清单污染）。可在 `index.md` 末尾保留一行指向 `uningest.md` 的链接。




