# 口癖从哪来：后训练相关研究

本仓库的基本判断：模型会说人话，它说不好是后训练养成的习惯。问题集中在两处，一是各家不同的口癖，二是为了短而压缩信息。下面是支撑这个判断的研究，以及厂商自己给出的修正提示。

## 1. 压缩：后训练让模型偏爱短而难懂的句式

**Clark, Martin & Mahowald, *Why is AI-generated language so hard to understand?*, arXiv 2610.29162（2026-10）** <https://arxiv.org/abs/2610.29162>

- 测了 14 个模型（GPT-5.6 Luna/Terra/Sol、Claude Sonnet 5 / Opus 5 / Opus 5.5 / Fable 5、Kimi K2.5、GLM 5、Olmo、Llama），场景是多轮聊天、写代码、单篇作文。
- 和人类文本、以及同义回译文本比，9 个前沿模型全部更多使用：
  - 无生命主语配有生命动词：「is_file() swallows that」「this asymmetry bites」
  - 低频词组（参照语料里从没出现过的二元组）
  - 多数模型还更多用：长距离依存、三个以上名词堆叠（「reader-patience budget」）、省掉关系代词的宾语从句、名词直接当动词（「footnote it」）
- Olmo 家族里，这些特征从 base → instruct → think 逐级增加。
- 多轮聊天和写代码时最明显，单篇作文较弱。作者推测长对话本身就在逼模型压缩。
- 实验：给 Qwen2.5-1.5B 在 GRPO 里加长度惩罚，模型在两种同义句式里**一律选短的**（人类会看上下文选），并且迁移到训练没见过的句式上。
- 作者的解释：人类语言是为沟通优化的；可验证奖励（数学、代码）只奖励答对，不奖励被看懂，长度惩罚和上下文成本又推着模型往信息密度走。
- Claude Opus 5.5 在 21 项比较里 19 项比 Opus 5 好，说明训练可以把它修回来。

对应到中文 GPT-6.x 的口癖（见 `references/gpt-codex.md`）：

| 论文里的特征 | 中文表现 | 例子 |
|---|---|---|
| 名词当动词、单字动词 | E 节 | 「核一下」「落代码」「我给你接」 |
| 无生命主语配有生命动词 | E、D 节 | 「吃目标值」「这样更硬」「没被伤到」 |
| 堆叠名词、低频组合 | C 节 | 「验收口径」「收据」「最小闭环」「整体验收」 |
| 省掉可有可无的词 | 全篇 | 省主语、省「的」、省连接词，读者得自己补 |

**Reinhart et al., *Do LLMs write like humans?*, PNAS 2025** <https://www.pnas.org/doi/10.1073/pnas.2422455122>

- 用 Biber 的 66 个语法修辞特征比较人类和多个 LLM。差异最大的是指令微调模型；Llama base 模型最接近人类。
- 指令微调模型的名词化（nominalization）是人类的 1.5–2 倍，作者结论：指令微调没有让模型更像人，而是训练出一种信息密集、名词为主的特定文风。

**Lamparth, Fein et al., *Reward Bias Substitution*, arXiv 2605.27996（2026-05）** <https://arxiv.org/abs/2605.27996>

- 在 GRPO 里加长度惩罚，回答确实变短了，但策略变得更**过度自信**，开放问题的准确率下降。修掉一个偏差，压力会转移到相关的另一个代理指标上。

**Telegraph Test（Travis Smith，2026-10）** <https://fiveminutesforward.com/post/2026-10-04-telegraph-test/>

- 让模型用电报体写记录，省 40%–49% 的 token，**另一个模型**读这些记录几乎不损失信息。
- 但让模型直接用电报体回答人，准确率降到明文的 0.81。作者的结论：读者是模型时可以压缩，读者是人时写明文。

## 2. 防御：评测和奖励在推着模型多表达不确定

**OpenAI, *Why language models hallucinate*（2025-09）** <https://openai.com/index/why-language-models-hallucinate/>

- OpenAI 主张评测应该「对自信的错误罚得比不确定更重，并给恰当的不确定表达部分分数」。
- GPT-5 系统卡里的 SimpleQA：gpt-5-thinking-mini 弃答率 52%，o4-mini 是 1%。
- 这篇论文没有直接说 GPT-5 以后会更爱加限定语。但奖励「表达不确定」、惩罚「自信出错」的方向，和 GPT-6.x 满篇「不能证明」「尚未验证」「仅凭……不能确定」在逻辑上一致。这是本仓库的推断。

**Sharma et al., *Towards Understanding Sycophancy*, ICLR 2024** <https://arxiv.org/abs/2310.13548>

- 5 个 RLHF 助手都会附和用户；人类偏好数据里，符合用户观点的回答更容易被选中。对应 Claude 的「你说得对」。

