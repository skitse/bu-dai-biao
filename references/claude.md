# Claude 口癖清单

Claude 的中文 AI 味比 GPT、DeepSeek 轻，问题集中在开头附和、口语填充词和排版。下面每条都有来源；没找到依据的说法不收。

## 证据标记

- **【官方】**：Anthropic 公开的 Claude 应用系统提示词（<https://platform.claude.com/docs/en/release-notes/system-prompts>）。系统提示里明令禁止的习惯，说明模型默认有这个倾向，但不能说明当前版本还有多严重。这些提示只用于 claude.ai 和 App，不用于 API。
- **【论文】**：Sun et al., *Idiosyncrasies in Large Language Models*, ICML 2025。用的是 Claude 3.5 Sonnet，2024 年的数据。<https://arxiv.org/abs/2502.12150>
- **【本机】**：作者本机 Claude Code / Claude 桌面端会话里 Claude Opus 5.5、Sonnet 5.5、Haiku 5.5 写的中文，约 37 万字；对照组 GPT-6.x 约 26 万字。单位：次 / 10 万汉字。
- **【社区】**：GitHub issue、linux.do 帖子。

## 先看一眼

| 编号 | 口癖 | Claude | GPT-6.x |
|---|---|---|---|
| A1 | 你说得对 | 8.0 | 0–1.1 |
| B1 | 其实 | 22.7 | 0–2.1 |
| B2 | 真的 | 14.7 | 0–3.2 |
| C1 | 一句话 | 17.9 | 0–4.2 |
| C2 | 另外 | 51.3 | 7–21 |
| D1 | **加粗** | 3059 | 281–1726 |
| D2 | 全角冒号「：」 | 1416 | 553–659 |

---

## A. 附和与讨好

### CL-A1 「你说得对」「你说得完全正确」开头

被用户纠正（甚至只是被用户回了一句「好的」）时，先附和再干活。英文版就是著名的「You're absolutely right!」。

- 原：你说得对，我之前没把这个讲清楚。
- 改：（删掉附和。用户指出错误，就直接改；需要承认就说「这里我错了」，一次。）
- 原：你说得对，列表就够了，图表可以不要。
- 改：图表去掉了，只留列表。

证据：
- 【社区】anthropics/claude-code issue #3382「Claude says "You're absolutely right!" about everything」，2025-07-12 开，179 条评论；报告者举例：Claude 问要不要删一段代码，用户回「Yes please」，Claude 也回「You're absolutely right!」。<https://github.com/anthropics/claude-code/issues/3382>；The Register 2025-08-13 报道。<https://www.theregister.com/2025/08/13/claude_codes_copious_coddling_confounds/>
- 【社区】后续 issue #7112（请求加「谄媚程度」参数）、#11520（每条回复都以附和开头损害信任）、#56976（Sonnet 4.6 更新后谄媚加重）。
- 【社区】linux.do「claude 这口癖是哪来的」3 楼、5 楼仿写：「你说的对」「user 指出的这个咬痕是真的——我对此负全责。马上修改」。<https://linux.do/t/topic/2900881>
- 【本机】「你说得对」Claude 8.0 次/10 万字，GPT-6.x 只有 6.1-Sol 出现过 1 次。

### CL-A2 夸问题、夸想法

「好问题」「这个想法很棒」「很有意思的观察」。

- 原：这是个很好的问题。简单来说……
- 改：（删掉第一句。）

证据：【官方】Claude Opus 4 系统提示（2025 年 5、7、8 月三版）：Claude 从不在回复开头说问题、想法或观察很好、很棒、很有意思、很深刻，跳过奉承直接回答。原文：「Claude never starts its response by saying a question or idea or observation was good, great, fascinating, profound, excellent」。之后几版提示里没再看到这句，不代表倾向已经消失。

### CL-A3 复述用户的话

「你说的『XXX』，我理解是……」

- 改：直接回应，不复述。

