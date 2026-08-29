#!/usr/bin/env python3
"""
check-assets: List a piece-folder's assets/ contents and flag which ones
are referenced anywhere in the target document.

A "reference" is just the bare filename appearing as a substring in the
target text — covers Obsidian embeds (![[name.png]]), plain links, and
filename mentions in prose. A miss is strong evidence of an unreferenced
asset, not proof: an asset can still be referenced by description alone
with no filename in sight. Treat "unreferenced" results as a shortlist to
glance at, not a final verdict.

Usage:
    python3 _AI/local/scripts/check-assets.py <piece-folder> [<target-file>]

    <piece-folder>  path to the piece-folder (relative to vault root, or absolute)
    <target-file>   defaults to <piece-folder>/output.md

Example:
    python3 _AI/local/scripts/check-assets.py projects/my-project/design-doc
"""

import os
import sys
from pathlib import Path


def _find_vault_root():
    d = Path(__file__).resolve().parent
    while d != d.parent:
        if (d / 'CLAUDE.md').exists():
            return d
        d = d.parent
    raise RuntimeError(f"Could not find vault root — no CLAUDE.md found above {__file__}")


VAULT_ROOT = _find_vault_root()


def _resolve(path_str):
    p = Path(path_str)
    return p if p.is_absolute() else VAULT_ROOT / p


def main():
    if len(sys.argv) < 2:
        print("Usage: check-assets.py <piece-folder> [<target-file>]", file=sys.stderr)
        sys.exit(1)

    piece_folder = _resolve(sys.argv[1])
    target = _resolve(sys.argv[2]) if len(sys.argv) > 2 else piece_folder / 'output.md'
    assets_dir = piece_folder / 'assets'

    if not assets_dir.exists():
        print(f"No assets/ folder in {piece_folder}")
        sys.exit(0)

    if not target.exists():
        print(f"Target file not found: {target}", file=sys.stderr)
        sys.exit(1)

    target_text = target.read_text(encoding='utf-8')

    assets = sorted(f for f in assets_dir.iterdir() if f.is_file())
    if not assets:
        print(f"assets/ is empty in {piece_folder}")
        sys.exit(0)

    referenced, unreferenced = [], []
    for asset in assets:
        (referenced if asset.name in target_text else unreferenced).append(asset.name)

    for name in referenced:
        print(f"referenced: {name}")
    for name in unreferenced:
        print(f"unreferenced: {name}")

    print(f"\n{len(referenced)} referenced, {len(unreferenced)} unreferenced (out of {len(assets)})")


if __name__ == '__main__':
    main()
