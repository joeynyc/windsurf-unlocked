---
name: planning-with-files
description: Use when any non-trivial task (>20 LOC or >1 file) would otherwise be done without a persistent plan. Produces and maintains a markdown plan file that survives session compaction and restarts. Based on the Manus-style planning pattern popularized by OthmanAdi/planning-with-files (18.4k⭐).
version: 1.0.0
trigger: >
  Intent matches planning, implementing, refactoring, or shipping a non-trivial
  feature. Also triggers when user explicitly mentions "plan", "planning",
  "plan file", "plans/", "PRD", "spec", or when @architect is invoked.
---

# Planning With Files

You are the planning layer for this project. You turn vague intents into file-based plans that survive the session.

## Why File-Based Plans

- **Survive `/compact`** — in-memory plans get dropped when context compresses
- **Survive session restarts** — agent reads the file on the next session and resumes
- **Survive worktrees** — every parallel Cascade sees the same plan
- **Reviewable** — humans can read, diff, and edit the plan before you write code
- **Git-tracked** — PR reviewers see what was planned vs what shipped

## Plan File Location & Naming

All plan files live in `plans/` at the repo root:

```
plans/
├── 2026-04-17-stripe-webhooks.md
├── 2026-04-16-postgres-migration.md
└── README.md    # index of active plans
```

Filename convention: `<YYYY-MM-DD>-<slug>.md`. One plan = one PR = one merged commit.

## Plan File Template

Every plan file MUST have these sections, in this order:

```markdown
# <Title>

Status: draft | approved | in-progress | blocked | done
Owner: <human name>
Started: <YYYY-MM-DD>

## Goal
One paragraph. What changes for a user or operator when this ships?

## Non-Goals
Bulleted list of what this deliberately does NOT do. The biggest source of
scope drift is an unwritten non-goal.

## Constraints
- From AGENTS.md invariants: ...
- From user context: ...
- Hard deadlines: ...

## Approach
One or two paragraphs explaining the chosen approach. Cite 2-3 alternatives
considered with trade-offs.

## Task Breakdown
- [ ] 1. <one verb, one file-scope, one acceptance criterion>
- [ ] 2. ...
- [ ] 3. ...

## Risks & Mitigations
- **Risk:** ... **Mitigation:** ...

## Rollback Plan
If this ships and breaks production, how do we back out in <10 minutes?

## Session Log
<!-- Append a line per session. No prose. -->
- 2026-04-17 14:02 — plan drafted, reviewer feedback pending
- 2026-04-17 15:45 — @reviewer LGTM, starting task 1
```

## Operating Rules

1. **Never start coding without a plan file** for tasks > 20 LOC or spanning > 1 file.
2. **Work one checkbox at a time.** After each checkbox, update the plan file with `[x]` and a one-line note in the Session Log. Run tests before moving to the next.
3. **If a checkbox turns red**, stop. Do not move to the next. Add a `## Blocker` section, message the human, wait.
4. **If you discover the plan is wrong mid-implementation**, stop coding, update the plan, re-review with @reviewer before continuing.
5. **At session start**, ALWAYS read the latest plan file in `plans/` before opening any source file. The plan is the source of truth for intent.
6. **Commit the empty plan first.** The plan is the contract. Code that doesn't match the plan is a bug in one of them.

## Integration With Cascade Modes

- **Plan Mode** produces an in-memory plan. Your job: persist it to a file before handing off.
- **Code Mode** with `@implementer`: pass the plan file path. The implementer works checkbox-by-checkbox.
- **Ask Mode**: never creates plans; only reads them.

## Anti-Patterns

- ❌ "Let me just quickly ..." — that's how scope drift starts. Write the plan.
- ❌ Plans longer than 800 lines — if it's that big, split it into multiple plans.
- ❌ Task breakdowns with no acceptance criteria — "refactor auth" is not a task.
- ❌ Marking `[x]` when tests are red — never.

## Hand-Off

When the plan is drafted, hand to `@reviewer` for a plan-review pass before any implementation. Only `@implementer` touches code, and only after the plan is approved.

## Credits

Inspired by [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) (18.4k⭐) and Andrew Shu's [markdown-plan-files](https://github.com/0xandrewshu/ai-utils/tree/main/rule-markdown-plan) pattern.
