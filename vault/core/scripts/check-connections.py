#!/usr/bin/env python3
"""
Check that all ## Wider connections wikilinks are reciprocal.
Scans all .md files in wiki/ folders across the vault.
Run from anywhere — resolves vault root relative to this script.
"""
import os
import re
from pathlib import Path

def _find_vault_root():
    for p in [Path.cwd(), *Path.cwd().parents]:
        if (p / '_AI').is_dir():
            return p
    raise RuntimeError("Vault root not found — run from within the vault directory")

VAULT_ROOT = _find_vault_root()


def find_wiki_files():
    files = []
    for root, dirs, fs in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if Path(root).name == 'wiki':
            for f in fs:
                if f.endswith('.md'):
                    files.append(Path(root) / f)
    return files


def extract_wider_links(filepath):
    text = filepath.read_text(encoding='utf-8')
    m = re.search(r'^## Wider connections\s*\n(.*?)(?=\n^##|\Z)', text, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    section = m.group(1)
    return re.findall(r'\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]', section)


def resolve_link(link, all_files):
    link = link.strip().rstrip('/')
    # Full path match relative to vault root
    candidate = (VAULT_ROOT / link).with_suffix('.md')
    if candidate.exists():
        return candidate
    # Stem-only match
    stem = Path(link).name
    matches = [f for f in all_files if f.stem == stem]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        # Prefer the file whose vault-relative path contains the link string
        for m in matches:
            rel = str(m.relative_to(VAULT_ROOT)).replace('\\', '/')
            if link in rel:
                return m
        return matches[0]
    return None


def has_backlink(source, target, all_files):
    target_links = extract_wider_links(target)
    source_rel = str(source.relative_to(VAULT_ROOT)).replace('\\', '/').replace('.md', '')
    for raw in target_links:
        resolved = resolve_link(raw, all_files)
        if resolved and resolved.resolve() == source.resolve():
            return True
        # Fallback: path fragment or stem match
        raw = raw.strip()
        if source_rel.endswith(raw) or raw.endswith(source.stem):
            return True
    return False


def main():
    all_files = find_wiki_files()
    issues = []
    checked = 0

    for filepath in sorted(all_files):
        links = extract_wider_links(filepath)
        for raw_link in links:
            target = resolve_link(raw_link, all_files)
            if target is None:
                # Bare wikilinks without a path separator are person/concept mentions —
                # they intentionally have no file and are silently skipped.
                if '/' not in raw_link:
                    continue
                issues.append(
                    f"UNRESOLVED LINK\n"
                    f"  in: {filepath.relative_to(VAULT_ROOT)}\n"
                    f"  [[{raw_link}]] — no matching file found"
                )
                continue
            checked += 1
            if not has_backlink(filepath, target, all_files):
                issues.append(
                    f"MISSING BACKLINK\n"
                    f"  {filepath.relative_to(VAULT_ROOT)}\n"
                    f"  → {target.relative_to(VAULT_ROOT)}\n"
                    f"  (target has no return link in its ## Wider connections)"
                )

    if issues:
        print(f"\n{len(issues)} issue(s) found  ({checked} link(s) checked):\n")
        for issue in issues:
            print(f"  {issue}\n")
    else:
        print(f"\nAll clear — {checked} link(s) checked, all reciprocal.\n")


if __name__ == '__main__':
    main()
