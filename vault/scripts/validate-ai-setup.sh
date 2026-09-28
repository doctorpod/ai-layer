#!/usr/bin/env bash

# Run from the root of the vault.

PASS="✓"
FAIL="✗"
WARN="!"
errors=0
warnings=0

check() {
  local label="$1"
  local result="$2"
  local fix="$3"
  if [ "$result" = "ok" ]; then
    echo "  $PASS $label"
  else
    echo "  $FAIL $label"
    echo "    → $fix"
    errors=$((errors + 1))
  fi
}

warn() {
  local label="$1"
  local result="$2"
  local note="$3"
  if [ "$result" = "ok" ]; then
    echo "  $PASS $label"
  else
    echo "  $WARN $label (optional)"
    echo "    → $note"
    warnings=$((warnings + 1))
  fi
}

echo ""
echo "AI layer setup check"
echo "--------------------"

# Core structure
[ -d "_AI/local" ] && r="ok" || r="fail"
check "_AI/local/ exists" "$r" "Run: bash ~/Dev/ai-layer/scripts/install-target.sh --vault"

[ -f "_AI/local/AI.md" ] && r="ok" || r="fail"
check "_AI/local/AI.md exists" "$r" "Check that _AI/local is correctly symlinked (run install-target.sh --vault)"

[ -d "_AI/shared" ] && r="ok" || r="fail"
check "_AI/shared/ exists" "$r" "Run: bash ~/Dev/ai-layer/scripts/install-target.sh --vault"

[ -d "_AI/docs" ] && r="ok" || r="fail"
check "_AI/docs/ exists" "$r" "Run: bash ~/Dev/ai-layer/scripts/install-target.sh --vault"

# Required directories
[ -d "_AI/chats" ] && r="ok" || r="fail"
check "_AI/chats/ directory exists" "$r" "Run: mkdir -p _AI/chats"

[ -d "_AI/logs" ] && r="ok" || r="fail"
check "_AI/logs/ directory exists" "$r" "Run: mkdir -p _AI/logs"

# GOALS.md
[ -f "_AI/GOALS.md" ] && r="ok" || r="fail"
check "_AI/GOALS.md exists" "$r" "Create _AI/GOALS.md describing the goals and focus areas for this vault"

# CONVENTIONS.md (optional)
[ -f "_AI/CONVENTIONS.md" ] && r="ok" || r="missing"
warn "_AI/CONVENTIONS.md exists" "$r" "Create _AI/CONVENTIONS.md to document vault-specific operating conventions"

# AI boot file
boot_found=""
boot_wired=""
for f in CLAUDE.md AGENTS.md .cursorrules; do
  if [ -f "$f" ]; then
    boot_found="$f"
    grep -q "_AI/local/AI.md" "$f" && boot_wired="ok"
    break
  fi
done

[ -n "$boot_found" ] && r="ok" || r="fail"
check "AI boot file exists (CLAUDE.md / AGENTS.md / .cursorrules)" "$r" "Create a boot file (e.g. CLAUDE.md) containing: See \`_AI/local/AI.md\` for vault context and available workflows."

if [ -n "$boot_found" ]; then
  [ -n "$boot_wired" ] && r="ok" || r="fail"
  check "$boot_found references _AI/local/AI.md" "$r" "Add the line: See \`_AI/local/AI.md\` for vault context and available workflows."
fi

# Pre-commit sensitivity hook
hook=".git/hooks/pre-commit"
if [ -f "$hook" ] && [ -x "$hook" ]; then
  r="ok"
else
  r="fail"
fi
check "Pre-commit sensitivity hook installed" "$r" "Run: cp _AI/local/scripts/pre-commit-sensitivity-check.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit"

# RELATED.md files (optional)
# Prints each "- Path:" value, trimmed, unquoted from backticks, with a leading ~ expanded.
related_paths() {
  local line p
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      "- Path:"*) ;;
      *) continue ;;
    esac
    p="${line#- Path:}"
    p="${p#"${p%%[![:space:]]*}"}"
    p="${p%"${p##*[![:space:]]}"}"
    p="${p#\`}"
    p="${p%\`}"
    case "$p" in
      "~"|"~/"*) p="$HOME${p#\~}" ;;
    esac
    echo "$p"
  done < "$1"
}

while IFS= read -r f; do
  [ -n "$f" ] || continue
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    [ -e "$p" ] || warn "RELATED.md path resolves — $f: $p" "missing" "Fix the Path: line in $f, or create the missing location"
  done <<EOF
$(related_paths "$f")
EOF
done <<EOF
$(find . -name RELATED.md -not -path './_AI/*' -not -path './.git/*')
EOF

# Verdict
echo ""
if [ "$errors" -eq 0 ] && [ "$warnings" -eq 0 ]; then
  echo "All checks passed — AI layer is correctly installed."
elif [ "$errors" -eq 0 ]; then
  echo "Required checks passed. $warnings optional item(s) not set up (see ! above)."
else
  echo "$errors issue(s) found — fix the above before using AI workflows."
  [ "$warnings" -gt 0 ] && echo "$warnings optional item(s) also not set up (see ! above)."
fi
echo ""

exit $errors
