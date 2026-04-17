---
name: megaplan
description: Aggressive Plan Mode — asks the full battery of clarifying questions up front before writing a line of plan. Use for non-reversible or high-complexity work (migrations, redesigns, new core systems).
---

# /megaplan

Plan Mode, but paranoid. For work where getting the plan wrong costs days.

## When to Use

- Database migrations
- API redesigns with consumer impact
- New core subsystems (auth, billing, orchestration)
- Performance-critical rewrites
- Anything that touches production data
- Anything the team has opinions about

## How It Differs From `/plan-then-implement`

Regular Plan Mode asks 3–5 clarifying questions, then writes. Megaplan asks 15–20 questions across these dimensions before writing anything:

### Scope
- What is explicitly in scope?
- What is explicitly out of scope?
- What adjacent systems are affected?

### Constraints
- What AGENTS.md invariants apply?
- What prior ADRs in `vault/decisions/` apply?
- What deadlines / dependencies / blockers?
- What's the rollout constraint — instant, staged, dark-launch?

### Users
- Who uses this? (Internal, external, API consumer, admin?)
- What do they expect today? What will change?
- Is downtime acceptable? How much?

### Data
- Does this touch persistent state? Migrate schema?
- How much data, how old, what's the read/write pattern?
- What's the backup/rollback plan if migration fails halfway?

### Performance
- What's the current p50/p95/p99?
- What's the target?
- How will we measure?

### Security
- New trust boundaries? New auth surface? New PII?
- Compliance impact (SOC2 / GDPR / HIPAA)?

### Team
- Who else touches this code?
- Who needs to review?
- Who's on-call during rollout?

### Rollback
- Specifically, how do we undo this if prod catches fire?
- What's the maximum time we'd accept between "something's wrong" and "it's rolled back"?

## Output

Same format as `/speckit-plan`, but *every* section is filled in. No `TBD`s. Pair with
[§21 Spec-Driven Development](https://github.com/OnlyTerp/windsurf-unlocked#21-spec-driven-development-with-cascade)
for the full SDD flow.

## Never

- Skip a question to "save time." The questions exist because someone got burned.
- Accept "we'll figure it out later" on migration or rollback. Figure it out now.
- Write megaplans for routine features. It's overhead; use it when warranted.