## 3. 千篇一律：偏好数据把模型推向最典型的说法

**Zhang et al., *Verbalized Sampling*, arXiv 2510.01171（2025）** <https://arxiv.org/abs/2510.01171>

- 标注者偏爱熟悉的文本（典型性偏差），即使奖励模型完美，偏好数据本身也会让分布收窄。
- 一个不需要训练的提示就能部分恢复多样性：让模型「给出 5 个候选及其概率」。这是「小提示能撬动后训练习惯」的直接证据。

**Paech et al., *Antislop*, ICLR 2026** <https://arxiv.org/abs/2510.15061>

- 有些套话在 LLM 输出里的频率是人类文本的 1000 倍以上。
- 生成时回溯重采样（Antislop Sampler）或微调（FTPO）能压掉 85%–90% 的套话；单纯禁词在 2000 条左右就不可用了。
- 对本仓库的启示：禁词表只能压表面，而且有「打地鼠」效应。

## 4. 小提示的上限

**Rallapalli et al., *Interpretable Stylistic Variation in Human and LLM Writing*, EMNLP Findings 2026** <https://arxiv.org/abs/2604.14111>

- 11 个模型、8 种文体、4 种解码策略。用提示让模型「写得像人」、或者给它人写的文本去续写，**关键的文风差异基本不变**。
- **文体对文风的影响比来源（人或模型）更大**；模型的影响比解码策略大。

结论：小提示能修**具体口癖**（某几个词、某个句式、防御句），改不动整体文风画像。所以本仓库的做法是：

1. 用小提示压住有名有姓的口癖和压缩习惯。
2. 用「按文体和读者写」来带动整体文风，而不是「写得像人」「口语化一点」。
3. 剩下的靠改稿（`zh-deai` 主流程）。

## 5. 厂商自己给的修正提示

两家都在官方文档里承认了自家模型的口癖，并给了一段话的修正提示。这是目前最可靠的「trigger」来源。

**OpenAI, Using GPT-6** <https://developers.openai.com/api/docs/guides/latest-model>

- 承认：GPT-6 Astra「倾向于详细、带格式的回答，会在不同会话里重复使用同样的短语」；对 skills 和 AGENTS.md 里的指令更敏感，建议审查这些文件。
- 官方提示原文（节选）：
  - "State the intended action directly. Avoid adding what you won't do, what will remain unchanged, or how you'll separate or categorize results."
  - "Do not use contrastive framing such as 'X, not Y' that introduces an unprompted alternative that the user didn't ask about."
  - "Avoid invented compound labels like 'exact-head checks' and 'editorial-row layouts', vague qualifiers, and canned transitions; use plain verbs and prepositions to state the actual relationship directly."
  - "Do not introduce unsolicited warnings, disclaimers, approval flows, or safety/compliance checklists due to hypothetical risk."
  - "Calibrate your writing to the level of background knowledge assumed from the user's prompt and context."

这几条和本仓库 GPT 清单的 A3（汇报没做的事）、N2（不是……而是）、C（自造名词）、A 节（防御）一一对应，而且对应的正好是 Clark 等人说的压缩特征（invented compound labels = 堆叠名词）。

**Anthropic, Prompting Claude Fable 5.1** <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1>

- 承认：Fable 5.1 有时比 Fable 5 更密，句子更长，分段更少。
- 官方提示的写法值得学：先**定义反模式**（mannered prose：用比喻和修饰代替直接陈述），给两个前后对照的例子，再解释读者为什么讨厌它，最后给改法（有字面说法就用字面说法）。短版「Please remove all mannered prose.」也常常有效。
- 另一条：早期模型爱用列表和加粗，很多提示里写了反格式规则；Fable 5.1 反而格式不足，旧规则要删掉或改成「什么时候该用格式」。**为旧模型写的限制会在新模型上起反作用。**

## 6. 由此得出的规则设计原则

1. **按模型给提示。** 厂商自己的提示都是针对自家模型的具体问题写的，通用提示做不到。
2. **定义反模式，给对照例子，说明读者为什么难受。** 比列禁词有效（Anthropic 的写法；Antislop 和 DeepSeek V4 用户反馈都显示禁词表会反向提示）。
3. **解压缩，而不是口语化。** 问题在信息被压进了堆叠名词、单字动词和省略里。修法是把主语、宾语、连接关系补回来，让每句话只承载读者一次能接住的信息量（均匀信息密度，UID）。口语化程度应该跟着场合走。
4. **按读者和文体校准。** 文体对文风的影响最大（Rallapalli 等）；OpenAI 官方也要求按用户背景知识调整。
5. **删掉为旧模型写的硬性限制。** 句长上限、长短句交替、每段破折号几个，这些多来自 2023—2024 年的 GPT-4 时代清单，在新模型上要么无关，要么起反作用。
