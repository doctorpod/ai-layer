#!/usr/bin/env python3
"""
check-docs: Report drift in the user docs under docs/writing/. Never edits.

Usage (from the repo root):
    python3 scripts/check-docs.py

Checks:
    Stale    a page lists a source in its `sources:` frontmatter whose last
             commit is dated after the page's `checked:` date (or on that date
             but after the page's own last commit), or which has uncommitted
             changes
    Missing  a page with no `sources:` or `checked:`, a listed source that
             doesn't exist, or an in-scope workflow with no page
    Links    a [[wikilink]] that resolves to no file, or to more than one

Exits 1 if anything is reported, else 0.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = 'docs/writing'

# Pages checked for broken links. The design-time docs beside them (PRINCIPLES,
# PATTERNS, My AI commandments) link into the owner's vault, so they can't
# resolve here.
LINK_SCOPE = ['docs/README.md', DOCS_DIR]

IN_SCOPE_WORKFLOWS = [
    'sync-guide', 'interview', 'elicit', 'beats', 'polish', 'scribe',
    'sanity', 'gap-check', 'diploma-ready',
]

# `_AI/` is excluded because its `docs` symlink would duplicate every page.
EXCLUDED_DIRS = {'.git', '_AI', 'node_modules'}

FENCE_RE = re.compile(r'^(```|~~~).*?^\1[^\n]*$', re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r'(`+).+?\1', re.DOTALL)
WIKILINK_RE = re.compile(r'!?\[\[([^\]\n]+)\]\]')


def _git(*args):
    return subprocess.run(['git', *args], cwd=REPO_ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()


def _frontmatter(text):
    """Parse the `sources:` list and `checked:` date. Returns (sources, checked);
    either is None when absent."""
    if not text.startswith('---\n'):
        return None, None
    end = text.find('\n---', 4)
    if end == -1:
        return None, None

    sources, checked, in_sources = None, None, False
    for line in text[4:end].splitlines():
        if in_sources and re.match(r'\s+-\s', line):
            sources.append(line.split('-', 1)[1].strip().strip('"\''))
            continue
        in_sources = False
        key, _, value = line.partition(':')
        value = value.strip()
        if key == 'sources':
            if value.startswith('['):
                sources = [s.strip().strip('"\'') for s in value.strip('[]').split(',') if s.strip()]
            else:
                sources, in_sources = [], True
        elif key == 'checked':
            checked = value.strip('"\'') or None
    return sources, checked


def _doc_pages():
    return sorted((REPO_ROOT / DOCS_DIR).rglob('*.md'))


def _rel(path):
    return path.relative_to(REPO_ROOT).as_posix()


def _committed_after_page(source, page):
    """Tiebreak for a source committed on the page's `checked:` date: was it
    committed after the page itself? An uncommitted or never-committed page is
    mid-check, so its `checked:` date stands."""
    page_rel = _rel(page)
    if _git('status', '--porcelain', '--', page_rel):
        return False
    page_time = _git('log', '-1', '--format=%ct', '--', page_rel)
    if not page_time:
        return False
    return int(_git('log', '-1', '--format=%ct', '--', source)) > int(page_time)


def check_sources():
    stale, missing = [], []
    for page in _doc_pages():
        sources, checked = _frontmatter(page.read_text(encoding='utf-8'))
        if not sources or not checked:
            missing.append(f'{_rel(page)} — no `sources:` or `checked:` frontmatter')
            continue
        for source in sources:
            if not (REPO_ROOT / source).exists():
                missing.append(f'{_rel(page)} — source not found: {source}')
                continue
            last_commit = _git('log', '-1', '--format=%cs', '--', source)
            if _git('status', '--porcelain', '--', source):
                stale.append(f'{_rel(page)} — {source} has uncommitted changes')
            elif last_commit > checked:
                stale.append(f'{_rel(page)} — {source} changed {last_commit}, checked {checked}')
            elif last_commit == checked and _committed_after_page(source, page):
                stale.append(f'{_rel(page)} — {source} changed {last_commit} after the page was last committed')
    return stale, missing


def check_missing_pages():
    return [f'{DOCS_DIR}/workflows/{name} workflow.md — no page for the {name} workflow'
            for name in IN_SCOPE_WORKFLOWS
            if not (REPO_ROOT / DOCS_DIR / 'workflows' / f'{name} workflow.md').exists()]


def _repo_files():
    files = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        rel_dir = Path(dirpath).relative_to(REPO_ROOT).as_posix()
        files.extend(f if rel_dir == '.' else f'{rel_dir}/{f}' for f in filenames)
    return files


def _link_targets(text):
    text = FENCE_RE.sub('', text)
    text = INLINE_CODE_RE.sub('', text)
    for match in WIKILINK_RE.finditer(text):
        # A `\|` alias separator appears inside Markdown tables.
        target = re.split(r'\\?\|', match.group(1), maxsplit=1)[0]
        target = target.split('#', 1)[0].strip()
        if target:
            yield target


def check_links():
    files = _repo_files()
    pages = []
    for scope in LINK_SCOPE:
        path = REPO_ROOT / scope
        pages.extend(sorted(path.rglob('*.md')) if path.is_dir() else [path] if path.exists() else [])

    findings = []
    for page in pages:
        for target in _link_targets(page.read_text(encoding='utf-8')):
            name = target if Path(target).suffix else f'{target}.md'
            matches = [f for f in files if f == name or f.endswith(f'/{name}')]
            if not matches:
                findings.append(f'{_rel(page)} — broken: [[{target}]]')
            elif len(matches) > 1:
                findings.append(f'{_rel(page)} — ambiguous: [[{target}]] matches {", ".join(matches)}')
    return findings


def main():
    stale, missing = check_sources()
    missing += check_missing_pages()
    links = check_links()

    for heading, findings in (('Stale', stale), ('Missing', missing), ('Links', links)):
        if findings:
            print(f'{heading}:')
            for line in findings:
                print(f'  {line}')

    if stale or missing or links:
        sys.exit(1)
    print('Docs OK')


if __name__ == '__main__':
    main()
