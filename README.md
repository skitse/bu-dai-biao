# 不代表（bu-dai-biao）

> 本仓库不代表你的稿子一定有 AI 味，也不能证明它是人写的；至于能不能过检测，仅凭这份 README 还不能完全确定。
>
> ——GPT-6

好，下面说人话。先说结论：市面上的去 AI 味 skill，大多还活在 2023 年，这一点我已经核对过收据。根因很清楚：它们郑重地教你删掉「delve」，但这不代表 GPT-6 会说 delve，它只说「尚未验证」「不代表」「收据已补齐，待验收」。它们要求你长短句交替，口径来自三年前 GPTZero 的「突发性」；照这条链路跑下来，你的文章会稳稳落到 Claude 那一侧：「不是细节。是设计。」它们要你多加第一人称、多写感受，结果技术文档里冒出「说实话，家人们，这个 bug 我真的破防了」，这并不能证明作者是人，只能证明作者破防了。破折号这块更硬：一份清单要求一律删除，一份要求每段最多两个，一份建议没有就加两个，三份同时落盘，模型当场宕机，本轮未恢复。往深里抠一下：这些规则大多抄自同一个 Wikipedia 页面，抄的人又被下一个人抄，传到第五手时，已经没人能确认原文写的是 GPT-4。拿这张清单去改 GPT-6.1 的稿子，就像拿着去年的病历给今年的病人开药：它精准删掉了本来就没有的破折号，满篇的「不能证明」「仅凭……不能确定」一个没动，最后还附上一份验收报告，说你的文章已经很像人了。需要指出的是，以上判断仅基于本仓库的调研，不代表所有 skill 都过时；我不靠猜，这版说法一定站得住。如果你愿意，我可以顺手把剩下的口径也收一下，你回一句「确认」我立马开始。

说穿了：从「好，下面说人话」开始，这一整段就没停过 GPT 味，你数到第几个口癖才发现的？其实它是 Claude 模仿 GPT-6 写的。你说得对，这确实不只是模仿，而是致敬。（好吧，这一句是 Claude 自己的口癖，我们认。）能模仿得这么像，说明每个模型的口癖都认得出来，这正是这个仓库存在的理由。

针对模型的中文 humanizer（model-tics-zh）。

先认出文字是哪个模型写的，再按那个模型的口癖去改。目前收了 GPT-6 / 6.1（Codex）、DeepSeek、Claude 三份清单，每条口癖附例子、改法和出处。可以装成 Claude Code 或 Codex 的 skill。

## 和常见 humanizer 的区别

| | 常见做法 | bu-dai-biao |
|---|---|---|
| 规则来源 | 改编自 Wikipedia「Signs of AI writing」和 blader/humanizer，项目之间互相转抄 | 每条口癖来自具体模型的语料统计、厂商文档或社区原话，条目里写明出处和证据强弱 |
| 针对谁 | 一张清单对付所有模型 | GPT、DeepSeek、Claude 各一份清单，按模型判断 |
| 时代 | 主要描述 2023—2024 年 GPT-4 的英文输出 | GPT-6 / 6.1、DeepSeek V4、Claude 5.x 的中文输出 |
| 对节奏的要求 | 长短句交替、单句字数上限、段落句数配额 | 句长跟内容走 |
| 对口语的要求 | 一律口语化，加第一人称和感受 | 按场合定语体：聊天、汇报、文档、论文各一套 |
| 对篇幅的要求 | 越短越好，砍掉一半 | 删掉零信息的防御句和套话，同时把被压缩的信息展开 |
| 禁词表 | 直接写进提示词 | 只在改稿时检查；提示词里写反模式定义和对照例子 |
| 证据 | 作者经验 | 本机约 63 万字语料、8 个模型同题语料、十几篇论文和两家厂商的官方文档 |

## 通行做法的问题

我们调研了 47 个开源 humanizer（清单见 `evidence/oss-survey-2026-11.md`），42 个用的是同一类通用清单。下面几条规则在这些项目里反复出现，多数是从一个项目抄到另一个项目，每抄一次离原始依据就远一点。

「长短句交替」「提高 burstiness」出现在 20 个项目里。它的来历是 2023 年 GPTZero 一类检测器的「突发性」指标，用意是骗过当时的检测器。照这条去写，得到的是「Not a detail. A design decision.」这种为节奏而切碎的短句，这恰好是 Claude 被吐槽最多的写法之一（`references/claude-en.md` CE-7）。现在的检测器是训练出来的分类器，Pangram 的技术报告显示它们学的是整体写法，单靠句长变化改不了分数。

