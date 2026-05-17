#!/usr/bin/env python3
import argparse
import datetime as dt
import re
import shutil
from pathlib import Path


DEFAULT_ROOT = Path("/Users/shu/Documents/Book-Wiki")


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a Book Wiki entry for a local book file.")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="Book Wiki root directory")
    parser.add_argument("--source", help="Local book file path to archive")
    parser.add_argument("--title", help="Book title")
    parser.add_argument("--author", default="", help="Book author")
    parser.add_argument("--slug", help="Optional slug override")
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

    archived_source = ""
    if source_path:
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        target = original_dir / source_path.name
        if not target.exists():
            shutil.copy2(source_path, target)
        archived_source = str(target)

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
                    "date": today,
                },
            ),
            encoding="utf-8",
        )

    print(f"root={root}")
    print(f"slug={slug}")
    print(f"raw_dir={raw_dir}")
    print(f"source_md={source_md}")
    print(f"book_note={book_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
