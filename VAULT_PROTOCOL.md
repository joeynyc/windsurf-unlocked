# Vault Protocol — Drop-In AGENTS.md Block

> A compounding, markdown-first alternative to embeddings-based RAG for agent memory. Karpathy-advocated. Works with Cascade, Claude Code, Cursor, Codex, and Gemini CLI identically.

Paste the block below into your `AGENTS.md` (or append this whole file as `vault/PROTOCOL.md` and reference it from `AGENTS.md`). You can start with an empty `vault/` and it compounds over weeks of sessions.

## Why Vault > RAG for Agent Memory

- **Readable by humans.** You can diff, grep, and hand-edit it. Vector embeddings are a black box.
- **Compounds across sessions.** Every session enriches the vault; the next session is smarter.
- **Git-tracked.** You can see what the agent wrote, review it, revert bad entries.
- **Cheap.** One `rg` or file read — no embedding infra, no recall/precision tuning.
- **Portable.** Works with any agent that can read files.

## Directory Layout

Matches [`starter/vault/`](./starter/vault) — if you installed via `install.sh`, this is already scaffolded.

```
vault/
├── INDEX.md                 # Map of Contents — what's where
├── decisions/               # Architectural decision records (ADRs)
│   └── ADR-001-use-redis-for-rate-limiting.md
├── incidents/               # Postmortems — what broke, why, and the invariant we added
│   └── 2026-04-17-stripe-webhook-storm.md
├── services/                # One page per service/component — owners, runbooks, gotchas
│   └── auth-api.md
├── people/                  # Who owns what (for multi-team repos)
│   └── alice.md
├── moc/                     # Maps of Content — topic-level hubs that link related pages
│   └── billing.md
└── glossary.md              # Project-specific vocabulary (one file, not a directory)
```

Every file is plain markdown, 20–150 lines. One topic per file. Title-case slug.

The `wiki-update` skill in the starter kit writes to these exact paths — if you diverge (adding `runbooks/`, `gotchas/`, `patterns/`, etc.), update [`starter/.windsurf/skills/wiki-update/SKILL.md`](./starter/.windsurf/skills/wiki-update/SKILL.md) and `vault/INDEX.md` to match so agents don't write to directories that don't exist.

## The AGENTS.md Block (copy-paste)

```markdown
## Vault Protocol

This repo maintains a compounding `vault/` of project knowledge. The vault is the
first place you look and the last place you write.

### At Session Start

1. Read `vault/INDEX.md` to see what's documented.
2. If the task touches a topic with an existing vault page, read it BEFORE reading source code.
3. If the task touches a topic WITHOUT a vault page, note it — you'll write one at the end.

### During the Session

- When you encounter something non-obvious (a gotcha, a decision, a pattern):
  - Check if `vault/` has a page for it. If yes, do not re-discover it.
  - If no, note it for end-of-session capture.
- Never cite internal knowledge the user can't verify. If it's not in `vault/`, don't claim it as fact.

### At Session End

When the session produced a decision, solved a non-obvious problem, or established a pattern:

1. Write a vault page. Location rules (match the directories that exist in this repo's `vault/`):
   - Decisions (why we chose X over Y) → `vault/decisions/ADR-NNN-<slug>.md` (next sequential number)
   - Postmortems → `vault/incidents/<YYYY-MM-DD>-<slug>.md`
   - Service/component notes, runbooks, gotchas → `vault/services/<service>.md`
   - Ownership → `vault/people/<name>.md`
   - Cross-cutting topic hubs → `vault/moc/<topic>.md` (a "Map of Content" that links related pages)
   - Glossary entries → append to `vault/glossary.md`
2. Update `vault/INDEX.md` to link the new page.
3. One page per topic. If a page grows > 150 lines, split it.

### Writing Style

- Plain markdown. No front-matter unless required by another tool.
- Lead with the **bottom line**: the answer in the first 2 lines, details below.
- Use the present tense for current state ("we use Redis") and past tense for history ("we tried DynamoDB, it didn't fit").
- Include dates on decisions — these age, and agents need to know how fresh a claim is.
- No prose walls. Headers, lists, tables, code blocks.

### Never

- Put secrets in `vault/`. It's git-tracked — assume public.
- Put PII in `vault/`. Same reason.
- Write vault pages that duplicate code comments. The vault is for things code can't express.
- Leave `vault/INDEX.md` out of date. The index is the API.

### Skills Involved

- `wiki-query` — called first, reads relevant vault pages for the current intent.
- `wiki-update` — called last, writes new or updated pages before session ends.

Both ship in the starter kit under `.windsurf/skills/`.
```

## Vault Page Templates

### Decision (ADR)

```markdown
# <Decision Title>

Date: YYYY-MM-DD
Status: proposed | accepted | superseded by <link>
Deciders: <names>

## Context
What's the situation that forces a decision?

## Options Considered
- **Option A:** ... Pros: ... Cons: ...
- **Option B:** ...
- **Option C:** ...

## Decision
We chose **Option X** because ...

## Consequences
- Positive: ...
- Negative: ...
- Follow-ups: <link to plans/>
```

### Gotcha

`````markdown
# <Surprising Behavior>

## Symptom
What you'll see in logs, tests, or prod when this bites.

## Root Cause
One paragraph. The real reason, not the first thing you tried.

## Workaround / Fix
```bash
# The exact incantation
```

## Why We Can't Just Fix It Upstream
(Optional.) If the root cause is in a library/service we don't own.
`````

### Runbook

```markdown
# How To <Recurring Task>

Last run: YYYY-MM-DD by <person>
Expected duration: ~N minutes

## Preconditions
- [ ] ...

## Steps
1. ...
2. ...
3. ...

## Verification
How you know it worked.

## Rollback
If step N failed, do ...
```

### Pattern

`````markdown
# <Pattern Name>

## When to Use
- ...

## When NOT to Use
- ...

## The Pattern
```ts
// Minimal example
```

## Where We Use It
- `src/billing/idempotency.ts`
- `src/webhooks/stripe.ts`

## Trade-Offs
- ...
`````

## INDEX.md Maintenance

Keep it skim-able. Group by category, one line per page:

```markdown
# Vault Index

Last updated: 2026-04-17

## Decisions
- [ADR-001 — Use Redis for rate limiting](./decisions/ADR-001-use-redis-for-rate-limiting.md) — Apr 17, 2026

## Services
- [Auth API](./services/auth-api.md)

## Incidents
- [Stripe webhook storm](./incidents/2026-04-17-stripe-webhook-storm.md)

## Maps of Content
- [Billing](./moc/billing.md)

## People
- [Alice](./people/alice.md)

## Glossary
- [Project terms](./glossary.md)
```

## Hook Integration (Auto-Capture)

The starter kit's `.windsurf/hooks/wiki_update.py` runs on `post_cascade_response_with_transcript` and suggests vault entries when the session introduced new knowledge. It does NOT auto-commit — it drops a `vault/_pending/*.md` for human review before you merge.

## Credits

Protocol synthesized from:
- [Andrej Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (Apr 4, 2026)
- [MirkoSon/llm-wiki-vault](https://github.com/MirkoSon/llm-wiki-vault) — reference implementation
- [Epsilla — RAG is Dead, Long Live the Agentic Wiki](https://www.epsilla.com/blogs/karpathy-agentic-wiki-beyond-rag-enterprise-memory)
- Covered in [windsurf-unlocked §20 Context Engineering](./README.md#20-context-engineering--the-agentic-wiki)
