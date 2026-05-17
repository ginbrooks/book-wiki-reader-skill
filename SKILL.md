---
name: book-wiki-reader
description: Use when the user wants to read a book with AI, build or maintain a Book Wiki, import a book into structured raw/wiki folders, create book/theme/idea/author/reading-plan notes, or asks to "按 Book Wiki 读这本书", "共读", "读书 flow", "book wiki", or turn reading into a personal knowledge base.
---

# Book Wiki Reader

Use this skill to help a user turn books into a structured personal knowledge base while reading with them. The goal is not pretty summaries; the goal is durable understanding, judgment, reusable themes, and user-owned ideas.

## Default Wiki Root

Use the user's existing Book Wiki unless they specify another location:

`/Users/shu/Documents/Book-Wiki`

If this path does not exist, create the standard structure:

- `raw/books/`
- `raw/inbox/`
- `wiki/books/`
- `wiki/themes/`
- `wiki/ideas/`
- `wiki/authors/`
- `wiki/reading-plans/`
- `templates/`

## Quick Start

When the user gives a book file or asks to start reading:

1. Read `references/reading-workflow.md`.
2. If the user gave a local file, run `scripts/init_book_wiki.py` to create the raw archive and book note.
3. If the file is not directly readable, use the appropriate local capability to extract readable text, then archive both original and converted text.
4. Give a book introduction first, not a full summary.
5. Ask how the user wants to use the book.
6. If the user wants to continue, do inspectional reading and produce a reading map.
7. Confirm the reading path.
8. Co-read by problem blocks or idea blocks, not mechanically by chapter.
9. After each meaningful unit, record author view, AI judgment, and user view separately.
10. At the end, give a summary and routing draft; let the user confirm what should be preserved.

## Initialization Script

For local files, prefer the deterministic script:

```bash
python3 /Users/shu/.codex/skills/book-wiki-reader/scripts/init_book_wiki.py \
  --root /Users/shu/Documents/Book-Wiki \
  --source "/path/to/book.txt" \
  --title "Book Title" \
  --author "Author Name"
```

If title or author is unknown, omit them and infer what you can from the file name and text.

The script creates:

- `raw/books/<book-slug>/original/<source-file>`
- `raw/books/<book-slug>/source.md`
- `wiki/books/<book-slug>.md`

## Co-Reading Contract

The core split:

- AI reads and explains: problem, author answer, argument, examples.
- User confirms meaning: relevance, disagreement, personal connection, future reuse.

Use the three-question reading card:

1. What problem is this unit solving?
2. What answer does the author give?
3. Why does that answer hold? What argument and examples support it?

Then ask the user one fourth-question prompt:

> What might this have to do with you?

Do not answer this for the user. You may offer 2-3 possible directions, but the user must confirm, revise, or reject the meaning.

## Question Selection

Ask one main question per reading unit. Avoid vague prompts like "What do you think?"

Choose by content type:

- Concept or definition: ask a comprehension question.
- Author claim: ask a judgment question.
- Argument: ask an evidence question.
- Method or steps: ask an application question.
- Case or story: ask what it proves.
- Long-term reusable idea: ask an asset-routing question.

## Asset Routing

Do not save everything. Preserve only what is likely to be reused.

- `wiki/books/`: the book's structure, core claims, arguments, user judgments.
- `wiki/themes/`: cross-book concepts and recurring questions.
- `wiki/ideas/`: the user's own ideas, project sparks, claims, or methods.
- `wiki/authors/`: important authors only.
- `wiki/reading-plans/`: reading paths and future study plans.
- `raw/books/`: original files, extracted text, source metadata.

Keep author views, AI judgments, and user views separate.

## Copyright Boundary

When working with books, summarize and analyze. Do not reproduce long copyrighted passages. Use short excerpts only when necessary and attach chapter, page, or location when available.
