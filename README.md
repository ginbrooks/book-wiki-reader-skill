# Book Wiki Reader Skill

Book Wiki Reader is a Codex skill for reading books into a structured personal knowledge base.

It helps an AI assistant:

- import a book into a Book Wiki folder
- create raw source records and structured book notes
- introduce the book before reading
- inspect the book and build a reading map
- co-read by problem blocks or idea blocks
- use a three-question reading card to understand the text
- ask the reader to decide personal meaning
- route durable material into book notes, theme cards, idea cards, author cards, and reading plans

The goal is not to generate pretty summaries. The goal is to help readers build durable understanding, judgment, and a reusable reading memory.

## Install

Clone or download this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/wjc2336098412-star/book-wiki-reader-skill.git ~/.codex/skills/book-wiki-reader
```

If you downloaded a zip file, unzip it and place the folder here:

```text
~/.codex/skills/book-wiki-reader
```

Then restart Codex or start a new session so the skill can be discovered.

## Usage

Say something like:

```text
Use $book-wiki-reader to read this book into my Book Wiki.
```

Or:

```text
按 Book Wiki 读这本书。
```

If you provide a local book file, the skill can initialize the wiki entry with:

```bash
python3 ~/.codex/skills/book-wiki-reader/scripts/init_book_wiki.py \
  --root ~/Documents/Book-Wiki \
  --source "/path/to/book.txt" \
  --title "Book Title" \
  --author "Author Name"
```

## Default Wiki Structure

The skill uses this structure:

```text
Book-Wiki/
  raw/
    books/
    inbox/
  wiki/
    books/
    themes/
    ideas/
    authors/
    reading-plans/
  templates/
```

## Reading Flow

1. Intake and archive the source.
2. Give a book introduction.
3. Ask how the reader wants to use the book.
4. Inspect the book and create a reading map.
5. Confirm the reading path.
6. Co-read by problem blocks or idea blocks.
7. Ask one useful question per unit.
8. Summarize and route only future-useful material into the wiki.

## Co-Reading Card

The AI answers:

1. What problem is this unit solving?
2. What answer does the author give?
3. Why does that answer hold? What argument and examples support it?

The reader answers:

4. What might this have to do with you?

## Notes

- Keep author views, AI judgments, and reader views separate.
- Save only material likely to be reused.
- Preserve raw sources for traceability.
- Summarize and analyze books; do not reproduce long copyrighted passages.
