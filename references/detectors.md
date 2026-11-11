# AI 检测器：公开了什么、没公开什么

用户问「知网到底查什么」「为什么同义词替换没用」时读这份。结论先说：**没有人公开过对知网、维普、万方 AIGC 检测的真正逆向**。能找到的只有厂商白皮书（Turnitin、Pangram）、独立评测，以及降 AI 率实践者的经验。下面按可信度分开写。

## 1. 厂商自己公开的（可信度：较高，但只说了一部分）

### Turnitin

- 把文章切成**每段约 5–10 句（几百词）的片段，片段互相重叠**，让每句都带上下文。
- 每句打 0–1 分，再把所有片段的分数平均成整篇的估计值。
- 来源：Turnitin 官方 FAQ 与白皮书 *Turnitin's AI writing detection model architecture and testing protocol*（2024 年 8 月）。<https://www.turnitin.com/whitepapers/turnitin-ai-writing-detection-model-architecture-and-testing-protocol>、<https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities>
- 第三方评测文章说 2026 年版是「AIW-1、AIW-2 加一个绕过检测模型」三段式，约 250 词一段，这个没能在 Turnitin 文件里核实。

### Pangram

- 一个 Transformer 分类器，先用约 100 万篇文档训练。
- **困难负样本挖掘**：用训练好的模型在大数据里找自己误判的人类文本，加进训练集再训练。
- **合成镜像**：每条人类样本，都生成一条在主题、长度、体裁等方面尽量相同的 AI 样本。这样模型学到的是「LLM 特有的写法」，不是主题或文体。
- 来源：技术报告 arXiv 2402.14873；Pangram 官网说明。<https://arxiv.org/abs/2402.14873>、<https://pangram.com/research/how-it-works>

由此可知：这类分类器学的是「指令微调模型的写法」整体，不是某几个词。所以：

- **换同义词基本没用**，句子结构和信息分布没变。
- AshwinSathian/humanize-writing-skill 的作者也明确说，风格指南改不了这类分类器的分数。<https://github.com/AshwinSathian/humanize-writing-skill>

## 2. 知网、维普、万方（可信度：低）

- **官方**：知网说它的 AIGC 检测服务系统以知网的文献大数据为基础（OSCHINA 报道 <https://www.oschina.net/news/258083>），没有公开模型结构、特征和阈值。维普、万方的官方页面也没有方法说明。
- **媒体**：央视等报道把原理概括为「困惑度」和「突发性」。<https://news.qq.com/rain/a/20260624A0BCCS00>
- **网上的「深度解析」**：博客园、CSDN 上大量文章声称知网已升级到「AIGC 学术文本检测系统 3.0」、加了「句式熵检测」「跨段落语义一致性分析」、特征库扩到 DeepSeek、豆包、Kimi。这些文章几乎都出自降 AI 率服务商，互相矛盾，没有官方出处。不要当事实引用。

## 3. 实践者的经验（可信度：中，样本是一篇论文）

qingshanliuci/cnki-aigc---skill：作者用 Claude 改自己的本科毕业论文，知网 AIGC 总分从 20.6% 降到 10.1%，**所有「红色显著」片段都降成了「疑似」**。作者总结知网抓的是 5 种语言模式（作者自己的归纳，没有对照实验）：<https://github.com/qingshanliuci/cnki-aigc---skill>

1. **句长可预测**：LLM 句子集中在 20–35 字。
2. **信息密度均匀**：每段密度都差不多；人写的有高密度论证段，也有低密度铺陈段。
3. **术语总在主语位置**：可以不改术语，只改它在句子里的位置（放到宾语或话题位置）。
4. **连接词功能重叠**：因此、从而、进而、由此连着用。
5. **模板段**：三四项工整排比、抽象名词链、段尾元话语收束（「综上所述」「这表明」）。

他还列了几条**不要做**的：

- 换同义词（「显著」→「明显」）：没用。
- 全面口语化：从 AI 腔变成博客腔，老师观感差。
- 把「较为」「一定程度上」「显著」删光：适度的学术限定反而是人写的特征。
- 给术语加引号拉开距离（「所谓……」）：这是 LLM 的典型动作（和 `gpt-codex.md` I2 一致）。
- 低于 10% 通常意味着已经不像学术论文了，不建议追。

这些和 `academic-cnki.md` 的方向一致，可以一起用。

## 4. 独立评测（可信度：中，结论互相冲突）

- 布鲁塞尔自由大学 2026 年 6 月的研究（160 篇已知来源文档，发表于 *International Journal for Educational Integrity*）：Pangram 优于 GPTZero、Copyleaks、Turnitin，尤其是混合文本和经过「人性化」提示改写的文本。（这个结论是通过 Pangram 自己的博客读到的。）
- Epoch AI 2026 年 7 月：Pangram 正确分类了全部 495 篇人类文本和 297 篇基础提示生成的 AI 文本。
- 反例：Reuters Institute 报道 Pangram 把 Alexios Mantzarlis 收集的 588 篇 AI 样本中的 86% 判成了人写的；arXiv 2608.11256（2026 年 8 月）发现经过人性化改写后，超过 96% 的 AI 改写稿能躲过 Pangram 和 GPTZero。
- 误判：多份来源指出检测器对非英语母语作者误判率高；Turnitin 自称误判率低于 1%。

## 5. 对本仓库的意义

- 去 AI 味的目标是**写得像一个具体的人**。按模型清单改掉口癖，能让文字好读；能不能改变检测分数，没有可靠证据，不承诺。
- 知网这类检测器的主要信号在结构（句长分布、信息密度、模板段），不在个别词。所以改写时多改结构，少换词。
- 别信「保证降到 X%」的说法。
