#!/usr/bin/env python3
"""论文段落检查：信息密度分析 + 改写保真检查。只用标准库，不调用模型。

用法：
    python3 scripts/paper_check.py density 段落.txt
        逐句标出：有没有具体信息（数字、统计量、图表、引用、专名），
        有没有零信息套话，有没有过度断言，句子大致在做什么（背景、缺口、方法、结果、讨论）。

    python3 scripts/paper_check.py compare 原文.txt 改写.txt
        比较 AI 改写或总结前后：数字和引用有没有丢、有没有新出现的数字（可能是编造），
        限定语有没有被删（可能→证明），结论范围有没有被放大（本样本→普遍）。

依据见 references/academic-cnki.md「模仿与总结的走样」一节：
Peters & Chin-Yee 2025（LLM 总结科研论文时把结论说得比原文更宽）、
多项摘要语步研究（AI 摘要少给背景和方法细节、偏重结论和意义）。
"""
import re
import sys
from pathlib import Path

# 具体信息的标记
NUM = r"\d+(?:\.\d+)?\s*(?:%|％|‰|倍|个|项|例|名|人|篇|次|年|月|天|小时|分钟|秒|元|万|亿|kg|g|mg|mL|L|m|cm|mm|km|℃|°C|Hz|kHz|MHz|GB|MB)?"
STAT = r"(?:[pP]\s*[<>=＜＞]\s*0?\.\d+|[nN]\s*=\s*\d+|[rR]²?\s*=\s*-?0?\.\d+|β\s*=|OR\s*=|95%\s*CI|SD|标准差|置信区间)"
FIGTAB = r"(?:表|图|Table|Fig\.?|Figure)\s*\d+"
CITE = r"(?:[（(][^（）()]{1,40}?(?:19|20)\d{2}[a-z]?[）)]|\[\d+(?:[,，–-]\s*\d+)*\]|等人?[（(](?:19|20)\d{2}[）)])"

# 零信息套话（元话语、空泛评价、程式化过渡）
FILLER = [
    "值得注意的是", "需要指出的是", "不难发现", "由此可见", "综上所述", "总而言之", "总的来说",
    "具有重要的理论意义和实践价值", "具有重要意义", "具有一定的参考价值", "提供了新思路", "提供了理论支撑",
    "奠定了基础", "深入探讨", "深刻揭示", "系统梳理", "日益受到关注", "随着.{1,15}的(?:快速|不断|飞速)?发展",
    "在.{1,12}背景下", "本文旨在", "起到了.{1,8}作用", "发挥了.{1,8}作用", "不可或缺", "至关重要",
]
# 过度断言 / 范围放大
OVERCLAIM = ["证明了", "证实了", "揭示了", "充分说明", "表明了.{0,4}普遍", "普遍", "广泛", "所有", "一切", "总是",
             "必然", "完全", "彻底", "首次", "显著(?!性水平|性检验|差异\\(p)", "极大地", "大幅"]
# 限定语（原文有、改写里没了，就要警惕）
HEDGE = ["可能", "或许", "也许", "在一定程度上", "初步", "倾向于", "提示", "推测", "似乎", "有待", "尚需",
         "本研究中", "本样本", "在本研究条件下", "在.{1,10}条件下", "部分"]
# 句子功能的粗略线索（参考 Swales 语步）
MOVES = {
    "背景": ["随着", "近年来", "已有研究", "研究表明", "广泛应用", "受到关注", "是.{1,10}的重要"],
    "缺口": ["然而", "但是", "尚未", "仍不清楚", "较少", "缺乏", "不足", "空白", "鲜有"],
    "本文": ["本文", "本研究", "我们", "笔者"],
    "方法": ["采用", "利用", "通过", "构建", "选取", "收集", "测定", "分析了", "模型", "样本", "问卷", "实验"],
    "结果": ["结果显示", "结果表明", "发现", "显示", "提高了", "降低了", "增加了", "减少了"],
    "讨论": ["说明", "意味着", "可能是因为", "原因", "与.{1,15}一致", "相比", "解释"],
    "意义": ["意义", "启示", "为.{1,20}提供", "有助于", "参考价值", "未来"],
}


def sentences(text):
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[。！？；])", text)
    return [p.strip() for p in parts if re.search(r"[一-鿿]{4}", p)]


def find_all(pats, s):
    out = []
    for p in pats:
        out += re.findall(p, s)
    return [x if isinstance(x, str) else x[0] for x in out]


