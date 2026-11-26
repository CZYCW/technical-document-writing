import re
import sys
from collections import Counter
from pathlib import Path

from markdown_prose import prose_lines

# 用字词与正则表达式匹配方法论第 21.2—21.4 节中能够匹配的规则，代码块与行内代码不参与扫描
# 每一条命中都回到上下文判断，判断方法见 SKILL.md 第 6 步

FORBIDDEN = [
    "栈", "死", "拆", "落",
    "契约", "走读", "总账", "打挂", "炸了", "翻车", "牙齿", "第一刀", "凿接缝", "喂给", "全程证明", "放心提交", "原文粘贴",
    "一句话总结", "总之", "综上", "总的来说", "简而言之", "换句话说", "下面详细", "如上所述", "以上内容", "上述内容",
    "第一版", "稳妥", "激进", "硬编码", "实操", "夯实", "扎实", "虚空", "而不是", "而非",
    "兜底", "收口", "闭环", "抓手", "赋能", "拉通", "打通", "沉淀", "颗粒度",
]
PATTERNS = {"不是……而是……": re.compile(r"不是[^。！？\n]*?而是")}

# 受限的字与允许出现的复合词；不在列表中的复合词也可能成立，需要回到上下文判断
LIMITED = {
    "粗": ["粗略"],
    "细": ["详细", "明细", "仔细", "细节", "细致", "精细", "细则", "细分"],
    "硬": ["硬件", "硬盘"],
    "软": ["软件"],
    "实": ["实现", "实际", "实测", "事实", "实例", "实时", "实收", "实付", "核实", "确实", "实施", "实践", "真实", "实验",
          "实体", "实质", "证实", "如实", "实行", "属实", "实用", "实线", "现实", "实证", "实名", "实参", "实数", "充实",
          "实在", "实力", "务实", "翔实", "切实", "实情", "实效", "其实", "实务"],
    "虚": ["虚拟", "虚线", "虚构", "虚假", "虚数", "虚函数", "谦虚"],
    "判": ["判定", "判断", "判别", "判据", "研判", "评判", "误判", "裁判", "判决", "判读"],
    "轴": ["坐标轴", "时间轴", "横轴", "纵轴", "数轴"],
    "面": ["页面", "界面", "书面", "方面", "表面", "全面", "前面", "后面", "上面", "下面", "里面", "外面", "面向", "层面",
          "平面", "面板", "正面", "反面", "侧面", "局面", "面对", "面临", "当面", "面试", "版面", "封面", "字面", "画面",
          "对面", "见面", "会面", "面积", "面谈", "片面", "面前"],
}
# 只在特定用法中允许的说法：“是不是”用于是非问题，“对齐”只用于技术含义
CHECK = {"不是": ["是不是"], "对齐": ["内存对齐", "地址对齐", "字节对齐"]}
REPORT_WORDS = re.compile(r"walkthrough|rollup|ledger", re.I)


def covered(prose, words):
    spans = set()
    for word in words:
        for m in re.finditer(re.escape(word), prose):
            spans.update(range(m.start(), m.end()))
    return spans


def context(prose, start, end):
    return prose[max(0, start - 8): end + 8].strip()


text = Path(sys.argv[1]).read_text(encoding="utf-8")
counts = Counter()
for line, prose in prose_lines(text):
    flagged = set()
    for name, pattern in PATTERNS.items():
        for m in pattern.finditer(prose):
            counts["禁止的句式"] += 1
            flagged.update(range(m.start(), m.end()))
            print("第", line, "行", "禁止的句式", name, "：", context(prose, m.start(), m.end()))
    for word in FORBIDDEN:
        for m in re.finditer(re.escape(word), prose):
            counts["禁止的字词"] += 1
            flagged.update(range(m.start(), m.end()))
            print("第", line, "行", "禁止的字词", word, "：", context(prose, m.start(), m.end()))
    for word, allowed in CHECK.items():
        ok = covered(prose, allowed)
        for m in re.finditer(word, prose):
            if m.start() in flagged or m.start() in ok:
                continue
            counts["需要核对的说法"] += 1
            print("第", line, "行", "需要核对的说法", word, "：", context(prose, m.start(), m.end()))
    for ch, allowed in LIMITED.items():
        ok = covered(prose, allowed)
        for m in re.finditer(ch, prose):
            if m.start() in flagged or m.start() in ok:
                continue
            counts["需要核对的受限用字"] += 1
            print("第", line, "行", "需要核对的受限用字", ch, "：", context(prose, m.start(), m.end()))
    for m in REPORT_WORDS.finditer(prose):
        counts["需要核对的英文报告用语"] += 1
        print("第", line, "行", "需要核对的英文报告用语", m.group(0), "：", context(prose, m.start(), m.end()))
print("命中", dict(counts) if counts else "无")
