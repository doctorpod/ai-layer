#!/usr/bin/env python3
"""
enrich-select: Select notes for enrichment or deep-dive analysis.

Two modes:

  enrich (default) — randomly select notes eligible for link enrichment.
    A note is eligible if it lives in a lib/YYYY/ folder and its 'enriched'
    frontmatter field is absent or older than --days days.

  dive — select notes for a deep-dive analysis session:
    - Recent daily notes (last --recent-days days, from the gig journal folder)
    - Latest N recently modified notes from lib/ and gig lib/ folders
    - N random notes from the same pool
    Useful for surfacing patterns and insights from current + broader context.

Usage:
    python3 _AI/core/scripts/enrich-select.py [--mode enrich|dive] [--count N] [--days N]

Options:
    --mode          enrich or dive (default: enrich)
    --count N       Notes to select per category in dive mode, or total in enrich mode (default: 5)
    --days N        Enrichment: skip notes enriched within N days (default: 90)
    --recent-days N Dive: how many days back to look for recent dailies (default: 7)
"""

import os
import re
import sys
import yaml
import random
import argparse
from datetime import datetime, timedelta, date
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


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--mode', choices=['enrich', 'dive'], default='enrich')
    p.add_argument('--count', type=int, default=5)
    p.add_argument('--days', type=int, default=90)
    p.add_argument('--recent-days', type=int, default=7)
    return p.parse_args()


def get_frontmatter_date(path, field):
    """Return a date value from a frontmatter field, or None."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                fm = yaml.safe_load(parts[1]) or {}
                val = fm.get(field)
                if val:
                    if isinstance(val, str):
                        return datetime.strptime(val[:10], '%Y-%m-%d')
                    if hasattr(val, 'year'):
                        return datetime(val.year, val.month, val.day)
    except Exception:
        pass
    return None


def find_lib_notes():
    """All .md notes in lib/YYYY/ and gigs/*/lib/YYYY/ folders."""
    notes = []

    lib_root = os.path.join(VAULT_ROOT, 'lib')
    if os.path.isdir(lib_root):
        for year_dir in os.listdir(lib_root):
            year_path = os.path.join(lib_root, year_dir)
            if os.path.isdir(year_path) and re.match(r'^\d{4}$', year_dir):
                for fname in os.listdir(year_path):
                    if fname.endswith('.md'):
                        notes.append(os.path.join(year_path, fname))

    gigs_root = os.path.join(VAULT_ROOT, 'gigs')
    if os.path.isdir(gigs_root):
        for gig in os.listdir(gigs_root):
            gig_lib = os.path.join(gigs_root, gig, 'lib')
            if os.path.isdir(gig_lib):
                for year_dir in os.listdir(gig_lib):
                    year_path = os.path.join(gig_lib, year_dir)
                    if os.path.isdir(year_path) and re.match(r'^\d{4}$', year_dir):
                        for fname in os.listdir(year_path):
                            if fname.endswith('.md'):
                                notes.append(os.path.join(year_path, fname))
    return notes


# ── Enrich mode ──────────────────────────────────────────────────────────────

def find_eligible_for_enrich(days_threshold):
    cutoff = datetime.now() - timedelta(days=days_threshold)
    eligible = []
    for path in find_lib_notes():
        enriched = get_frontmatter_date(path, 'enriched')
        if enriched is None or enriched < cutoff:
            eligible.append(path)
    return eligible


def run_enrich(args):
    eligible = find_eligible_for_enrich(args.days)
    if not eligible:
        print("No eligible notes found.", file=sys.stderr)
        sys.exit(0)
    count = min(args.count, len(eligible))
    selected = random.sample(eligible, count)
    print(f"Enrich mode — selected {count} of {len(eligible)} eligible notes:\n")
    for path in selected:
        print(f"  {os.path.relpath(path, VAULT_ROOT)}")


# ── Dive mode ─────────────────────────────────────────────────────────────────

def find_recent_dailies(recent_days):
    """Find daily notes from the last N days. Checks gig journal folders."""
    cutoff = date.today() - timedelta(days=recent_days)
    found = []

    # Check gigs/*/journal/
    gigs_root = os.path.join(VAULT_ROOT, 'gigs')
    if os.path.isdir(gigs_root):
        for gig in os.listdir(gigs_root):
            journal = os.path.join(gigs_root, gig, 'journal')
            if os.path.isdir(journal):
                for fname in sorted(os.listdir(journal), reverse=True):
                    if re.match(r'^\d{4}-\d{2}-\d{2}\.md$', fname):
                        note_date = date.fromisoformat(fname[:10])
                        if note_date >= cutoff:
                            found.append(os.path.join(journal, fname))

    # Also check root journal/
    root_journal = os.path.join(VAULT_ROOT, 'journal')
    if os.path.isdir(root_journal):
        for fname in sorted(os.listdir(root_journal), reverse=True):
            if re.match(r'^\d{4}-\d{2}-\d{2}\.md$', fname):
                note_date = date.fromisoformat(fname[:10])
                if note_date >= cutoff:
                    found.append(os.path.join(root_journal, fname))

    return found


def find_recently_modified(all_notes, n):
    """Return the N most recently modified notes from a list."""
    dated = [(os.path.getmtime(p), p) for p in all_notes if os.path.exists(p)]
    dated.sort(reverse=True)
    return [p for _, p in dated[:n]]


def run_dive(args):
    n = args.count

    dailies = find_recent_dailies(args.recent_days)
    all_lib = find_lib_notes()
    recent = find_recently_modified(all_lib, n)
    random_pool = [p for p in all_lib if p not in recent]
    random_picks = random.sample(random_pool, min(n, len(random_pool)))

    print(f"Dive mode — {args.recent_days}-day dailies + {n} recent + {n} random:\n")

    if dailies:
        print("Recent daily notes:")
        for p in dailies:
            print(f"  {os.path.relpath(p, VAULT_ROOT)}")
    else:
        print("Recent daily notes: none found")

    print(f"\nLatest {n} modified lib notes:")
    for p in recent:
        print(f"  {os.path.relpath(p, VAULT_ROOT)}")

    print(f"\nRandom {n} lib notes:")
    for p in random_picks:
        print(f"  {os.path.relpath(p, VAULT_ROOT)}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    if args.mode == 'dive':
        run_dive(args)
    else:
        run_enrich(args)


if __name__ == '__main__':
    main()
