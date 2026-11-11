#!/usr/bin/env python3
"""按模型扫描中文文本里的 AI 口癖。

用法：
    python3 scripts/scan.py 文件.txt            # 汇总 + 每条命中
    python3 scripts/scan.py 文件.txt --summary  # 只看汇总
    cat 文件.txt | python3 scripts/scan.py -

输出每个模型的加权命中密度（每千字），以及每条命中的行号和上下文。
这是改写辅助工具，不是 AI 检测器：分数高只说明某个模型的口癖多，不说明文本是谁写的。
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_patterns():
    data = json.loads((HERE / "patterns.json").read_text(encoding="utf-8"))
    data.pop("_note", None)
    for group in data.values():
        for p in group:
            p["rx"] = re.compile(p["re"], re.M)
    return data


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    src = argv[1]
    text = sys.stdin.read() if src == "-" else Path(src).read_text(encoding="utf-8")
    text = strip_code(text)
    summary_only = "--summary" in argv
    n_cjk = len(re.findall(r"[一-鿿]", text)) or 1
    lines = text.splitlines()
    starts, pos = [], 0
    for ln in lines:
        starts.append(pos)
        pos += len(ln) + 1

    def line_of(i):
        lo, hi = 0, len(starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if starts[mid] <= i:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    patterns = load_patterns()
    results = {}
    for model, group in patterns.items():
        hits = []
        score = 0
        for p in group:
            for m in p["rx"].finditer(text):
                hits.append((p["id"], line_of(m.start()), m.group(0), p["hint"], m.start(), m.end()))
                score += p["weight"]
        results[model] = (score / n_cjk * 1000, hits)

    print(f"汉字数：{n_cjk}")
    print("模型        加权密度(每千字)  命中数")
    for model, (dens, hits) in sorted(results.items(), key=lambda x: -x[1][0]):
        print(f"{model:<12}{dens:>14.1f}{len(hits):>8}")
    if summary_only:
        return 0
    for model, (dens, hits) in results.items():
        if not hits:
            continue
        print(f"\n== {model}（对照 references/{'gpt-codex' if model == 'gpt-codex' else model}.md）")
        hits.sort(key=lambda h: (h[0], h[4]))
        for pid, ln, word, hint, s, e in hits:
            ctx = text[max(0, s - 15):e + 15].replace("\n", " ")
            print(f"  [{pid}] 第{ln}行 「{word}」 {hint}  …{ctx}…")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