「单句不超过 40 个汉字」「平均 25 词以内」这类句长上限，会把一个完整的因果关系切成几截，读者得自己把它们拼回去。Clark 等人（2026）测了 14 个模型，发现 AI 文字难懂的原因在堆叠名词、名词当动词、拟人化主语和长距离依存，句子长短本身影响很小。

「多加第一人称、感受、感官细节」在改别人的稿子时等于编造经历。AI 写口语很容易，hylarucoder 的提示和 humanize-kit 的 Instagram 模式都能做到，口语化从来就是简单的那部分。Rallapalli 等人（2026）测了 11 个模型、8 种文体，发现用提示让模型「写得像人」，关键的文风差异基本不变，文体的影响比模型来源还大。

「越短越好」在新模型上会帮倒忙。后训练里的长度惩罚正是 GPT-6.x「核一下」「吃目标值」「验收口径」这类怪话的来源（Clark 等 2026 用实验复现了这个过程）。再要求它砍掉一半，只会压得更狠。

破折号的规定互相打架：有的项目要求「一律删除」，有的规定「每段不超过 2 处」，还有的要求「没有就加 1 到 2 处增加节奏」，humanize-kit 甚至建议「用破折号代替逗号」。实际上破折号算不算口癖取决于模型：GPT-6.x 很少用，Claude Opus 5 每千词 12.9 个、Opus 5.5 几乎为零，DeepSeek V4 爱用破折号插注释。

把禁词表塞进提示词，效果常常相反。DeepSeek V4 的用户反馈里，「禁词表当提词器」几乎是共识；Antislop（ICLR 2026）的实验显示禁词规模一大就失效，压下一个词又冒出另一个。

还有一个讽刺的现象：很多去 AI 味的 skill，自己就写得像 GPT。网上流传的一份「去防御」规则，全文 28 个「禁止」、18 个「禁用」，连「但」「其实」「重」「冷」都禁，犯错时却要求「深刻道歉，篇幅足够、诚意足够、情绪反馈充足」；某个降 AIGC 的 skill 写着「知网 3.0 准确率 98.6%」，出处是一份没有作者的报告；两个学术 skill 有一半的行完全相同，都说自己做过同一组降 AI 率实验。拿否定句写反否定的规则，拿编出来的数字教人别编，效果可想而知。

逐条判定见 `evidence/rules-audit.md`（通用规则和这份「去防御」规则）和 `evidence/academic-audit-2026-11.md`（11 个学术 humanizer）。

## 我们怎么取舍

素材来自 55 个以上的 humanizer 项目：本地装过的 8 个去 AI 味 skill，加上 GitHub 上细读过的 47 个（另有约 65 个浅克隆下来做规则扫描）。每条规则我们都拿三样东西去核对：本机约 63 万字的 GPT-6.x 和 Claude 语料、8 个模型的同题英文语料（slop-score），以及相关论文和厂商文档。对得上的收下，对不上的剔除或降级，理由都写在条目里。

收下的，和它们经得起核对的原因：

| 素材 | 来源 | 核对结果 |
|---|---|---|
| GPT-6.1 的防御性回复（不代表、尚未、未修改、说得太绝对） | molang163/chinese-natural-reply | 本机语料里这些词在 GPT-6.x 中的频率是 Claude 的 3 到 70 多倍；OpenAI 的 GPT-6 指南也点名了同类写法 |
| 「不是……而是」要控制 | 多个中文项目 | 本机语料和同题语料都显示 Claude、DeepSeek V3.2 偏多，GPT-6.x 偏少，所以改成按模型判断 |
| DeepSeek V4 的金句和短句排比 | V4 用户反馈汇总、bili-ai-killer | 和同题语料里 V3.2「not X but Y」全场最多的结果方向一致 |
| 知网标红的 5 类信号（句长可预测、密度均匀、术语位置、连接词重叠、模板段） | qingshanliuci/cnki-aigc---skill | 和 Clark 等 2026、Pangram 技术报告对「结构比词更关键」的结论一致；样本只有一篇论文，标为经验 |
| 一段式修正提示的写法 | Anthropic、OpenAI 官方指南 | 厂商针对自家模型写的，直接采用 |
| 结论强度跟着证据走；合理限定语保留一个；压缩的表达要展开；主语和动词要搭配；连接词别删过头 | matsuikentaro1/humanizer_academic、AIScientists-Dev/academic-humanizer | 前者的作者发表过 PubMed 用词研究；这几条分别和 Peters & Chin-Yee 2025（结论被说大）、Clark 等 2026（信息压缩）的结论一致 |
| 把「AI 味」拆成论文质量问题，先建「结论—证据」对照表 | YouCun-Official/paper_llm_style_review | 和「可核对」trigger 的依据（Prover-Verifier Games）一致 |
| 不重新定义用户的问题；不把用户当成需要纠正的人 | 网上流传的 no-defensive-writing-cn | 和 molang163 整理的 GPT-6.1 原话一致，已并入 `gpt-nodefense` 第 6 条 |

