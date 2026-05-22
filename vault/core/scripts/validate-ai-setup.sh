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
[ -d "_AI/core" ] && r="ok" || r="fail"
check "_AI/core/ exists" "$r" "Run: mkdir -p _AI && ln -s ~/Dev/vault-ai-layer/core _AI/core"

[ -f "_AI/core/AI.md" ] && r="ok" || r="fail"
check "_AI/core/AI.md exists" "$r" "Check that _AI/core is correctly symlinked or copied from vault-ai-layer"

# Required directories
[ -d "_AI/chats" ] && r="ok" || r="fail"
check "_AI/chats/ directory exists" "$r" "Run: mkdir -p _AI/chats"

[ -d "_AI/logs" ] && r="ok" || r="fail"
check "_AI/logs/ directory exists" "$r" "Run: mkdir -p _AI/logs"

# GOALS.md
[ -f "_AI/GOALS.md" ] && r="ok" || r="fail"
check "_AI/GOALS.md exists" "$r" "Create _AI/GOALS.md describing the goals and focus areas for this vault"

# VOICE.md (optional)
[ -f "_AI/VOICE.md" ] && r="ok" || r="missing"
warn "_AI/VOICE.md exists" "$r" "Create _AI/VOICE.md to enable prose drafting in your voice (compose workflow)"

# AI boot file
boot_found=""
boot_wired=""
for f in CLAUDE.md AGENTS.md .cursorrules; do
  if [ -f "$f" ]; then
    boot_found="$f"
    grep -q "_AI/core/AI.md" "$f" && boot_wired="ok"
    break
  fi
done

[ -n "$boot_found" ] && r="ok" || r="fail"
check "AI boot file exists (CLAUDE.md / AGENTS.md / .cursorrules)" "$r" "Create a boot file (e.g. CLAUDE.md) containing: Everything you need starts in \`_AI/core/AI.md\`."

if [ -n "$boot_found" ]; then
  [ -n "$boot_wired" ] && r="ok" || r="fail"
  check "$boot_found references _AI/core/AI.md" "$r" "Add the line: Everything you need starts in \`_AI/core/AI.md\`."
fi

# Pre-commit sensitivity hook
hook=".git/hooks/pre-commit"
if [ -f "$hook" ] && [ -x "$hook" ]; then
  r="ok"
else
  r="fail"
fi
check "Pre-commit sensitivity hook installed" "$r" "Run: cp _AI/core/scripts/pre-commit-sensitivity-check.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit"

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
