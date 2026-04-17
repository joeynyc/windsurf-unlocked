# AGENTS.md — Project Constitution

> This file is read by Cascade (and any AGENTS.md-aware tool: Claude Code, Cursor, Codex, Gemini CLI) at the start of every session. Keep it short, specific, and current. If a rule isn't being followed, it's probably buried under noise — cut the noise.

---

## Project

**Name:** <FILL IN>
**One-line purpose:** <FILL IN — e.g., "B2B invoice SaaS for Shopify merchants">
**Stage:** <FILL IN — prototype / beta / production>

## Stack

- **Language(s):** <FILL IN>
- **Framework:** <FILL IN>
- **Database:** <FILL IN>
- **Package manager:** <FILL IN — pnpm / uv / cargo / ...>
- **Deploy target:** <FILL IN>

## Commands

| What | Command |
|---|---|
| Install | `<FILL IN>` |
| Dev server | `<FILL IN>` |
| Test | `<FILL IN>` |
| Lint | `<FILL IN>` |
| Typecheck | `<FILL IN>` |
| Build | `<FILL IN>` |

Run these *yourself* before declaring a task done. The reviewer and tester subagents will too.

---

## Invariants (Constitution)

These are never negotiable. If a request would violate them, **ask first — don't silently proceed.**

1. **Security.** No API key, token, or secret ever in logs, commits, tests, or error messages. PII never in logs. Run `.windsurf/hooks/secret_scan.py` before any commit.
2. **Testing.** Every new public function gets a test. Coverage stays ≥ 80% on `src/`. Never weaken an existing test to make a change pass — fix the change.
3. **API shape.** Every endpoint returns `{ ok: boolean, data?: T, error?: { code, message } }`. No exceptions.
4. **Migrations.** Schema changes are always a two-phase deploy (expand → migrate → contract). No destructive migrations that can't be rolled back.
5. **Dependencies.** No new dependency with < 6 months of commit history, < 100 stars, or unknown maintainer. If you must add one, justify it in the PR.
6. **AI diffs.** Any Cascade-generated diff over 50 lines gets a `@reviewer` pass before commit. For production code, also a `@security` pass.
7. **Docs.** If you change behaviour, you update docs. The `@docs` subagent runs at the end of every feature branch.

---

## Directory Layout (What Lives Where)

```
<FILL IN — the 5-10 directories a new contributor would care about>
```

Example:
```
src/api/          # HTTP endpoints
src/domain/       # Business logic, no I/O
src/db/           # Schema + migrations
tests/            # Jest + Playwright
vault/            # Agentic wiki — read before starting any non-trivial task
.windsurf/        # Agent configuration
```

---

## Style

- <FILL IN — language-specific conventions>
- No comments on self-evident code. Only explain *why*, never *what*.
- No `any` / `getattr` / catch-all types. If you're reaching for one, you don't understand the type yet.
- Errors are values, not exceptions. (Adjust if your stack disagrees.)
- Imports at top. Never import inside a function.

---

## Never Do

- Commit to `main` / `master` directly — always a PR.
- `git push --force` on shared branches. `--force-with-lease` on your own feature branch is fine.
- Skip hooks (`--no-verify`) unless explicitly asked.
- Add a dependency to solve a 10-line problem.
- Delete or rewrite a migration that has run in production.
- Log request bodies for endpoints that handle PII.

## Always Do

- Read `vault/INDEX.md` before starting a non-trivial task — the wiki probably has context.
- After a session that made a decision, added a fact, or fixed an incident — the `wiki-update` skill runs automatically via hook. If it doesn't, run it manually.
- At PR time, run the `pr-ready` skill to polish the description + commits.

---

## Subagents

This repo has 8 role subagents in `.windsurf/agents/`. Invoke by `@<role>`:

| Role | When to use |
|---|---|
| `@architect` | "Help me plan X" — produces a spec/plan before any code |
| `@implementer` | "Implement the plan in `~/.windsurf/plans/X.md`" — SWE 1.6 Fast, terse |
| `@reviewer` | Any non-trivial diff — read-only PR-style feedback |
| `@tester` | "Fill test gaps" / "why does the suite fail?" |
| `@security` | Threat model, vuln scan, auth review |
| `@docs` | README / CHANGELOG / AGENTS.md updates |
| `@perf` | Profiling, benchmarking, regression hunting |
| `@shipper` | PR descriptions, release notes, deploy checklists |

Run them in parallel via [Worktrees](https://github.com/OnlyTerp/windsurf-unlocked#11-worktrees--parallel-cascade) in a single [Space](https://github.com/OnlyTerp/windsurf-unlocked#2-agent-command-center--spaces).

---

## Rules Loaded From

- `AGENTS.md` (this file) — project rules, always loaded
- `.windsurfrules` — legacy Windsurf rules, also loaded if present
- `.windsurf/agents/<role>/AGENT.md` — per-subagent personality, loaded on `@<role>` invoke
- `.windsurf/skills/**/SKILL.md` — auto-loaded when the skill's `description:` matches intent
- Cascade Memories (personal, not committed) — loaded via Cascade UI

If any of those contradict this file, **this file wins.**
