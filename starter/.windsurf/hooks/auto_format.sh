#!/usr/bin/env bash
# Auto-format any file Cascade writes or edits.
# Triggered by post_tool_use on write_file / edit_file.
#
# Reads the tool output JSON from stdin; extracts file_path; runs the
# right formatter based on extension + project config.
set -euo pipefail

# Read the tool payload; extract the file path.
PAYLOAD="$(cat)"
FILE_PATH=$(printf '%s' "$PAYLOAD" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("file_path") or d.get("path") or "", end="")' 2>/dev/null || true)

if [[ -z "$FILE_PATH" || ! -f "$FILE_PATH" ]]; then
  exit 0
fi

ext="${FILE_PATH##*.}"

case "$ext" in
  ts|tsx|js|jsx|mjs|cjs)
    if [[ -f biome.json || -f biome.jsonc ]]; then
      npx --no-install biome format --write "$FILE_PATH" 2>/dev/null || true
    elif command -v prettier >/dev/null 2>&1 || [[ -f .prettierrc || -f .prettierrc.json ]]; then
      npx --no-install prettier --write "$FILE_PATH" 2>/dev/null || true
    fi
    ;;
  py)
    if command -v ruff >/dev/null 2>&1; then
      ruff format "$FILE_PATH" 2>/dev/null || true
      ruff check --fix "$FILE_PATH" 2>/dev/null || true
    elif command -v black >/dev/null 2>&1; then
      black --quiet "$FILE_PATH" 2>/dev/null || true
    fi
    ;;
  rs)
    command -v rustfmt >/dev/null 2>&1 && rustfmt "$FILE_PATH" 2>/dev/null || true
    ;;
  go)
    command -v gofmt >/dev/null 2>&1 && gofmt -w "$FILE_PATH" 2>/dev/null || true
    ;;
  json)
    # Prefer repo-specific, fall back to jq for pretty-print.
    if [[ -f .prettierrc || -f .prettierrc.json ]]; then
      npx --no-install prettier --write "$FILE_PATH" 2>/dev/null || true
    fi
    ;;
  md|markdown)
    if [[ -f .prettierrc || -f .prettierrc.json ]]; then
      npx --no-install prettier --write "$FILE_PATH" 2>/dev/null || true
    fi
    ;;
esac

exit 0
