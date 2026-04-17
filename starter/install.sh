#!/usr/bin/env bash
# windsurf-unlocked starter installer
# Drops a production-grade .windsurf/ setup into the current repo.
# Usage: curl -fsSL <raw url>/starter/install.sh | bash
#    or: bash install.sh [--update] [--dir <path>]

set -euo pipefail

TARGET_DIR="${PWD}"
UPDATE=0
SOURCE_REPO="https://github.com/OnlyTerp/windsurf-unlocked"
SOURCE_BRANCH="main"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --update) UPDATE=1; shift ;;
    --dir) TARGET_DIR="$2"; shift 2 ;;
    --source) SOURCE_REPO="$2"; shift 2 ;;
    --branch) SOURCE_BRANCH="$2"; shift 2 ;;
    -h|--help)
      cat <<USAGE
windsurf-unlocked starter installer

Usage:
  install.sh               Install into \$PWD
  install.sh --update      Refresh skills/hooks/workflows, preserve AGENTS.md / vault / mcp_config
  install.sh --dir <path>  Install into a specific directory

Flags:
  --source <url>    Override source repo (default: $SOURCE_REPO)
  --branch <name>   Override branch (default: $SOURCE_BRANCH)

USAGE
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

bold()  { printf '\033[1m%s\033[0m\n' "$*"; }
green() { printf '\033[32m%s\033[0m\n' "$*"; }
yellow(){ printf '\033[33m%s\033[0m\n' "$*"; }
red()   { printf '\033[31m%s\033[0m\n' "$*"; }

bold "windsurf-unlocked starter installer"
echo "target: $TARGET_DIR"
echo

# Fetch source
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

if [[ -d "$(dirname "$0")/.windsurf" ]]; then
  # Running from inside the repo clone
  STARTER_SRC="$(cd "$(dirname "$0")" && pwd)"
else
  echo "fetching starter from $SOURCE_REPO@$SOURCE_BRANCH..."
  git clone --depth 1 --branch "$SOURCE_BRANCH" --quiet "$SOURCE_REPO" "$STAGE/repo"
  STARTER_SRC="$STAGE/repo/starter"
fi

mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# Copy helpers
copy_skip_if_exists() {
  local src="$1" dst="$2"
  if [[ -e "$dst" ]]; then
    yellow "  skip $dst (already exists)"
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    green "  add  $dst"
  fi
}

copy_tree() {
  local src="$1" dst="$2"
  mkdir -p "$dst"
  rsync -a "$src/" "$dst/" 2>/dev/null || cp -R "$src/"* "$dst/"
  green "  sync $dst"
}

bold "installing .windsurf/"
copy_tree "$STARTER_SRC/.windsurf/agents"    ".windsurf/agents"
copy_tree "$STARTER_SRC/.windsurf/skills"    ".windsurf/skills"
copy_tree "$STARTER_SRC/.windsurf/workflows" ".windsurf/workflows"
copy_tree "$STARTER_SRC/.windsurf/hooks"     ".windsurf/hooks"

if [[ $UPDATE -eq 0 ]]; then
  copy_skip_if_exists "$STARTER_SRC/.windsurf/hooks.json"      ".windsurf/hooks.json"
  copy_skip_if_exists "$STARTER_SRC/.windsurf/mcp_config.json" ".windsurf/mcp_config.json"
fi

if [[ $UPDATE -eq 0 ]]; then
  bold "installing AGENTS.md + vault/"
  copy_skip_if_exists "$STARTER_SRC/AGENTS.md" "AGENTS.md"
  if [[ ! -d "vault" ]]; then
    copy_tree "$STARTER_SRC/vault" "vault"
  else
    yellow "  skip vault/ (already exists)"
  fi
fi

chmod +x .windsurf/hooks/*.sh .windsurf/hooks/*.py 2>/dev/null || true

echo
bold "done."
echo
if [[ $UPDATE -eq 1 ]]; then
  green "updated skills / agents / workflows / hook scripts."
  echo "preserved: AGENTS.md, vault/, hooks.json, mcp_config.json"
else
  green "installed."
  echo
  bold "next steps:"
  cat <<NEXT
  1. edit AGENTS.md — fill in the <FILL IN> sections (stack, commands, invariants)
  2. edit .windsurf/hooks.json — flip on the hooks you want (all disabled by default)
  3. edit .windsurf/mcp_config.json — add secrets via \$ENV_VAR references
  4. in Cascade:  @reviewer Read AGENTS.md and list invariants that need filling in

docs:  https://github.com/OnlyTerp/windsurf-unlocked
update:  re-run with --update to pull newer skills/hooks without touching your configs
NEXT
fi
