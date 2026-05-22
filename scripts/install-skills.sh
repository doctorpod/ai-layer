#!/usr/bin/env bash
set -e

SKILLS_SRC="$(cd "$(dirname "$0")/../skills" && pwd)"
SKILLS_DEST="$HOME/.claude/skills"

mkdir -p "$SKILLS_DEST"

# Build a set of skill names from source
declare -A src_skills
for src in "$SKILLS_SRC"/*.md; do
  name=$(basename "$src" .md)
  src_skills["$name"]=1
  mkdir -p "$SKILLS_DEST/$name"
  ln -sf "$src" "$SKILLS_DEST/$name/SKILL.md"
  echo "Synced: $name"
done

# Remove only skill directories that we installed (SKILL.md is a symlink into our source)
for dir in "$SKILLS_DEST"/*/; do
  name=$(basename "$dir")
  skill_file="$dir/SKILL.md"
  if [[ -z "${src_skills[$name]}" && -L "$skill_file" ]]; then
    link_target="$(readlink "$skill_file")"
    if [[ "$link_target" == "$SKILLS_SRC"/* ]]; then
      rm -rf "$dir"
      echo "Removed: $name"
    fi
  fi
done
