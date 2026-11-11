#!/usr/bin/env python3
"""把 gpt-nodefense 装成「GPT 一律生效」的常驻规则。

做三件事（都可撤销）：
  1. 在 Codex 全局 AGENTS.md（$CODEX_HOME/AGENTS.md，默认 ~/.codex/AGENTS.md）写入核心规则块。
     Codex 跑的都是 GPT，所以这里无条件生效。
  2. 在 Claude Code 全局 CLAUDE.md（~/.claude/CLAUDE.md）写入同一块规则，但加一句条件：
     只有当前模型是 GPT 系列时才生效（用 CC Switch 让 Claude Code 调 GPT 的情况）。
  3. 把 gpt-nodefense skill 软链接到 ~/.codex/skills 和 ~/.claude/skills，完整规则和例子在里面。

规则块放在两行标记之间，文件里的其他内容不动；重复运行只更新这一块。

用法：
  python3 scripts/install_gpt_nodefense.py             安装或更新
  python3 scripts/install_gpt_nodefense.py --dry-run   只打印会写什么
  python3 scripts/install_gpt_nodefense.py --remove    撤销以上三项
  python3 scripts/install_gpt_nodefense.py --codex-only / --claude-only
"""
import argparse
import os
import re
from pathlib import Path

BEGIN = "<!-- gpt-nodefense:begin -->"
END = "<!-- gpt-nodefense:end -->"
REPO = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO / "gpt-nodefense"

CORE = """## 中文回复：去防御（gpt-nodefense）

{cond}给用户写中文时照下面做（进度消息、汇报、闲聊都算）。

1. 第一句回答用户问的。
2. 篇幅跟着问题走：随口问的，几句话答完；需要步骤、建议、话术的，照样给全。要删的是给自己留后路的句子，有用的内容照常给。
3. 用肯定句说结论和做法：说「做 Y」，少说「别 X」「这不代表 X」「不能证明 X」。
4. 没做完的事写成下一步。真正影响用户决定的风险或不确定，用一句平常的话说一次，跟在建议后面。
5. 用户用过的词优先；动作写全，让做事的人当主语。
6. 按用户的原话回答他问的问题，把他当成同行：直接给信息，省掉「你实际问的是……」「很多人会……」「这是常见的误解」这类铺垫。

下面是三个好回答的样子：

问：剩饭在冰箱里放了三天，还能吃吗？
答：一般能吃，热透再吃。米饭和肉类最好两天内吃完，闻着有酸味或者表面发黏，就倒掉。

问：你刚改完导出 Excel 的功能，只在 Chrome 上试过。说一下结果。
答：导出改好了，现在中文文件名不会乱码。我只在 Chrome 上试过，你上线前用 Edge 和 Safari 各导一次看看。

问：下周第一次去面试，怎么准备？
答：把这三件事做好就够了：
- 把简历上的每段经历都准备一个具体例子，说清楚你做了什么、结果怎样。
- 查一下公司最近在做的产品，准备两个想问面试官的问题。
- 提前一天把路线和衣服定好，当天早到十分钟。

用户说「保留防御」「#defense-on」「把不确定的都列出来」时，本次对话停用这一段；「#defense-off」恢复。"""

COND_CODEX = ""
COND_CLAUDE = ("**只在你是 GPT / OpenAI 系列模型时生效**（看系统提示里的模型名，例如 gpt-6.1-sol、gpt-6-astra、"
               "codex）。Claude、DeepSeek、Kimi 等其他模型跳过这一段。\n\n")


def block(cond):
    return f"{BEGIN}\n{CORE.format(cond=cond)}\n{END}"


def upsert(path: Path, text: str, remove: bool, dry: bool):
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    m = re.search(re.escape(BEGIN) + ".*?" + re.escape(END), old, re.S)
    if remove:
        if not m:
            return f"{path}：没有这一块"
        new = (old[:m.start()].rstrip("\n") + "\n\n" + old[m.end():].lstrip("\n")).strip("\n")
        new = new + "\n" if new else ""
        act = "已删除"
    elif m:
        new = old[:m.start()] + text + old[m.end():]
        act = "已更新"
    else:
        new = (old.rstrip("\n") + "\n\n" if old.strip() else "") + text + "\n"
        act = "已写入"
    if new == old:
        return f"{path}：已经是最新"
    if dry:
        return f"[dry-run] {act} {path}\n{text if not remove else ''}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new, encoding="utf-8")
    return f"{path}：{act}"


def link(target_dir: Path, remove: bool, dry: bool):
    dst = target_dir / "gpt-nodefense"
    if remove:
        if dst.is_symlink():
            if not dry:
                dst.unlink()
            return f"{dst}：已删除链接"
        return f"{dst}：没有链接（如果是普通目录，请手动处理）"
    if dst.is_symlink() and dst.resolve() == SKILL_DIR:
        return f"{dst}：已存在"
    if dst.exists():
        return f"{dst}：已有同名目录，跳过"
    if not dry:
        target_dir.mkdir(parents=True, exist_ok=True)
        dst.symlink_to(SKILL_DIR)
    return f"{'[dry-run] ' if dry else ''}{dst} -> {SKILL_DIR}"


def main():
    if any(k in str(REPO) for k in ("scratch-workspaces", "/tmp/", "/private/tmp/")):
        print(f"提醒：仓库在临时目录 {REPO}，软链接会随目录删除失效。建议先 clone 到 ~/.claude/skills/bu-dai-biao 再运行。")
    ap = argparse.ArgumentParser()
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--codex-only", action="store_true")
    ap.add_argument("--claude-only", action="store_true")
    a = ap.parse_args()
    codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    claude_home = Path.home() / ".claude"
    out = []
    if not a.claude_only:
        out.append(upsert(codex_home / "AGENTS.md", block(COND_CODEX), a.remove, a.dry_run))
        out.append(link(codex_home / "skills", a.remove, a.dry_run))
    if not a.codex_only:
        out.append(upsert(claude_home / "CLAUDE.md", block(COND_CLAUDE), a.remove, a.dry_run))
        out.append(link(claude_home / "skills", a.remove, a.dry_run))
    print("\n".join(out))
    if not a.dry_run:
        print("新开的 Codex / Claude Code 会话生效。")


if __name__ == "__main__":
    main()
