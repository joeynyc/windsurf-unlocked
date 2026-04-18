---
name: max-think
description: Route the next task to Opus 4.7 Think — MAX tier for deepest reasoning. Use sparingly for the hardest 5% of your work.
---

# MAX Think Mode (Opus 4.7 Think — MAX)

Use the highest thinking-level tier on Opus 4.7 for this task.

## When to Run

- Hardest 5% of your work: novel algorithms, distributed-systems debugging, gnarly data-model decisions
- Cross-system architecture or migration planning
- Security / threat-model review on a new data path
- Root-cause analysis on bugs that have survived 2+ fix attempts
- Irreversible decisions where getting it wrong costs more than the extra credits

## When NOT to Run

- A lower tier (Think Low / Medium / High) can plausibly solve it
- The task is search-shaped, not reasoning-shaped — a wiki lookup or `@docs` query would answer it faster and cheaper
- You haven't read the surrounding code yet (MAX can't fix a context deficit)
- Simple refactors, typo fixes, straightforward test writing — use SWE 1.6 Fast or base Opus 4.7
- You're on free tier or close to your credit cap (MAX carries the highest multiplier; check the in-picker rate display first)

## Instructions

Switch Cascade to **Opus 4.7 Think — MAX** in the model picker, then:

- Prefer correctness over speed — this is a reasoning task, not a speed run
- Produce 2–3 hypotheses before converging on one
- Cite specific files and line ranges for every claim
- If uncertainty is unresolvable with the information at hand, say so and stop — do not guess
- Acceptable latency: up to 60s to first token. Do not preempt.
- When done, write the conclusion to `plans/<YYYY-MM-DD>-<slug>.md` so the reasoning survives session compaction

## Never

- Use MAX as a default. Every MAX call that a lower tier could have handled is wasted credits.
- Chain multiple MAX calls in one session without re-evaluating whether the next one still needs MAX.
- Skip reading the surrounding code first. MAX amplifies reasoning; it doesn't substitute for context.
