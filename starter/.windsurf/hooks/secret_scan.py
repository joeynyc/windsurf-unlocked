#!/usr/bin/env python3
"""
Secret scanner for Cascade hooks.

Modes:
  --mode=tool-input     Scan the JSON payload Cascade pipes in on pre_tool_use
  --mode=staged-diff    Scan `git diff --cached` for secrets
  --mode=working-tree   Scan all tracked files (slow — for manual audits)

Exits nonzero on any CRITICAL finding to block the operation.
Tuned to be low-false-positive. Add allow-list entries to .gitallowed.

Docs: https://github.com/OnlyTerp/windsurf-unlocked#8-hooks
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple


class Pattern(NamedTuple):
    name: str
    regex: re.Pattern[str]
    severity: str  # CRITICAL | MEDIUM


PATTERNS: list[Pattern] = [
    Pattern("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "CRITICAL"),
    Pattern("GitHub classic PAT", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36}\b"), "CRITICAL"),
    Pattern("GitHub fine-grained PAT", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{82}\b"), "CRITICAL"),
    Pattern("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "CRITICAL"),
    Pattern("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"), "CRITICAL"),
    Pattern("Stripe live key", re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{24,}\b"), "CRITICAL"),
    Pattern("OpenAI key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{40,}\b"), "CRITICAL"),
    Pattern("Anthropic key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{90,}\b"), "CRITICAL"),
    Pattern("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"), "CRITICAL"),
    Pattern(
        "Private key block",
        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
        "CRITICAL",
    ),
    Pattern(
        "Hardcoded password",
        re.compile(r"""(?i)\b(?:password|passwd|pwd)\s*[:=]\s*["'][^"'\s]{6,}["']"""),
        "MEDIUM",
    ),
    Pattern(
        "Hardcoded api_key",
        re.compile(r"""(?i)\b(?:api[_-]?key|apikey|access[_-]?token)\s*[:=]\s*["'][^"'\s]{10,}["']"""),
        "MEDIUM",
    ),
    Pattern(
        "DB connection with password",
        re.compile(r"\b(?:postgres|mysql|mongodb|redis)://[^/\s:]+:[^/@\s]+@"),
        "MEDIUM",
    ),
]

ALLOWED_PATH_SUFFIXES = (
    ".env.example",
    ".env.sample",
    "/sample.env",
    "/example.env",
)


def is_allowed_path(path: str) -> bool:
    lower = path.lower()
    if any(lower.endswith(s) for s in ALLOWED_PATH_SUFFIXES):
        return True
    try:
        for line in Path(".gitallowed").read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and line in path:
                return True
    except FileNotFoundError:
        pass
    return False


def redact(value: str) -> str:
    if len(value) <= 8:
        return "*" * len(value)
    return value[:4] + "…" + value[-4:]


def scan_text(path: str, text: str) -> list[tuple[Pattern, int, str]]:
    if is_allowed_path(path):
        return []
    findings: list[tuple[Pattern, int, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for p in PATTERNS:
            for m in p.regex.finditer(line):
                findings.append((p, lineno, m.group(0)))
    return findings


def scan_tool_input() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # nothing to scan — let the tool through
    path = payload.get("file_path") or payload.get("path") or "<unknown>"
    text = payload.get("content") or payload.get("new_string") or ""
    findings = scan_text(path, text)
    return report(findings, context=f"write to {path}")


def scan_staged_diff() -> int:
    try:
        diff = subprocess.check_output(
            ["git", "diff", "--cached", "--unified=0", "--no-color"],
            text=True,
        )
    except subprocess.CalledProcessError:
        return 0
    findings: list[tuple[Pattern, int, str]] = []
    current_path = "<unknown>"
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current_path = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            findings += [(p, 0, m) for (p, _, m) in scan_text(current_path, line[1:])]
    return report(findings, context="staged diff")


def scan_working_tree() -> int:
    try:
        files = subprocess.check_output(
            ["git", "ls-files"], text=True
        ).splitlines()
    except subprocess.CalledProcessError:
        return 0
    findings: list[tuple[Pattern, int, str]] = []
    for path in files:
        try:
            text = Path(path).read_text(errors="replace")
        except (FileNotFoundError, PermissionError, IsADirectoryError):
            continue
        findings += [(p, n, m) for (p, n, m) in scan_text(path, text)]
    return report(findings, context="working tree")


def report(findings: list[tuple[Pattern, int, str]], context: str) -> int:
    if not findings:
        return 0
    criticals = [f for f in findings if f[0].severity == "CRITICAL"]
    mediums = [f for f in findings if f[0].severity == "MEDIUM"]
    print(f"\n🚨 secret_scan: {len(criticals)} CRITICAL, {len(mediums)} MEDIUM in {context}\n", file=sys.stderr)
    for p, n, val in criticals:
        print(f"  CRITICAL  {p.name:30s} line {n}  {redact(val)}", file=sys.stderr)
    for p, n, val in mediums:
        print(f"  MEDIUM    {p.name:30s} line {n}  {redact(val)}", file=sys.stderr)
    if criticals:
        print(
            "\nRemediation:\n"
            "  1. Rotate the credential NOW.\n"
            "  2. Replace the literal with an env-var reference.\n"
            "  3. If already pushed, the credential is compromised — rotation is mandatory.\n"
            "  4. Consider `bfg` or `git filter-repo` to scrub history.\n"
            "\nTo override (discouraged):  git commit --no-verify\n",
            file=sys.stderr,
        )
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["tool-input", "staged-diff", "working-tree"], required=True)
    args = ap.parse_args()
    if args.mode == "tool-input":
        return scan_tool_input()
    if args.mode == "staged-diff":
        return scan_staged_diff()
    if args.mode == "working-tree":
        return scan_working_tree()
    return 0


if __name__ == "__main__":
    sys.exit(main())
