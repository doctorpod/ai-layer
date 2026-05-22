#!/usr/bin/env bash
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DEST="$HOME/.claude/skills"

SKILL_DIRS=(
  "$REPO_ROOT/shared/skills"
  "$REPO_ROOT/code/skills"
  "$REPO_ROOT/vault/skills"
)

mkdir -p "$SKILLS_DEST"

# Install skills from all source directories, tracking names in a plain list
installed_names=""
for skills_src in "${SKILL_DIRS[@]}"; do
  [[ -d "$skills_src" ]] || continue
  for src in "$skills_src"/*.md; do
    [[ -e "$src" ]] || continue
    name=$(basename "$src" .md)
    installed_names="$installed_names $name "
    mkdir -p "$SKILLS_DEST/$name"
    ln -sf "$src" "$SKILLS_DEST/$name/SKILL.md"
    echo "Synced: $name"
  done
done

# Remove only skill directories that we installed (SKILL.md is a symlink into our repo)
for dir in "$SKILLS_DEST"/*/; do
  name=$(basename "$dir")
  skill_file="$dir/SKILL.md"
  if [[ -L "$skill_file" ]]; then
    link_target="$(readlink "$skill_file")"
    if [[ "$link_target" == "$REPO_ROOT"/* ]]; then
      # Only remove if not in the current install set
      if [[ "$installed_names" != *" $name "* ]]; then
        rm -rf "$dir"
        echo "Removed: $name"
      fi
    fi
  fi
done
