# zh-deai：针对模型的中文 humanizer

先认出文字是哪个模型写的，再按那个模型的口癖去改。目前收了 GPT-6 / 6.1（Codex）、DeepSeek、Claude 三份清单，每条口癖附例子、改法和出处。可以装成 Claude Code 或 Codex 的 skill。

## 为什么要分模型

每个模型露馅的地方差得很远。

GPT-6.1 的文字满是防御：「这不代表……」「尚未验证」「我前面说得太绝对」，外加「收据」「验收」「本轮」「口径」这些自造名词。它聊天时 39% 的句子带否定词。

DeepSeek V4 爱造金句：「她笑了。不是温暖的笑。而是幸福的笑。」「这就够了。」评论区机器人张口就是「这条我收下了——」。

Claude 爱附和、爱用口语填充词：「你说得对」开头，「其实」「真的」穿插，结尾补一行「一句话：……」。

同一组词，在不同模型里的频率能差几十倍：

| 每 10 万字出现次数 | GPT-6.x | Claude |
|---|---|---|
| 尚未 | 32–160 | 2 |
| 不代表 / 不等于 / 不意味 | 13–79 | 6 |
| 收据 | 20–73 | 2 |
| 其实 | 0–2 | 23 |
| 你说得对 | 0–1 | 8 |
| 不是……而是 | 0–5 | 18 |

所以拿一张通用清单去「去 AI 味」，结果常常很好笑：改 GPT-6.1 的稿子时，删掉了它本来就很少用的破折号和「此外」，满篇的「不代表」「尚未」原样留着。我们调研的 47 个开源 humanizer 里，42 个用的正是这种通用清单，大多改编自 2023 年 GPT-4 时代的 Wikipedia 条目（详见 `evidence/oss-survey-2026-11.md`）。

## 我们的判断

模型会说人话。它说不好，是后训练养成的两种习惯：一是各家不同的口癖，二是为了短而压缩信息，把一句话塞进自造名词和单字动词里。2026 年 Clark 等人的实验显示，在强化学习里加长度惩罚，模型就会系统地选更短、更难懂的句式。所以这里的改法是按模型修口癖、把压缩的信息解开，口语化程度按场合定。各家 humanizer 里「长短句交替」「单句 40 字以内」「多加第一人称和感受」这类为骗检测器写的规则，我们都去掉了，理由见 `evidence/rules-audit.md`。

## 文件

```
SKILL.md                    触发条件和流程
gpt-nodefense/SKILL.md      GPT / Codex 常驻规则：去掉回复里的防御性表达
references/
  gpt-codex.md              GPT-6 / 6.1 与 Codex，从否定句堆叠讲起，附逐句标注的整段样本
  deepseek.md               DeepSeek V4 长文、评论区短句模板、R1 / V3 华丽文风
  claude.md                 Claude 中文
  claude-en.md              Claude 英文，写英文论文时用
  shared.md                 各家都有的套话
  academic-cnki.md          论文：知网、维普、万方
  detectors.md              Turnitin、Pangram、知网等检测器公开过哪些信息
  watermark.md              Claude 文本水印的原理和相关研究
scripts/
  scan.py                   按模型扫描口癖，输出命中位置
  patterns.json             扫描用的正则，编号对应 references
evidence/
  local-corpus-2026-11.md   本机 GPT-6.x 与 Claude 语料词频
  slopscore-2025.md         8 个模型同题英文语料的独有高频词
  oss-survey-2026-11.md     47 个开源 humanizer 的调研
  post-training-research.md 口癖和信息压缩从哪来：后训练相关研究
  rules-audit.md            各家 humanizer 规则逐条判定：哪些删、哪些留
  tools/                    重跑统计的脚本
triggers/                   候选的一段式修正提示（待测试）
SOURCES.md                  全部出处
```

## 安装

```bash
git clone https://github.com/skitse/zh-deai ~/.claude/skills/zh-deai
ln -s ~/.claude/skills/zh-deai ~/.codex/skills/zh-deai   # Codex
```

用 CC Switch 管理的话，放进 `~/.cc-switch/skills/zh-deai`。

### GPT 常驻去防御（gpt-nodefense）

`zh-deai` 用来改稿子；`gpt-nodefense` 用来约束 GPT 自己说话，装好后 GPT 的每条中文消息都按它来，直到你在对话里说「保留防御」或「#defense-on」。

```bash
cd ~/.claude/skills/zh-deai
python3 scripts/install_gpt_nodefense.py --dry-run   # 先看会写什么
python3 scripts/install_gpt_nodefense.py             # 安装
python3 scripts/install_gpt_nodefense.py --remove    # 撤销
```

安装脚本做三件事：

1. 在 `~/.codex/AGENTS.md` 写入 6 条核心规则。Codex 跑的都是 GPT，所以每次对话都生效。
2. 在 `~/.claude/CLAUDE.md` 写入同一组规则，附带条件「只在你是 GPT 系列模型时生效」，覆盖用 CC Switch 让 Claude Code 调 GPT 的情况。
3. 把 `gpt-nodefense` 软链接到 `~/.codex/skills` 和 `~/.claude/skills`，完整规则和例子在里面。

规则块放在两行标记之间，文件里原有的内容原样保留。只装 skill、不写 AGENTS.md 的话，长对话后几轮 GPT 会慢慢回到防御腔；molang163 实测 30 轮里有 3 轮回退，写进 AGENTS.md 后是 0 轮。

## 用法

对 Claude Code 或 Codex 说「这段一股 Codex 味，改成人话」「把这段 DeepSeek 写的去 AI 味」「论文这章降一下 AI 率」。

单独扫描一份稿子：

```bash
python3 scripts/scan.py draft.txt
```

## 证据来源

公开资料包括 linux.do 口癖帖、molang163 公开的 GPT-6.1-Sol 原版回答、DeepSeek V4 用户反馈汇总、bili-ai-killer 的 DeepSeek 句式规则、slop-score 的同题语料、Anthropic 公开的系统提示词、Arize 对 Claude Opus 5 / 5.5 的人工标注、HC3 与 CCL 等中文 AI 文本研究。

本机语料是作者自己的 Codex（GPT-6-Luna、6-Astra、6.1-Terra、6.1-Sol）和 Claude（Opus / Sonnet / Haiku 5.5）会话，约 63 万汉字，只统计模型写给用户的中文。原文留在本机，仓库里只放汇总数字和脚本。

每条口癖都标了证据来源；证据弱或互相矛盾的，条目里会写明。

## 边界

这个仓库只管文风。判断文字由谁写、能否通过知网或 Turnitin、去除模型水印，都在范围之外；`references/detectors.md` 和 `references/watermark.md` 讲清楚了这些机制，供参考。改写时保留原文的事实、数据和引用。

## 维护

模型一更新，口癖就会变：GPT-5.x 的「砍一刀」「压实」，到 6.x 已经很少见。更新步骤：

1. 用 `evidence/tools/` 的脚本在新语料上重跑，看哪些词升、哪些词降。
2. 到 linux.do、小红书搜「口癖」「说人话」「X 味」看新帖。
3. 改 reference 和 `scripts/patterns.json`，在 `evidence/` 里加一份新日期的统计。

欢迎提交新模型（Kimi、豆包、Gemini、Qwen）的清单，附上原始输出或统计。

## 许可

MIT
