# technical-document-writing

technical-document-writing 是一个 agent skill，让 AI agent 按《技术文档写作方法论-像设计产品一样写文档》编写中文技术文档。方法论把写文档看作设计产品：先研究读者阅读以后要做什么、会在哪里卡住，再写下读者的问题、设计大纲、编写正文，最后测试读者能否读懂。适用的文档包括系统架构设计文档、产品需求文档（PRD）、技术方案、讨论会材料、接入与使用指南、故障复盘、调研报告、技术教案、导读与技术博客，新建、改写、润色与审阅文档时都可以使用。

## 1. 执行步骤与产出

新建一份文档时，agent 依次执行下面七个步骤，每一步读取方法论的对应章节：

| 步骤 | 产出 | 读取的方法论章节 |
|---|---|---|
| 1. 读者分析 | 读者分析表：读者、阅读以后要做的事、已经知道什么、会卡在哪里、需要阅读的章节 | 第 2、26 章 |
| 2. 写作前的判断与材料 | 文档类型与内容性质的判断结果、问题序列与讨论范围、材料清单与事实记录 | 第 3—5 章 |
| 3. 文档设计与大纲 | 大纲：高层抽象、概念的依赖顺序、由浅入深的层次、主线问题、贯穿全文的例子、各章的标题与要点 | 第 6—11、19、23 章 |
| 4. 大纲确认 | agent 把大纲交给用户，停下来等待确认 | 第 23 章 |
| 5. 编写正文 | 正文 | 第 19—22 章，以及按内容性质选读的第 12—18 章 |
| 6. 成稿检查与读者测试 | 检查记录：脚本检查、数字复算、读者测试的结果 | 第 24、26 章 |
| 7. 读者反馈的处理 | 按反馈修改以后的文档，以及从同类反馈中提炼出的写作规则 | 第 25 章 |

只修改个别自然段、润色语言、审阅文档或处理读者反馈时，agent 只执行相关的步骤，对应关系写在 `SKILL.md` 的“执行步骤的选择”一节中。

第 6 步的读者测试由新启动的 subagent 完成。subagent 只拿到读者背景、文档与问题，回答问题以后报告哪里需要猜测、哪个名称看不懂、哪个问题找不到答案。作者自己通读时已经知道答案，会不自觉地补上缺少的步骤，读者测试能发现作者通读时发现不了的问题。

## 2. 安装

用 skills CLI 安装到用户目录，所有项目都能使用。skills CLI 需要 Node.js 22.20 或更高版本，运行时会询问安装到哪些 agent：

```bash
npx skills add CZYCW/technical-document-writing -g
```

只在 Claude Code 中使用时，也可以把仓库克隆到 Claude Code 的个人 skill 目录：

```bash
git clone https://github.com/CZYCW/technical-document-writing.git ~/.claude/skills/technical-document-writing
```

检查脚本需要 Python 3 与 markdown-it-py：

```bash
pip install markdown-it-py
```

## 3. 使用

安装以后，直接请 agent 新建、改写或审阅技术文档，agent 会按 `SKILL.md` 的步骤执行。请求的例子：

- “给产品团队写一份计费系统的接入指南，他们读完要能自己上报用量。”
- “把这份故障复盘改得更容易读懂，读者是没有参加排查的值班工程师。”
- “审阅 docs/design.md 这份架构设计文档。”

在 Claude Code 中也可以输入 `/technical-document-writing` 直接调用这个 skill。

三个检查脚本可以单独运行，`<skill 目录>` 是 skill 的安装位置：

```bash
python3 -B <skill 目录>/scripts/check_language.py <文档路径>
python3 -B <skill 目录>/scripts/check_tables.py <文档路径>
python3 -B <skill 目录>/scripts/check_refs.py <文档路径>
```

| 脚本 | 检查内容 |
|---|---|
| `check_language.py` | 方法论第 21.2—21.4 节中能用字词匹配的语言规则：禁止的句式、禁止的字词、只能出现在复合词中的字，代码块与行内代码不参与扫描 |
| `check_tables.py` | 每张表格中每一行的竖线数量与表头一致 |
| `check_refs.py` | “第 x 章”“第 x.y 节”的引用编号在本文的标题中存在 |

脚本的命中项都需要回到上下文判断，判断方法写在 `SKILL.md` 第 6 步。

## 4. 文件结构

| 文件 | 内容 |
|---|---|
| `SKILL.md` | 七个执行步骤：每一步读取的章节、产出，以及停下来等待用户确认的位置 |
| `references/technical-document-writing-methodology.md` | 《技术文档写作方法论-像设计产品一样写文档》全文，共 27 章 |
| `scripts/check_language.py`、`scripts/check_tables.py`、`scripts/check_refs.py` | 成稿检查使用的三个脚本 |
| `scripts/markdown_prose.py` | `check_language.py` 与 `check_refs.py` 共用的函数：用 markdown-it-py 取出代码以外的正文与带编号的标题 |

## 5. 许可

MIT，见 [LICENSE](LICENSE)。
