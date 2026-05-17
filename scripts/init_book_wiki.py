#!/usr/bin/env python3
import argparse
import datetime as dt
import re
import shutil
from pathlib import Path


DEFAULT_ROOT = Path("/Users/shu/Documents/Book-Wiki")
DEFAULT_CHUNK_SIZE = 8000
TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".text"}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-_")
    return value or "untitled-book"


def read_template(skill_dir: Path, name: str) -> str:
    return (skill_dir / "assets" / "templates" / name).read_text(encoding="utf-8")


def fill_template(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def ensure_dirs(root: Path) -> None:
    for rel in [
        "raw/books",
        "raw/inbox",
        "wiki/books",
        "wiki/themes",
        "wiki/ideas",
        "wiki/authors",
        "wiki/reading-plans",
        "templates",
    ]:
        (root / rel).mkdir(parents=True, exist_ok=True)


def copy_templates(skill_dir: Path, root: Path) -> None:
    source_dir = skill_dir / "assets" / "templates"
    target_dir = root / "templates"
    for item in source_dir.glob("*.md"):
        target = target_dir / item.name
        if not target.exists():
            shutil.copy2(item, target)


def read_text_file(path: Path) -> str:
    for encoding in ["utf-8", "utf-8-sig", "gb18030", "latin-1"]:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def split_long_paragraph(paragraph: str, max_chars: int) -> list[str]:
    parts = []
    text = paragraph.strip()
    while len(text) > max_chars:
        cut = text.rfind("。", 0, max_chars)
        if cut < max_chars // 2:
            cut = text.rfind(".", 0, max_chars)
        if cut < max_chars // 2:
            cut = max_chars
        parts.append(text[: cut + 1].strip())
        text = text[cut + 1 :].strip()
    if text:
        parts.append(text)
    return parts


def chunk_text(text: str, max_chars: int) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = []
    current = []
    current_len = 0

    for paragraph in paragraphs:
        paragraph_parts = split_long_paragraph(paragraph, max_chars)
        for part in paragraph_parts:
            part_len = len(part)
            if current and current_len + part_len + 2 > max_chars:
                chunks.append("\n\n".join(current))
                current = []
                current_len = 0
            current.append(part)
            current_len += part_len + 2

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def first_line(text: str) -> str:
    for line in text.splitlines():
        clean = line.strip().lstrip("#").strip()
        if clean:
            return clean[:80]
    return ""


def create_chunks(raw_dir: Path, title: str, source_path: Path, chunk_size: int) -> tuple[int, str]:
    if source_path.suffix.lower() not in TEXT_EXTENSIONS:
        return 0, "非纯文本文件，未自动分块。请先转换为 txt 或 md 后再导入。"

    chunks_dir = raw_dir / "chunks"
    index_path = raw_dir / "chunk-index.md"
    if index_path.exists() and chunks_dir.exists():
        existing = sorted(chunks_dir.glob("chunk-*.md"))
        return len(existing), "分块已存在，未重复生成。"

    text = read_text_file(source_path)
    chunks = chunk_text(text, chunk_size)
    chunks_dir.mkdir(parents=True, exist_ok=True)

    index_lines = [
        f"# Chunk Index: {title}",
        "",
        f"- Source file: {source_path}",
        f"- Chunk size target: {chunk_size} characters",
        f"- Total chunks: {len(chunks)}",
        "",
        "## Chunks",
        "",
    ]

    for idx, chunk in enumerate(chunks, start=1):
        filename = f"chunk-{idx:04d}.md"
        chunk_path = chunks_dir / filename
        heading = first_line(chunk)
        chunk_path.write_text(
            "\n".join(
                [
                    f"# {title} - Chunk {idx:04d}",
                    "",
                    f"- Source file: {source_path}",
                    f"- Chunk: {idx}/{len(chunks)}",
                    "",
                    "## Text",
                    "",
                    chunk,
                    "",
                ]
            ),
            encoding="utf-8",
        )
        index_lines.append(f"- `{filename}` ({len(chunk)} chars): {heading}")

    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return len(chunks), f"已生成 {len(chunks)} 个分块。"


def create_stack_files(raw_dir: Path, title: str) -> None:
    stack_dir = raw_dir / "stack"
    stack_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "book-skeleton.md": [
            f"# Book Skeleton: {title}",
            "",
            "## 骨架状态",
            "",
            "- 类型：初版骨架 / 校准骨架 / 修订骨架",
            "- 生成依据：快速检视 / 全书索引 / 共读修订",
            "- 可信度说明：",
            "",
            "## 全书核心问题",
            "",
            "## 作者主线",
            "",
            "## 主要观点",
            "",
            "## 论证路线",
            "",
            "## 关键例子",
            "",
            "## 薄弱点和疑问",
            "",
            "## 和读者相关的资产",
            "",
        ],
        "section-summaries.md": [
            f"# Section Summaries: {title}",
            "",
            "每个部分读完后更新：它解决什么问题、作者答案、论证路线、关键例子、可跳读内容。",
            "",
        ],
        "unit-summaries.md": [
            f"# Unit Summaries: {title}",
            "",
            "每个问题块、观点块、论证块或方法块读完后更新。",
            "",
        ],
        "chunk-summaries.md": [
            f"# Chunk Summaries: {title}",
            "",
            "按 chunk 记录 5-10 条压缩要点、关键词、例子和可回溯位置。",
            "",
        ],
        "reader-memory.md": [
            f"# Reader Memory: {title}",
            "",
            "## 阅读意图",
            "",
            "## 用户已确认观点",
            "",
            "## 用户不同意或保留判断",
            "",
            "## 未来要调用的想法",
            "",
        ],
    }
    for filename, lines in files.items():
        path = stack_dir / filename
        if not path.exists():
            path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a Book Wiki entry for a local book file.")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="Book Wiki root directory")
    parser.add_argument("--source", help="Local book file path to archive")
    parser.add_argument("--title", help="Book title")
    parser.add_argument("--author", default="", help="Book author")
    parser.add_argument("--slug", help="Optional slug override")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help="Target characters per text chunk")
    parser.add_argument("--no-chunks", action="store_true", help="Archive only; do not create chunk files")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    root = Path(args.root).expanduser().resolve()
    ensure_dirs(root)
    copy_templates(skill_dir, root)

    source_path = Path(args.source).expanduser().resolve() if args.source else None
    inferred_title = source_path.stem if source_path else "Untitled Book"
    title = args.title or inferred_title
    author = args.author or ""
    slug = args.slug or slugify(title)
    today = dt.date.today().isoformat()

    raw_dir = root / "raw" / "books" / slug
    original_dir = raw_dir / "original"
    original_dir.mkdir(parents=True, exist_ok=True)
    create_stack_files(raw_dir, title)

    archived_source = ""
    chunk_count = 0
    chunk_note = "没有提供可分块的本地文本。"
    if source_path:
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        target = original_dir / source_path.name
        if not target.exists():
            shutil.copy2(source_path, target)
        archived_source = str(target)
        if not args.no_chunks:
            chunk_count, chunk_note = create_chunks(raw_dir, title, target, args.chunk_size)

    source_md = raw_dir / "source.md"
    if not source_md.exists():
        source_md.write_text(
            "\n".join(
                [
                    f"# Source: {title}",
                    "",
                    f"- Title: {title}",
                    f"- Author: {author}",
                    f"- Imported: {today}",
                    f"- Original source: {source_path or ''}",
                    f"- Raw archive: {archived_source}",
                    f"- Chunk index: {raw_dir / 'chunk-index.md' if chunk_count else ''}",
                    f"- Chunk count: {chunk_count}",
                    f"- Chunk note: {chunk_note}",
                    f"- Context stack: {raw_dir / 'stack'}",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    book_note = root / "wiki" / "books" / f"{slug}.md"
    if not book_note.exists():
        template = read_template(skill_dir, "book-note.md")
        book_note.write_text(
            fill_template(
                template,
                {
                    "title": title,
                    "author": author,
                    "source": str(source_path or ""),
                    "raw_archive": str(raw_dir),
                    "chunk_index": str(raw_dir / "chunk-index.md") if chunk_count else "",
                    "context_stack": str(raw_dir / "stack"),
                    "date": today,
                },
            ),
            encoding="utf-8",
        )

    print(f"root={root}")
    print(f"slug={slug}")
    print(f"raw_dir={raw_dir}")
    print(f"source_md={source_md}")
    print(f"chunk_count={chunk_count}")
    print(f"chunk_note={chunk_note}")
    print(f"context_stack={raw_dir / 'stack'}")
    print(f"book_note={book_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
