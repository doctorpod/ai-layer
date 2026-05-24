#!/usr/bin/env bash
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  echo "Usage: bash $0 [--code|--vault]"
  echo ""
  echo "Run from the root of the target project. Creates:"
  echo "  _AI/local  -> $REPO_ROOT/{code|vault}"
  echo "  _AI/shared -> $REPO_ROOT/shared"
  exit 1
}

CONTEXT=""
case "${1:-}" in
  --code)  CONTEXT="code" ;;
  --vault) CONTEXT="vault" ;;
  *)       usage ;;
esac

# Warn about old _AI/core symlink
if [[ -L "_AI/core" ]]; then
  echo "WARNING: _AI/core symlink found — this is the old structure."
  echo "Remove it manually after verifying the new symlinks work:"
  echo "  rm _AI/core"
  echo ""
fi

mkdir -p _AI

# Create _AI/local
if [[ -e "_AI/local" && ! -L "_AI/local" ]]; then
  echo "ERROR: _AI/local exists and is not a symlink. Remove it manually and re-run."
  exit 1
fi
ln -sf "$REPO_ROOT/$CONTEXT" _AI/local
echo "Linked: _AI/local -> $REPO_ROOT/$CONTEXT"

# Create _AI/shared
if [[ -e "_AI/shared" && ! -L "_AI/shared" ]]; then
  echo "ERROR: _AI/shared exists and is not a symlink. Remove it manually and re-run."
  exit 1
fi
ln -sf "$REPO_ROOT/shared" _AI/shared
echo "Linked: _AI/shared -> $REPO_ROOT/shared"

echo ""
echo "Done. Next steps:"
echo "  1. Create or update your CLAUDE.md to include:"
echo "     See \`_AI/local/AI.md\` for project context and available workflows."
if [[ "$CONTEXT" == "code" ]]; then
  echo "  2. Create _AI/OVERVIEW.md — project description, architecture, key files, anti-patterns."
  echo "  3. Create _AI/VALIDATION.md — commands to run at each validation gate."
  echo "  4. Optionally create _AI/CODEX.md — personal coding preferences."
else
  echo "  2. Create _AI/GOALS.md — vault purpose and focus areas."
  echo "  3. Optionally create _AI/VOICE.md — writing voice reference for the Compose workflow."
fi
