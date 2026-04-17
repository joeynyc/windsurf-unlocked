---
name: prd-driven
description: Starts a new feature by writing a PRD (product requirements doc) that Cascade reads at the start of every session. The cheapest drift-prevention device ever invented. Pair with Planning With Files for the full workflow.
---

# PRD-Driven Development

Before any non-trivial feature, write a 1-2 page PRD at `plans/prd-<slug>.md`. Cascade reads it at session start. Scope drift becomes a file diff, not a surprise in review.

## Why PRDs Work With Coding Agents

1. **Grounds every session in the same intent.** Agent comes back three days later, reads the PRD, resumes aligned.
2. **Surfaces ambiguity early.** Writing the PRD forces you to answer questions Cascade would otherwise guess at (and guess wrong).
3. **Commit-able contract.** Diffs to the PRD during implementation are visible. Scope creep has a paper trail.
4. **Gives reviewers a spec to grade against.** The PR description becomes "does this match the PRD?" instead of subjective review.

## When to Use

- Any feature > 1 day of work
- Any cross-service / cross-repo change
- Any change that touches auth, billing, data retention, or a public API
- Any task where 3+ reasonable interpretations exist

## The Template

See [`starter/templates/PRD.template.md`](../../templates/PRD.template.md). The 9 sections:

1. **One-line summary** — what this is, in one sentence
2. **Problem** — who hurts today, in what way, and how often
3. **Goals** — measurable outcomes (not "improve UX")
4. **Non-goals** — what this does NOT do (the most valuable section)
5. **User stories** — 3-5 concrete scenarios with steps
6. **API / UI surface** — endpoints, schemas, screens that change
7. **Constraints** — AGENTS.md invariants in play, deadlines, dependencies
8. **Risks & open questions** — what we don't know yet
9. **Acceptance criteria** — bulleted "this is done when ..."

## Workflow

```
1. Human drafts prd-<slug>.md from template
2. @reviewer PRD review pass (not a code review — a spec review)
3. @architect turns PRD into plans/<slug>.md (see Planning With Files)
4. @implementer works the plan checkbox-by-checkbox
5. @reviewer final diff review against the PRD
6. @shipper opens the PR referencing both PRD and plan
```

## Cascade Prompts

**Starting:**
```
Read plans/prd-checkout-flow.md. If anything is ambiguous, list
the ambiguities — don't guess. Wait for me to resolve them before
moving to the plan.
```

**Resuming days later:**
```
Read plans/prd-checkout-flow.md and plans/checkout-flow.md.
Report current checkbox status and what you'd pick up next.
Don't start coding yet.
```

**Mid-implementation drift check:**
```
The diff so far: [paste]. Does it match plans/prd-checkout-flow.md?
List any drift. For each drift item, recommend: (a) update the PRD
or (b) change the code to match.
```

## PRD vs Spec vs Plan

| File | Audience | Contents | Lifetime |
|------|----------|----------|----------|
| `prd-<slug>.md` | Product + eng | What & why (problem-space) | Until feature ships; then archived |
| `spec-<slug>.md` | Eng only | How at API/schema level | Same as PRD |
| `<slug>.md` (plan) | Agent + reviewer | Checkbox breakdown of tasks | One PR |

Not every feature needs all three. A tiny fix needs none. A public-API-breaking refactor needs all three.

## Anti-Patterns

- ❌ PRD that's really just a task list — that's a plan, not a PRD
- ❌ PRD without "Non-goals" — the most important section is always the one people skip
- ❌ PRD written after the code — that's not a PRD, that's documentation. Both are fine, neither prevents drift.
- ❌ PRD updated silently during implementation without re-reviewing — the whole point is visible drift

## Credits

Pattern from [prd.md by subtle.so](https://www.subtle.so/prd-md), [vibecoding.app's anti-drift guide](https://vibecoding.app/blog/anti-drift-workflows-vibe-coders-guide), and the broader Spec-Driven Development movement covered in [§21](../../../README.md#21-spec-driven-development-with-cascade).
