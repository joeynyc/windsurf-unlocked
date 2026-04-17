---
name: speckit-specify
description: GitHub Spec Kit v0.5.0 — turn a loose request into a formal spec. First step of the Spec-Driven Development flow.
---

# /speckit-specify

Turn a user request into a formal spec document.

## Input

A natural-language feature request. Examples:
- "Add a rate limiter for /api/auth/*"
- "Let users export their data as CSV"
- "Migrate from MySQL to Postgres"

## Output

A markdown spec at `specs/NNN-<slug>.md` with these sections:

```markdown
# Spec NNN: <Feature title>

**Status:** Draft
**Date:** YYYY-MM-DD
**Author:** <name or @agent>
**Related ADRs:** <link to vault/decisions/ if any>

## Problem
One paragraph. What's the user pain? Why now?

## Proposed solution
One paragraph. What are we building?

## User stories
- As a <role>, I want <capability>, so that <outcome>.
- ...

## Functional requirements
- [ ] FR-001: ...
- [ ] FR-002: ...

## Non-functional requirements
- [ ] NFR-001: p95 latency ≤ 200ms
- [ ] NFR-002: 99.9% availability
- [ ] NFR-003: scales to N users

## Out of scope
- What this does *not* include, explicitly
- ...

## Open questions
- [ ] Q-001: ...
- [ ] Q-002: ...

## Success metrics
- How we'll know it worked: metrics, signals, timelines
- ...

## References
- External docs, similar patterns in other systems, prior incidents
```

## Process

1. **Read** `AGENTS.md` (stack + invariants) and `vault/INDEX.md` (prior decisions).
2. **Draft the spec** — be specific, avoid hand-waving.
3. **Flag open questions** — don't invent answers.
4. **Cite constraints** from AGENTS.md invariants that shape the spec.
5. **Save** to `specs/NNN-<slug>.md` (auto-increment NNN).
6. **Next step:** run `/speckit-clarify` to reduce open questions, then `/speckit-plan` to decompose.

## Template origin

Derived from [GitHub Spec Kit](https://github.com/github/spec-kit) v0.5.0 — adapted for Cascade Workflows. The full Spec Kit toolchain (7 commands) is documented in
[§21 Spec-Driven Development](https://github.com/OnlyTerp/windsurf-unlocked#21-spec-driven-development-with-cascade).
