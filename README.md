# Book Wiki Reader

把一本书变成可以继续讨论、查证和积累的个人知识库。

Book Wiki Reader 是一个面向 Codex 的读书 skill，包含 Python 导入脚本、Markdown 笔记模板和共读工作流。它先保存原文、建立分块索引，再让 Codex 围绕问题与读者讨论，把作者观点、AI 判断和读者自己的想法分别记录。

适合想认真读书、做主题阅读，或希望把阅读所得用于写作和项目的人。目前是个人使用的 skill MVP，需要在 Codex 中完成 AI 共读；没有独立网页应用。

## 已经实现了什么

| 部分 | 当前行为 |
| --- | --- |
| Python 脚本 | 归档本地文件；将 txt/md 等纯文本分块；生成索引、来源记录、笔记模板和上下文目录；重复运行时保留已有内容。只使用 Python 标准库，不调用模型。 |
| Codex 工作流 | 根据 skill 指令生成阅读地图、解释论证、提出问题，并在读者回应后整理笔记。效果取决于模型、输入材料和实际执行过程。 |
| 笔记结构 | 提供 book、theme、idea、author、reading-plan 五类模板；分层保存原文、摘要和读者观点。初始化后摘要与观点字段为空，由后续共读填写。 |

工作流有三个具体选择：

- **先看地图再深入。** 先展示目录、主要问题和阅读建议，让读者决定从哪里读。
- **让读者参与判断。** 每个阅读单元先解释问题、作者答案和证据，再等待读者回应；不把 AI 猜测写成用户观点。
- **原文与理解分开保存。** 原文留在 `raw/`，可复用笔记留在 `wiki/`，讨论时可以回到对应分块核对。

长书采用分层上下文：原文分块 → 分块摘要 → 阅读单元 → 章节摘要 → 全书骨架。快速检视所得的骨架标为暂定；全书索引需要逐块读取。这个设计旨在减少后续重复搬运全文，**目前没有 token 节省或阅读准确率的量化评测**。

## 安装与开始

需要 Python 3.9+。AI 共读还需要能加载本地 skill 的 Codex 环境。

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/ginbrooks/book-wiki-reader-skill.git ~/.codex/skills/book-wiki-reader
```

下载 ZIP 时，将仓库内容放入 `~/.codex/skills/book-wiki-reader/`。如果配置了其他 skills 目录，使用对应目录。开启新会话后，可以对 Codex 说：

```text
用 $book-wiki-reader 把这本书读进我的 Book Wiki。
```

也可以先用脚本导入自己的文本：

```bash
python3 ~/.codex/skills/book-wiki-reader/scripts/init_book_wiki.py \
  --root ~/Documents/Book-Wiki \
  --source "/path/to/book.txt" \
  --title "书名" \
  --author "作者"
```

默认根目录为当前用户的 `~/Documents/Book-Wiki`，可用 `--root` 指定其他位置。文本默认按约 8000 字符分块，可用 `--chunk-size` 调整；`--no-chunks` 仅归档、不切分文本。

## 不用模型也能跑的示例

仓库附带一篇为演示编写的短文。它不是书籍摘录，也不包含假造的用户讨论或 AI 阅读结果。在仓库根目录运行：

```bash
python3 scripts/init_book_wiki.py \
  --root ./example-output \
  --source ./examples/reading-note.md \
  --title "把笔记写成能回答的问题" \
  --author "Book Wiki Reader 示例" \
  --slug reading-note-demo \
  --chunk-size 300
```

然后打开 `example-output/raw/books/reading-note-demo/chunk-index.md` 看分块索引，打开 `example-output/wiki/books/reading-note-demo.md` 看初始化笔记。摘要与观点部分此时应当仍为空。

[示例说明](examples/README.md)介绍预期产物和如何继续在 Codex 中共读。验证导入、原文完整性及重复运行保护：

```bash
python3 -m unittest discover -s tests -v
```

这些测试验证本地脚本行为，不评估模型的阅读质量。

## 产物结构

```text
Book-Wiki/
  raw/books/<book-slug>/
    original/                 原文件副本
    chunks/                   可按需读取的原文分块
    chunk-index.md            分块编号、长度与首行索引
    source.md                 来源、导入日期和文件位置
    stack/                    分块、单元、章节摘要与读者记忆
  raw/inbox/
  wiki/
    books/
    themes/
    ideas/
    authors/
    reading-plans/
  templates/
```

完整共读规则见 [SKILL.md](SKILL.md) 和 [reading-workflow.md](references/reading-workflow.md)。

## 当前边界

- PDF、EPUB、DOCX 可以归档，但脚本不会提取其中的文字；需要先转换成 txt/md 再导入。
- 初始化只生成文件和模板，不会自动生成摘要、主题卡或跨书关联。
- 同一 slug 的已有文件与分块会保留。导入修订版或另一本同名书时，请指定新的 `--slug`，避免沿用旧内容。
- 主题卡自动合并、更完整的格式转换和独立前端仍是后续方向。
- 原文只保存在用户指定的本地目录。将材料交给 Codex 处理时，应遵守所用服务的数据规则；发布示例时不要上传私人笔记或无权公开的书籍全文。
