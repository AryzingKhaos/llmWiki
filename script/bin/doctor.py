#!/usr/bin/env python3
"""doctor — llmWikis 全仓确定性体检脚本。

用法：
    python3 script/bin/doctor.py            # 体检所有 *Wiki 库
    python3 script/bin/doctor.py investWiki # 只体检指定库

检查项（全部确定性，零 LLM）：
  [E] 库结构：*Wiki 缺 wiki/ 或 wiki/index.md
  [E] 死链：index.md 与 wiki/**/*.md 中相对 md 链接的目标文件不存在
  [W] 锚点失效：链接 #锚点 在目标文件中找不到对应标题（宽容匹配后仍不中）
  [E] 标题空格：wiki/sources/*.md 各级标题内容含空格/Tab/全角空格（违反 ingest 硬约束）
  [W] 未登记：wiki/sources/*.md 存在但 index.md 中无对应链接
  [W] 摘要超长：index.md 简短摘要 >100 字（违反 ingest 索引规范 2026-07-03 修订版）
  [W] 索引污染：index.md 中残留 check_uningest 的待入库清单（`ingest xxx "..."` 行）
  [W] 缺 Source Path：wiki/sources/*.md 中无 `Source Path:` 字段
  [W] 孤儿页：wiki/sources|concepts/*.md 除索引文件外无任何入链（Karpathy lint 的 orphan pages）

退出码：有 [E] 级问题时为 1，否则 0。
"""

import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parent.parent.parent

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
SUMMARY_RE = re.compile(r"^-\s*[`]?简短摘要[：:]\s*(.*)$")
INGEST_LINE_RE = re.compile(r"ingest\s+\S+\s+\"")
SPACE_CHARS = (" ", "\t", "　")

issues = []  # (severity, library, message)


def add(sev, lib, msg):
    issues.append((sev, lib, msg))


def iter_md_lines(path):
    """逐行读取 md，跳过 fenced code block 内部。yield (lineno, line)"""
    in_fence = False
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        yield from ()
        return
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield i, line


def normalize_anchor(s):
    """宽容归一：小写 + 只保留字母数字（含 CJK），用于锚点与标题的比对。"""
    s = unquote(s)
    s = unicodedata.normalize("NFKC", s)
    return "".join(c for c in s.lower() if c.isalnum())


def headings_of(path, cache={}):
    if path not in cache:
        hs = []
        for _, line in iter_md_lines(path):
            m = HEADING_RE.match(line)
            if m:
                hs.append(m.group(2))
        # 也兼容"## 标题内容无前导空格之外的写法"：`##标题` 极少见，不解析
        cache[path] = hs
    return cache[path]


def extract_links(line):
    """返回 [(target, anchor)]，剔除外链/绝对路径/纯锚点。"""
    out = []
    for _, raw in LINK_RE.findall(line):
        target = raw.strip().split(" ")[0]  # 去掉可选的 "title"
        if target.startswith(("http://", "https://", "mailto:", "/")):
            continue
        if target.startswith("#"):
            continue  # 文档内锚点，暂不检
        if "#" in target:
            file_part, anchor = target.split("#", 1)
        else:
            file_part, anchor = target, ""
        if not file_part.endswith(".md"):
            continue
        out.append((unquote(file_part), anchor))
    return out


def check_links_in_file(lib, md_file, base_dir):
    for lineno, line in iter_md_lines(md_file):
        for file_part, anchor in extract_links(line):
            target = (base_dir / file_part).resolve()
            rel = md_file.relative_to(REPO)
            if not target.exists():
                add("E", lib, f"死链 {rel}:{lineno} → {file_part}")
                continue
            if anchor:
                want = normalize_anchor(anchor)
                if want and not any(
                    normalize_anchor(h) == want for h in headings_of(target)
                ):
                    add("W", lib, f"锚点失效 {rel}:{lineno} → {file_part}#{unquote(anchor)}")


