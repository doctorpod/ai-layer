#!/usr/bin/env python3
"""
set-enriched: Add or update the 'enriched' frontmatter field on a note.

Sets enriched to today's date. If the note has no frontmatter, adds a minimal
frontmatter block. If frontmatter exists, updates or inserts the enriched field.

Usage:
    python3 _AI/core/scripts/set-enriched.py <note-path>

Example:
    python3 _AI/core/scripts/set-enriched.py "gigs/2022-06-MoJ/lib/2024/My note.md"
"""

import os
import sys
import yaml
from datetime import date
from pathlib import Path


def _find_vault_root():
    """Walk up from this file to find the vault root (directory containing CLAUDE.md)."""
    d = Path(__file__).resolve().parent
    while d != d.parent:
        if (d / 'CLAUDE.md').exists():
            return str(d)
        d = d.parent
    raise RuntimeError(f"Could not find vault root — no CLAUDE.md found above {__file__}")


VAULT_ROOT = _find_vault_root()


def main():
    if len(sys.argv) < 2:
        print("Usage: set-enriched.py <note-path>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isabs(path):
        path = os.path.join(VAULT_ROOT, path)

    if not os.path.exists(path):
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    today = date.today().isoformat()

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            fm['enriched'] = today
            fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
            new_content = f'---\n{fm_str}---{parts[2]}'
        else:
            # Malformed frontmatter — prepend fresh block
            fm_str = yaml.dump({'enriched': today}, allow_unicode=True, default_flow_style=False)
            new_content = f'---\n{fm_str}---\n{content}'
    else:
        # No frontmatter — prepend minimal block
        fm_str = yaml.dump({'enriched': today}, allow_unicode=True, default_flow_style=False)
        new_content = f'---\n{fm_str}---\n{content}'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    rel = os.path.relpath(path, VAULT_ROOT)
    print(f"Set enriched: {today} on {rel}")


if __name__ == '__main__':
    main()
