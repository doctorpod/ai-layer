#!/usr/bin/env python3
"""
List Question notes in a folder with their status/opened/updated frontmatter.
Used by questions.md so dedup checks and reviews don't need to read every
Question file in full.

Usage:
  python3 list-questions.py <questions-folder>

Output:
  filename                      status     opened      updated
  Q1 - TPO status unclear.md    dismissed  2026-06-01  2026-08-06
  Q2 - DW nests in the mart.md  surmised   2026-07-10  2026-07-10

Run from vault root.
"""

import re
import sys
from pathlib import Path


def extract_field(frontmatter, key):
    m = re.search(rf'^{key}:\s*(.+)$', frontmatter, re.MULTILINE)
    if not m:
        return ''
    return m.group(1).strip().strip('"').strip("'")


def parse_question_note(path):
    content = path.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return None
    end = content.find('\n---', 3)
    if end == -1:
        return None
    fm = content[4:end]
    return {
        'status': extract_field(fm, 'status') or '(none)',
        'opened': extract_field(fm, 'opened'),
        'updated': extract_field(fm, 'updated'),
    }


def main():
    if len(sys.argv) < 2:
        print('Usage: list-questions.py <questions-folder>', file=sys.stderr)
        sys.exit(1)

    folder = Path(sys.argv[1])
    if not folder.exists():
        print(f'Error: folder not found: {folder}', file=sys.stderr)
        sys.exit(1)

    entries = []
    for path in sorted(folder.glob('*.md')):
        parsed = parse_question_note(path)
        if parsed is None:
            print(f'  (skipped {path.name} — no frontmatter)', file=sys.stderr)
            continue
        entries.append((path.name, parsed))

    if not entries:
        print('No Question notes found.')
        return

    name_col = min(max(len(name) for name, _ in entries) + 2, 40)
    status_col = min(max(len(p['status']) for _, p in entries) + 2, 14)
    opened_col = 14

    for name, p in entries:
        print(f"{name:<{name_col}}{p['status']:<{status_col}}{p['opened']:<{opened_col}}{p['updated']}")

    print(f"\n{len(entries)} Question note(s) in {folder}")


if __name__ == '__main__':
    main()