def check_library(lib_dir):
    lib = lib_dir.name
    wiki = lib_dir / "wiki"
    index = wiki / "index.md"
    raw = lib_dir / "raw"

    if not wiki.is_dir():
        add("E", lib, "缺 wiki/ 目录")
        return
    if not index.is_file():
        add("E", lib, "缺 wiki/index.md")
        return

    sources_dir = wiki / "sources"
    source_files = sorted(sources_dir.glob("*.md")) if sources_dir.is_dir() else []

    # --- index.md 检查 ---
    linked_targets = set()
    for lineno, line in iter_md_lines(index):
        # 死链 + 收集已登记的 sources
        for file_part, anchor in extract_links(line):
            target = (wiki / file_part).resolve()
            if target.exists():
                linked_targets.add(target)
            else:
                add("E", lib, f"死链 wiki/index.md:{lineno} → {file_part}")
        # 摘要超长
        m = SUMMARY_RE.match(line.strip())
        if m:
            content = m.group(1).strip().strip("`")
            if len(content) > 100:
                title = content[:24]
                add("W", lib, f"摘要超长 index.md:{lineno}（{len(content)}字 >100）：{title}…")
        # 索引污染（待入库清单）
        if INGEST_LINE_RE.search(line):
            add("W", lib, f"索引污染 index.md:{lineno}：残留待入库清单行，应移至 wiki/uningest.md")

    # 未登记的 sources
    for f in source_files:
        if f.resolve() not in linked_targets:
            add("W", lib, f"未登记 index.md 缺条目：sources/{f.name}")

    # --- sources/*.md 检查 ---
    for f in source_files:
        text_has_source_path = False
        for lineno, line in iter_md_lines(f):
            m = HEADING_RE.match(line)
            if m and any(ch in m.group(2) for ch in SPACE_CHARS):
                add("E", lib, f"标题含空格 sources/{f.name}:{lineno}：{m.group(2)[:40]}")
            if "Source Path" in line:
                text_has_source_path = True
        if not text_has_source_path:
            add("W", lib, f"缺 Source Path：sources/{f.name}")
        check_links_in_file(lib, f, f.parent)

    # 其余 wiki 子目录只做死链/锚点检查
    for sub in ("fragment", "query", "practice", "concepts"):
        d = wiki / sub
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                check_links_in_file(lib, f, f.parent)

    # --- 孤儿页检查：sources/concepts 页除索引文件外无任何入链 ---
    inbound = set()
    for f in wiki.rglob("*.md"):
        if f.name == "index.md":  # wiki/index.md 与 concepts/index.md 均为索引，不算入链
            continue
        for _, line in iter_md_lines(f):
            for file_part, _ in extract_links(line):
                t = (f.parent / file_part).resolve()
                if t.exists() and t != f.resolve():
                    inbound.add(t)
    for sub in ("sources", "concepts"):
        d = wiki / sub
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                if f.name == "index.md":
                    continue
                if f.resolve() not in inbound:
                    add("W", lib, f"孤儿页 {sub}/{f.name}：除索引外无任何入链")

    # --- 概览统计 ---
    n_raw = sum(1 for p in raw.rglob("*") if p.is_file()) if raw.is_dir() else 0
    print(f"  {lib}: raw={n_raw} sources={len(source_files)} index={index.stat().st_size // 1024}KB")


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    libs = sorted(p for p in REPO.iterdir() if p.is_dir() and p.name.endswith("Wiki"))
    if only:
        libs = [p for p in libs if p.name == only]
        if not libs:
            print(f"未找到库：{only}")
            return 1

    print("== 库概览 ==")
    for lib_dir in libs:
        check_library(lib_dir)

    errors = [i for i in issues if i[0] == "E"]
    warns = [i for i in issues if i[0] == "W"]

    for title, group in (("== 错误（E）==", errors), ("== 警告（W）==", warns)):
        print(f"\n{title} 共{len(group)}项")
        for _, lib, msg in group:
            print(f"  [{lib}] {msg}")

    print(f"\n体检完成：{len(errors)} 错误，{len(warns)} 警告。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
