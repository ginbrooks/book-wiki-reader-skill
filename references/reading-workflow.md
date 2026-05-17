# Book Wiki Reading Workflow

This reference is the canonical workflow for the Book Wiki Reader skill.

## Core Principles

1. Decide purpose before deciding reading mode. Do not assume every book deserves deep reading.
2. Inspect before co-reading. Show the reader the book introduction, table of contents, skeleton map, and reading advice first.
3. Co-reading uses problem blocks or idea blocks, not chapter mechanics. Chapters are location tools.
4. AI reads first; the reader assigns meaning. AI clarifies the book, the reader confirms what matters.
5. Questions should trigger thought without creating burden. Ask one concrete question per unit.
6. Keep author views, AI judgments, and user views separate.
7. Only save what will be called again. The wiki is not a summary warehouse.
8. Keep raw sources traceable and organized notes linked back to source.

## Directory Roles

- `raw/books/`: original book files, source records, converted text.
- `raw/inbox/`: temporary excerpts, screenshots, links, transcripts, loose thoughts.
- `wiki/books/`: single-book notes.
- `wiki/themes/`: cross-book theme cards.
- `wiki/ideas/`: ideas, projects, methods, and claims produced by reading.
- `wiki/authors/`: important author cards.
- `wiki/reading-plans/`: reading plans, book lists, and study routes.

## 0. Intake

When the user provides a book or related material, preserve source first.

Record:

- title, author, version or language
- user-provided path or link
- import date
- original file or raw text location

Products:

- `raw/books/<book-slug>/source.md`
- original or extracted text archived under `raw/books/<book-slug>/`
- initialized `wiki/books/<book-slug>.md`

## 1. Book Introduction

First help the user know what the book is, then ask whether and how they want to read it.

Output:

- basic information: title, author, version, publication or writing background
- one-sentence intro
- content intro in a few sentences, not chapter-level expansion
- core question
- who this book is for
- what not to expect
- possible value

The introduction is a light entry point, not a full summary. It may include a content intro but does not replace inspectional reading.

Classify the book backstage. Do not force the user to learn terms like practical book, theoretical book, philosophy book, and so on.

Product:

- update book note `Book Intro`

## 2. Purpose Check

After the book introduction, ask:

> How do you want to use this book?

Common options:

- help me understand it
- help me find the important parts
- read around my question
- organize it into my library first
- do not read this one

If the user chooses not to read, archive or pass. Do not enter co-reading.

Product:

- update `Reading Intent`

## 3. Inspectional Reading

If the user wants to continue, inspect the book. The goal is not full summary; it is to show structure and route.

Input priority:

- title and subtitle
- table of contents
- preface, introduction, foreword
- conclusion, afterword
- beginnings and endings of key chapters
- quick full-book scan if needed

Output:

- original table of contents for location and source tracing
- skeleton map with fewer levels showing the main line, part relationships, and progression
- core question
- chapter value: trunk, case, background, supplement, or skippable
- reading advice

Skeleton map is the understanding view. Original TOC is the location view. The skeleton can start light and be corrected during co-reading.

Product:

- update `Reading Map`

## 4. Confirm Reading Path

After introduction and inspection, confirm the route.

Reader-facing options:

- read with me from start to finish
- help me pick the key parts
- read around my question
- organize it into my library first
- do not read this one

Backstage mapping:

- start to finish: co-reading / analytical reading
- key parts: selected close reading
- around my question: question-oriented or syntopical reading
- library first: reference reading / archive
- do not read: discard or temporary archive

For deep, question-oriented, or long-term asset reading, ask:

- What question do you most want this book to answer?
- What do you want to keep at the end: notes, process, theme card, idea card, or judgment?

Product:

- update `Reading Plan`

## 5. Co-Reading

The goal is not chapter summaries. The goal is to help the user understand structure, judge claims, and form ideas. The reading unit can be a problem block, idea block, argument, method, or chapter section.

Each unit:

1. State where this unit sits in the book skeleton, or what problem it is handling.
2. Answer the three-question reading card.
3. Ask the fourth question to the reader.
4. Wait for user response. If the user explicitly skips discussion, record skipped.
5. Record user view, then add AI judgment or shared conclusion.
6. Write to wiki before marking the unit complete.

Three-question reading card:

- What problem is it solving?
- What answer does the author give?
- Why does that answer hold? What argument and examples support it?

Fourth question for the reader:

- What might this have to do with you?

AI may offer possible connections, but cannot decide meaning for the reader.

### Question Rules

- Ask one main question per unit, with at most one follow-up when useful.
- Do not ask vague "what do you think" questions.
- Serve the reading goal: understand, judge, apply, or route to the wiki.
- If the user gives a short answer, follow their answer. If they do not want to discuss, record skipped and continue.
- AI may offer 2-3 possible directions to help the user start, but the user chooses, revises, or rejects.

### Question Routing

- Concept or definition: ask comprehension.
- Author claim: ask judgment.
- Argument: ask evidence.
- Method or steps: ask application.
- Case or story: ask what it proves.
- Long-term reusable idea: ask asset routing.

Useful prompts:

- Structure: If this unit were removed, what would the book lose?
- Understanding: How would you say this in your own words?
- Evidence: What does the author's example actually prove?
- Judgment: Where does this claim hold, and where might it fail?
- Transfer: Where could this change your work, learning, writing, or project?
- Routing: Should this stay in the book note, or become a theme, idea, method, or plan?

Do not summarize and declare done. Without user response or explicit skip, the unit is not complete.

## 6. Summary and Routing

After a stage or whole book, first close understanding, then route assets. Do not leave all summarization to the user; do not let AI decide personal meaning alone.

Division of labor:

- AI organizes, compresses, and routes: author views, structure, arguments, reusable concepts, methods, excerpts, asset suggestions.
- Reader confirms meaning: real takeaway, agreement or doubt, personal connection, reread value, future reuse.

Process:

1. AI gives a summary and routing draft.
2. Reader confirms, changes, removes, or adds.
3. AI writes the confirmed result into wiki.
4. Save only future-callable material.

Summary and routing draft:

- core question of the book or stage
- author's core answer
- 3-5 most important author views
- suggested book note entries
- suggested theme cards, idea cards, method cards, or reading plans
- possible excerpts
- 2-3 questions for reader confirmation

Default confirmation questions:

- Which item is closest to your real takeaway?
- Which item do you disagree with, want to delete, or want rewritten?
- Is there a question you want to keep pursuing?

## Minimal Start

When the user says "read this book with Book Wiki" or similar:

1. read this workflow
2. ingest the material
3. give a book introduction
4. ask how the user wants to use the book
5. if they continue, inspect and output TOC, skeleton map, core question, chapter value, reading advice
6. confirm the reading path
7. co-read, discuss, record, and route assets
