# 初始化示例

`reading-note.md` 是为本仓库编写的短文，文中人物和行为均为假设。示例不需要 API key，也不会调用模型。

在仓库根目录执行 README 中的示例命令，脚本会归档这篇短文，按 300 字符目标切分，并创建以下内容：

```text
example-output/
  raw/books/reading-note-demo/
    original/reading-note.md
    chunks/chunk-0001.md …
    chunk-index.md
    source.md
    stack/
      book-skeleton.md
      chunk-summaries.md
      unit-summaries.md
      section-summaries.md
      reader-memory.md
  wiki/books/reading-note-demo.md
  templates/
```

检查时可以从三处开始：

1. `original/reading-note.md` 应与输入文件相同；`chunks/` 中应覆盖全部正文。
2. `chunk-index.md` 应列出生成的分块编号、字符数和首行提示。
3. `book-skeleton.md` 和 book note 是待填写的模板，不应出现已经读懂文章或完成用户讨论的假结果。

运行 `python3 -m unittest discover -s tests -v` 可在临时目录验证导入、分块内容、模板生成、重复运行保留修改，以及仅归档模式。测试结束后临时目录会自动删除。

如果要体验 AI 共读，在 Codex 中提供这个示例文件并说：

```text
用 $book-wiki-reader 共读 examples/reading-note.md。
Wiki 根目录使用当前仓库的 example-output，slug 使用 reading-note-demo。
先给我阅读地图，再选一个问题讨论。
```

这一步需要模型实际执行。仓库没有预先伪造生成结果，也没有用初始化测试代替阅读质量评测。`example-output/` 已被 Git 忽略，避免将本地绝对路径和后续个人讨论误提交。
