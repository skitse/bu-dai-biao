# 文本水印（Claude 及其他）

这份只讲事实：水印是什么、哪些模型有、能检测到什么。本仓库不提供去水印的方法和工具。

## Claude 从 2026 年 8 月起有文本水印

- **为什么**：欧盟《人工智能法》第 50 条要求标注 AI 生成内容。Anthropic 和约 190 家机构在 2026 年 7 月签了欧盟《AI 生成内容透明度行为准则》。Anthropic 说目前没法按地区区分，所以全球统一加。<https://www.anthropic.com/news/claude-text-watermark>
- **哪些模型**：2026 年 8 月 2 日后发布的模型默认带；9 月 1 日加入 Claude Fable 5.1、Mythos 5.1；11 月 3 日起 Mythos 5、Opus 4.7、Sonnet 4.6 也开始带（各报道对旧模型名单说法不一，以 Anthropic 的 release notes 为准）。<https://platform.claude.com/docs/en/release-notes/overview>
- **方法**：Google DeepMind 2024 年发表在 *Nature* 上的 SynthID-Text 的一个版本，属于 Scott Aaronson 2022 年提出的那一类方法。

## 它怎么工作（和「近义词 AB 库」不是一回事）

常见的想象是：厂商准备一张近义词对照表（「灰」和「阴」之类），让模型偏向其中一边，再统计比例。Claude 用的不是这种。

按 Anthropic 的说明：模型每次选下一个词时，本来就要在几个差不多的候选里随机挑一个。加水印后，挑的方式还是随机的，但随机数不再来自普通的随机数生成器，而是由**一把密钥加上前面几个词**算出来。

由此可知：

- **没有固定的词表。** 同一个位置选「灰」还是「阴」，取决于前文。不存在「全文 A 词用多了」这种可以数出来的比例，也就没有可以对照替换的 AB 库。
- **只在可选可不选的地方起作用。** 事实性的词（「Principia」后面只能是「Mathematica」）、代码、算式没有水印。
- **文本越长越容易检测**，短文本信息不够。
- **读者看不出来**：不加字符、不加 token，不影响质量（DeepMind 在 Gemini 线上流量和人工对照实验中都没测到质量差异）。
- **不含身份信息**，不能追溯到具体用户、组织或对话。

另一类常被讨论的方案是 Kirchenbauer 等人 2023 年的「绿名单」水印：按前一个词把词表随机分成绿、红两组，偏向绿组。它的分组同样随前文变化，也不是固定词表。

## 能检测到什么

- 只能回答「这段文字有多大可能有 Claude 参与」。**分不清是 Claude 写的还是 Claude 大改过的**，也不能证明是人写的。
- **翻译**：Claude 翻译的文本带水印，因为每个词都是 Claude 选的。
- **校对**：只改语法标点时，水印只能落在那几处修改上，通常太少，检测不到。改得越多，水印越多。
- **人工改写**：Anthropic 的说法是，轻度编辑大概率去不掉；每个词都换掉的完全重写可以去掉，但那时也很难再说它是 AI 生成的。
- **检测接口**：私有预览，只开放给欧盟法规要求的机构（监管、执法、媒体、事实核查、独立研究者、教育机构等）和有合规义务的企业。普通人和一般查重网站目前查不了。BleepingComputer 报道称市面上的「去水印工具」几乎都证明不了自己有效。
- **采样参数**：Sonnet 4.6 上把 temperature、top_p、top_k 设成非默认值，输出可能不带水印（文档原话是「might not carry」）。<https://platform.claude.com/docs/en/build-with-claude/text-watermark>

## 研究文献：水印经过改写、翻译后还在不在

以下是公开论文的结论摘要，用来理解水印能证明什么、不能证明什么。各篇论文的攻击设置和指标不同，数字不能直接互相比较。**没有任何一篇公开论文测的是 Anthropic 的水印**（密钥不公开），下面多数测的是 Google 的 SynthID-Text 或学术方案。

