#!/usr/bin/env python3
"""
write-coverage: Batch-write the `coverage` frontmatter field on guide/
theme notes, so gap-check.md doesn't need a separate Read+Edit per theme.

Usage:
    python3 _AI/local/scripts/write-coverage.py <guide-folder> <theme-file>=<verdict> [<theme-file>=<verdict> ...]

    <guide-folder>  path to the piece's guide/ folder (relative to vault root, or absolute)
    <verdict>       one of: full, thin, missing

Skips (and reports, never writes coverage on) any theme whose `status` is
`rejected` — that's gap-check.md's own rule, enforced here too in case the
caller passes one by mistake.

Example:
    python3 _AI/local/scripts/write-coverage.py projects/my-project/design-doc/guide \\
        soil-drainage.md=full access-constraints.md=thin water-source.md=missing
"""

import re
import sys
from pathlib import Path

import yaml

VALID_VERDICTS = {'full', 'thin', 'missing'}
COVERAGE_LINE_RE = re.compile(r'^coverage:.*$', re.MULTILINE)


def _find_vault_root():
    # Try the invocation path before the symlink-resolved one: the AI layer is
    # usually symlinked into a vault, and .resolve() follows that link out into
    # the ai-layer repo — which has its own CLAUDE.md and would win wrongly.
    for start in (Path(__file__).absolute(), Path(__file__).resolve()):
        d = start.parent
        while d != d.parent:
            if (d / 'CLAUDE.md').exists():
                return d
            d = d.parent
    raise RuntimeError(f"Could not find vault root — no CLAUDE.md found above {__file__}")


VAULT_ROOT = _find_vault_root()


def _resolve(path_str):
    p = Path(path_str)
    return p if p.is_absolute() else VAULT_ROOT / p


def _parse_pairs(args):
    pairs = []
    errors = []
    for arg in args:
        if '=' not in arg:
            errors.append(f"{arg} — missing '=' (expected <theme-file>=<verdict>)")
            continue
        theme_file, verdict = arg.split('=', 1)
        if verdict not in VALID_VERDICTS:
            errors.append(f"{arg} — verdict must be one of {sorted(VALID_VERDICTS)}")
            continue
        pairs.append((theme_file, verdict))
    return pairs, errors


def _write_coverage(theme_path, verdict):
    """Returns a (status, detail) tuple: status is 'updated', 'skipped', or 'not_found'."""
    if not theme_path.exists():
        return 'not_found', None

    content = theme_path.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return 'skipped', 'no frontmatter'

    parts = content.split('---', 2)
    if len(parts) < 3:
        return 'skipped', 'malformed frontmatter'

    fm_text = parts[1]
    fm = yaml.safe_load(fm_text) or {}

    if fm.get('status') == 'rejected':
        return 'skipped', 'status: rejected'

    if not COVERAGE_LINE_RE.search(fm_text):
        return 'skipped', 'no coverage field in frontmatter'

    # Targeted line replace, not a full yaml.dump round-trip — that would
    # reformat every field's quoting/indentation, not just coverage.
    new_fm_text = COVERAGE_LINE_RE.sub(f'coverage: {verdict}', fm_text, count=1)
    new_content = f'---{new_fm_text}---{parts[2]}'
    theme_path.write_text(new_content, encoding='utf-8')
    return 'updated', None


def main():
    if len(sys.argv) < 3:
        print("Usage: write-coverage.py <guide-folder> <theme-file>=<verdict> [...]", file=sys.stderr)
        sys.exit(1)

    guide_folder = _resolve(sys.argv[1])
    pairs, errors = _parse_pairs(sys.argv[2:])

    if errors:
        print("Aborted — invalid arguments, nothing written:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)

    updated, skipped, not_found = [], [], []
    for theme_file, verdict in pairs:
        status, detail = _write_coverage(guide_folder / theme_file, verdict)
        if status == 'updated':
            updated.append(f"{theme_file} -> {verdict}")
        elif status == 'skipped':
            skipped.append(f"{theme_file} ({detail})")
        else:
            not_found.append(theme_file)

    if updated:
        print(f"Updated {len(updated)}:")
        for line in updated:
            print(f"  {line}")
    if skipped:
        print(f"Skipped {len(skipped)}:")
        for line in skipped:
            print(f"  {line}")
    if not_found:
        print(f"Not found {len(not_found)}:")
        for line in not_found:
            print(f"  {line}")


if __name__ == '__main__':
    main()