剔除或降级的，和理由：

| 素材 | 来源 | 处理 | 理由 |
|---|---|---|---|
| 长短句交替、单句字数上限、段落句数配额 | 20 多个项目互相转抄 | 剔除 | 来自 2023 年检测器的突发性指标；研究显示难懂与否取决于堆叠名词、拟人化主语等，句长影响很小 |
| 强制口语化、加第一人称和感受 | hylarucoder、humanize-kit 等 | 剔除 | 改别人稿子时等于编造；「写得像人」的提示改不动深层文风（Rallapalli 等 2026） |
| 故意写残句、小写、错别字 | humanize-kit 等英文项目 | 剔除 | 为骗检测器设计，读者受罪 |
| 破折号固定配额（一律删 / 每段 2 处 / 没有就加） | 多个项目，互相矛盾 | 改成按模型 | 本机和同题语料显示各模型差异极大 |
| happycapy 的「Claude 专属词库」（however、moreover、I'd be happy to……） | happycapy-ai/Happycapy-skills | 剔除 | 同题语料里 moreover、additionally 是 GPT-4o 的独有高频词；Sun 等 2025 也把 certainly 归给 ChatGPT |
| delve、tapestry 等英文高频词表 | Wikipedia 系清单 | 降级为背景 | 属于 2023—2024 年 GPT-4 时代；GPT-5 以后的独有高频词已完全不同 |
| GPT-5.x 的「砍一刀」「压实」「稳稳接住」 | linux.do 口癖帖 | 降级为次要 | 本机 GPT-6.x 语料里这些词出现 0 次，6.x 的主要问题已经换成防御腔 |
| 「Claude 爱用破折号」 | 多个项目和博客 | 改成分版本 | Opus 5 每千词 12.9 个，Opus 5.5 在 5.7 万词里只有 2 个（Arize 2026） |
| 禁词表写进提示词 | 多个项目 | 改用法 | Antislop 和 DeepSeek V4 用户反馈都显示会反向提示；只在改稿时检查 |
| 繁体和台湾用语规范、「您」改「你」 | chinese-content-writing-guideline | 剔除 | 作者个人的写作规范，和 AI 味无关 |
| 「禁止任何限定和免责」「深刻道歉」、禁用「但」「其实」和一批单字 | 网上流传的 no-defensive-writing-cn | 剔除 | 两轮评测显示一刀切会删掉该说的风险；禁词写进提示词会反向提示；「深刻道歉」是新的表演 |
| 配额（高频词每段 ≤2 个、成语每千字 2–3 处、段落 3 句和 7 句交替）、同义词替换表 | 多个中文学术 skill | 剔除 | 没有来源；检测器学的是整体写法；替换会破坏术语一致性 |
| 「知网 3.0 准确率 98.6%」一类精确数字 | xiaofenggan01/aigc-reduce | 剔除 | 唯一出处是一份没有作者和链接的报告 |
| 「补上局限和不确定」「加入具体细节」 | 多个中文 humanizer | 剔除 | 原文没有就是编造 |

完整的逐条判定见 `evidence/rules-audit.md`，项目清单见 `evidence/oss-survey-2026-11.md`。

## 为什么要分模型

每个模型露馅的地方差得很远。

GPT-6.1 的文字满是防御：「这不代表……」「尚未验证」「我前面说得太绝对」，外加「收据」「验收」「本轮」「口径」这些自造名词。它聊天时 39% 的句子带否定词。

DeepSeek V4 爱造金句：「她笑了。不是温暖的笑。而是幸福的笑。」「这就够了。」评论区机器人张口就是「这条我收下了——」。

Claude 写稿时爱用对比反转（「这不是技术问题，是沟通问题」）和矫饰比喻（「这个参数值得拧一拧」「这一点很承重」）。它在 Claude Code 对话里的「你说得对」「一句话：」「需要我帮你做什么吗」是正常的工作交流，不在处理范围。

同一组词，在不同模型里的频率能差几十倍：

| 每 10 万字出现次数 | GPT-6.x | Claude |
|---|---|---|
| 尚未 | 32–160 | 2 |
| 不代表 / 不等于 / 不意味 | 13–79 | 6 |
| 收据 | 20–73 | 2 |
| 其实 | 0–2 | 23 |
| 不是……而是 | 0–5 | 18 |

