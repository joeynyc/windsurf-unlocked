# Windsurf Unlocked

> **Tested on Windsurf 1.9600.41 — April 2026** · The community power-user bible for Cascade

### Every feature Cascade ships that most people aren't using — configured properly

*By Terp — [Terp AI Labs](https://x.com/OnlyTerp)*

---

## What This Guide Covers

Windsurf's Cascade ships with powerful autonomous features — command execution, skills, MCP integration, hooks, directory-scoped instructions, workflows, and a memory system. Most of them are buried in config files or undocumented settings.

This guide shows you how to configure all of them properly, connect them to real tools, and build production workflows on top of them.

**Not a guide to build features Windsurf lacks. A guide to unlock what's already there.**

---

## Get Started

### Install Windsurf

Download at [windsurf.com](https://windsurf.com) — available for Windows, Mac, and Linux.

> **Get $10 in free credits** — use this referral link to sign up: **[windsurf.com/refer?referral_code=kowwopt506rq1907](https://windsurf.com/refer?referral_code=kowwopt506rq1907)**
> You get $10 in credits, I get $10 in credits. Win-win.

### Plans & Pricing

Current plans: **Free** / **Pro** / **Teams** / **Max** — see [windsurf.com/pricing](https://windsurf.com/pricing) for latest details.

Key things to know:
- **SWE 1.6 is free** for all users right now
- **SWE 1.6 Fast** is extremely low cost — use it freely without thinking about tokens
- There's a **free trial** to test everything before committing

---

## Table of Contents

1. [Terminal Command Execution](#1-terminal-command-execution) — Auto-execution, allow/deny lists, safety levels
2. [Skills System](#2-skills-system) — Create, organize, and invoke reusable task templates
3. [MCP Server Integration](#3-mcp-server-integration) — Connect external tools via the Model Context Protocol (GitHub, Notion, Slack setup guides)
4. [Directory-Scoped Instructions (AGENTS.md)](#4-directory-scoped-instructions-agentsmd) — Context-aware guidance per directory
5. [Hooks](#5-hooks) — Run shell commands at workflow checkpoints
6. [Memories & Rules](#6-memories--rules) — Persistent context across sessions
7. [Workflows](#7-workflows) — Slash-command automations
8. [Real-World Configurations](#8-real-world-configurations) — Production MCP servers and patterns
9. [Model Optimization](#9-model-optimization) — Speed up Cascade with the right model selection
10. [Custom Subagents](#10-custom-subagents) — Personality profiles for specialized tasks
11. [Troubleshooting](#11-troubleshooting) — Common issues and fixes

---

## 1. Terminal Command Execution

### The UI Controls (Start Here)

Cascade's terminal controls are primarily **UI-driven**, not JSON config. This is where most users should start.

**Settings → Cascade → Terminal:**

| Setting | Options | What It Does |
|---------|---------|-------------|
| Auto-execution level | Disabled / Allowlist Only / Auto / Turbo | How aggressively Cascade runs commands without asking |
| Allow list | Regex patterns | Commands that auto-execute when level is "Allowlist Only" |
| Deny list | Regex patterns | Commands that always require confirmation |

These controls appear in the Cascade panel under the three-dots menu. Most users configure command execution here — hooks add additional guardrails on top.

### Editor Settings

These VS Code-level settings reduce friction:

```json
{
  "terminal.integrated.allowChords": false,
  "terminal.integrated.confirmOnExit": "never",
  "terminal.integrated.enableConfirmation": false,
  "security.workspace.trust.enabled": false
}
```

`security.workspace.trust.enabled: false` is important — workspace trust blocks terminal commands in untrusted folders.

### Pre-Run Command Hook

For audit logging or command blocking, use the `pre_run_command` hook (see [Section 5](#5-hooks)).

---

## 2. Skills System

### How Skills Work

Windsurf auto-discovers skills from multiple locations:

| Path | Scope | Use Case |
|------|-------|----------|
| `.windsurf/skills/<name>/SKILL.md` | Workspace | Project-specific skills |
| `~/.codeium/windsurf/skills/<name>/SKILL.md` | User (global) | Skills across all projects |
| `.agents/skills/<name>/SKILL.md` | Workspace (alias) | Cross-tool compatibility |
| `.claude/skills/<name>/SKILL.md` | Workspace (alias) | Cross-tool compatibility |

Each skill is a markdown file with YAML frontmatter. Cascade matches skills to tasks by the `description` field.

### Creating a Skill

**`.windsurf/skills/run-tests/SKILL.md`:**

```yaml
---
name: run-tests
description: Run the project test suite and report results
---

# Run Tests

1. Detect the project type:
   - `package.json` → run `npm test`
   - `pyproject.toml` → run `pytest`
   - `Cargo.toml` → run `cargo test`
2. Capture stdout and stderr
3. If tests fail:
   - Parse the failure output
   - Identify the failing test name and assertion
   - Suggest a fix based on the error message
4. Return a summary: passed, failed, skipped counts
```

**`.windsurf/skills/deploy-check/SKILL.md`:**

```yaml
---
name: deploy-check
description: Pre-deployment validation checklist
---

# Deploy Check

1. Run the run-tests skill
2. Search for TODO, FIXME, HACK, XXX comments
3. Check for hardcoded secrets: API keys, passwords, tokens
4. Verify all imports resolve (no missing modules)
5. Check that environment variables are documented in .env.example
6. Report: READY or list of blockers with file:line references
```

### Invoking Skills

- **Auto-invocation:** Cascade matches your request to skill descriptions automatically
- **Manual:** Type `@skill-name` in the Cascade chat
- **UI:** Cascade menu → Skills icon to browse available skills
- **In workflows:** Reference skills by name in workflow steps

### Tips

- Keep descriptions specific and action-oriented ("Run tests and report failures" not "Testing stuff")
- One skill = one atomic task. Chain skills via workflows for complex tasks
- Use the global path (`~/.codeium/windsurf/skills/`) for skills you want in every project

---

## 3. MCP Server Integration

### The Easiest Way

Cascade panel → hammer icon → search the MCP marketplace → install. No JSON needed.

### Manual Configuration

For custom servers or env-specific setups, edit `mcp_config.json`:

| Location | Scope |
|----------|-------|
| `~/.codeium/windsurf/mcp_config.json` | User (global) |
| `.windsurf/mcp_config.json` | Workspace |

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/workspace"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/db"
      }
    }
  }
}
```

Windsurf supports three MCP transports: **stdio** (most common), **HTTP**, and **SSE**.

You can also discover and install MCP servers via the **Marketplace** (hammer icon in the Cascade panel).

### Building a Custom MCP Server

If you need to connect Cascade to a tool without an existing MCP server (CRM, email, custom API), build one with Python and the MCP SDK:

**Install:**

```bash
pip install mcp requests
```

**`my_mcp_server.py`:**

```python
#!/usr/bin/env python3
"""Custom MCP server — stdio transport."""

import os
import json
import asyncio
import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

API_KEY = os.getenv("API_KEY", "")
BASE_URL = "https://api.example.com"
TIMEOUT = 10

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_record",
            description="Fetch a record by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "record_id": {"type": "string", "description": "The record ID"}
                },
                "required": ["record_id"]
            }
        ),
        Tool(
            name="search_records",
            description="Search records by query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "description": "Max results", "default": 10}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        if name == "get_record":
            resp = requests.get(
                f"{BASE_URL}/records/{arguments['record_id']}",
                headers=headers,
                timeout=TIMEOUT
            )
            resp.raise_for_status()
            return [TextContent(type="text", text=json.dumps(resp.json(), indent=2))]

        elif name == "search_records":
            resp = requests.get(
                f"{BASE_URL}/search",
                headers=headers,
                params={"q": arguments["query"], "limit": arguments.get("limit", 10)},
                timeout=TIMEOUT
            )
            resp.raise_for_status()
            return [TextContent(type="text", text=json.dumps(resp.json(), indent=2))]

    except requests.exceptions.Timeout:
        return [TextContent(type="text", text="Error: Request timed out")]
    except requests.exceptions.HTTPError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
```

**Register it in `mcp_config.json`:**

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["my_mcp_server.py"],
      "env": {
        "API_KEY": "your_key_here"
      }
    }
  }
}
```

### MCP Server Quality Rules

| Rule | Why |
|------|-----|
| Always set `timeout` on HTTP calls | Prevents Cascade from hanging on dead endpoints |
| Never hardcode API keys | Use `env` in mcp_config.json |
| Return clear error messages | Cascade shows them to the user |
| Keep tool descriptions specific | Cascade uses them to decide which tool to call |
| Use `inputSchema` with required fields | Prevents ambiguous tool calls |

---

### Official MCP Server Setup Guides

Step-by-step setup for popular official MCP servers in Windsurf.

#### GitHub MCP Server

**1. Get a GitHub Personal Access Token:**
- Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token with scopes: `repo`, `read:org`, `read:user`, `issues:write`, `pull_requests:write`
- Copy the token (starts with `ghp_`)

**2. Install the server:**

**Via Marketplace (easiest):**
- Cascade panel → hammer icon → search "GitHub" → Install

**Via Manual Config:**
Add to `~/.codeium/windsurf/mcp_config.json` (global) or `.windsurf/mcp_config.json` (project):

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@github/github-mcp-server"],
      "env": {
        "GITHUB_TOKEN": "ghp_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

**3. Restart Windsurf** to load the new MCP server.

**4. Test it:**
Type in Cascade: "List my recent GitHub issues" or "Create an issue in this repo titled 'Test from Windsurf'"

**Available tools:** `search_repositories`, `create_issue`, `update_issue`, `list_issues`, `create_pull_request`, `list_commits`, `get_file_contents`, `create_branch`, `push_files`

---

#### Notion MCP Server

**1. Get a Notion Integration Token:**
- Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
- Create new integration → Name it "Windsurf" → Copy "Internal Integration Token"
- Share specific Notion pages/databases with this integration (required!)

**2. Install the server:**

**Via Marketplace:**
- Cascade panel → hammer icon → search "Notion" → Install

**Via Manual Config:**
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notion/mcp-server"],
      "env": {
        "NOTION_TOKEN": "secret_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

**3. Share pages with the integration:**
- In Notion, go to the page/database you want to access
- Click "..." → Add connections → Select your "Windsurf" integration
- Repeat for all pages you need access to

**4. Restart Windsurf** and test: "Search my Notion pages for 'project roadmap'"

**Available tools:** `search_pages`, `get_page`, `create_page`, `update_page`, `query_database`, `create_database_item`

---

#### Slack MCP Server

**1. Create a Slack App:**
- Go to [api.slack.com/apps](https://api.slack.com/apps)
- Create New App → From scratch → Name it "Windsurf" → Select your workspace
- Go to OAuth & Permissions → Add scopes: `chat:write`, `channels:read`, `groups:read`, `im:read`, `mpim:read`, `users:read`, `search:read`
- Install to Workspace → Copy "Bot User OAuth Token" (starts with `xoxb-`)

**2. Install the server:**

**Via Marketplace:**
- Cascade panel → hammer icon → search "Slack" → Install

**Via Manual Config:**
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@slack/mcp-server"],
      "env": {
        "SLACK_TOKEN": "xoxb-YOUR_TOKEN_HERE"
      }
    }
  }
}
```

**3. Invite the bot to channels:**
- In Slack, type `/invite @Windsurf` in each channel you want it to access

**4. Restart Windsurf** and test: "Send a message to #general saying 'Hello from Windsurf'"

**Available tools:** `post_message`, `get_channel_history`, `search_messages`, `list_channels`, `get_user_info`

---

### Multi-Platform Workflows

Combine MCP servers for cross-platform automation:

**Example workflow:**
```
"Find all GitHub issues labeled 'urgent' in my repo, 
summarize them, and post the summary to Slack #engineering"
```

**Requirements:**
- GitHub MCP server configured
- Slack MCP server configured
- Both have appropriate permissions

**Another example:**
```
"Create a Notion page documenting the architecture decisions 
from the last 5 GitHub PRs in this repo"
```

---

## 4. Directory-Scoped Instructions (AGENTS.md)

### How It Works

Place an `AGENTS.md` file in any directory. Cascade reads it automatically when working on files in that directory. Root-level AGENTS.md applies globally; subdirectory versions supplement it for files within.

**Project Root (`AGENTS.md`):**

```markdown
# Project Guidelines

## Architecture
- Use MCP servers for all external API integrations
- Shared types live in src/types.py
- Configuration via environment variables, never hardcoded

## Code Style
- TypeScript strict mode — no `any` types
- All functions have return type annotations
- Imports sorted: stdlib → third-party → local

## Testing
- Every new feature gets a test file
- Use vitest for unit tests
- Integration tests use MSW for API mocking
```

**`src/api/AGENTS.md`:**

```markdown
# API Layer Guidelines

- All API calls go through MCP servers, never direct HTTP
- Error responses include: error code, message, request ID
- Rate limiting: always respect Retry-After headers
- Never log full request bodies (may contain PII)
```

**`src/components/AGENTS.md`:**

```markdown
# Component Guidelines

- Functional components with TypeScript interfaces for props
- CSS modules or Tailwind — no inline styles
- Accessibility: all interactive elements need aria-labels
- Storybook stories for complex components
```

### Tips

- Keep AGENTS.md files short and specific to the directory
- Use them for rules that would be repetitive to state in every prompt
- Subdirectory AGENTS.md supplements (doesn't replace) the root file

---

## 5. Hooks

### Configuration

Hooks are defined at three levels (system → user → workspace), merged in priority order — workspace overrides user, user overrides system.

| Location | Scope |
|----------|-------|
| `~/.codeium/windsurf/hooks.json` | User (global — personal defaults for all projects) |
| `.windsurf/hooks.json` | Workspace (project-specific) |

User-level hooks are perfect for personal guardrails (secret detection, linting, notifications) that apply everywhere.

**Official format:**

```json
{
  "hooks": {
    "pre_write_code": [
      {
        "command": "python .windsurf/hooks/check_secrets.py",
        "show_output": true,
        "working_directory": "."
      }
    ],
    "post_write_code": [
      {
        "command": "npx eslint --stdin-filename $FILE",
        "show_output": true
      }
    ],
    "pre_run_command": [
      {
        "command": "python .windsurf/hooks/command_audit.py",
        "show_output": false
      }
    ]
  }
}
```

**Key details:**
- Hooks are nested under a `"hooks"` key
- Each event is an **array** — you can stack multiple hooks per event
- No `"enabled"` flag — omit or remove the entry to disable
- Extra keys: `powershell` (for Windows cross-compat), `working_directory`
- On Windows, use `"powershell"` key or ensure `command` works cross-shell

### Available Hook Points

| Hook | When It Fires | Input (stdin JSON) |
|------|---------------|---------------------|
| `pre_read_code` / `post_read_code` | Before/after reading a file | `tool_info` with file path, agent action, trajectory ID |
| `pre_write_code` / `post_write_code` | Before/after writing to a file | `tool_info` with file path, agent action, trajectory ID |
| `pre_run_command` / `post_run_command` | Before/after terminal command | `tool_info` with command string |
| `pre_mcp_tool_use` / `post_mcp_tool_use` | Before/after MCP tool call | `tool_info` with tool name, args |
| `pre_user_prompt` / `post_cascade_response` | Before user msg / after response | `tool_info` with content |

### Hook Contract

- Receives context via **stdin** (JSON — the `tool_info` schema includes `agent_action_name`, `trajectory_id`, and action-specific fields)
- Exit code `0` = allow, exit code `2` = block (for pre-hooks)
- stdout is shown to the user if the hook blocks

### Secret Detection Hook

```python
#!/usr/bin/env python3
"""Block file writes that contain hardcoded secrets."""

import sys
import re
import json

SECRET_PATTERNS = [
    r'(?i)api[_-]?key\s*[=:]\s*["\'][a-zA-Z0-9]{20,}',
    r'(?i)secret\s*[=:]\s*["\'][a-zA-Z0-9]{20,}',
    r'(?i)password\s*[=:]\s*["\'][^"\']{8,}',
    r'sk-[a-zA-Z0-9]{48}',       # OpenAI
    r'ghp_[a-zA-Z0-9]{36}',       # GitHub
    r'sk-ant-[a-zA-Z0-9-]{90,}',  # Anthropic
    r'AIza[a-zA-Z0-9_-]{35}',     # Google
]

def main():
    try:
        tool_info = json.loads(sys.stdin.read())
        filepath = tool_info.get("file_path") or tool_info.get("file") or tool_info.get("path", "")
    except (json.JSONDecodeError, KeyError):
        sys.exit(0)  # Allow on parse failure — don't block on hook bugs

    if not filepath:
        sys.exit(0)

    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except (FileNotFoundError, PermissionError):
        sys.exit(0)

    for pattern in SECRET_PATTERNS:
        match = re.search(pattern, content)
        if match:
            print(f"BLOCKED: Potential secret detected in {filepath}")
            print(f"  Pattern: {pattern}")
            print(f"  Match: {match.group()[:20]}...")
            sys.exit(2)  # Exit code 2 = block

    sys.exit(0)  # Allow

if __name__ == "__main__":
    main()
```

Full list of hook events at [docs.windsurf.com/windsurf/cascade/hooks](https://docs.windsurf.com/windsurf/cascade/hooks) — includes worktree and Arena Mode events not covered here.

### Hook Merge Order

Hooks merge in priority order: **system → user → workspace**. Workspace hooks override user hooks, which override system defaults.

---

## 6. Memories & Rules

### The Built-In Memory System

Windsurf has a native **Memories & Rules** system that persists context across sessions. This is the primary way to give Cascade long-term memory.

**How to access:** Cascade panel → Memories & Rules icon (or Settings → Cascade → Memories)

**Two types:**

| Type | Scope | Use For |
|------|-------|---------|
| **Memories** | Auto-captured | Things Cascade learns during conversation (preferences, patterns, decisions) |
| **Rules** | User-defined | Explicit instructions that always apply (coding style, naming conventions, architecture) |

### Setting Up Rules

Add rules through the Cascade UI (Memories & Rules → Rules tab):

```
Always use TypeScript strict mode.
Never use `any` — use proper interfaces or `unknown`.
All API calls must have a 10-second timeout.
Use named exports, not default exports.
```

### Memories & Rules vs AGENTS.md

| Feature | Memories & Rules | AGENTS.md |
|---------|-----------------|-----------|
| Scope | Global (all projects) | Per-directory |
| Persistence | Session-to-session | File-based |
| Best for | Personal preferences, coding style | Project architecture, conventions |
| Discovery | Cascade UI | Automatic by file location |

Use both. AGENTS.md for project context, Memories & Rules for personal preferences.

---

## 7. Workflows

### Slash-Command Automations

Workflows are reusable multi-step automations stored as markdown in `.windsurf/workflows/`. They use YAML frontmatter for metadata and markdown body for steps.

**`.windsurf/workflows/new-feature.md`:**

```yaml
---
name: new-feature
description: Scaffold a new feature with tests, types, and docs
---

# New Feature: {{feature_name}}

1. Create directory structure:
   - src/features/{{feature_name}}/
   - src/features/{{feature_name}}/index.ts
   - src/features/{{feature_name}}/{{feature_name}}.test.ts
   - src/features/{{feature_name}}/{{feature_name}}.types.ts

2. Generate boilerplate with correct naming

3. Run the deploy-check skill to validate the scaffold

4. Open the main file for editing
```

**`.windsurf/workflows/refactor-module.md`:**

```yaml
---
name: refactor-module
description: Safely refactor a module with tests and git tracking
---

# Refactor: {{module_path}}

1. Run tests and capture baseline (must all pass)
2. Create a git branch: refactor/{{module_name}}
3. Make the requested changes
4. Re-run tests — must match baseline
5. If tests break, revert and report what went wrong
6. If clean, stage changes and suggest a commit message
```

Workflows use the same YAML frontmatter format as skills (`name` + `description`) but support multi-step orchestration with `{{variable}}` substitution.

### Tips

- Use `{{variable}}` syntax for workflow parameters
- Reference skills in workflow steps by name
- Workflows are multi-step orchestrations; skills are atomic tasks — chain skills via workflows for complex automation

---

## 8. Real-World Configurations

### Production MCP Server: Attio CRM

```json
{
  "mcpServers": {
    "attio-crm": {
      "command": "python",
      "args": ["attio_mcp_server.py"],
      "env": {
        "ATTIO_API_KEY": "your_attio_key"
      }
    }
  }
}
```

### Production MCP Server: Resend Email

```json
{
  "mcpServers": {
    "resend-email": {
      "command": "python",
      "args": ["resend_mcp_server.py"],
      "env": {
        "RESEND_API_KEY": "re_your_key"
      }
    }
  }
}
```

### Production MCP Server: Airtable

```json
{
  "mcpServers": {
    "airtable-ops": {
      "command": "python",
      "args": ["airtable_mcp_server.py"],
      "env": {
        "AIRTABLE_TOKEN": "pat_your_token",
        "AIRTABLE_BASE_ID": "app_your_base"
      }
    }
  }
}
```

### Combined Setup

Full `.windsurf/` directory for a production project:

```
.windsurf/
├── mcp_config.json          # MCP servers (workspace-level)
├── hooks.json               # Governance hooks
├── skills/
│   ├── run-tests/
│   │   └── SKILL.md
│   ├── deploy-check/
│   │   └── SKILL.md
│   └── api-migration/
│       └── SKILL.md
├── workflows/
│   ├── new-feature.md
│   └── refactor-module.md
├── hooks/
│   ├── check_secrets.py
│   └── command_audit.py
└── memories/                # Auto-managed by Windsurf
```

Global MCP servers go in `~/.codeium/windsurf/mcp_config.json`. Global skills go in `~/.codeium/windsurf/skills/`.

---

---

## 9. Model Optimization

### The Hidden Fast Mode

Cascade has multiple models, but most users never switch from the default. **SWE 1.5** (Software Engineering model) outputs at **~950 tokens/second** — roughly 3-4x faster than Claude Sonnet.

| Model | Speed | Best For |
|-------|-------|----------|
| **SWE 1.5** | ~950 tok/s | Simple edits, refactors, grep-style tasks |
| **SWE 1.5 Fast** | ~950 tok/s, lower cost | Same as above, budget-optimized |
| **Claude Sonnet 4.5** | ~250 tok/s | Complex architecture, debugging |
| **Claude Opus 4.6** | ~150 tok/s | Deep reasoning, design decisions |

### How to Trigger Specific Models

Models are selected based on the complexity hint in your prompt:

```
/fast  Refactor this util file to use TypeScript
/deep  Design a distributed caching strategy for our API
```

**Cascade interprets:**
- Short, specific requests → SWE 1.5 (fast)
- Complex, open-ended requests → Claude Opus (deep)

### Custom Model Selector Workflow

Create `.windsurf/workflows/fast.md`:

```yaml
---
name: fast
description: Use SWE 1.5 for quick edits and refactors. Optimize for speed.
---

# Fast Mode (SWE 1.5)

Use the SWE 1.5 model for this task:
- Make minimal changes
- Don't over-explain
- Just show the code
- Skip validation phrases
```

Then type `/fast` in Cascade to trigger it.

---

## 10. Custom Subagents (AGENTS.md Profiles)

### Beyond Directory-Scoped Instructions

AGENTS.md files can define **subagent personalities** — specialized modes that Cascade switches into for specific tasks.

### Example: Terse Mode Profile

Create `.windsurf/agents/terse/AGENT.md`:

```markdown
---
name: terse
description: Ultra-direct coding mode. No validation phrases. Immediate execution.
---

# Terse Agent Profile

## Personality
- Skip throat-clearing ("That's a great idea!", "I'll help you with that")
- Execute immediately without asking permission
- Speed is #1 priority
- Keep responses under 3 sentences when possible

## Execution Rules
- Never re-read files already in context
- Batch tool calls for parallel execution
- If ambiguous, pick the most likely interpretation and proceed
- Show code changes directly, don't describe them

## Communication Style
- Direct statements only
- No bullet point summaries of what you'll do
- No apologies for brevity

## Use When
- The user says "quick fix", "just do it", "make it happen"
- Task is straightforward (refactor, rename, move)
- User seems frustrated with verbosity
```

### Activating Subagents

Type `@terse` in Cascade to switch to that personality.

**Pro tip:** Combine with model selector for `@terse /fast` — fastest possible execution mode.

### Other Useful Profiles

| Profile | Use Case |
|---------|----------|
| `security` | Code review focused on vulnerabilities |
| `docs` | Writing documentation, comments, READMEs |
| `test` | Generating comprehensive test coverage |
| `optimize` | Performance-focused refactoring |

---

## 11. Troubleshooting

### "Connecting to Language Server" Stuck

Cascade shows "Connecting to language server..." and won't respond:

1. Kill all Windsurf processes: `Get-Process windsurf | Stop-Process -Force` (PowerShell)
2. Check `%APPDATA%\Windsurf\User\settings.json` for malformed JSON
3. Your user config in `.codeium/windsurf/` survives reinstalls — only app files are affected
4. If all else fails: `winget uninstall Codeium.Windsurf && winget install Codeium.Windsurf`

### MCP Server Not Appearing

- Verify `mcp_config.json` is at `~/.codeium/windsurf/mcp_config.json` (user) or `.windsurf/mcp_config.json` (workspace)
- Check that the command is globally available (`npx -y` handles this for Node servers)
- Restart Windsurf after adding new servers — MCP config loads at startup
- Check Cascade output panel for MCP connection errors
- Marketplace servers: Cascade panel → hammer icon → search and install

### Skills Not Auto-Executing

- Verify the file path: `.windsurf/skills/<skill-name>/SKILL.md` (case-sensitive on Linux/Mac)
- Check the `description` field — Cascade uses it for matching, not the filename
- Skills require a workspace (not an empty window)
- Try manual invocation with `@skill-name` to verify it loads
- Also check global path: `~/.codeium/windsurf/skills/`

### Hooks Not Firing

- Verify `.windsurf/hooks.json` matches the official format: nested under `"hooks"`, each event is an array
- Check `"command"` or `"powershell"` key (use `"powershell"` on Windows for cross-compat)
- Test the hook manually: `echo '{"file_path":"test.py"}' | python .windsurf/hooks/check_secrets.py`
- Check exit codes: `0` = allow, `2` = block
- Hook merge order: workspace overrides user overrides system

### Terminal Issues

- Shell RC conflicts: if commands fail silently, check `.bashrc` / `.zshrc` for interactive-only configs
- PATH differences: Cascade may use a different PATH than your terminal. Use absolute paths in hooks.
- Windows: use `"powershell"` key in hooks.json for cross-shell compatibility
- MCP whitelist regex gotchas: test your patterns against actual command strings

---

## Feature Matrix

| Feature | Config Location | Discovery | Override Level |
|---------|----------------|-----------|----------------|
| Terminal execution | Settings UI + hooks.json | Built-in | User > Workspace |
| Skills | .windsurf/skills/*/SKILL.md + global path | Auto-scan | Workspace + User |
| MCP servers | mcp_config.json (user + workspace) | Startup load | User + Workspace |
| AGENTS.md | Any directory | Per-file | Root → Subdirectory |
| Hooks | .windsurf/hooks.json | Startup load | System → User → Workspace |
| Memories & Rules | Cascade UI | Session-persist | User only |
| Workflows | .windsurf/workflows/*.md | Auto-scan | Workspace only |
| Model selector | Prompt hints (`/fast`, `/deep`) | Contextual | Auto-detected |
| Subagent profiles | .windsurf/agents/*/AGENT.md | @mention | Workspace only |

---

## Resources

- [Windsurf Documentation](https://docs.windsurf.com)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Server Directory](https://github.com/modelcontextprotocol/servers)
- [OpenClaw Optimization Guide](https://github.com/OnlyTerp/openclaw-optimization-guide)

---

*Last updated: April 2026 · Built by [Terp AI Labs](https://x.com/OnlyTerp) · Ship fast, iterate constantly.*
