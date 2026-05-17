---
name: book-wiki-reader
description: 当用户想和 AI 共读一本书、建立或维护 Book Wiki、把书导入结构化 raw/wiki 目录、创建 book/theme/idea/author/reading-plan 笔记，或提到“按 Book Wiki 读这本书”“共读”“读书 flow”“book wiki”“把读书变成知识库”时使用。
---

# Book Wiki Reader

使用这个 skill，把一本书和读书过程转化为结构化的个人知识库。目标不是生成漂亮摘要，而是沉淀用户自己的理解、判断、主题、方法和想法。

## 默认 Wiki 根目录

除非用户指定其他位置，默认使用：

`/Users/shu/Documents/Book-Wiki`

如果这个目录不存在，创建标准结构：

- `raw/books/`
- `raw/inbox/`
- `wiki/books/`
- `wiki/themes/`
- `wiki/ideas/`
- `wiki/authors/`
- `wiki/reading-plans/`
- `templates/`

## 快速开始

当用户提供一本书，或要求开始共读时：

1. 读取 `references/reading-workflow.md`。
2. 如果用户提供了本地文件，运行 `scripts/init_book_wiki.py`，创建 raw 归档和 book note。
3. 如果文件不能直接读取，先用合适的本地能力提取可读文本，再同时归档原文件和转换文本。
4. 先给书籍介绍，不要一上来做完整总结。
5. 询问用户想怎么使用这本书。
6. 如果用户想继续读，做检视阅读并生成阅读地图。
7. 确认读法。
8. 按问题块或观点块共读，不机械按章节推进。
9. 每个有意义的阅读单元后，分开记录作者观点、AI 判断和用户观点。
10. 阶段结束或全书读完后，先给总结入库草案，再让用户确认保留什么。

## 初始化脚本

处理本地书籍文件时，优先使用确定性的初始化脚本：

```bash
python3 /Users/shu/.codex/skills/book-wiki-reader/scripts/init_book_wiki.py \
  --root /Users/shu/Documents/Book-Wiki \
  --source "/path/to/book.txt" \
  --title "书名" \
  --author "作者"
```

如果书名或作者未知，可以省略，让 AI 从文件名和文本中尽量推断。

脚本会创建：

- `raw/books/<book-slug>/original/<source-file>`
- `raw/books/<book-slug>/source.md`
- `wiki/books/<book-slug>.md`

## 共读分工

核心分工：

- AI 负责读解：问题、作者答案、论证、例子。
- 读者负责赋义：相关性、不同意的地方、个人连接、未来是否复用。

使用三问读解卡：

1. 这个阅读单元在解决什么问题？
2. 作者给出的答案是什么？
3. 这个答案凭什么成立？有哪些论证和例子？

然后把第四问抛给读者：

> 这可能和你有什么关系？

不要替读者回答这一问。AI 可以给 2-3 个可能方向，但意义必须由用户确认、修正或否定。

## 提问选择

每个阅读单元只问一个主问题。不要问空泛的“你怎么看”。

根据内容类型选择问题：

- 概念或定义：问理解问题。
- 作者主张：问判断问题。
- 论证过程：问证据问题。
- 方法或步骤：问应用问题。
- 案例或故事：问它证明了什么。
- 长期可复用观点：问入库问题。

## 入库分流

不要保存所有内容，只保存未来可能被调用的内容。

- `wiki/books/`：书本身的结构、核心主张、论证和用户判断。
- `wiki/themes/`：跨书复用的概念和长期问题。
- `wiki/ideas/`：用户自己的想法、项目灵感、判断和方法。
- `wiki/authors/`：重要作者。
- `wiki/reading-plans/`：阅读路线和未来学习计划。
- `raw/books/`：原始文件、转换文本和来源元数据。

作者观点、AI 判断、用户观点必须分开记录。

## 版权边界

处理书籍时，以总结和分析为主。不要复制大段受版权保护的内容。只有在必要时使用短摘录，并尽量附上章节、页码或位置。
