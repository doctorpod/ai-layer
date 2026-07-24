#!/usr/bin/env python3
"""
List radar notes in a folder with their status/latest/updated frontmatter.
Used by add-to-radar.md so Capture mode's dedup check and Review mode don't
need to read every radar note in full.

Usage:
  python3 list-radar.py <radar-folder>

Output:
  filename                     status     updated     latest
  stale-permits.md             watching   2026-06-01  Council said mid-July
  vendor-dispute.md            dormant    2026-04-12  No movement since escalation

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


def parse_radar_note(path):
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
        'latest': extract_field(fm, 'latest') or '(none)',
    }


def main():
    if len(sys.argv) < 2:
        print('Usage: list-radar.py <radar-folder>', file=sys.stderr)
        sys.exit(1)

    folder = Path(sys.argv[1])
    if not folder.exists():
        print(f'Error: folder not found: {folder}', file=sys.stderr)
        sys.exit(1)

    entries = []
    for path in sorted(folder.glob('*.md')):
        parsed = parse_radar_note(path)
        if parsed is None:
            print(f'  (skipped {path.name} — no frontmatter)', file=sys.stderr)
            continue
        entries.append((path.name, parsed))

    if not entries:
        print('No radar notes found.')
        return

    name_col = min(max(len(name) for name, _ in entries) + 2, 40)
    status_col = min(max(len(p['status']) for _, p in entries) + 2, 14)
    updated_col = 14

    for name, p in entries:
        print(f"{name:<{name_col}}{p['status']:<{status_col}}{p['updated']:<{updated_col}}{p['latest']}")

    print(f"\n{len(entries)} radar note(s) in {folder}")


if __name__ == '__main__':
    main()
