#!/bin/bash
# pre-commit-sensitivity-check.sh
# Git pre-commit hook. Scans staged markdown files for sensitive content.
# Patterns are loaded from _AI/core/scripts/sensitive-patterns.conf.
# Blocks the commit if potential issues are found.
#
# Installation (run once from vault root):
#   cp _AI/core/scripts/pre-commit-sensitivity-check.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit

PATTERNS_FILE="_AI/core/scripts/sensitive-patterns.conf"

if [ ! -f "$PATTERNS_FILE" ]; then
    echo "Warning: sensitivity patterns file not found at $PATTERNS_FILE — skipping check."
    exit 0
fi

STAGED_MD=$(git diff --cached --name-only --diff-filter=ACM | grep "\.md$" | grep -v "\.excalidraw\.md$")

if [ -z "$STAGED_MD" ]; then
    exit 0
fi

# Build combined pattern from conf file
PATTERN=$(grep -v '^\s*#' "$PATTERNS_FILE" | grep -v '^\s*$' | tr '\n' '|' | sed 's/|$//')

if [ -z "$PATTERN" ]; then
    exit 0
fi

FOUND=0

for file in $STAGED_MD; do
    # Skip _AI/ folder (config files, not content)
    [[ "$file" == _AI/* ]] && continue

    result=$(grep -i -n -E "$PATTERN" "$file" 2>/dev/null | grep -iv 'noscan')

    if [ -n "$result" ]; then
        echo "⚠️  Possible sensitive content in: $file"
        echo "$result"
        echo ""
        FOUND=1
    fi
done

if [ "$FOUND" -eq 1 ]; then
    echo "Commit blocked — review the above, edit the files, re-stage, then commit again."
    echo "To update the pattern list, edit _AI/core/scripts/sensitive-patterns.conf."
    exit 1
fi

exit 0
