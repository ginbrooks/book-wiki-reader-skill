# Book Wiki Reader Skill

Book Wiki Reader 是一个 Codex skill，用来把“读一本书”变成结构化的个人知识库。

它可以帮助 AI 助手：

- 把一本书导入 Book Wiki 文件夹
- 自动创建 raw 来源记录和结构化 book note
- 在正式阅读前先介绍这本书
- 做检视阅读，生成阅读地图
- 按问题块或观点块共读，而不是机械按章节摘要
- 用“三问读解卡”帮助读者读懂文本
- 把“这和我有什么关系”交给读者判断
- 把真正有长期价值的内容分流到 book note、theme card、idea card、author card 和 reading plan

这个 skill 的目标不是生成漂亮摘要，而是帮助读者形成可以长期调用的理解、判断、主题和想法。

## 安装

把这个仓库克隆或下载到你的 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/wjc2336098412-star/book-wiki-reader-skill.git ~/.codex/skills/book-wiki-reader
```

如果你下载的是 zip 文件，解压后把文件夹放到：

```text
~/.codex/skills/book-wiki-reader
```

然后重启 Codex，或者开启一个新会话，让 Codex 重新发现这个 skill。

## 使用方式

你可以这样说：

```text
用 $book-wiki-reader 把这本书读进我的 Book Wiki。
```

或者更口语一点：

```text
按 Book Wiki 读这本书。
```

如果你提供的是本地书籍文件，可以用脚本初始化 wiki 条目：

```bash
python3 ~/.codex/skills/book-wiki-reader/scripts/init_book_wiki.py \
  --root ~/Documents/Book-Wiki \
  --source "/path/to/book.txt" \
  --title "书名" \
  --author "作者"
```

## 默认 Wiki 结构

这个 skill 默认使用下面的结构：

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

## 阅读流程

1. 入库并保存原始来源。
2. 先输出书籍介绍。
3. 询问读者想怎么使用这本书。
4. 做检视阅读，生成阅读地图。
5. 确认读法。
6. 按问题块或观点块共读。
7. 每个阅读单元只问一个真正有用的问题。
8. 最后只把未来还会被调用的内容沉淀进 wiki。

## 三问读解卡

AI 负责回答：

1. 这个阅读单元在解决什么问题？
2. 作者给出的答案是什么？
3. 这个答案凭什么成立？有哪些论证和例子？

读者负责回答：

4. 这可能和我有什么关系？

## 原则

- 作者观点、AI 判断、读者观点要分开。
- 只保存未来可能复用的内容。
- 保留 raw 来源，方便追溯。
- 对书籍做总结和分析，不复制大段受版权保护的原文。