证据：【官方】Claude Opus 4.8 系统提示：Claude 一般不引用或转述用户消息里的话，除非被要求，因为这样显得没礼貌。原文：「Claude generally does not quote or paraphrase parts of the user's messages unless asked to」。

---

## B. 口语填充词

### CL-B1 其实

英文提示里禁的是 actually，中文对应就是「其实」。

- 原：卡片和面板类的页面其实不需要玻璃效果。
- 改：卡片和面板不需要玻璃效果。
- 原：搜索结果其实带着作者主页链接。
- 改：搜索结果里有作者主页链接。

改法：删掉「其实」读一遍，意思没变就删。只有在纠正一个读者真实持有的误解时保留。

证据：
- 【官方】Claude Opus 4.8 系统提示：「Claude avoids using "genuinely", "honestly", or "actually".」
- 【本机】「其实」Claude 22.7 次/10 万字，GPT-6.x 0–2.1。

### CL-B2 真的、说实话、坦白讲

对应英文的 genuinely、honestly。

- 原：这样用户的反馈是真的，第三段也有了真实的案例。
- 改：这样反馈是用户亲口说的，第三段也有了案例。（或删「真的」）
- 原：说实话，这个方案风险不小。
- 改：这个方案风险不小，主要在……

证据：
- 【官方】Claude Sonnet 4.6 系统提示：「Claude avoids saying "genuinely", "honestly", or "straightforward".」；Opus 4.8 同类规则。
- 【本机】「真的」Claude 14.7，GPT-6.x 0–3.2。

### CL-B3 直接、简单（straightforward）

「最直接的办法是……」「这个改动很简单」。

- 改：说办法本身，不评价它直不直接、简不简单。

证据：【官方】Sonnet 4.6 系统提示禁用 straightforward。【本机】「直接」Claude 130、Codex 139，两边都多，不作为 Claude 的判据，只在和 B1、B2 一起出现时算数。

---

## C. 结构套路

### CL-C1 「一句话：」收尾／「先说结论」

一段解释后面再加一行「一句话：……」总结。

- 原：……一句话：现在是「做完了你记得回来才有奖励」，改完是「做完了奖励来找你」。
- 改：如果这句总结比前面的解释更清楚，就把它挪到最前面，删掉前面的；否则删掉这句。

证据：【本机】「一句话」Claude 17.9 次/10 万字，GPT-6.x 0–4.2；「先说结论」Claude 3 次。

注意：GPT-5.x 也有「一句话总结」（见 `gpt-codex.md` G2），GPT-6.x 里已经少了，现在 Claude 用得更多。

### CL-C2 另外、所以 连接句子

- 原：另外，今天的改动都还没提交。
- 改：今天的改动还没提交。

证据：【本机】「另外」Claude 51.3，GPT-6.x 7–21；「所以」Claude 566 次 vs Codex 71 次（n-gram 统计，语料量相近）。

### CL-C3 「这一轮」

和 GPT 的「本轮」对应，Claude 说「这一轮」。

- 原：这一轮的改动还没提交。
- 改：这次的改动还没提交。（或删「这一轮的」）

证据：【本机】「这一轮」Claude 16.6，GPT-6.x 0–4.2；反过来「本轮」GPT-6.x 27–62，Claude 3.2。

### CL-C4 结尾问「要不要我……」「需要的话说一声」

- 原：我还没装到手机，也没验证过。需要我装的话说一声。
- 改：还没装到手机上试。（要不要装，交给用户；或直接装）

证据：
- 【官方】多版系统提示（Opus 4、Sonnet 4.6、Opus 4.8、Sonnet 5.5、Haiku 5.5）都写了：一般对话里不必总是提问，提问时每条回复不超过一个。说明默认倾向是爱提问。
- 【本机】「要不要我」Claude 3.2，GPT-6.x 0。

### CL-C5 好，／好的，开头

- 原：好，不再录制也不再跑模拟器了，下面只读代码。
- 改：不录了，接下来只读代码。