def specifics(s):
    nums = [n for n in re.findall(NUM, s) if re.search(r"\d", n)]
    return {
        "数字": nums,
        "统计量": re.findall(STAT, s),
        "图表": re.findall(FIGTAB, s),
        "引用": re.findall(CITE, s),
    }


def density(path):
    text = Path(path).read_text(encoding="utf-8")
    sents = sentences(text)
    total_spec = zero_info = filler_n = over_n = 0
    move_count = {k: 0 for k in MOVES}
    print(f"共 {len(sents)} 句，{len(re.findall(r'[一-鿿]', text))} 字\n")
    for i, s in enumerate(sents, 1):
        sp = specifics(s)
        n_spec = sum(len(v) for v in sp.values())
        fil = find_all(FILLER, s)
        ovr = find_all(OVERCLAIM, s)
        mv = [k for k, cues in MOVES.items() if any(re.search(c, s) for c in cues)]
        for k in mv:
            move_count[k] += 1
        total_spec += n_spec
        filler_n += bool(fil)
        over_n += bool(ovr)
        flag = []
        if n_spec == 0 and fil:
            flag.append("零信息")
            zero_info += 1
        if ovr and not sp["统计量"] and not sp["引用"]:
            flag.append("断言缺依据")
        tag = "、".join(mv) if mv else "-"
        spec_s = "；".join(f"{k}:{'/'.join(v)}" for k, v in sp.items() if v)
        print(f"[{i}] ({tag}) {'⚠ ' + '，'.join(flag) if flag else ''}")
        print(f"    {s}")
        if spec_s:
            print(f"    具体信息 → {spec_s}")
        if fil:
            print(f"    套话 → {'、'.join(fil)}")
        if ovr:
            print(f"    强断言 → {'、'.join(ovr)}")
    n = max(1, len(sents))
    print("\n== 汇总")
    print(f"每句平均具体信息：{total_spec / n:.2f} 个")
    print(f"含套话的句子：{filler_n}/{len(sents)}；其中没有任何具体信息的：{zero_info}")
    print(f"含强断言的句子：{over_n}/{len(sents)}")
    print("语步分布：" + "，".join(f"{k} {v}" for k, v in move_count.items()))
    if move_count["方法"] == 0 and move_count["结果"] > 0:
        print("提示：有结果没有方法细节。AI 摘要常见问题是少给背景和方法、偏重结论和意义。")
    if move_count["意义"] > move_count["结果"]:
        print("提示：谈意义的句子比报告结果的还多，检查是否在空泛拔高。")


def compare(src_path, new_path):
    src = Path(src_path).read_text(encoding="utf-8")
    new = Path(new_path).read_text(encoding="utf-8")

    def nums(t):
        return set(re.findall(r"\d+(?:\.\d+)?", t))

    def cites(t):
        return set(re.findall(CITE, t))

    lost_nums = sorted(nums(src) - nums(new), key=float)
    new_nums = sorted(nums(new) - nums(src), key=float)
    lost_cites = sorted(cites(src) - cites(new))
    hedges_src = find_all(HEDGE, src)
    hedges_new = find_all(HEDGE, new)
    over_src = find_all(OVERCLAIM, src)
    over_new = find_all(OVERCLAIM, new)
    print("== 改写保真检查")
    print(f"原文数字 {len(nums(src))} 个，改写后丢失：{lost_nums or '无'}")
    print(f"改写里新出现的数字（核对是否编造）：{new_nums or '无'}")
    print(f"丢失的引用：{lost_cites or '无'}")
    print(f"限定语：原文 {len(hedges_src)} 处（{'、'.join(hedges_src) or '无'}），改写后 {len(hedges_new)} 处（{'、'.join(hedges_new) or '无'}）")
    print(f"强断言：原文 {len(over_src)} 处（{'、'.join(over_src) or '无'}），改写后 {len(over_new)} 处（{'、'.join(over_new) or '无'}）")
    warn = []
    if len(hedges_new) < len(hedges_src):
        warn.append("限定语变少：结论可能被说得比原文更确定")
    if len(over_new) > len(over_src):
        warn.append("强断言变多：结论范围可能被放大（Peters & Chin-Yee 2025 发现的典型问题）")
    if lost_nums:
        warn.append("有数字丢失：具体结果可能被概括掉了")
    if new_nums:
        warn.append("出现原文没有的数字")
    print("\n" + ("\n".join("⚠ " + w for w in warn) if warn else "未发现明显走样。"))


def main(argv):
    if len(argv) >= 3 and argv[1] == "density":
        density(argv[2])
    elif len(argv) >= 4 and argv[1] == "compare":
        compare(argv[2], argv[3])
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
