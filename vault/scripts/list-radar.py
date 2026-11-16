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

import sys
from pathlib import Path

from vaultyaml import radar_item


def parse_radar_note(path):
    item = radar_item(path)
    if item is None:
        return None
    item['status'] = item['status'] or '(none)'
    item['latest'] = item['latest'] or '(none)'
    return item


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
