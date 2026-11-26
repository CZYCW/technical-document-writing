from markdown_it import MarkdownIt


# 用 markdown-it-py 解析 Markdown，返回正文文字及其在源文件中的行号；代码块、行内代码与 HTML 标签不计入正文
def prose_lines(text):
    tokens = MarkdownIt("commonmark").enable("table").parse(text)
    lines = []
    block_line = 0
    for tok in tokens:
        if tok.map:
            block_line = tok.map[0]
        if tok.type != "inline":
            continue
        line = block_line
        parts = []
        for child in tok.children:
            if child.type == "text":
                parts.append(child.content)
            elif child.type == "code_inline":
                parts.append("`…`")
            elif child.type == "html_inline":
                parts.append(" ")
            elif child.type in ("softbreak", "hardbreak"):
                lines.append((line + 1, "".join(parts)))
                parts = []
                line += 1
        lines.append((line + 1, "".join(parts)))
    return lines


# 返回各级标题的编号与标题文字：二级标题形如“## 12. 名称”，三级与四级标题形如“### 12.3 名称”“#### 12.3.1 名称”
def numbered_headings(text):
    tokens = MarkdownIt("commonmark").enable("table").parse(text)
    headings = []
    for tok, nxt in zip(tokens, tokens[1:]):
        if tok.type == "heading_open" and tok.tag in ("h2", "h3", "h4"):
            headings.append((tok.tag, tok.map[0] + 1, nxt.content))
    return headings
