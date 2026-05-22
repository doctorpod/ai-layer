#!/usr/bin/env bash

# Run from the root of the target codebase.

PASS="✓"
FAIL="✗"
errors=0

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

echo ""
echo "AI layer setup check"
echo "--------------------"

# Core structure
[ -d "_AI/core" ]    && r="ok" || r="fail"
check "_AI/core/ exists" "$r" "Run: mkdir -p _AI && ln -s ~/Dev/code-ai-layer/core _AI/core (or copy the folder)"

[ -f "_AI/core/AI.md" ] && r="ok" || r="fail"
check "_AI/core/AI.md exists" "$r" "Check that _AI/core is correctly symlinked or copied from code-ai-layer"

[ -d "_AI/PRPs" ] && r="ok" || r="fail"
check "_AI/PRPs/ directory exists" "$r" "Run: mkdir -p _AI/PRPs"

# OVERVIEW.md
if [ ! -f "_AI/OVERVIEW.md" ]; then
  check "_AI/OVERVIEW.md exists" "fail" "Create _AI/OVERVIEW.md (see code-ai-layer README for required sections)"
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
  check "_AI/VALIDATION.md exists" "fail" "Create _AI/VALIDATION.md (see code-ai-layer README for required sections)"
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
    grep -q "_AI/core/AI.md" "$f" && boot_wired="ok"
    break
  fi
done

[ -n "$boot_found" ] && r="ok" || r="fail"
check "AI boot file exists (CLAUDE.md / AGENTS.md / .cursorrules)" "$r" "Create a boot file (e.g. CLAUDE.md) containing: See \`_AI/core/AI.md\` for project context and available workflows."

if [ -n "$boot_found" ]; then
  [ -n "$boot_wired" ] && r="ok" || r="fail"
  check "$boot_found references _AI/core/AI.md" "$r" "Add the line: See \`_AI/core/AI.md\` for project context and available workflows."
fi

# Verdict
echo ""
if [ "$errors" -eq 0 ]; then
  echo "All checks passed — AI layer is correctly installed."
else
  echo "$errors issue(s) found — fix the above before using AI workflows."
fi
echo ""

exit $errors
