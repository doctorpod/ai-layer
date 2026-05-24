#!/usr/bin/env bash

# Run from the root of the target codebase.

PASS="✓"
FAIL="✗"
errors=0
WARN="!"
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
check "_AI/local/ exists" "$r" "Run: bash ~/Dev/ai-layer/scripts/install-target.sh --code"

[ -f "_AI/local/AI.md" ] && r="ok" || r="fail"
check "_AI/local/AI.md exists" "$r" "Check that _AI/local is correctly symlinked (run install-target.sh --code)"

[ -d "_AI/shared" ] && r="ok" || r="fail"
check "_AI/shared/ exists" "$r" "Run: bash ~/Dev/ai-layer/scripts/install-target.sh --code"

[ -d "_AI/PRPs" ] && r="ok" || r="fail"
check "_AI/PRPs/ directory exists" "$r" "Run: mkdir -p _AI/PRPs"

# CODEX.md (optional)
[ -f "_AI/CODEX.md" ] && r="ok" || r="missing"
warn "_AI/CODEX.md exists" "$r" "Create _AI/CODEX.md to provide a domain glossary for AI workflows"

# OVERVIEW.md
if [ ! -f "_AI/OVERVIEW.md" ]; then
  check "_AI/OVERVIEW.md exists" "fail" "Create _AI/OVERVIEW.md (see ai-layer README for required sections)"
  check "_AI/OVERVIEW.md has ## Architecture" "fail" "Add an ## Architecture section to _AI/OVERVIEW.md"
  check "_AI/OVERVIEW.md has ## Anti-patterns" "fail" "Add an ## Anti-patterns section to _AI/OVERVIEW.md"
else
  check "_AI/OVERVIEW.md exists" "ok" ""
  grep -q "^## Architecture" "_AI/OVERVIEW.md" && r="ok" || r="fail"
  check "_AI/OVERVIEW.md has ## Architecture" "$r" "Add an '## Architecture' heading to _AI/OVERVIEW.md"
  grep -q "^## Anti-patterns" "_AI/OVERVIEW.md" && r="ok" || r="fail"
  check "_AI/OVERVIEW.md has ## Anti-patterns" "$r" "Add an '## Anti-patterns' heading to _AI/OVERVIEW.md"
fi

# VALIDATION.md
if [ ! -f "_AI/VALIDATION.md" ]; then
  check "_AI/VALIDATION.md exists" "fail" "Create _AI/VALIDATION.md (see ai-layer README for required sections)"
  check "_AI/VALIDATION.md has ## Validation gates" "fail" "Add a ## Validation gates section to _AI/VALIDATION.md"
else
  check "_AI/VALIDATION.md exists" "ok" ""
  grep -q "^## Validation gates" "_AI/VALIDATION.md" && r="ok" || r="fail"
  check "_AI/VALIDATION.md has ## Validation gates" "$r" "Add a '## Validation gates' heading to _AI/VALIDATION.md"
fi

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
check "AI boot file exists (CLAUDE.md / AGENTS.md / .cursorrules)" "$r" "Create a boot file (e.g. CLAUDE.md) containing: See \`_AI/local/AI.md\` for project context and available workflows."

if [ -n "$boot_found" ]; then
  [ -n "$boot_wired" ] && r="ok" || r="fail"
  check "$boot_found references _AI/local/AI.md" "$r" "Add the line: See \`_AI/local/AI.md\` for project context and available workflows."
fi

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
