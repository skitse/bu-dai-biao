# Claude：矫饰和否定反转

状态：草稿，待测试。

## Anthropic 官方原文（Fable 5.1 指南）

```text
Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
```

短版：`Please remove all mannered prose.`

## 中文补充（针对 Claude 中文口癖）

```text
还有两种同类写法要改。一是对比反转：「这不是技术问题，是沟通问题」。读者没以为是技术问题，这句话就是在替他制造一个错误再纠正。直接说「问题出在沟通上」，再说具体哪里。二是附和和填充：「你说得对」「其实」「真的」「一句话：」。删掉后意思不变的，就删。
```

来源：<https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1>；Arize 2026-09 标注（contrast reframe 约占 153 处里的 30 处）。
