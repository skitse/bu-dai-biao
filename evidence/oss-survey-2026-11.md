# 开源 humanizer / 去 AI 味项目调研（2026-11-11）

用 `gh search repos` 搜了 24 组关键词（humanizer、去AI味、降AIGC、说人话、slop、claudisms、gpt-isms、unslop 等），得到 758 个仓库。按相关性和星数挑出 47 个读了 README，再扫它们的文件树找按模型命名的文件，最后用 GitHub 代码搜索找 `claude-isms`、`gpt-isms`、`DeepSeek味`、`kimi味`、`model-specific tells` 之类的文件。

## 结论

47 个项目里，**按模型区分处理的只有 5 个**。其余 42 个用同一张清单处理所有模型，清单多数来自 Wikipedia「Signs of AI writing」或 blader/humanizer 的 24 条。星数最高的几个全在后一类：blader/humanizer（6.8 万星）、op7418/Humanizer-zh（2.3 万）、hardikpandya/stop-slop（1.9 万）、petergyang/no-ai-slop（1.3 万）。

这些通用清单的条目大多来自 2023—2025 年 GPT-4/4o 的英文输出（delve、tapestry、em dash、rule of three）。拿它们去改 GPT-6.1 的中文，命中的主要是各家共有的套话，GPT-6.1 自己的防御腔和自造名词基本漏掉。

## 按模型处理的项目

| 项目 | 针对 | 做法 | 证据 |
|---|---|---|---|
| [molang163/chinese-natural-reply](https://github.com/molang163/chinese-natural-reply) | GPT-6.1-Sol 中文 | 从两个月真实对话整理防御性回复，写成规则 | 16 题盲评，公开全部原版回答 |
| [makoMakoGo/fish-claude](https://github.com/makoMakoGo/fish-claude) `gpt-isms-stamp-out` | GPT-5.4 中英文 | 七级清单：不是而是、把字句、结尾推销、谄媚、黑话、虚假确定、标题括号注释 | 无测试，条目和 linux.do 口癖帖高度重合 |
| [ItsssssJack/SlopMonster](https://github.com/ItsssssJack/SlopMonster) | 跨模型 | 先扫描，再交给**另一家**模型改第二遍：Claude 写的交给 Codex，GPT 写的交给 Claude | 无量化 |
| [athola/claude-night-market](https://github.com/athola/claude-night-market) `model-specific-tells.md` | GPT / Claude / Gemini 的**代码** | 按模型调整代码审查重点：GPT 爱编造 API，Claude 爱漏掉边界情况，Gemini 爱写错控制流 | 引用 Sonar 排行榜的缺陷率 |
| [AshwinSathian/humanize-writing-skill](https://github.com/AshwinSathian/humanize-writing-skill) `claude-tics.md` | Claude Opus 5 / Fable 5.1 英文 | 单列一份 Claude 习惯表，带证据分级 | Anthropic 提示词指南、*The Economist* 研究、社区报告 |

## 有按模型的数据，但不是 humanizer

| 项目 | 内容 |
|---|---|
| [sam-paech/slop-score](https://github.com/sam-paech/slop-score) | 同一批 300 道英文写作题，公开了 Claude Sonnet 4/4.5、GPT-4o、GPT-5-mini、DeepSeek R1/V3.2、Gemini 2.5 Flash、Kimi K2 的全部原始回答。本仓库用它算了各模型的独有高频词，见 `slopscore-2025.md`。 |
| [sam-paech/slop-forensics](https://github.com/sam-paech/slop-forensics) | 生成每个模型的 `slop_profile__{model}.json`（过度使用的词、二元组、三元组）。 |
| [archiewood/claudeisms](https://github.com/archiewood/claudeisms) | Claude Code 输出对比 Stack Overflow 评论的词频。 |
| [Logic259/bili-ai-killer](https://github.com/Logic259/bili-ai-killer) | B 站评论区 AI 机器人识别插件，里面有一套「DeepSeek 味」句式规则（区分 DeepSeek 1.0 和 2.0），已收进 `deepseek.md`。 |
| [devswha/patina](https://github.com/devswha/patina) | 韩语 humanizer，`docs/research/ko-gpt-miss-taxonomy-v1.md` 专门整理 GPT 韩语输出里通用规则漏掉的问题。 |
| [ilyautov/humanizer-ru](https://github.com/ilyautov/humanizer-ru) | 俄语评测语料按来源模型命名（`*_gpt_*`、`*_claude_*`、`*_gemini_*`、`gpt56_*`），规则本身不分模型。 |
| [seyedehsanhadi/sloptrim](https://github.com/seyedehsanhadi/sloptrim) | 本地 AI 腔检测器，按来源模型报告了检出率：GPT-4o AUC 0.943，Claude 3.5 Sonnet 0.842。说明同一套规则对 Claude 的文字抓得少。 |
| [hexiecs/talk-normal](https://github.com/hexiecs/talk-normal) | 通用的精简提示词，但示例和测试都在 GPT-4o-mini、GPT-5.4 上做，专门点名「如果你要我还可以……」。 |

## 自称针对模型、实际是通用清单

[happycapy-ai/Happycapy-skills](https://github.com/happycapy-ai/Happycapy-skills) 的 `claude-isms.md` 标题是「Claude-Specific Vocabulary Database」，内容是 however、therefore、furthermore、moreover、I'd be happy to……没有出处，也没有和别的模型对比。这些词按 Sun et al. 2025 和 slop-score 数据，更像 GPT-4o 的特征（见 `slopscore-2025.md`：moreover、additionally 是 GPT-4o 的独有高频词）。

## 其他语言的 humanizer

韩语 epoko77-ai/im-not-ai（6500 星）、俄语 ilyautov/humanizer-ru、德语 marmbiz/humanizer-de、日语 iKora128/stop-ai-slop-jp、土耳其语 yucezerey/turkish-anti-ai-skill、繁中 Raymondhou0917/speak-human-tw。这些都按**语言**定制（翻译腔、本国公文腔），模型维度一律不分。

## 学术方向

| 项目 | 说明 |
|---|---|
| [qingshanliuci/cnki-aigc---skill](https://github.com/qingshanliuci/cnki-aigc---skill) | 知网实战，见 `references/detectors.md` |
| [YouCun-Official/paper_llm_style_review](https://github.com/YouCun-Official/paper_llm_style_review) | 把「AI 味」拆成论文质量问题（动机、公式、列表、引用、实验叙事），不分模型 |
| [matsuikentaro1/humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic) | 医学论文，引用 PubMed 词频研究（ChatGPT 后 delve 等词的增长） |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer)、xiaofenggan01/aigc-reduce、redbaronyyyyy-eng/humanizer-zh-academic、Yezery/aigc-down-skill | 通用清单 |

## 可借鉴的做法

1. **用另一家模型改第二遍**（SlopMonster）。理由和本仓库一致：同一个模型改自己的稿子，会用同样的口癖替换口癖。
2. **公开原始输出做评测**（molang163、slop-score）。有了原文，别人才能复查结论。
3. **规则写成正面描述，少列禁词**（smixs 的 no-slop 风格、DeepSeek V4 反馈里的「禁词表当提词器」）。模型看到禁词反而更容易写出来。
