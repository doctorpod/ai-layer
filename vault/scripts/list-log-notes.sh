#!/usr/bin/env bash
# Usage: list-log-notes.sh YYYY-MM-DD
# Lists all log notes on or after the given date, sorted chronologically.
# Run from the vault root.

date_arg="${1:?Usage: $0 YYYY-MM-DD}"

find -E . \
  -not -path './.git/*' \
  -not -path './_AI/*' \
  -regex ".*/[0-9]{4}-[0-9]{2}-[0-9]{2} .*\.md" \
  -print | while IFS= read -r file; do
    filename=$(basename "$file")
    file_date="${filename:0:10}"
    [[ ! "$file_date" < "$date_arg" ]] && echo "$file"
done | sort
