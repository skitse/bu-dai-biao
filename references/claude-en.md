# Claude English tics (for papers and English drafts)

Claude Opus 5 / 5.5 and Fable 5.1 era. English sources are much richer than Chinese ones, so this file is in English, with a column showing the Chinese form of the same move where one exists (see `claude.md`).

## The main finding: moves, not words

Jim Bennett (Arize, September 2026) hand-annotated 53,000 words of Opus 5 output and flagged 153 "Claudisms". A list of famous phrases ("load-bearing", "delve", "crucially", "genuinely") matched only **9 of the 153**. "Load-bearing" appeared three times in 53,000 words. What he flagged were rhetorical moves. <https://arize.com/blog/anthropic-says-it-fixed-claudes-writing/>

| Move | Share of flags | Example | Chinese equivalent |
|---|---|---|---|
| Salience flag: says something matters instead of showing why | ~48 / 153 | "The interaction matters." "a fact worth internalising" "deserves a moment" | 值得注意的是、这一点很关键、值得停下来想一想 |
| Contrast reframe | ~30 | "It's a topology, not a genre." | 不是 X，而是 Y |
| Verdict intensifier | ~25 | "the honest answer", "the whole point" | 说实话、真正的问题是、最关键的是 |
| Signpost that teases instead of telling | ~20 | "Here's the part that surprises people…" | 接下来是有意思的部分、有意思的是 |
| Stock metaphor | ~10 | "load-bearing", "earns its keep" | 承重、托住、接住、扛住 |
| Gotcha framing | ~7 | "the trap is" | 坑在于、陷阱是 |

The same eval found Opus 5.5 cut the em dash from 12.9 per 1,000 words (Opus 5) to two in 57,000 words, and roughly halved the other Claudisms. "Better, but not fixed."

How to use this: when revising, look for the move. Banning the phrase doesn't work, because the model produces the same move with a different noun.

---

## CE-1 Salience flags

- Before: This distinction matters more than it first appears.
- After: (Delete. Then state the consequence: "Mixing the two inflates the error rate by about a third.")
- Before: It's worth sitting with that for a moment.
- After: (Delete.)

Family: "worth talking about", "worth stating plainly", "worth naming precisely", "this matters", "because it matters", "deserves a moment", "a fact worth internalising".

Evidence: Arize (largest category); claudisms.ai entries "worth sitting with", "worth talking about", "because it matters". <https://claudisms.ai/>

## CE-2 "It is not X. It is Y." (sentence-initial negative parallelism)

- Before: It is not a scheduling problem. It is a trust problem.
- After: People skip the meetings because they don't believe decisions made there will stick.

Evidence: smixs/awesome-claude-output-styles "Claudisms, 2026 field guide" calls it "the single most-reported pattern". <https://github.com/smixs/awesome-claude-output-styles/blob/main/docs/claudisms-2026.md>; *The Economist* (30 July 2026, via secondary sources) reports ChatGPT and Claude using "not X but Y" and rule-of-three most per 1,000 sentences; Arize "contrast reframe".

## CE-3 Verdict intensifiers and announced candor

"the honest answer", "honestly", "frankly", "genuinely", "the real tension", "the whole point", "the whole game", "the only thing that matters".

- Before: The honest answer is that nobody knows.
- After: Nobody knows.
- Before: That's the whole game.
- After: (Say what the thing does, at its real size.)

Evidence: Anthropic's own app system prompts tell Claude to avoid "genuinely", "honestly", "actually" (Opus 4.8) and "straightforward" (Sonnet 4.6) <https://platform.claude.com/docs/en/release-notes/system-prompts>; archiewood/claudeisms measures "genuinely" at 224× its rate in Stack Overflow comments <https://github.com/archiewood/claudeisms>; claudisms.ai "the whole game" family.

## CE-4 Teasing signposts

"Here's where it gets interesting", "Here's the part that surprises people", "Here's the thing that landed", "the one that surprised me most", "the question I keep coming back to".

- After: open with the thing itself.

Evidence: Arize "signpost"; claudisms.ai (several entries).

## CE-5 Stock and placement metaphors

