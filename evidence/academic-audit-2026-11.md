# 学术写作 humanizer 审计（2026-11-11）

范围：GitHub 上 8 个学术方向的 humanizer（已浅克隆），加上作者本地装过的 3 个。用来核对的证据：本仓库两轮 GPT 评测、Peters & Chin-Yee 2025（LLM 总结论文时把结论说大）、Clark 等 2026（后训练导致信息压缩）、检测器公开资料（`references/detectors.md`）。

## 总评

| 项目 | 语言 | 质量 | 一句话 |
|---|---|---|---|
| matsuikentaro1/humanizer_academic | 英（医学） | 高 | 作者自己发表过 PubMed 用词研究；有「因果断言过强」「人为压缩的表达」「主语和动词要搭配」「别把连接词删过头」等少见且有依据的条目 |
| AIScientists-Dev/academic-humanizer | 英（含 NSF/NIH 基金） | 高 | 核心是「每个结论配数字、图表或引用，动词强度不超过证据」，并单列「这些别改过头」 |
| YouCun-Official/paper_llm_style_review | 英 | 高（思路） | 把「AI 味」拆成论文质量问题：动机、记号、列表、引用与结论是否匹配、实验叙事 |
| qingshanliuci/cnki-aigc---skill | 中（知网） | 中 | 实战经验诚实，劝退「降到 5% 以下」，反对换同义词、反对删光限定语；但依据只有一篇论文，句长分布的说法没有出处 |
| chi111i/BypassAIGC | 中英 | 中 | 名字叫 Bypass，实际提示词要求不补事实、术语不动，写得比名字靠谱；问题在长短句要求、破折号一刀切、字数硬约束，以及把前文改写结果当后文的风格参考 |
| cangtianhuang/humanizer-academic-zh（本地已装） | 中 | 中 | 「文体标定」表实用；但「原文没有破折号就加 1–2 处」「短句有力」是在制造节奏，示例里还有原文没有的访谈细节 |
| Yezery/aigc-down-skill | 中 | 低 | 和下一个项目约一半的行完全相同；配额式规则多 |
| redbaronyyyyy-eng/humanizer-zh-academic | 中 | 低 | 同上；两个项目都声称自己做过「AIGC 率从 >50% 降至 11%」的实验 |
| xiaofenggan01/aigc-reduce | 中 | 低（证据） | 检测原理文档里一大批精确数字（知网 3.0 准确率 98.6%、万方用 GPT+BERT+XGBoost、引用密集型误判率 12.3%……），唯一出处是一份没写作者和链接的「研究报告」；附大张同义词替换表 |
| wentor chinese-text-humanizer（本地装过） | 中 | 低 | 配额式规则（「本文」每页 ≤2 次、四字格每段 ≤1–2 个、段落 3 句和 7 句交替）；示例改写加进了原文没有的论断 |
| voidborne-d humanize-chinese（本地已装） | 中 | 中低 | 通用清单；学术部分建议「结论太完整就补上局限或不确定」，没有依据时等于编造局限 |

## 反复出现的问题

1. **配额。** 「AI 高频词每段 ≤2 个」「理论起笔的段落 ≤20%」「成语和口语每千字 2–3 处」「段落 3 句和 7 句交替」。这些数字没有任何来源，而且检测器学的是整体写法（Pangram 技术报告），数够配额改变不了这一点。
2. **长短句交替。** 除 AIScientists 和 YouCun 外几乎每个都有，matsuikentaro1 甚至把「先给每段制造 burstiness」放在改词之前。来历是 2023 年检测器的突发性指标（`evidence/rules-audit.md`）。
3. **同义词替换表。** aigc-reduce 的替换表最大。cnki-aigc 的实战结论是换同义词没用；Pangram 的「合成镜像」训练方式也说明，检测器不靠个别词判断。替换还容易破坏术语一致性，学术写作里这是硬伤。
4. **为了降 AI 率补内容。** 「承认局限与意外」「补上不确定」「加入具体细节」，原文没有时就是编造。几个中文项目给的示例本身就加进了原文没有的访谈细节和论断。
5. **没有出处的精确数字。** 98.6%、12.3%、「LLM 句长集中在 20–35 字，人类呈齐夫分布」。这类数字一旦被模型读进去，会被当成事实复述给用户。
6. **把降 AI 率当成目标。** 多数中文项目的卖点是「从 X% 降到 Y%」，每个案例都只是一篇论文、一个平台、一次检测。
7. **互相复制。** Yezery 和 redbaronyyyyy 有一半的行相同，都声称做过同一组降 AI 率实验。
8. **全都不分模型。** 没有一个区分稿子是 GPT、DeepSeek 还是 Claude 写的。

## 值得借鉴的

| 做法 | 来源 | 并入本仓库的位置 |
|---|---|---|
| 结论强度不超过证据：动词跟着证据等级走（shows / suggests / is consistent with） | AIScientists；matsuikentaro1 #22 | `academic-cnki.md`；与 `paper_check.py compare` 的强断言检查一致 |
| 合理的限定语保留，删的是叠加的多层限定 | cnki-aigc；matsuikentaro1 #17 | 同上 |
| 人为压缩的表达要展开，压缩过的语义关系要重新交代 | matsuikentaro1 #23、#28 | 和 Clark 等 2026 一致，对应 `shared.md` S14 |
| 主语和动词要搭配 | matsuikentaro1 | 对应无生命主语配有生命动词 |
| 逻辑连接词别删过头：关系真实存在就保留 | matsuikentaro1 #27 | `academic-cnki.md` |
| 「这些别改」清单：学科固定说法、方法部分的规范表达、文献引用句 | AIScientists Layer 3；cnki-aigc「不适用场景」 | `academic-cnki.md` |
| 理由轻重不一时，篇幅和重要性成正比 | Yezery / redbaronyyyyy 模式 3 | 已有（「允许不对称」） |
| 全文风格保持一点起伏，别统一成同一种腔 | Yezery 误区 3 | `academic-cnki.md` |
| 把「AI 味」拆成论文质量问题，先建「结论—证据」对照表 | YouCun；AIScientists Layer 4 | `academic-cnki.md` 模仿流程第 3 步 |

## 不采纳的

配额、长短句交替、同义词替换表、为降 AI 率补内容、没有出处的数字、「原文没有破折号就加」。
