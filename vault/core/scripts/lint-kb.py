#!/usr/bin/env python3
"""
Structural lint check for a knowledge base wiki folder.

Usage:
    python3 lint-kb.py <path-to-kb>   # lint one KB
    python3 lint-kb.py                 # lint all auto-discovered KBs (any folder with wiki/)

Checks:
    - Format compliance per page (Summary, Sources, Last updated, ---, ## Related)
    - Orphan pages (no inbound links from other pages in the same KB)
    - Broken cross-KB wikilinks (path-style [[a/b/c]] that resolve to nothing)
    - Pending [!caution] markers (unresolved verification items)

Bare wikilinks ([[Name]] with no path separator) are treated as person/concept
references and are not checked for file existence.
"""

import os
import re
import sys
from pathlib import Path

def _find_vault_root():
    for p in [Path.cwd(), *Path.cwd().parents]:
        if (p / '_AI').is_dir():
            return p
    raise RuntimeError("Vault root not found — run from within the vault directory")

VAULT_ROOT = _find_vault_root()

REQUIRED_FIELDS = ['**Summary**', '**Sources**', '**Last updated**']


def discover_kbs():
    kbs = []
    for root, dirs, _ in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '_AI']
        if 'wiki' in dirs:
            kbs.append(Path(root))
    return sorted(kbs)


def find_all_vault_wiki_files():
    files = []
    for root, dirs, filenames in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if Path(root).name == 'wiki':
            for f in filenames:
                if f.endswith('.md'):
                    files.append(Path(root) / f)
    return files


def find_wiki_files(kb_path):
    wiki_dir = kb_path / 'wiki'
    if not wiki_dir.exists():
        return []
    return sorted(wiki_dir.glob('*.md'))


def extract_wikilinks(text):
    return re.findall(r'\[\[([^\]|#\n]+?)(?:\|[^\]\n]*)?\]\]', text)


def resolve_path_link(link, all_vault_files):
    link = link.strip().rstrip('/')
    candidate = (VAULT_ROOT / link).with_suffix('.md')
    if candidate.exists():
        return candidate
    stem = Path(link).name
    matches = [f for f in all_vault_files if f.stem == stem]
    return matches[0] if len(matches) == 1 else (matches[0] if matches else None)


def lint_kb(kb_path, all_vault_files):
    wiki_files = find_wiki_files(kb_path)
    if not wiki_files:
        return None

    # Build inbound link counts for orphan detection
    stems_linked_from = {f: set() for f in wiki_files}
    for f in wiki_files:
        text = f.read_text(encoding='utf-8')
        for link in extract_wikilinks(text):
            target_stem = Path(link).name.lower()
            for other in wiki_files:
                if other != f and other.stem.lower() == target_stem:
                    stems_linked_from[other].add(f)

    format_issues = []
    link_issues = []
    caution_items = []

    for f in wiki_files:
        text = f.read_text(encoding='utf-8')
        rel = str(f.relative_to(VAULT_ROOT))

        # --- Format checks ---
        for field in REQUIRED_FIELDS:
            if field not in text:
                format_issues.append(f"{rel} — missing {field}")

        if '\n---\n' not in text:
            format_issues.append(f"{rel} — missing --- separator after header block")

        if '## Related\n' not in text and '## Related\r\n' not in text:
            if '## Related pages' in text:
                format_issues.append(f"{rel} — uses '## Related pages' (should be '## Related')")
            else:
                format_issues.append(f"{rel} — missing ## Related section")

        # --- Orphan check ---
        if not stems_linked_from[f]:
            link_issues.append(f"{rel} — orphan: no inbound links from other pages in this KB")

        # --- Broken path-style wikilinks ---
        for link in extract_wikilinks(text):
            if '/' in link:
                if not resolve_path_link(link, all_vault_files):
                    link_issues.append(f"{rel} — broken link [[{link}]]")

        # --- Pending caution markers ---
        for match in re.finditer(r'>\s*\[!caution\]\s*(.+)', text):
            caution_items.append(f"{rel} — {match.group(1).strip()}")

    return {
        'page_count': len(wiki_files),
        'format_issues': format_issues,
        'link_issues': link_issues,
        'caution_items': caution_items,
    }


def print_report(kb_path, result):
    label = str(kb_path.relative_to(VAULT_ROOT))
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}")

    if result is None:
        print("  No wiki/ folder found.")
        return

    total = len(result['format_issues']) + len(result['link_issues'])

    if result['format_issues']:
        print(f"\nFORMAT  ({len(result['format_issues'])} issue(s))")
        for issue in result['format_issues']:
            print(f"  • {issue}")

    if result['link_issues']:
        print(f"\nLINKS  ({len(result['link_issues'])} issue(s))")
        for issue in result['link_issues']:
            print(f"  • {issue}")

    if result['caution_items']:
        print(f"\nPENDING VERIFICATION  ({len(result['caution_items'])} item(s))")
        for item in result['caution_items']:
            print(f"  • {item}")

    if total == 0:
        print(f"\n  All clear — {result['page_count']} page(s) checked, no structural issues.")
    else:
        print(f"\n  {total} structural issue(s) across {result['page_count']} page(s).")

    if result['caution_items']:
        print(f"  {len(result['caution_items'])} item(s) still pending verification.")


def main():
    all_vault_files = find_all_vault_wiki_files()

    if len(sys.argv) > 1:
        kb_path = Path(sys.argv[1])
        if not kb_path.is_absolute():
            kb_path = VAULT_ROOT / sys.argv[1]
        kb_paths = [kb_path]
    else:
        kb_paths = discover_kbs()

    for kb_path in kb_paths:
        result = lint_kb(kb_path, all_vault_files)
        print_report(kb_path, result)

    print()


if __name__ == '__main__':
    main()
