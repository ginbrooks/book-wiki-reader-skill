#!/usr/bin/env python3
"""Build a portable, offline Book Wiki reader. No server, model, or dependency."""

import argparse
import hashlib
import json
import posixpath
import re
import tempfile
from pathlib import Path
from urllib.parse import unquote

from init_book_wiki import create_chunks, ensure_dirs


REPO = Path(__file__).resolve().parents[1]
KINDS = {"books": "读书笔记", "themes": "主题", "ideas": "想法", "authors": "作者", "reading-plans": "阅读计划"}
PRIVATE_FIELDS = re.compile(r"^\s*(?:-\s*)?(?:Original source|Raw archive|Chunk index|Context stack|Source file|source|raw_archive|chunk_index|context_stack|来源|Raw 归档|分块索引)\s*[:：]", re.I)


def clean_note(text):
    """Remove importer path metadata, not arbitrary reader-authored prose."""
    lines = []
    for line in text.splitlines():
        field = PRIVATE_FIELDS.match(line)
        if field and re.match(r"^(?:/|~[/\\]|[A-Za-z]:[/\\]|file://)", line[field.end():].strip()):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def read_inside(root, path):
    """A symlink must not turn an export into a read outside the chosen Wiki."""
    try:
        path.resolve().relative_to(root)
    except ValueError:
        return None
    return path.read_text(encoding="utf-8-sig")


def title_of(text, fallback):
    for line in text.splitlines():
        if re.match(r"^#{1,3} ", line):
            return line.lstrip("#").strip()
    return fallback


def collect_library(root, demo=False):
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError("Wiki 根目录不存在：" + str(root))
    if not (root / "raw/books").is_dir() and not (root / "wiki").is_dir():
        raise ValueError("目录中未找到 raw/books 或 wiki；请先导入一本书。")
    books = []
    documents = []
    skipped = []

    def read(path):
        try:
            value = read_inside(root, path)
            if value is None:
                skipped.append(path.relative_to(root).as_posix() + "（外部符号链接）")
            return value
        except (OSError, UnicodeError):
            skipped.append(path.relative_to(root).as_posix() + "（不可读 UTF-8 文本）")
            return None

    for book_dir in sorted((root / "raw/books").glob("*")):
        if not book_dir.is_dir():
            continue
        source = read(book_dir / "source.md") if (book_dir / "source.md").is_file() else ""
        source = source or ""
        fields = dict(re.findall(r"^- (Title|Author):[ \t]*(.*)$", source, re.M))
        book = {"id": book_dir.name, "title": fields.get("Title") or book_dir.name,
                "author": fields.get("Author", ""), "chunks": [], "notes": []}
        books.append(book)
        for chunk in sorted((book_dir / "chunks").glob("*.md")):
            text = read(chunk)
            if text is None:
                continue
            text = text.partition("## Text\n\n")[2] or clean_note(text)
            doc_id = chunk.relative_to(root).as_posix()
            document = {"id": doc_id, "book": book["id"], "kind": "原文", "title": title_of(text, "原文 " + str(len(book["chunks"]) + 1)),
                        "text": text.strip(), "references": []}
            documents.append(document)
            book["chunks"].append(doc_id)

    by_book = {book["id"]: book for book in books}
    chunk_ids = {doc_id for book in books for doc_id in book["chunks"]}
    for folder, kind in KINDS.items():
        for path in sorted((root / "wiki" / folder).glob("*.md")):
            text = read(path)
            if text is None:
                continue
            text = clean_note(text)
            book_id = path.stem if folder == "books" and path.stem in by_book else None
            doc_id = path.relative_to(root).as_posix()
            # Resolve only explicitly written Markdown links; never invent evidence.
            references = []
            for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                target = unquote(link.split("#", 1)[0])
                relative = posixpath.normpath(posixpath.join(posixpath.dirname(doc_id), target))
                resolved = target if target in chunk_ids else relative if relative in chunk_ids else None
                if resolved and resolved not in references:
                    references.append(resolved)
            documents.append({"id": doc_id, "book": book_id, "kind": kind,
                              "title": title_of(text, path.stem), "text": text, "references": references})
            if book_id:
                by_book[book_id]["notes"].append(path.relative_to(root).as_posix())

    # Namespace local progress by document identities; exports remain machine-portable.
    identity = "\n".join(document["id"] for document in documents)
    return {"version": 1, "id": hashlib.sha256(identity.encode()).hexdigest()[:16],
            "demo": demo, "books": books, "documents": documents, "skipped": skipped}


def build_html(library):
    template = (REPO / "assets" / "reader.html").read_text(encoding="utf-8")
    # HTML's script parser recognizes closing tags even inside JSON strings.
    payload = json.dumps(library, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return template.replace("__BOOK_WIKI_DATA__", payload)


def make_demo(root):
    """Only original, repository-owned example prose enters the public demo."""
    ensure_dirs(root)
    for slug, source, title in [
        ("reading-note-demo", "reading-note.md", "把笔记写成能回答的问题"),
        ("small-experiment", "small-experiment.md", "把计划变成一个小实验"),
    ]:
        raw = root / "raw/books" / slug
        raw.mkdir(parents=True)
        (raw / "source.md").write_text(f"- Title: {title}\n- Author: Book Wiki Reader 原创示例\n", encoding="utf-8")
        create_chunks(raw, title, REPO / "examples" / source, 420)
    for path in (REPO / "examples" / "demo-notes").glob("*.md"):
        folder = "books" if path.stem == "reading-note-demo" else "themes"
        (root / "wiki" / folder / path.name).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="生成可离线打开的 Book Wiki 阅读工作台；导出的 HTML 包含原文与笔记。")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--root", type=Path, help="本地 Book Wiki 根目录")
    source.add_argument("--demo", action="store_true", help="仅使用仓库自带原创示例")
    parser.add_argument("--output", type=Path, required=True, help="生成的单文件 HTML 路径")
    args = parser.parse_args()
    try:
        if args.demo:
            with tempfile.TemporaryDirectory() as folder:
                make_demo(Path(folder))
                library = collect_library(Path(folder), demo=True)
        else:
            library = collect_library(args.root)
        output = args.output.expanduser().resolve()
        if output.suffix.lower() not in {".html", ".htm"}:
            parser.error("--output 必须是 .html 或 .htm 文件，以免覆盖笔记。")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(build_html(library), encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"已生成 {output}\n{len(library['books'])} 本读物 · {len(library['documents'])} 篇原文与笔记")
    print("双击 HTML 即可使用，无需联网。文件包含导出的正文，公开前请检查内容。")
    if library["skipped"]:
        print("跳过：" + "、".join(library["skipped"]))


if __name__ == "__main__":
    main()
