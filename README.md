# zh-deai：按模型去中文 AI 味

一个 Claude Code / Codex skill。GPT、DeepSeek、Claude 的中文口癖各不一样，这个 skill 先认模型，再按那个模型的清单改。每条口癖都有例子、改法和出处。

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
  academic-cnki.md          论文场景：知网、维普、万方
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

## 不做什么

- 不判断文本是不是 AI 写的。
- 不承诺能过知网、维普、万方或任何检测器。
- 不编造事实、数据、文献。

## 维护

模型更新后口癖会变（GPT-5.x 的「砍一刀」「压实」到 6.x 基本没了）。更新方法：

1. 用 `evidence/tools/` 的脚本在新语料上重跑，看哪些词升了、哪些降了。
2. 去 linux.do 搜「口癖」「说人话」看新帖。
3. 改 reference 和 `scripts/patterns.json`，在 `evidence/` 里加一份新日期的统计。

## 许可

MIT