| Claudism | Plain version |
|---|---|
| load-bearing | essential, the part everything depends on |
| earns its keep | still worth it |
| a dial worth turning | a parameter worth varying |
| carries the argument | the argument depends on it |
| shape (of the problem) | structure, direction, how it feels |
| lives (the risk lives in X) | is, happens, shows up |
| the engine | what drives it |
| surface (verb) | show, raise, find |
| sit with / hold (an idea) | think about / believe |
| smoking gun | the cause |
| blast radius | how much it affects |
| seam | boundary, interface |

Evidence: Anthropic, "Prompting Claude Fable 5.1", section "Writing density", calls this "mannered prose" and gives "a dial worth turning" and "earns its keep" as examples (cited in AshwinSathian/humanize-writing-skill, `reference/claude-tics.md`) <https://github.com/AshwinSathian/humanize-writing-skill>; archiewood/claudeisms measured Opus 4.7/4.8 Claude Code output against Stack Overflow comments: "load-bearing" >7,500×, "gating" 762×, "dedup" 649×, "decisive" 639×, "verdict" 633×, "scaffolds" 572×, "settles" 435×, "handoff" 360× (note: "load-bearing" also appears in the Claude Code system prompt); claudisms.ai; smixs field guide.

## CE-6 Agent-report vocabulary (Claude Code)

From archiewood's ranking (all ≥ 20× Stack Overflow rate): verdict, decisive, settles, gating/gated, scaffold(ed), blocker, pre-existing, drift, surfaced, divergence, round-trip, flips, stale, wiring/wired, mint, landed, parity, mirrors, seam, authoritative, canonical, cleanly, silently, verbatim, honest, fallback.

In a paper these words rarely belong. Replace with the ordinary term, or delete.

## CE-7 Fragments for drama

- Before: Not a detail. A design decision.
- After: This was a design decision, not an oversight.

Evidence: AshwinSathian `claude-tics.md` (community reports on Opus 5, via explainx.ai and paddo.dev).

## CE-8 Dense, noun-heavy, Latinate prose

Long sentences, few paragraph breaks, "significant", "increasingly", "methodology" outside technical use. When asked to be concise, Claude produces shorter but more cryptic text.

- Before: Coverage-aware cost projection: ledger-derived cost figures with exact, lower-bound, and unavailable states.
- After: Don't show incomplete cost totals as exact. Say "at least $X" or "unknown".

Evidence: Anthropic Fable 5.1 prompting guide (dense prose, vs. previous model); *The Economist* names Gemini and Claude as the strongest cases of long, Latinate vocabulary; the before/after pair is the r/ClaudeCode example quoted in the smixs field guide.

## CE-9 Combat framing and compliment sandwiches

"here's where I'd push back", "here's where I'd hold the line", "You're right to push back, and that's on me."

Evidence: smixs field guide; anthropics/claude-code issue #3382 ("You're absolutely right!").

## CE-10 Copula avoidance

"serves as", "stands as", "functions as" for "is".

Evidence: smixs field guide; Wikipedia "Signs of AI writing" (attributes "serves as" to GPT and Gemini as well, so not Claude-only).

## CE-11 Em dashes (version-dependent)

- Opus 5: 12.9 em dashes per 1,000 words (Arize). *The Economist* (July 2026): only Claude exceeded the human em-dash rate among ChatGPT, Claude, Gemini, Grok.
- Opus 5.5: two in 57,000 words (Arize).

So a dash-heavy English draft points to Opus 5 or earlier, not Opus 5.5.

---

## For academic English specifically

Order of work:

1. Cut salience flags and signposts (CE-1, CE-4). Reviewers notice these first.
2. Replace stock metaphors (CE-5) with the technical term.
3. Turn "It is not X. It is Y." (CE-2) into a direct claim with a citation.
4. Split dense sentences (CE-8) where the subject changes.
5. Keep hedges that carry information ("may", "in this sample"). One hedge per claim.

Do not invent figures, quotes, or references to sound specific.

## Note on banlists

The smixs repo deliberately does not paste its list into prompts, because instruction-tuned models tend to reproduce tokens mentioned even inside a ban. The DeepSeek V4 feedback report says the same ("禁词表当提词器"). Use these lists for revision, not as negative prompts.
