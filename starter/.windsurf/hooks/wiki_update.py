#!/usr/bin/env python3
"""
Auto-invoke the wiki-update skill after any session that produced
a decision, fact, or state change.

Reads the Cascade hook payload from stdin, checks whether the session
likely produced wiki-worthy output, and if so prints an instruction
that Cascade picks up as a follow-up invocation of the wiki-update skill.

The actual vault/ maintenance is done by the skill (`.windsurf/skills/wiki-update/SKILL.md`).

Docs: https://github.com/OnlyTerp/windsurf-unlocked#20-context-engineering--the-agentic-wiki
"""
from __future__ import annotations

import json
import re
import sys

TRIGGER_PHRASES = (
    r"\bdecided\b",
    r"\bdecision\b",
    r"\bwe(?:'|)ll use\b",
    r"\bgoing with\b",
    r"\bchose\b",
    r"\bowner\b",
    r"\bowns\b",
    r"\bincident\b",
    r"\bpost[- ]mortem\b",
    r"\broot cause\b",
    r"\bmigrated\b",
    r"\badded adr\b",
    r"\bnew service\b",
)


def should_trigger(transcript: str) -> bool:
    text = transcript.lower()
    return any(re.search(p, text) for p in TRIGGER_PHRASES)


def main() -> int:
    try:
        ctx = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    transcript = ctx.get("transcript") or ctx.get("response") or ""
    if not should_trigger(transcript):
        return 0
    # Cascade picks up follow-up instructions from stdout of hooks.
    # Emit a terse invocation; the skill's own description field will
    # re-trigger it properly.
    print("Run the wiki-update skill on the preceding session: extract decisions, "
          "facts, incidents, and ownership info into vault/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
