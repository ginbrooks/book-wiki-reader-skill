# 初始化示例

## 可交互的阅读工作台

[在线演示](https://ginbrooks.github.io/demos/book/)只使用本目录下的 `reading-note.md`、`small-experiment.md` 和 `demo-notes/`。两篇文章为原创虚构情景，笔记与主题卡为人工编写的演示材料，不包含真实用户观点或模型生成结果。

运行 `python3 scripts/build_reader.py --demo --output reader.html` 即可生成相同的离线页面。`docs/demo/index.html` 是提交到仓库的可复现构建，`docs/demo/screenshot.png` 是实际界面截图。生成器不会读取默认个人 Book Wiki 路径。

## 导入器示例

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
