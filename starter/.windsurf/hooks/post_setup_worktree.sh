#!/usr/bin/env bash
# Seed a newly-created Cascade worktree so it's immediately runnable.
# Triggered by the post_setup_worktree hook.
#
# Docs: https://github.com/OnlyTerp/windsurf-unlocked#11-worktrees--parallel-cascade
set -euo pipefail

WORKTREE_DIR="${CASCADE_WORKTREE_PATH:-$PWD}"
cd "$WORKTREE_DIR"

# Copy .env from the primary checkout if present.
# Cascade sets CASCADE_PRIMARY_PATH to the parent checkout.
if [[ -n "${CASCADE_PRIMARY_PATH:-}" && -f "$CASCADE_PRIMARY_PATH/.env" ]]; then
  cp "$CASCADE_PRIMARY_PATH/.env" .env
  echo "post_setup_worktree: copied .env"
fi

# Install dependencies for whatever package manager this repo uses.
if [[ -f pnpm-lock.yaml ]]; then
  pnpm install --frozen-lockfile
elif [[ -f yarn.lock ]]; then
  yarn install --frozen-lockfile
elif [[ -f package-lock.json ]]; then
  npm ci
elif [[ -f uv.lock ]]; then
  uv sync
elif [[ -f poetry.lock ]]; then
  poetry install --no-root
elif [[ -f Cargo.lock ]]; then
  cargo fetch
elif [[ -f go.mod ]]; then
  go mod download
else
  echo "post_setup_worktree: no lockfile detected — skipping install"
fi

echo "post_setup_worktree: worktree ready at $WORKTREE_DIR"
