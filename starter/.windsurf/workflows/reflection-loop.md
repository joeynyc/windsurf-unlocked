---
name: reflection-loop
description: Generate → evaluate → revise. Use when there's an external quality signal (tests, lints, types) or a separate critic model. Boosts coding accuracy but can harm tasks without external verification — the workflow calls out when NOT to use it.
---

# Reflection Loop

The agent produces an output, something evaluates it, and the agent revises if the evaluation flags a problem. This pattern drove HumanEval from 80% → 91% in published studies. But naive self-reflection **decreases** performance on tasks without external grounding (e.g. GSM8K math). Use it only where the evaluation signal is external and deterministic.

## Three Variants — Pick the Right One

### 1. External-Signal Retry (the one that always works)

The evaluator is code: a test runner, a type checker, a linter, a compiler.

```
generate → run external signal → pass? done. fail? retry with error.
```

**Good for:** test-driven implementation, type errors, compile errors, lint violations, schema validation.

**Use:** the [`ralph-safe`](./ralph-safe.md) workflow is the production-grade version of this.

### 2. Critic-Model Review (works for code quality)

A *different* model critiques the first model's output. Because each has different biases and training data, the critic catches what the generator misses.

```
Generator (SWE 1.6 Fast) → Critic (Claude Opus 4.6) → Generator rewrites
```

**Good for:** security review, performance review, code-style enforcement, documentation quality.

**Windsurf mapping:** the `@reviewer` subagent pinned to a frontier model (Opus 4.6 or GPT-5.4), reviewing work from `@implementer` pinned to SWE 1.6 Fast.

**Cascade prompt:**
```
@implementer just produced <diff>.
@reviewer please do a PR-style review. Focus on correctness and security.
Output: a numbered list of issues with severity.
Then @implementer addresses the issues one at a time.
```

### 3. Self-Critique (use sparingly — dangerous)

The same agent re-reads its output and critiques it against a checklist.

```
Generator → Generator (rewrites with checklist) → output
```

**Good for:** drafts, plans, docs, emails — subjective artifacts where "better" is about clarity, not correctness.

**Bad for:** math, factual claims, code logic. Research shows models often "correct" correct answers to wrong ones when self-reflecting without grounding.

**Cascade prompt (the right way):**
```
Read your draft above. Score it against this checklist:
- [ ] Is the Goal section 1 paragraph?
- [ ] Are there explicit Non-goals?
- [ ] Does every task have an acceptance criterion?
- [ ] Is the rollback plan concrete (<10 min)?

Only rewrite sections where the checklist fails.
Don't touch sections that already pass.
```

The explicit checklist is load-bearing. Without it, self-critique degrades.

## When NOT to Reflect

- ❌ Math or arithmetic — self-correction reduces accuracy
- ❌ Factual retrieval ("what year did X happen?") — use RAG or tools, not reflection
- ❌ Creative writing the user liked — reflection tends toward safe/bland
- ❌ Anything where the external signal is missing — use critic-model review instead

## Combining With Other Patterns

- **Reflection + Planning With Files:** Generator produces a plan; Critic reviews the plan before implementation starts.
- **Reflection + Ralph Loop:** External-signal variant — the Ralph loop IS a reflection loop.
- **Reflection + Subagents:** Each subagent is already a specialist; `@reviewer` is the built-in critic. Use them.

## Guardrails

- **Cap the iterations.** 3 rounds of critique-rewrite is usually plenty. 5 is a code smell.
- **Measure whether it helps.** Track before/after on a specific metric. If reflection isn't moving the number, stop using it.
- **Log the critiques.** When the agent ignores a critic's feedback repeatedly, that's a signal the critic is wrong or the generator can't address it — escalate to human.

## Credits

Pattern documented in [ToolHalla's reflection-pattern post](https://toolhalla.ai/blog/reflection-pattern-ai-agents-2026) and grounded in the research summarized at [tianpan.co — closed-loop self-improvement](https://tianpan.co/blog/2026-04-10-agents-teach-themselves-closed-loop-self-improvement) and [Nexumo's failure-mode investigation](https://medium.com/@Nexumo_/i-tried-agent-self-correction-tool-errors-made-it-worse-d6ea76a17c1c).
