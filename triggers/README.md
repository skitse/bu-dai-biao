# 候选 trigger：用一小段提示撬动后训练习惯

状态：**草稿，待测试**。每段都有来源，但还没在我们的语料上做 A/B 对比。

## 为什么相信小提示有用

- **Verbalized Sampling**（Zhang 等 2025）：一句「给出 5 个候选及其概率」，就能部分恢复被偏好训练压窄的多样性。
- **厂商自己在用。** OpenAI 的 GPT-6 指南、Anthropic 的 Fable 5.1 指南都给了一段话的修正提示，针对的正是自家模型的口癖。
- **上限也清楚**：Rallapalli 等（2026）显示，「写得像人」这种笼统提示改不动深层文风。所以每个 trigger 只瞄准一个具体习惯。

## 写法（照 Anthropic 的 mannered prose 提示）

1. 给反模式起个名字，下定义。
2. 给两个前后对照的例子。
3. 说读者为什么难受。
4. 给改法。
5. 别在提示里列一长串禁词。模型会把禁词当提示（Antislop；DeepSeek V4 用户反馈「禁词表当提词器」）。

## 候选清单

| 文件 | 针对 | 来源 |
|---|---|---|
| `gpt-defensive.md` | GPT-6.x 防御腔 | OpenAI GPT-6 指南原文 + 本仓库 GPT-A、N 节 |
| `gpt-compression.md` | GPT-6.x 压缩：自造名词、单字动词、拟人主语 | OpenAI 指南「invented compound labels」+ Clark 等 2026 |
| `claude-mannered.md` | Claude 的矫饰比喻和否定反转 | Anthropic Fable 5.1 指南原文 + Arize 标注 |
| `deepseek-aphorism.md` | DeepSeek V4 的金句和短句排比 | V4 用户反馈汇总 + bili-ai-killer 模板 |
| `register.md` | 各模型通用：按读者和场合定语体 | OpenAI 指南「calibrate to background knowledge」+ Rallapalli 等 2026 |

## 测试计划

- 题目：molang163 的 16 道日常题，加 5 道工作汇报类题（干活场景压缩更重）。
- 每题跑「不加 / 加 trigger」各 3 次，用 `codex exec --ephemeral`（不留会话记录）和 `claude -p`。
- 指标：`scripts/scan.py` 各模型密度；否定句占比；防御词数；堆叠名词和单字动词数；字数。
- 盲评：另一家模型当评委（GPT 的输出给 Claude 评，反过来也一样），问「哪个更好懂、信息是否完整」。
- 结果放进 `evidence/`，没通过的 trigger 删掉。
