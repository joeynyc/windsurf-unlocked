# Windsurf Unlocked Starter

One-command install of a production-grade `.windsurf/` setup. Drops an 8-role subagent team, working hooks, curated skills, Spec-Driven workflows, a wiki scaffold, and an `AGENTS.md` constitution into any repo.

Takes ~30 seconds to install. Turns any project into a Cascade power-user environment.

---

## What You Get

```
<your-repo>/
├── AGENTS.md                         # Project constitution + invariants (edit me)
├── vault/                            # Agentic Wiki — persistent project memory
│   ├── INDEX.md
│   ├── decisions/
│   ├── services/
│   ├── incidents/
│   ├── people/
│   └── glossary.md
└── .windsurf/
    ├── agents/                       # 8 personality profiles
    │   ├── architect/AGENT.md        # Plan Mode, clarifying questions
    │   ├── implementer/AGENT.md      # SWE 1.6 Fast, terse, parallel tools
    │   ├── reviewer/AGENT.md         # Read-only PR review
    │   ├── tester/AGENT.md           # Coverage ≥80%, runs the suite
    │   ├── security/AGENT.md         # Threat model + vuln scan
    │   ├── docs/AGENT.md             # README/CHANGELOG keeper
    │   ├── perf/AGENT.md             # Benchmarks + regressions
    │   └── shipper/AGENT.md          # PR descriptions, release notes
    ├── skills/                       # Auto-triggered on intent
    │   ├── wiki-update/              # Maintain vault/ after each session
    │   ├── wiki-query/               # Read vault/ before starting work
    │   ├── pr-ready/                 # Turn branch into clean PR
    │   ├── test-backfill/            # Fill gaps to hit coverage target
    │   ├── secret-scrubber/          # Block diffs with leaked secrets
    │   ├── planning-with-files/      # Manus-style persistent plan files
    │   ├── ast-grep/                 # Structural (AST-aware) search + refactor
    │   └── compact-hygiene/          # Proactive /compact with preservation
    ├── hooks/                        # Shell + Python hook scripts
    │   ├── secret_scan.py            # pre_tool_use on file writes
    │   ├── langfuse_logger.py        # post_cascade_response telemetry
    │   ├── wiki_update.py            # auto-invokes wiki-update skill
    │   └── post_setup_worktree.sh    # copy .env, install deps
    ├── hooks.json                    # Wires the above to Cascade events
    ├── workflows/                    # Slash commands
    │   ├── plan-then-implement.md
    │   ├── speckit-specify.md
    │   ├── speckit-plan.md
    │   ├── megaplan.md
    │   ├── ralph-safe.md             # Persistent loop with killswitch + cost cap
    │   ├── prd-driven.md             # Spec-first, anti-drift feature workflow
    │   ├── reflection-loop.md        # generate → evaluate → revise
    │   └── visual-iteration.md       # Screenshot → describe → fix (Chrome DevTools MCP)
    └── mcp_config.json               # Curated server list (all Streamable HTTP)

../plans/                              # File-based plans (planning-with-files skill)
../templates/
    └── PRD.template.md               # 9-section drop-in PRD
```

Every piece is documented in [the main guide](../README.md) — this is just the working reference implementation.

---

## Install

```bash
# From the root of whatever repo you want to upgrade
curl -fsSL https://raw.githubusercontent.com/OnlyTerp/windsurf-unlocked/main/starter/install.sh | bash
```

Or if you don't pipe curl to bash (respect):

```bash
git clone --depth 1 https://github.com/OnlyTerp/windsurf-unlocked /tmp/wu
bash /tmp/wu/starter/install.sh
```

The installer:
1. Copies `.windsurf/` and `vault/` into the current directory
2. Copies `AGENTS.md` (only if one doesn't already exist — won't overwrite)
3. Prints the 3 things you need to customize before first use
4. Prints the Cascade commands to verify everything loaded

---

## First 5 Minutes After Install

1. **Edit `AGENTS.md`** — fill in the "Stack" section and any project-specific invariants. The template has a checklist.

2. **Enable the hooks you want.** `hooks.json` ships with all hooks disabled by default. Flip the ones you want on:
   ```bash
   $EDITOR .windsurf/hooks.json
   ```
   Recommended for day one: `secret_scan` (pre-commit safety) and `wiki_update` (auto-maintains vault/).

3. **Add any missing MCP secrets.** `mcp_config.json` references env vars — set them in your shell profile:
   ```bash
   export GITHUB_TOKEN="..."
   export LANGFUSE_PUBLIC_KEY="..."
   export LANGFUSE_SECRET_KEY="..."
   ```

4. **Verify in Cascade.** Open the repo in Windsurf and run:
   ```
   @reviewer Read AGENTS.md and list any invariants that need to be filled in
   ```
   If the `reviewer` subagent loads and reads `AGENTS.md`, you're done.

---

## What to Customize

| File | What to change |
|---|---|
| `AGENTS.md` | Stack, commands, invariants — see the `<FILL IN>` markers |
| `.windsurf/mcp_config.json` | Add/remove MCP servers for your stack |
| `.windsurf/agents/implementer/AGENT.md` | Preferred model pin (defaults to SWE 1.6 Fast) |
| `vault/INDEX.md` | Starts empty — grows as the wiki-update skill fires |
| `vault/glossary.md` | Your team's terms of art |

Everything else works as-is.

---

## Updating

```bash
# Re-run the installer — it won't overwrite anything you've edited
curl -fsSL https://raw.githubusercontent.com/OnlyTerp/windsurf-unlocked/main/starter/install.sh | bash -s -- --update
```

`--update` refreshes the skills/hooks/workflows but skips `AGENTS.md`, `mcp_config.json`, and `vault/`.

---

## License

MIT. Take it. Fork it. Ship it.

If you publish derivative starters, a link back to [windsurf-unlocked](https://github.com/OnlyTerp/windsurf-unlocked) is appreciated but not required.