拿一张通用清单去改，结果常常很好笑：改 GPT-6.1 的稿子时，删掉了它本来就很少用的破折号和「此外」，满篇的「不代表」「尚未」原样留着。

## 设计依据

模型会说人话。它说不好，是后训练养成的习惯。我们按研究结论设计每一部分：

| 研究发现 | 设计 |
|---|---|
| 长度惩罚让模型偏爱短而难懂的句式：堆叠名词、名词当动词、拟人化主语、省略（Clark、Martin、Mahowald 2026） | 「解压缩」：把自造名词拆回「谁对什么做了什么」，单字动词换回完整说法，补回被省掉的主语和连接词 |
| 指令微调让模型写出信息密集、名词为主的文风，base 模型反而最像人（Reinhart 等，PNAS 2025） | 改稿时优先把名词化的表达改回动词 |
| 评测开始奖励表达不确定、重罚自信出错（OpenAI 2025）；单独压长度会让模型更过度自信（Lamparth、Fein 等 2026） | GPT 清单把防御句单列成最大的一类，并配一个常驻规则 `gpt-nodefense` |
| 「写得像人」的笼统提示改不动深层文风，文体的影响更大（Rallapalli 等 2026） | 用「语体校准」代替「口语化」，每个 trigger 只瞄准一个具体习惯 |
| 一句提示就能部分恢复被偏好训练压窄的多样性（Verbalized Sampling 2025） | 相信小提示有用，写成 `triggers/` 里的一段式修正提示 |
| 厂商官方承认自家口癖，并给出一段话的修正提示（OpenAI GPT-6 指南、Anthropic Fable 5.1 指南） | trigger 照官方写法：给反模式起名、下定义，附前后对照例子，说明读者为什么难受 |
| 禁词表会反向提示，规模大了就失效（Antislop 2026） | 清单只用来改稿检查，提示词里写正面描述 |
| 不同模型有可识别的用词指纹，分类器能以 97% 的准确率认出模型（Sun 等，ICML 2025） | 先认模型，再按模型改 |

研究细节见 `evidence/post-training-research.md`。

## 实测

GPT 去防御规则做了两轮盲评（21 道日常和工作汇报题，Claude Sonnet 打乱顺序评审）：

| 轮次 | 模型 | 不加规则的平均名次 | 加规则后的平均名次 | 防御词 | 含否定的句子 |
|---|---|---|---|---|---|
| 第一轮 | GPT-6 Astra | 2.71 | 1.62（示例式） | 9 → 1 | 26% → 24% |
| 第二轮 | GPT-6.1 Terra | 2.52 | 1.81（v2） | 5 → 0 | 28% → 16% |

第一轮发现两个问题：只给指令时模型会把该保留的风险也删掉；示例里的坏句子会被模仿。第二轮的 v2 针对这两点做了修改，现在是 `gpt-nodefense` 的常驻规则。详见 `evidence/eval-round1-2026-11.md`、`evidence/eval-round2-2026-11.md`。

`scripts/scan.py` 在本机语料上的 GPT 口癖密度：Codex 每千字 26.1，Claude 6.7，能分开两家。其余 trigger 的写作评测还没做，计划见 `triggers/README.md`。

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
  paper_check.py            论文段落：逐句信息密度分析；AI 改写或总结前后的保真检查
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
git clone https://github.com/skitse/bu-dai-biao ~/.claude/skills/bu-dai-biao
ln -s ~/.claude/skills/bu-dai-biao ~/.codex/skills/bu-dai-biao   # Codex
```

用 CC Switch 管理的话，放进 `~/.cc-switch/skills/bu-dai-biao`。

### GPT 常驻去防御（gpt-nodefense）

两个 skill 分工不同：`bu-dai-biao` 只管写作（改稿子、替人写稿）；`gpt-nodefense` 管 GPT 在 Codex 日常对话里的防御腔，因为它在对话里就已经造成困扰。Claude 的对话习惯不需要类似处理。`gpt-nodefense` 用来约束 GPT 自己说话，装好后 GPT 的每条中文消息都按它来，直到你在对话里说「保留防御」或「#defense-on」。

```bash
cd ~/.claude/skills/bu-dai-biao
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

检查论文段落的信息密度，或者核对 AI 总结、改写有没有把结论说大：

```bash
python3 scripts/paper_check.py density 段落.txt
python3 scripts/paper_check.py compare 原文.txt 改写.txt
```

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
