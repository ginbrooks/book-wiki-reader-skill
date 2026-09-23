"""Integration checks for local import; no model or network is involved."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "init_book_wiki.py"
SOURCE = REPO / "examples" / "reading-note.md"


class InitializationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "wiki"
        self.raw = self.root / "raw" / "books" / "reading-note-demo"

    def run_import(self, *extra):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root),
             "--source", str(SOURCE), "--title", "把笔记写成能回答的问题",
             "--author", "Book Wiki Reader 示例", "--slug", "reading-note-demo",
             "--chunk-size", "300", *extra],
            check=True, capture_output=True, text=True,
        )

    def test_import_preserves_source_and_covers_all_text(self):
        self.run_import()
        self.assertEqual((self.raw / "original" / SOURCE.name).read_bytes(), SOURCE.read_bytes())
        chunks = sorted((self.raw / "chunks").glob("chunk-*.md"))
        self.assertGreater(len(chunks), 1)
        text = "".join(p.read_text(encoding="utf-8").split("## Text\n\n", 1)[1] for p in chunks)
        self.assertEqual("".join(text.split()), "".join(SOURCE.read_text(encoding="utf-8").split()))
        index = (self.raw / "chunk-index.md").read_text(encoding="utf-8")
        for chunk in chunks:
            self.assertIn(chunk.name, index)
        self.assertEqual(
            {p.name for p in (self.raw / "stack").glob("*.md")},
            {"book-skeleton.md", "chunk-summaries.md", "unit-summaries.md",
             "section-summaries.md", "reader-memory.md"},
        )
        note = (self.root / "wiki/books/reading-note-demo.md").read_text(encoding="utf-8")
        self.assertNotIn("{{", note)
        self.assertIn(str(self.raw), note)
        templates = list((self.root / "templates").glob("*.md"))
        self.assertEqual(len(templates), 5)

    def test_rerun_preserves_reader_edits_and_existing_files(self):
        self.run_import()
        for relative in ("wiki/books/reading-note-demo.md",
                         "raw/books/reading-note-demo/stack/reader-memory.md",
                         "templates/book-note.md"):
            with (self.root / relative).open("a", encoding="utf-8") as handle:
                handle.write("\nUser-maintained content: keep this on reimport.\n")
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.run_import()
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_archive_only_skips_chunks(self):
        self.run_import("--no-chunks")
        self.assertEqual((self.raw / "original" / SOURCE.name).read_bytes(), SOURCE.read_bytes())
        self.assertFalse((self.raw / "chunks").exists())
        self.assertFalse((self.raw / "chunk-index.md").exists())
        self.assertTrue((self.raw / "source.md").is_file())
        self.assertTrue((self.raw / "stack/reader-memory.md").is_file())


if __name__ == "__main__":
    unittest.main()
