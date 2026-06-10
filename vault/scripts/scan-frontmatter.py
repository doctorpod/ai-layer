#!/usr/bin/env python3
"""
Parse YAML frontmatter from .md files and report categories.
Reads file paths from stdin (one per line) or scans a folder directly.
Groups output by undated (potential strays) and dated captures.

Usage:
  python3 scan-frontmatter.py [folder]
  python3 list-notes.py <folder> [options] | python3 scan-frontmatter.py

Output:
  === UNDATED (potential strays) ===
    path/to/note.md           Glossary, Touchpoints
    path/to/stray.md          (none)  *** NO CATEGORY

  === DATED CAPTURES ===
    path/to/2026-06-10 SU.md  (none)  *** NO CATEGORY

  N notes — M missing categories, K undated

Run from vault root.
"""

import sys
import re
from pathlib import Path

DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})')
EXCLUDE_NAMES = {'README.md', 'INDEX.md', 'QUESTIONS.md', 'DECISIONS.md', 'MEMORY.md', 'AI.md', 'STYLE.md', 'SPATIAL.md', 'VOICE.md'}
EXCLUDE_FOLDERS = {'.obsidian', '.git', '_AI', 'assets', 'attachments', 'curated', 'wiki', 'templates'}


def should_exclude(path):
    if path.name in EXCLUDE_NAMES:
        return True
    for part in path.parts:
        if part in EXCLUDE_FOLDERS:
            return True
    return False


def extract_cat_name(raw):
    """Extract display name from a raw category value like '[[lib/cats/Glossary|Glossary]]'."""
    raw = raw.strip().strip('"').strip("'")
    m = re.match(r'\[{1,2}([^\]]+)\]{1,2}', raw)
    if m:
        inner = m.group(1)
        return inner.split('|')[-1].strip()
    return raw


def parse_frontmatter_categories(content):
    """
    Returns:
      None  — no frontmatter at all
      []    — frontmatter present but no categories property
      [...]  — list of category display names
    """
    if not content.startswith('---'):
        return None

    end = content.find('\n---', 3)
    if end == -1:
        return None

    fm = content[4:end]

    cat_match = re.search(r'^categories:\s*\n((?:[ \t]+-[^\n]*\n?)*)', fm, re.MULTILINE)
    if cat_match:
        cats = []
        for line in cat_match.group(1).splitlines():
            item_match = re.match(r'^\s+-\s+(.+)$', line)
            if item_match:
                cats.append(extract_cat_name(item_match.group(1)))
        return cats

    inline_match = re.search(r'^categories:\s*\[([^\]]*)\]', fm, re.MULTILINE)
    if inline_match:
        items = inline_match.group(1).split(',')
        return [extract_cat_name(item) for item in items if item.strip()]

    return []


def scan(paths):
    undated = []
    dated = []

    for raw_path in paths:
        path = Path(raw_path.strip())
        if not path.exists() or path.suffix != '.md':
            continue

        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            sys.stderr.write(f'Could not read {path}: {e}\n')
            continue

        cats = parse_frontmatter_categories(content)
        is_dated = bool(DATE_RE.match(path.name))
        entry = (str(path), cats)

        if is_dated:
            dated.append(entry)
        else:
            undated.append(entry)

    return undated, dated


def format_cats(cats):
    if cats is None:
        return '(no frontmatter)'
    if not cats:
        return '(none)'
    return ', '.join(cats)


def print_section(title, entries):
    if not entries:
        return
    col = min(max((len(e[0]) for e in entries), default=0) + 2, 80)
    print(f'\n=== {title} ===')
    for path, cats in entries:
        label = format_cats(cats)
        flag = '  *** NO CATEGORY' if cats is not None and not cats else ''
        print(f'  {path:<{col}}{label}{flag}')


def main():
    if not sys.stdin.isatty():
        paths = sys.stdin.readlines()
    elif len(sys.argv) > 1:
        folder = Path(sys.argv[1])
        if not folder.exists():
            print(f'Error: folder not found: {folder}', file=sys.stderr)
            sys.exit(1)
        paths = [str(p) for p in sorted(folder.rglob('*.md')) if not should_exclude(p)]
    else:
        print('Usage: scan-frontmatter.py [folder]  OR  list-notes.py ... | scan-frontmatter.py', file=sys.stderr)
        sys.exit(1)

    undated, dated = scan(paths)

    print_section('UNDATED (potential strays)', undated)
    print_section('DATED CAPTURES', dated)

    total = len(undated) + len(dated)
    no_cat = sum(1 for _, c in undated + dated if c is not None and not c)
    print(f'\n{total} notes — {no_cat} missing categories, {len(undated)} undated')


if __name__ == '__main__':
    main()
