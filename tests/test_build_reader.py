"""Check real export boundaries and source links without a browser or model."""

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from build_reader import build_html, clean_note, collect_library, make_demo


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "wiki"
        make_demo(self.root)

    def test_demo_links_resolve_and_export_has_no_machine_paths(self):
        library = collect_library(self.root, demo=True)
        self.assertEqual(len(library["books"]), 2)
        self.assertEqual(len([d for d in library["documents"] if d["kind"] != "原文"]), 2)
        ids = {doc["id"] for doc in library["documents"]}
        for doc in library["documents"]:
            for ref in doc["references"]:
                self.assertIn(ref, ids)
        theme = next(d for d in library["documents"] if d["kind"] == "主题")
        self.assertEqual(len(theme["references"]), 2)
        output = build_html(library)
        self.assertNotIn(str(self.root), output)
        self.assertNotIn(str(REPO), output)
        self.assertNotIn("__BOOK_WIKI_DATA__", output)
        data = re.search(r'<script id="library-data" type="application/json">(.*?)</script>', output, re.S).group(1)
        self.assertEqual(json.loads(data), library)
        # Browser code/assets are embedded; no CDN or network dependency.
        self.assertNotRegex(output, r'<script[^>]+src=|<link[^>]+rel="stylesheet"')

    def test_export_cannot_inject_script_from_a_book(self):
        attack = '</script><script>window.injected = true</script><img src=x onerror=alert(1)>'
        note = self.root / "wiki/ideas/untrusted.md"
        note.write_text("# Example\n" + attack, encoding="utf-8")
        output = build_html(collect_library(self.root))
        self.assertNotIn(attack, output)
        data = re.search(r'<script id="library-data" type="application/json">(.*?)</script>', output, re.S).group(1)
        self.assertIn(attack, json.loads(data)["documents"][-1]["text"])

    def test_export_skips_external_symlinks_and_invalid_text(self):
        private = Path(self.temp.name) / "outside.md"
        private.write_text("NOT PART OF THIS WIKI", encoding="utf-8")
        (self.root / "wiki/themes/external.md").symlink_to(private)
        (self.root / "wiki/themes/broken.md").write_bytes(b"\xff\xfe")
        library = collect_library(self.root)
        self.assertEqual(len(library["skipped"]), 2)
        self.assertNotIn("NOT PART OF THIS WIKI", build_html(library))

    def test_relative_source_links_resolve_but_plain_mentions_do_not(self):
        (self.root / "wiki/ideas/reference.md").write_text(
            "# 引用\n[依据](../../raw/books/reading-note-demo/chunks/chunk-0001.md#text)\n"
            "这个路径仅作说明：raw/books/reading-note-demo/chunks/chunk-0002.md", encoding="utf-8")
        note = next(d for d in collect_library(self.root)["documents"] if d["title"] == "引用")
        self.assertEqual(note["references"], ["raw/books/reading-note-demo/chunks/chunk-0001.md"])

    def test_only_importer_path_fields_are_removed(self):
        result = clean_note("# Note\n- 来源：/private/input\n- Raw 归档：/private/raw\n- 分块索引：/private/index\n- Context Stack：/private/stack\n- 作者：作者名\n- 来源：https://example.org/source\n我的观点保留。")
        self.assertNotIn("/private/", result)
        self.assertIn("作者名", result)
        self.assertIn("我的观点保留。", result)
        self.assertIn("https://example.org/source", result)

    def test_rebuild_does_not_modify_notes_and_demo_is_reproducible(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*.md")}
        build_html(collect_library(self.root))
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*.md")})
        other = Path(self.temp.name) / "other"
        make_demo(other)
        self.assertEqual(build_html(collect_library(self.root, True)), build_html(collect_library(other, True)))

    def test_cli_rejects_wrong_root_or_output_without_touching_notes(self):
        for arguments in (["--root", str(self.root / "missing")], ["--demo"]):
            result = subprocess.run([sys.executable, str(REPO / "scripts/build_reader.py"), *arguments,
                                     "--output", str(self.root / "keep.md")], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((self.root / "keep.md").exists())


if __name__ == "__main__":
    unittest.main()