| 研究 | 测的方案 | 主要结论 |
|---|---|---|
| Dathathri et al., *Nature* 634 (2024)，SynthID-Text 原论文 <https://doi.org/10.1038/s41586-024-08025-4> | SynthID-Text | 在约 2000 万次 Gemini 回答上没测到质量差异。二手报道称原文承认：被另一个模型改写、翻译、大幅编辑后信号减弱，短文本和事实性文本本来就弱。 |
| Kirchenbauer et al., *On the Reliability of Watermarks for LLMs*, ICLR 2024 <https://arxiv.org/abs/2306.04634> | 绿名单（KGW） | 改写在 200–300 token 时看似有效，但文本到 600 token 时，经 GPT 和 DIPPER 改写的文本 AUC 回升到 0.9 以上；改写会漏掉原文的 n-gram 片段。强人工改写后平均约 800 token 可检出（误报率 1e-5）。**文本越长，改写越难完全去掉水印。** |
| He et al., *Can Watermarks Survive Translation?*, ACL 2024 <https://arxiv.org/abs/2402.14007> | KGW、UW、SIR | 提出「跨语言水印去除攻击」：在另一种语言里生成再翻译回来，检测 AUC 降到接近随机。作者同时提出防御方法 X-SIR（按跨语言语义聚类词表，让词翻译后仍落在同一组），据二手页面称把 AUC 从 0.67 提到 0.88。 |
| Han et al., *Robustness Assessment and Enhancement of Text Watermarking for Google's SynthID*, 2025 <https://arxiv.org/abs/2508.20228> | SynthID-Text | 改写、复制粘贴混排、回译都会显著降低可检测性；**以中文为中转语言的回译影响最大**。据摘要类来源，中度改写下真阳性率从 0.998 降到约 0.5。作者提出增强方案 SynGuard，F1 平均提高 11.1%。 |
| *Google's LLM Watermarking System is Vulnerable to Layer Inflation Attack*, ICLR 2026；arXiv 2603.03410 | SynthID-Text | 从理论上指出 SynthID 的均值打分函数存在结构性弱点。 |
| *Vaporizer*, arXiv 2605.07481 | 多种方案含 SynthID | 主流方案都怕保义改写；SynthID 比部分学术方案需要更大幅度的改动。 |
| *AI Watermark Evidence Fails Forensic Readiness*, arXiv 2607.16010 | 多种方案含 SynthID | SynthID 在 59 篇原本可检出的文本里，改写后 58 篇检不出；在干净文本上误报率 5.4%。作者结论：水印目前不够格当法证证据。 |

### 这些研究说明了什么

- **水印对「意思不变、措辞全换」的改动普遍脆弱**，这是领域共识，Anthropic 自己也承认（「完全重写可以去掉」）。所以它的定位是辅助信号，不是证据。
- **反过来，检不出水印也不说明是人写的。** 检测器从来不会根据「没水印」判定人类作者。
- **防御在跟进。** X-SIR、SynGuard 等专门针对翻译和改写做加固；SynthID 和各家实现会持续更新，论文里的结论会过时。厂商实际部署的版本和参数都不公开。
- **误报真实存在**（上表最后一行 5.4%），所以无论检出与否，都需要结合其他证据。
- 对 AIGC 检测（知网、Turnitin）来说，这些都不相关：它们用的是分类器，不读水印（见 `detectors.md`）。

本仓库只收录这些研究的结论，不提供实现。

## 其他厂商

Anthropic 说其他签了同一份准则的大厂也会上各自的水印，密钥和方法各不相同。Google 的 SynthID-Text 早在 2024 年就用在 Gemini 上并开源了。GPT、DeepSeek 的情况本仓库没有核实，不下结论。

## 对写论文的影响

- 自己写、让 Claude 改语法和措辞：留下的水印很少，Anthropic 自己也说可能检测不到。
- 让 Claude 整段生成或翻译：会带水印。
- 水印和 AIGC 检测是两回事：知网、维普、万方、Turnitin 用的是自己训练的分类器（见 `detectors.md`），拿不到 Anthropic 的密钥，检测不了 Claude 水印。
- 最稳妥的做法是按学校规定如实声明 AI 的使用范围。去 AI 味改的是文风，不改变「这段文字由谁写」这个事实。
