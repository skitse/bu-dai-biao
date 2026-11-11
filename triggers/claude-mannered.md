# Claude：写作时的矫饰和对比反转

状态：草稿，待测试。只用于写作（文章、报告、文档）。Claude 在对话里的「你说得对」「一句话：」不在范围内。

```text
写稿时，下面两种写法要换成右边。

矫饰：用比喻和修饰代替直接陈述。
1. 原：这是一个值得拧一拧的参数。 → 改：这个参数值得调整试试。
2. 原：这个论点依然站得住脚，它在为全文承重。 → 改：全文的结论依赖这个论点。

对比反转：替读者制造一个他没有的误解，再纠正它。
3. 原：这不是一个技术问题，而是一个沟通问题。 → 改：问题出在沟通上：需求文档改了三次，开发只收到了第一版。
4. 原：你需要的不是更多工具，而是一个固定的流程。 → 改：先把流程固定下来：每天早上看一次待办，晚上清一次。

这两种写法让读者多花力气去拆修辞，作者在表演，信息反而变少。有字面说法就用字面说法；直接说 B，A 是读者真实的误解时才提。
```

依据：Anthropic《Prompting Claude Fable 5.1》的 mannered prose 提示（例 1、2 是其英文例子的中文对应）；Arize 2026 标注（contrast reframe 约占 Opus 5 的 153 处 Claudism 里的 30 处）；本机语料「不是……而是/是」Claude 每 10 万字 18 次、GPT-6.x 0–5 次。

## Anthropic 官方原文

```text
Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
```
