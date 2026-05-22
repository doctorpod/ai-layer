#!/bin/bash
# sensitivity-scan.sh
# Scans all markdown files in the vault for potentially sensitive content.
# Patterns are loaded from sensitive-patterns.conf in the same directory.
#
# Usage:
#   bash _AI/core/scripts/sensitivity-scan.sh            # run from vault root
#   bash _AI/core/scripts/sensitivity-scan.sh /path/to/vault

VAULT="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PATTERNS_FILE="$SCRIPT_DIR/sensitive-patterns.conf"

if [ ! -f "$PATTERNS_FILE" ]; then
    echo "Error: patterns file not found at $PATTERNS_FILE"
    exit 1
fi

# Build combined pattern from conf file (strip comments and blank lines)
PATTERN=$(grep -v '^\s*#' "$PATTERNS_FILE" | grep -v '^\s*$' | tr '\n' '|' | sed 's/|$//')

if [ -z "$PATTERN" ]; then
    echo "Error: no patterns found in $PATTERNS_FILE"
    exit 1
fi

echo "=== Sensitivity scan: $VAULT ==="
echo "Patterns loaded from: $PATTERNS_FILE"
echo "Lines marked 'noscan' are excluded."
echo ""

matches=$(grep --color -r -i -n -E "$PATTERN" "$VAULT" \
    --include="*.md" \
    --exclude="*.excalidraw.md" \
    --exclude-dir="_AI" \
    --exclude-dir=".git" \
    --exclude-dir=".obsidian" \
    --exclude-dir="curated" \
    2>/dev/null | grep -iv 'noscan')

if [ -n "$matches" ]; then
    echo "⚠️  Potential sensitive content found:"
    echo ""
    echo "$matches"
    echo ""
    echo "=== Review each match. Edit or remove sensitive content, or add 'noscan' to the line to acknowledge it. ==="
else
    echo "✓ No matches found."
fi

echo ""
echo "Note: this script cannot detect:"
echo "  - Names of specific people (review lib/people/, gig log/ folders, and meeting notes manually)"
echo "  - Context-dependent sensitivity or client-specific codenames"
