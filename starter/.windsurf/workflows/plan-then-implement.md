---
name: plan-then-implement
description: The standard flow — architect plans, reviewer reviews the plan, implementer executes, reviewer reviews the diff, tester fills coverage, shipper opens PR.
---

# /plan-then-implement

For any task bigger than "change a string and commit". Produces a reviewable diff end-to-end.

## Flow

1. **Plan** — `@architect`
   - Reads `AGENTS.md` + `vault/INDEX.md`
   - Writes plan to `~/.windsurf/plans/<slug>.md`
   - Asks clarifying questions if needed
2. **Review plan** — `@reviewer`
   - Checks the plan against AGENTS.md invariants
   - Verifies alternatives are real, rollback is real
   - Verdict: LGTM / CHANGES REQUESTED / NEEDS DISCUSSION
3. **Implement** — `@implementer`
   - Reads plan in full
   - Executes checkbox-by-checkbox
   - Runs tests after every batch
4. **Review diff** — `@reviewer`
   - Correctness, security, tests, smell, perf, invariants
   - Blockers must be fixed before proceeding
5. **Fill coverage** — `@tester`
   - Identifies gaps
   - Writes tests matching existing style
   - Runs suite, hits coverage target
6. **Ship** — `@shipper`
   - Verifies all green (lint, types, tests, build)
   - Cleans up commits
   - Writes PR description
   - Opens PR

## Usage

```
/plan-then-implement Add a rate limiter for /api/auth/*
```

Cascade will walk all six steps. You can stop at any point.

## When to Shortcut

- For a true one-liner (< 20 lines), skip to implementer.
- For a pure docs/config change, skip to implementer + shipper (no tester needed).
- For a research-only task, architect alone is enough.

## Pair With Worktrees

For bigger tasks, run steps 3–5 in parallel worktrees. See
[§11 Worktrees](https://github.com/OnlyTerp/windsurf-unlocked#11-worktrees--parallel-cascade).
