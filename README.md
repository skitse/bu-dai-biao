# zh-deai：针对模型的中文 humanizer

**先认是哪个模型写的，再按那个模型的口癖改。** 支持 GPT-6 / 6.1（Codex）、DeepSeek、Claude，每条口癖都有例子、改法和出处。可以作为 Claude Code / Codex skill 使用。

大多数 humanizer 用同一张通用清单对付所有模型，「变换句长」「少用连接词」「别用破折号」之类。这解决不了问题，因为每个模型不像人的地方不一样：

| | GPT-6 / 6.1 | DeepSeek V4 | Claude |
|---|---|---|---|
| 主要问题 | 防御性写作、自造名词 | 修辞过度、短句排比 | 附和、填充词、排版 |
| 典型 | 「不代表」「尚未」「收据」「我前面说得太绝对」 | 「不是……而是……」「这就够了」 | 「你说得对」「其实」「一句话：」 |
| 「尚未」每 10 万字 | 32–160 | — | 2 |
| 「其实」每 10 万字 | 0–2 | — | 23 |

（数字来自作者本机语料，见 `evidence/`。）

通用规则在不同模型上还会起反作用：给 GPT-6 写「多表达不确定性」，它会更防御；给 DeepSeek V4 列禁词表，它会把禁词当提示词，用得更多。

## 为什么按模型分

- **GPT-6 / 6.1（Codex）**：防御性写作。「不代表」「不能证明」「尚未」「未运行」「我前面说得太绝对」，加上「收据」「验收」「本轮」「口径」这类自造名词。
- **DeepSeek**：修辞过度。V4 是「不是……而是……」拆成短句、「这就够了」、「像在说今天的天气」；R1 是量子、熵、拓扑、精确到 0.01 公分。
- **Claude**：轻一些。「你说得对」开头、「其实」「真的」、「一句话：」收尾、加粗和冒号小标题。

一套通用规则对付不了这三种，有时还互相冲突：给 GPT-6 的提示写「多表达不确定性」，只会让它更防御。

## 结构

```
SKILL.md                    触发条件和流程（短）
references/
  gpt-codex.md              GPT-6/6.1 与 Codex，最细
  deepseek.md               DeepSeek R1/V3 与 V4/V4.1
  claude.md                 Claude
  shared.md                 各家都有的套话
  claude-en.md              Claude 英文口癖（写英文论文用）
  academic-cnki.md          论文场景：知网、维普、万方
  detectors.md              Turnitin、Pangram、知网等检测器公开了什么
  watermark.md              Claude 文本水印是什么、能检测到什么
scripts/
  scan.py                   按模型扫描口癖（不是检测器）
  patterns.json             扫描用的正则，编号对应 references
evidence/
  local-corpus-2026-11.md   本机 GPT-6.x 与 Claude 语料的词频统计
  tools/                    重跑统计的脚本
SOURCES.md                  全部出处
```

## 安装

```bash
git clone <仓库地址> ~/.claude/skills/zh-deai
# Codex
ln -s ~/.claude/skills/zh-deai ~/.codex/skills/zh-deai
```

用 CC Switch 管理的话，放进 `~/.cc-switch/skills/zh-deai`，再按 CC Switch 的方式挂载。

## 用法

直接说「把这段去 AI 味」「这段一股 Codex 味，改成人话」「论文这章降一下 AI 率」。

单独扫描：

```bash
python3 scripts/scan.py draft.txt
```

## 证据怎么来的

- 公开资料：linux.do、V2EX 讨论帖，Anthropic 公开的系统提示词，ICML 2025 论文 *Idiosyncrasies in Large Language Models*，HC3、CCL 2023 等中文 AI 文本研究，DeepSeek V4 用户反馈汇总，以及几个开源去 AI 味仓库。见 `SOURCES.md`。
- 本机语料：作者自己的 Codex（GPT-6-Luna、6-Astra、6.1-Terra、6.1-Sol）和 Claude（Opus/Sonnet/Haiku 5.5）会话，约 63 万汉字，只统计模型写的中文。原文不入库，只放汇总数字和脚本。见 `evidence/local-corpus-2026-11.md`。

没有依据的说法不收。证据弱或互相冲突的，在条目里写明。

## 网上针对单个模型的项目

大多数 humanizer 用的是一张通用清单（多半来自 Wikipedia「Signs of AI writing」），不分模型。针对单个模型、而且有证据的不多，这几个被本仓库吸收了：

- **GPT-6.1**：[molang163/chinese-natural-reply](https://github.com/molang163/chinese-natural-reply)，从两个月 GPT-6.1-Sol 中文对话里整理防御性回复，带盲评。
- **GPT-5.x**：linux.do「[gpt-5.x (codex) 中文口癖收集](https://linux.do/t/topic/1768077)」及其衍生的[负面清单](https://linux.do/t/topic/1924570)。
- **DeepSeek V4**：[DeepSeek V4 用户反馈汇总](https://github.com/victorchen96/deepseek_v4_rolepaly_instruct/blob/main/deepseek_v4_feedback_report_20260520.md)。
- **Claude（英文）**：[archiewood/claudeisms](https://github.com/archiewood/claudeisms)（Claude Code 输出对比 Stack Overflow 的词频）、[claudisms.ai](https://claudisms.ai/)、[smixs 的 Claudisms 2026 field guide](https://github.com/smixs/awesome-claude-output-styles/blob/main/docs/claudisms-2026.md)、[Arize 对 Opus 5 / 5.5 的人工标注评测](https://arize.com/blog/anthropic-says-it-fixed-claudes-writing/)、[AshwinSathian/humanize-writing-skill](https://github.com/AshwinSathian/humanize-writing-skill) 的 `claude-tics.md`。
- **知网**：[qingshanliuci/cnki-aigc---skill](https://github.com/qingshanliuci/cnki-aigc---skill)，一篇本科论文 20.6% → 10.1% 的实战经验。

Claude 的中文口癖没有找到专门的项目，`claude.md` 用的是本机统计、官方系统提示和英文资料迁移。

## 不做什么

- 不判断文本是不是 AI 写的。
- 不承诺能过知网、维普、万方或任何检测器。
- 不编造事实、数据、文献。
- 不提供去除模型水印的方法（见 `references/watermark.md`）。

## 维护

模型更新后口癖会变（GPT-5.x 的「砍一刀」「压实」到 6.x 基本没了）。更新方法：

1. 用 `evidence/tools/` 的脚本在新语料上重跑，看哪些词升了、哪些降了。
2. 去 linux.do 搜「口癖」「说人话」看新帖。
3. 改 reference 和 `scripts/patterns.json`，在 `evidence/` 里加一份新日期的统计。

## 许可

MIT
