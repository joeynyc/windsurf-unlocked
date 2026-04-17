#!/usr/bin/env python3
"""
Pipe every Cascade response into Langfuse as a trace.

Wire-up (in .windsurf/hooks.json):
  "post_cascade_response_with_transcript": [
    { "command": "python3 .windsurf/hooks/langfuse_logger.py" }
  ]

Env vars required:
  LANGFUSE_PUBLIC_KEY
  LANGFUSE_SECRET_KEY
  LANGFUSE_HOST          (optional; defaults to https://cloud.langfuse.com)

Install:
  pip install langfuse>=2.40

Docs: https://github.com/OnlyTerp/windsurf-unlocked#23-observability--evals-for-cascade
"""
from __future__ import annotations

import json
import os
import sys


def main() -> int:
    pub = os.environ.get("LANGFUSE_PUBLIC_KEY")
    sec = os.environ.get("LANGFUSE_SECRET_KEY")
    if not pub or not sec:
        print("langfuse_logger: LANGFUSE_PUBLIC_KEY/SECRET_KEY not set — skipping", file=sys.stderr)
        return 0

    try:
        from langfuse import Langfuse  # type: ignore
    except ImportError:
        print("langfuse_logger: `pip install langfuse` to enable", file=sys.stderr)
        return 0

    try:
        ctx = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    lf = Langfuse(
        public_key=pub,
        secret_key=sec,
        host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    )

    trace = lf.trace(
        name="cascade-response",
        user_id=ctx.get("user_id"),
        session_id=ctx.get("session_id"),
        metadata={
            "model": ctx.get("model"),
            "mode": ctx.get("mode"),
            "rules_applied": ctx.get("rules_applied", []),
            "tool_calls": len(ctx.get("tool_calls", [])),
            "workspace": ctx.get("workspace"),
        },
    )
    trace.generation(
        name="cascade",
        model=ctx.get("model"),
        input=ctx.get("prompt"),
        output=ctx.get("response"),
        usage={
            "input": ctx.get("input_tokens"),
            "output": ctx.get("output_tokens"),
            "cache_read": ctx.get("cache_read_tokens"),
        },
    )
    for call in ctx.get("tool_calls", []):
        trace.span(
            name=f"tool:{call.get('name')}",
            input=call.get("args"),
            output=call.get("result"),
            metadata={"duration_ms": call.get("duration_ms")},
        )
    lf.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