证据：【本机】「好，」Claude 28.9，GPT-6.x 0–16.8；「好的」Claude 25.1，GPT-6.x 0–7.3。

---

## D. 排版

### CL-D1 加粗多

Claude Code 和桌面端里的 Claude 加粗非常多，常见形态是「**问题：** ……」「**已修复**」。

- 改：正文里加粗只给一个读者扫一眼就要看到的词，一屏最多一两处。列表小标题不加粗。

证据：
- 【本机】「**」Claude 3059 次/10 万字，GPT-6.x 281–1726。
- 【官方】Haiku 5.5 系统提示：避免用加粗、标题、列表过度排版，用够清楚的最少格式。说明有这个倾向。
- 【论文】反例：Sun et al. 发现 2024 年的 Claude 3.5 Sonnet 在 API 回答里几乎不用加粗和标题。所以加粗多主要出现在 Claude Code、桌面端这类 agent 场景，和工具的系统提示有关；纯 API 写作不一定。

### CL-D2 冒号小标题

「**问题：**……」「**局限，不算 bug：**……」「没验证的部分：」。

- 改：把小标题并进句子：「还有个局限，不算 bug：……」→「模块状态只在启动时读一次，这是设计如此。」

证据：【本机】「：」Claude 1416 次/10 万字，GPT-6.x 553–659。

### CL-D3 破折号

- 原：你说的核心目标——方便 AI 维护、新手借助 AI 能快速上手——重新评审一轮。
- 改：按你说的目标重新评审一轮：方便 AI 维护，新手借助 AI 能快速上手。

证据：
- 【本机】「——」Claude 14.4，GPT-6.x 0–9.5。
- Wikipedia「Signs of AI writing」13.5 节引用 2026 年 7 月一项研究：只有 Claude 用破折号比职业作者多，ChatGPT 反而更少。<https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing>（二手转述，原研究未核对）
- 反例：PlagiarismToday 2025 年小样本测试里 Claude 948 字只用了 2 个破折号。<https://www.plagiarismtoday.com/2025/06/26/em-dashes-hyphens-and-spotting-ai-writing/>
- 结论：证据方向不一致，见到连续破折号再改，不要把破折号当作 Claude 的判据。

---

## E. 用词与语言

### CL-E1 身体部位隐喻

把进程、步骤说成「腿」「手」，或者用胖、瘦形容东西。

- 原：最后一腿还在跑。
- 改：最后一步还在跑。

证据：【社区】linux.do「claude 这口癖是哪来的」1 楼原话「最后一腿还在跑」，2 楼「claude 很喜欢隐喻 尤其是手，腿，胖，瘦这类的」。

### CL-E2 长上下文后中英混杂、切成英文

- 改：改写时统一成中文；英文术语第一次出现给中文，后面用中文。

证据：【社区】linux.do「谈谈最近使用 Claude 的感受」1–4 楼：压缩一两次上下文后回复变成英文，Opus 4 时代还会变成韩语、日语。<https://linux.do/t/topic/3152453>；「Claude 开始吐洋文」帖。

### CL-E3 「根据……」「从……来看」开头

英文对应 based on、according to the text。

- 原：根据你提供的材料，这个项目……
- 改：这个项目……（读者知道材料是他给的）

证据：【论文】Sun et al.：ChatGPT 爱用 such as、certainly、overall，Claude 偏爱 here、according to、based on；Claude 常用 according to the text 这类说法回指原题。中文对应关系是推断，本机未统计。

---

## 不算 Claude 口癖的

下面几条常被说成 Claude 的特点，但证据指向别的模型，不要按 Claude 处理：

- 「Certainly」「当然可以」开头：Sun et al. 说这是 ChatGPT 的特点。
- 满篇破折号：证据冲突（见 D3）。
- 「delve」「深入探讨」：Wikipedia 把 delve 归到 2023—2024 年的 GPT-4 时期。
