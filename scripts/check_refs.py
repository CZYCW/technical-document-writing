import re
import sys
from pathlib import Path

from markdown_prose import numbered_headings, prose_lines

# 核对正文中“第 x 章”“第 x.y 节”的引用都指向本文存在的标题；引用其他文档的章节也会列出，需要回到上下文确认引用对象
text = Path(sys.argv[1]).read_text(encoding="utf-8")

chapters = set()
sections = set()
for tag, _, title in numbered_headings(text):
    if tag == "h2":
        m = re.match(r"(\d+)\. ", title)
        if m:
            chapters.add(m.group(1))
    else:
        m = re.match(r"(\d+(?:\.\d+)+) ", title)
        if m:
            sections.add(m.group(1))

ref = re.compile(r"第\s*(\d+(?:\.\d+)*(?:\s*(?:、|—|至)\s*\d+(?:\.\d+)*)*)\s*(节|章)")
missing = 0
total = 0
for line, prose in prose_lines(text):
    for m in ref.finditer(prose):
        target = chapters if m.group(2) == "章" else sections
        for number in re.split(r"\s*(?:、|—|至)\s*", m.group(1)):
            total += 1
            if number not in target:
                missing += 1
                print("第", line, "行", m.group(0), "：本文没有", number, m.group(2))
print("章", len(chapters), "节", len(sections), "引用", total, "本文不存在的引用", missing)
