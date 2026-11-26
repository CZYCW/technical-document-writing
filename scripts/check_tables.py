import sys
from pathlib import Path

from markdown_it import MarkdownIt

# 用 markdown-it-py 找出每张表格在源文件中的行范围，核对每一行的竖线数量与表头一致
# markdown-it-py 按表头的列数截断多出的单元格、补齐缺少的单元格，解析结果看不出这类错误，需要在源文件上核对
text = Path(sys.argv[1]).read_text(encoding="utf-8")
tokens = MarkdownIt("commonmark").enable("table").parse(text)
lines = text.splitlines()


def pipes(line):
    return line.count("|") - line.count("\\|")


tables = 0
problems = 0
for tok in tokens:
    if tok.type != "table_open":
        continue
    tables += 1
    first, last = tok.map
    header = pipes(lines[first])
    for no in range(first, last):
        if pipes(lines[no]) != header:
            problems += 1
            print("第", no + 1, "行的竖线数量", pipes(lines[no]), "与表头的", header, "不一致")
print("表格", tables, "问题", problems)
