#!/usr/bin/env python3
"""
Find decision blocks in a KB's PRPs/ folder that have no linked component yet.
Scans DECISIONS.md and prp.md files for `## heading` blocks lacking a
`**Component(s):**` line before the next heading or end of file.

Usage:
  python3 find-unlinked-decisions.py <kb-path>

<kb-path> is a repos/<name>/ folder containing a PRPs/ subfolder.

Output:
  path/to/PRPs/ticket/DECISIONS.md: Decision title
  path/to/PRPs/ticket/prp.md: Other decision title

  N unlinked decision block(s) across M file(s) checked.

Run from vault root, or pass an absolute/relative kb-path.
"""

import re
import sys
from pathlib import Path

SOURCE_NAMES = {'DECISIONS.md', 'prp.md'}
HEADING_RE = re.compile(r'^##\s+(.+?)\s*\n(.*?)(?=\n^##\s|\Z)', re.MULTILINE | re.DOTALL)
COMPONENT_RE = re.compile(r'\*\*Component\(s\):\*\*')


def find_source_files(kb_path):
    prps = kb_path / 'PRPs'
    if not prps.is_dir():
        return []
    return sorted(p for p in prps.rglob('*.md') if p.name in SOURCE_NAMES)


def unlinked_headings(path):
    text = path.read_text(encoding='utf-8')
    unlinked = []
    for m in HEADING_RE.finditer(text):
        title, body = m.group(1), m.group(2)
        if not COMPONENT_RE.search(body):
            unlinked.append(title)
    return unlinked


def main():
    if len(sys.argv) != 2:
        print('Usage: find-unlinked-decisions.py <kb-path>', file=sys.stderr)
        sys.exit(1)

    kb_path = Path(sys.argv[1])
    if not kb_path.is_dir():
        print(f'Error: not a folder: {kb_path}', file=sys.stderr)
        sys.exit(1)

    files = find_source_files(kb_path)
    total_unlinked = 0

    for path in files:
        for title in unlinked_headings(path):
            print(f'{path}: {title}')
            total_unlinked += 1

    print(f'\n{total_unlinked} unlinked decision block(s) across {len(files)} file(s) checked.')


if __name__ == '__main__':
    main()
