#!/usr/bin/env python3
"""
List .md files in a folder, filtered by date range or dated/undated flag.
Date filtering uses the filename prefix (YYYY-MM-DD), not filesystem dates.
Outputs one path per line — pipe to scan-frontmatter.py for category info.

Usage:
  python3 list-notes.py <folder> [options]

Options:
  --since YYYY-MM-DD | Nd   Include notes on or after this date (e.g. 2026-06-03 or 7d)
  --until YYYY-MM-DD        Include notes on or before this date
  --undated                 Only notes without a date prefix (potential strays)
  --dated                   Only notes with a date prefix

Examples:
  python3 list-notes.py gigs/2026-02-CCS/lib/2026 --since 7d
  python3 list-notes.py gigs/2026-02-CCS/lib/2026 --undated
  python3 list-notes.py gigs/2026-02-CCS/lib/2026 | python3 scan-frontmatter.py

Run from vault root.
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import date, timedelta

EXCLUDE_NAMES = {'README.md', 'INDEX.md', 'QUESTIONS.md', 'DECISIONS.md', 'MEMORY.md', 'AI.md', 'STYLE.md', 'SPATIAL.md', 'VOICE.md'}
EXCLUDE_FOLDERS = {'.obsidian', '.git', '_AI', 'assets', 'attachments', 'curated', 'wiki', 'templates'}
DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})')


def parse_since(val):
    if val is None:
        return None
    m = re.match(r'^(\d+)d$', val)
    if m:
        return date.today() - timedelta(days=int(m.group(1)))
    return date.fromisoformat(val)


def should_exclude(path):
    if path.name in EXCLUDE_NAMES:
        return True
    if path.suffix != '.md':
        return True
    for part in path.parts:
        if part in EXCLUDE_FOLDERS:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description='List notes in a folder with optional filters.')
    parser.add_argument('folder', help='Folder to scan (relative to vault root)')
    parser.add_argument('--since', help='Start date: YYYY-MM-DD or Nd')
    parser.add_argument('--until', help='End date: YYYY-MM-DD')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--undated', action='store_true', help='Only undated notes')
    group.add_argument('--dated', action='store_true', help='Only dated notes')
    args = parser.parse_args()

    if args.undated and (args.since or args.until):
        print('Warning: --since/--until ignored with --undated (undated notes have no date)', file=sys.stderr)

    since = parse_since(args.since)
    until = date.fromisoformat(args.until) if args.until else None

    folder = Path(args.folder)
    if not folder.exists():
        print(f'Error: folder not found: {folder}', file=sys.stderr)
        sys.exit(1)

    for path in sorted(folder.rglob('*.md')):
        if should_exclude(path):
            continue

        match = DATE_RE.match(path.name)

        if args.undated:
            if not match:
                print(path)
            continue

        if args.dated and not match:
            continue

        if match:
            try:
                note_date = date.fromisoformat(match.group(1))
            except ValueError:
                continue
            if since and note_date < since:
                continue
            if until and note_date > until:
                continue

        print(path)


if __name__ == '__main__':
    main()
