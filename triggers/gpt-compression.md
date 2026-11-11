# GPT-6.x：信息压缩

状态：草稿，待测试。

## 中文版

```text
压缩写法，指为了少写几个字，把一整句话压进一个自造名词或一个单字里：「统一验收口径后再做回归核对」「拆开核一下」「这个分支会吃掉异常」。写的人省了字，读的人得自己猜出被省掉的动作、对象和因果关系。改法：假设读者第一次看到这件事。自造名词拆回「谁对什么做了什么」（「先定好按什么标准算测试通过」），单字动词换回完整说法（「检查一下」），让真正做事的人或程序当主语（「这个分支捕获了异常，但没有处理」）。句子可以长一点，只要读者一次能看懂。
```

## OpenAI 官方原文

```text
Avoid invented compound labels like "exact-head checks" and "editorial-row layouts", vague qualifiers, and canned transitions; use plain verbs and prepositions to state the actual relationship directly.

Use plain language over jargon, and reference technical details only to the degree that it helps illustrate an idea or your work to the user.
```

依据：Clark、Martin、Mahowald, arXiv 2610.29162（长度惩罚导致堆叠名词、名词当动词、拟人主语增多）。
