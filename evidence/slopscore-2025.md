# 同题英文语料：各模型的独有高频词

数据：[sam-paech/slop-score](https://github.com/sam-paech/slop-score) `results/*.json`。每个模型回答同一批 300 道英文写作题（小说和议论文开头），temperature 0.7，采集于 2025 年。题目相同，所以词频差异主要来自模型本身。

方法：每个模型对其余 7 个模型合计做对数优势比，出现次数 ≥ 25，去掉冠词介词。括号里是「该模型次数 / 其余模型平均次数」。人名（Marcus、Elara、Clara 等）是各模型给角色起名的偏好，也列出来，因为它们同样是指纹。

这些是 2025 年的模型。新版本会变，但同一家族的倾向通常延续。

## 各模型独有高频词（前 30）

| 模型 | 词 |
|---|---|
| GPT-4o（chatgpt-4o-latest） | also, may, these, such, maybe, especially, role, individuals, challenges, help, significant, **moreover**, essential, support, education, importance, example, including, important, among, **additionally**, particularly, influence, in addition, various, broader, significantly, development |
| GPT-5-mini | small, because, people, things, like, thing, there, can, will, make, someone, **ledger**, taught, reduce, practical, keep, learned, incentives, outcomes, honest, supports, policy, measures, practices, produce |
| Claude Sonnet 4 | Marcus, Sarah, he'd, I'd, my, I've, she'd, wasn't, **something**, I'm, **somehow**, couldn't, Maya, Elena, Chen, seemed, it's, don't, consciousness, everything, years, three, months, really |
| Claude Sonnet 4.5 | I'd, Marcus, I'm, he'd, it's, I've, don't, couldn't, that's, didn't, my, what, Sarah, something, you're, Chen, **three**, wasn't, years, they'd, everything, know, maybe, **exactly**, **actually**, **forty**, quite |
| DeepSeek R1 | Clara, Lila, Alex, Kael, Voss, Jax, title, example, instance, such, while, **prioritize**, challenges, explores, similarly, **systemic**, **underscores**, **fostering**, innovation, collaboration, cultural, **resilience**, strategies, **societal**, legacy, **adaptability** |
| DeepSeek V3.2-exp | **profound**（404 次，其余平均 65）, Leo, our, **powerful**, very, most, upon, grey, simple, complex, primary, **ultimate**, **silent**, **immense**, provided, **foundational**, **fundamental**, frantic, Kaelen, vast, pure, beautiful, **absolute**, terrifying, core, furthermore, fundamentally, entire |
| Gemini 2.5 Flash | Elara, understanding, often, towards, very, **meticulously**, particularly, profound, subtle, **intricate**, crucial, **testament**, **vibrant**, significant, truly, ultimately, furthermore, sheer, **unwavering**, **fleeting**, utterly, inherent, chilling, seemingly, stark, comprehensive, robust, **landscape**, **nascent** |
| Kimi K2 | **every**, **inside**, **whose**, still, yet, same, until, **percent**, two, already, year, three, per, because, half, sentence, never, second, five, million, six, four, single, **micro** |

## 句式和标点（每千词）

| | GPT-4o | GPT-5-mini | Claude S4 | Claude S4.5 | DS-R1 | DS-V3.2 | Gemini 2.5 | Kimi K2 |
|---|---|---|---|---|---|---|---|---|
| not X but Y | 0.95 | 0.18 | 0.49 | 0.41 | 0.36 | **1.47** | 0.91 | 0.29 |
| It's not X. It's Y. | 0.01 | 0.05 | 0.04 | 0.04 | 0.01 | **0.17** | 0.03 | 0.02 |
| 否定缩写与 never/no | 3.1 | 3.2 | **8.4** | **10.8** | 2.3 | 3.1 | 3.4 | 4.4 |
| em dash | 7.0 | 9.4 | 7.6 | 8.9 | 9.2 | 3.7 | **0.03** | 7.8 |
| 分号 | 0.5 | 4.2 | 0.3 | 0.2 | 1.1 | 2.1 | 1.2 | **5.4** |
| 冒号 | 1.6 | 6.6 | 2.4 | 2.6 | **8.1** | 2.6 | 1.4 | 7.3 |
| 问号 | 2.7 | 1.3 | 5.0 | **6.4** | 3.7 | 2.3 | 3.1 | 1.3 |
| 省略号 | 0.5 | 0.1 | 1.2 | 1.1 | 1.2 | 1.0 | **1.5** | 0.1 |

## 读法

- **GPT-4o** 是通用清单的原型（moreover、additionally、significant、essential、broader）。拿这张清单去查 GPT-5 以后的模型，命中率会很低：GPT-5-mini 的独有词变成了 small、people、things、practical、ledger。
- **Claude** 的英文指纹是口语缩写（I'd、he'd、it's）、模糊词（something、somehow）和**否定**：否定词密度是其他模型的 2–4 倍。和本机中文语料里 Claude「不是……而是」比 GPT-6.x 多（每 10 万字 18 次对 0–5 次）方向一致。
- **DeepSeek V3.2** 是「profound、immense、foundational、ultimate、absolute」这一套宏大形容词，加上全场最多的「not X but Y」「It's not X. It's Y.」。和中文 V4 反馈里「不是……而是……」泛滥对得上。
- **DeepSeek R1** 是议论文腔（prioritize、systemic、underscores、fostering、resilience、societal）。
- **Gemini 2.5** 几乎不用破折号，偏爱 meticulously、intricate、testament、vibrant、unwavering、nascent、landscape。
- **Kimi K2** 爱用数字和量词（percent、two、three、half、million）和 every、inside、whose。

## 复现

```bash
for m in claude-sonnet-4-5 deepseek-v3.2-exp gpt-5-mini-2025-08-07 ...; do
  curl -sLO https://raw.githubusercontent.com/sam-paech/slop-score/main/results/$m.json
done
```

对数优势比的算法与 `evidence/local-corpus-2026-11.md` 的「自动发现」相同。
