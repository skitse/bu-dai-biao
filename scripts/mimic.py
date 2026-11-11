#!/usr/bin/env python3
"""反着用：把一句话包装成某个模型的腔调。

用法：
    python3 scripts/mimic.py gpt "冷藏三天内吃完" --topic 剩饭
    python3 scripts/mimic.py codex "登录接口已经修好" --topic 登录
    python3 scripts/mimic.py deepseek "早点睡" --topic 熬夜
    python3 scripts/mimic.py claude "先把流程固定下来" --topic 效率
    python3 scripts/mimic.py all "早点睡" --topic 熬夜 --explain

参数：
    模型      gpt（GPT-6.x 聊天）、codex（GPT-6.x 干活汇报）、deepseek、claude、all
    一句话    你真正想说的内容，会被埋进口癖里
    --topic   话题词，默认「这件事」
    --explain 每句后面标出用到的口癖编号（对应 references 里的编号）
    --seed N  固定随机种子，方便复现

每个句式都取自 references 里记录的原句或社区样本，不另造。
用途：段子和彩蛋、给检测器或评测造对照样本、练习认口癖。
输出离线生成，不调用任何模型；想要更自然的版本，让模型照 SKILL.md「反着用」一节写。
"""
import argparse
import random
import sys

# 每个模型：按段落位置分组，每组随机取一句。(模板, 口癖编号)
TEMPLATES = {
    "gpt": [
        [  # 开头：先否定一个没人说过的说法
            ("你说得不完全不对，但这并不能直接说明{t}已经有定论。", "GPT-N1 GPT-A2"),
            ("不建议一上来就把{t}想得太简单。", "GPT-N1"),
            ("没有统一的答案，但可以先这样理解：", "GPT-N1"),
        ],
        [  # 核心结论，带预先否定
            ("{c}；但这不代表所有情况都适用。", "GPT-A2 GPT-I1"),
            ("{c}，不过这不等于可以完全放心。", "GPT-A2"),
            ("更准确地说，我前面说得太绝对了：{c}，只是仅凭目前的信息还不能证明它适用于你的情况。", "GPT-A1 GPT-A4 GPT-A2"),
        ],
        [  # 划边界、留尾巴
            ("能确认的是：{c}；至于{t}的其他细节，目前尚未验证。", "GPT-A4 GPT-A5"),
            ("没有证据表明{t}一定会出问题，但仍需结合实际情况判断。", "GPT-A6 GPT-A5"),
        ],
        [  # 否定排比
            ("换言之，现在不能断言、不能保证、不能仅凭这一点就当作定论。", "GPT-N3"),
            ("不用焦虑，不必硬撑，也不要一次改太多。", "GPT-N3 GPT-N5"),
        ],
        [  # 不是……而是……
            ("我不是说不能做，而是不能只看表面。", "GPT-N2"),
            ("这不是说{t}不重要，而是别把它当成唯一的标准。", "GPT-N2 GPT-N5"),
        ],
        [  # 结尾
            ("还需要更多证据，才能更全面地说明这到底是不是那么一回事。", "GPT-A5"),
            ("别把「一次没出事」当作「一直不会出事」。", "GPT-N5 GPT-I2"),
        ],
    ],
    "codex": [
        [
            ("我会先把{t}的验收口径对齐，再动代码。", "GPT-F1 GPT-C2 GPT-C5"),
            ("我先说结论，免得说得太绝对：", "GPT-A1"),
        ],
        [
            ("{c}；但这不代表线上已经没有问题。", "GPT-A2 GPT-I1"),
            ("纸面上{c}，但仅凭本地复现还不能证明根因已经消除。", "GPT-A4 GPT-A2"),
        ],
        [
            ("本轮未修改其他模块，也未运行完整测试；配置保持不变。", "GPT-A3 GPT-C4 GPT-I1"),
            ("均未改动{t}以外的文件，无需重做迁移。", "GPT-A3"),
        ],
        [
            ("收据：改动 1 处，新增断言 2 条，其余尚未覆盖。", "GPT-C1 GPT-A5"),
            ("结论限定于当前分支；仍需在预发环境验证。", "GPT-A4 GPT-A5 GPT-I1"),
        ],
        [
            ("下一步我会只补测试，不扩大改动范围、不顺手重构、不碰无关依赖。", "GPT-F1 GPT-N3"),
        ],
    ],
    "deepseek": [
        [
            ("{t}。不是小事。而是一件需要认真对待的事。", "DS-A1 DS-A4"),
            ("看完只想说一句：最难的不是知道，是做到。", "DS-C3 DS-C5"),
            ("这条我收下了——", "DS-C1"),
        ],
        [
            ("「{c}」——这才是关键。", "DS-C8 DS-A6"),
            ("{c}——比硬扛实在得多。", "DS-C7"),
        ],
        [
            ("表面上是在问{t}，本质上是在问自己能不能稳稳接住生活。", "DS-C9 DS-A8"),
            ("你以为是在纠结{t}，其实是在和自己较劲。", "DS-C12"),
        ],
        [
            ("不慌，不急，不硬撑，就{c}。", "DS-A5"),
            ("{t}的熵，在那一刻悄悄降低了 0.37 个单位。", "DS-B1 DS-B2"),
        ],
        [
            ("这就够了。", "DS-A2"),
            ("这大概就是所谓的成长吧。", "DS-C14"),
        ],
    ],
    "claude": [
        [
            ("你说得对，这个问题问得很好。", "CL-A1 CL-A2"),
            ("好，先说结论。", "CL-C5 CL-C1"),
        ],
        [
            ("这其实不是{t}的问题，是习惯的问题。", "CL-F CL-B1"),
            ("问题不在{t}本身，在你怎么安排它。", "CL-F"),
        ],
        [
            ("**{c}。**", "CL-D1"),
            ("核心就一句话：{c}。", "CL-C1 CL-D2"),
        ],
        [
            ("说实话，这比看起来简单——真的。", "CL-B2 CL-B3 CL-D3"),
            ("另外，最后一腿其实很直接：照着做就行。", "CL-C2 CL-E1 CL-B1 CL-B3 CL-D2"),
        ],
        [
            ("要不要我帮你列个清单？", "CL-C4"),
            ("需要的话说一声，我再展开。", "CL-C4"),
        ],
    ],
}

NAMES = {"gpt": "GPT-6.x 聊天", "codex": "GPT-6.x 干活（Codex）", "deepseek": "DeepSeek", "claude": "Claude"}


def render(model, claim, topic, rng, explain):
    claim = claim.rstrip("。；;.！!")
    out = []
    for group in TEMPLATES[model]:
        tpl, tags = rng.choice(group)
        s = tpl.format(c=claim, t=topic)
        out.append(f"{s}〔{tags}〕" if explain else s)
    return "".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="把一句话包装成某个模型的腔调")
    ap.add_argument("model", choices=list(TEMPLATES) + ["all"])
    ap.add_argument("claim", help="你真正想说的那句话")
    ap.add_argument("--topic", default="这件事")
    ap.add_argument("--explain", action="store_true")
    ap.add_argument("--seed", type=int)
    args = ap.parse_args(argv)
    rng = random.Random(args.seed)
    models = list(TEMPLATES) if args.model == "all" else [args.model]
    for m in models:
        text = render(m, args.claim, args.topic, rng, args.explain)
        if len(models) > 1:
            print(f"【{NAMES[m]}】")
        print(text)
        if len(models) > 1:
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
