---
name: speckit-plan
description: GitHub Spec Kit v0.5.0 — decompose an approved spec into an implementable plan with checkboxes. Runs after /speckit-specify and /speckit-clarify.
---

# /speckit-plan

Take an approved spec and turn it into a concrete plan `@implementer` can execute.

## Input

An approved spec at `specs/NNN-<slug>.md`. If the spec has open questions, stop and run `/speckit-clarify` first.

## Output

A plan at `~/.windsurf/plans/NNN-<slug>.md`:

```markdown
# Plan NNN: <Feature title>

**Spec:** specs/NNN-<slug>.md
**Status:** Ready for implementation
**Est. complexity:** S | M | L | XL

## Goal
One paragraph, copy from the spec.

## Approach
How we're building it. Architectural sketch. Which files change.

### Alternatives considered
- **<Alt 1>:** rejected because...
- **<Alt 2>:** rejected because...

## Files to touch
- `src/...` — add ...
- `src/...` — modify ...
- `tests/...` — add ...
- `docs/...` — update ...

## Task breakdown

### Phase 1: Foundations
- [ ] Task 1.1: ...
- [ ] Task 1.2: ...

### Phase 2: Core
- [ ] Task 2.1: ...

### Phase 3: Wire up + tests
- [ ] Task 3.1: ...

### Phase 4: Docs + PR
- [ ] Task 4.1: Update README / AGENTS.md / CHANGELOG
- [ ] Task 4.2: Open PR via @shipper

## Risks & mitigations
- **Risk:** ...  **Mitigation:** ...

## Rollback
How to undo this if it breaks prod. Specific commands / feature-flag toggles.

## Dependencies
- Secrets needed: ...
- Infra changes: ...
- External services touched: ...
```

## Process

1. **Read the spec.** If status is Draft or questions are open, stop.
2. **Scan the codebase** for files the plan will touch. List them.
3. **Consider ≥ 2 approaches.** Document why you picked this one.
4. **Break into phases** — each phase ships a coherent change.
5. **Tasks should be 1–3 hours each.** If a task is bigger, split it.
6. **Write the rollback** — if you can't, the plan is missing something.
7. **Hand off to `@reviewer`** before implementation starts.

## Never

- Produce a plan without reading the referenced spec.
- Skip the rollback section.
- Leave tasks vague ("implement the thing") — every task should be executable.
