#!/usr/bin/env python3
"""Keep a vault's record of Jira as a baseline plus deltas. No AI involved.

Usage:
    python3 jira-snapshot.py ingest EXPORT.csv --dir SNAPSHOT_DIR [--date YYYY-MM-DD]
    python3 jira-snapshot.py current --dir SNAPSHOT_DIR [KEY ...] [--as-of YYYY-MM-DD] [--csv]

EXPORT.csv is Jira's own "Export CSV (all fields)" of a whole project
(`project = CVT ORDER BY key`). Exporting the whole project every time keeps
"gone" meaningful: a ticket missing from the export was deleted or moved,
not just filtered out.

ingest
    Slims the export to the columns worth keeping (see SLIM_FIELDS), compares
    each ticket with its current state, and writes into SNAPSHOT_DIR:
        YYYY-MM-DD.csv   only the tickets that are new or changed (the first
                         ingest writes every ticket: the baseline)
        YYYY-MM-DD.keys  every key in the export, one per line (the manifest)
        YYYY-MM-DD.md    the change report, readable in Obsidian
    A ticket counts as changed only if a kept field other than `updated`
    differs, so re-ranks and watcher changes don't create rows.
    Refuses to overwrite an existing snapshot. Without --date, a second
    export on the same day is stored as YYYY-MM-DD-2 (then -3, ...).

current
    Rebuilds the latest state of every ticket (each key's most recent row
    across all snapshots) and prints it, optionally limited to KEYs or to
    snapshots up to --as-of. Tickets absent from the latest manifest are
    marked gone. --csv prints CSV instead of a summary table.

Account ids in comments and @-mentions are replaced with people's names,
using the id/name pairs the export itself carries (assignee, reporter,
creator, watchers), so the stored files hold names, not ids.
"""

import argparse
import csv
import io
import os
import re
import sys
from datetime import date, datetime

SLIM_FIELDS = [
    "key", "summary", "type", "status", "resolution", "priority",
    "assignee", "reporter", "parent", "parent_summary", "sprints", "labels",
    "story_points", "created", "updated", "resolved", "due", "links",
    "description", "comments",
]
# Fields compared to decide whether a ticket changed.
COMPARED = [f for f in SLIM_FIELDS if f != "updated"]
# Fields shown as "old -> new" in the report; the rest are reported as changed.
SHORT_FIELDS = ["summary", "type", "status", "resolution", "priority", "assignee",
                "reporter", "parent", "sprints", "labels", "story_points", "due", "links"]
COMMENT_SEP = "\n\n----\n\n"
ID_PAIRS = [("Assignee", "Assignee Id"), ("Reporter", "Reporter Id"),
            ("Creator", "Creator Id"), ("Watchers", "Watchers Id")]
SNAP_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}(?:-\d+)?)\.csv$")


def snap_order(name):
    """Sort key: date, then same-day sequence (2026-11-11 < 2026-11-11-2 < 2026-11-11-10)."""
    return (name[:10], int(name[11:] or 1))


def jira_date(value):
    """'24/Aug/26 11:51 AM' -> '2026-08-24 11:51'. Unparseable values pass through."""
    value = value.strip()
    if not value:
        return ""
    for fmt in ("%d/%b/%y %I:%M %p", "%d/%b/%y %H:%M", "%d/%b/%y"):
        try:
            dt = datetime.strptime(value, fmt)
        except ValueError:
            continue
        return dt.strftime("%Y-%m-%d") if fmt == "%d/%b/%y" else dt.strftime("%Y-%m-%d %H:%M")
    return value


def read_export(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [r for r in reader if any(r)]
    return header, rows


def build_names(header, rows):
    """Map Jira account ids to display names from the id/name column pairs."""
    names = {}
    for name_col, id_col in ID_PAIRS:
        name_idx = [i for i, h in enumerate(header) if h == name_col]
        id_idx = [i for i, h in enumerate(header) if h == id_col]
        for row in rows:
            # Repeated columns (watchers) pair up by position.
            for ni, ii in zip(name_idx, id_idx):
                if ni < len(row) and ii < len(row) and row[ni] and row[ii]:
                    names.setdefault(row[ii], row[ni])
    return names


def slim(header, rows, names):
    def cols(name):
        return [i for i, h in enumerate(header) if h == name]

    def first(row, name):
        for i in cols(name):
            if i < len(row) and row[i].strip():
                return row[i].strip()
        return ""

    def every(row, name):
        return [row[i].strip() for i in cols(name) if i < len(row) and row[i].strip()]

    def person(acc_id):
        return names.get(acc_id, acc_id)

    def unmention(text):
        return re.sub(r"\[~accountid:([^\]]+)\]", lambda m: "@" + person(m.group(1)), text)

    link_cols = sorted({h for h in header if h.startswith(("Inward issue link", "Outward issue link"))})
    out = {}
    for row in rows:
        key = first(row, "Issue key")
        links = []
        for col in link_cols:
            m = re.match(r"(Inward|Outward) issue link \((.*)\)", col)
            for k in every(row, col):
                links.append(f"{m.group(1).lower()} {m.group(2)}: {k}")
        comments = []
        for c in every(row, "Comment"):
            parts = c.split(";", 2)
            if len(parts) == 3:
                when, who, body = parts
                comments.append(f"{jira_date(when)} {person(who)}: {unmention(body.strip())}")
            else:
                comments.append(unmention(c))
        out[key] = {
            "key": key,
            "summary": first(row, "Summary"),
            "type": first(row, "Issue Type"),
            "status": first(row, "Status"),
            "resolution": first(row, "Resolution"),
            "priority": first(row, "Priority"),
            "assignee": first(row, "Assignee"),
            "reporter": first(row, "Reporter"),
            "parent": first(row, "Parent key"),
            "parent_summary": first(row, "Parent summary"),
            "sprints": "; ".join(every(row, "Sprint")),
            "labels": "; ".join(sorted(every(row, "Labels"))),
            "story_points": first(row, "Custom field (Story point estimate)") or first(row, "Custom field (Story Points)"),
            "created": jira_date(first(row, "Created")),
            "updated": jira_date(first(row, "Updated")),
            "resolved": jira_date(first(row, "Resolved")),
            "due": jira_date(first(row, "Due date")),
            "links": "; ".join(sorted(links)),
            "description": unmention(first(row, "Description")),
            "comments": COMMENT_SEP.join(comments),
        }
    return out


def snapshot_dates(snap_dir, as_of=None):
    if not os.path.isdir(snap_dir):
        return []
    dates = sorted((m.group(1) for f in os.listdir(snap_dir) if (m := SNAP_RE.match(f))), key=snap_order)
    return [d for d in dates if as_of is None or snap_order(d) <= snap_order(as_of)]


def load_state(snap_dir, as_of=None):
    """Latest row per key, plus the latest manifest's keys (None if no snapshots)."""
    state = {}
    dates = snapshot_dates(snap_dir, as_of)
    for d in dates:
        with open(os.path.join(snap_dir, f"{d}.csv"), newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                state[row["key"]] = row
    present = None
    if dates:
        with open(os.path.join(snap_dir, f"{dates[-1]}.keys"), encoding="utf-8") as f:
            present = {line.strip() for line in f if line.strip()}
    return state, present, dates


def key_order(key):
    prefix, _, num = key.partition("-")
    return (prefix, int(num) if num.isdigit() else 0)


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SLIM_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def one_line(text, limit=160):
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def split_comments(text):
    return [c for c in text.split(COMMENT_SEP) if c] if text else []


def diff_ticket(old, new):
    """Report lines for one changed ticket."""
    lines = []
    for f in SHORT_FIELDS:
        if old.get(f, "") != new[f]:
            lines.append(f"  - {f}: {old.get(f, '') or '(none)'} → {new[f] or '(none)'}")
    if old.get("description", "") != new["description"]:
        lines.append("  - description changed")
    old_c = set(split_comments(old.get("comments", "")))
    added = [c for c in split_comments(new["comments"]) if c not in old_c]
    removed = len(old_c - set(split_comments(new["comments"])))
    for c in added:
        lines.append(f"  - new comment: {one_line(c)}")
    if removed:
        lines.append(f"  - {removed} comment(s) edited or removed")
    if old.get("parent_summary", "") != new["parent_summary"] and old.get("parent", "") == new["parent"]:
        lines.append("  - parent summary changed")
    return lines


def ingest(args):
    snap_date = args.date or date.today().isoformat()
    os.makedirs(args.dir, exist_ok=True)
    if not args.date:
        # A second export on the same day gets a sequence suffix: 2026-11-11-2.
        base, n = snap_date, 1
        while os.path.exists(os.path.join(args.dir, f"{snap_date}.csv")):
            n += 1
            snap_date = f"{base}-{n}"
    if os.path.exists(os.path.join(args.dir, f"{snap_date}.csv")):
        sys.exit(f"A snapshot for {snap_date} already exists in {args.dir}; not overwriting.")
    prior = snapshot_dates(args.dir)
    if prior and snap_order(prior[-1]) > snap_order(snap_date):
        sys.exit(f"The latest snapshot ({prior[-1]}) is newer than {snap_date}.")

    header, rows = read_export(args.export)
    if "Issue key" not in header:
        sys.exit("No 'Issue key' column: is this a Jira CSV export?")
    tickets = slim(header, rows, build_names(header, rows))
    state, present, _ = load_state(args.dir)
    baseline = present is None

    new_keys, changed, kept = [], [], []
    for key in sorted(tickets, key=key_order):
        t = tickets[key]
        old = state.get(key)
        if old is None:
            new_keys.append(key)
            kept.append(t)
        elif any(old.get(f, "") != t[f] for f in COMPARED):
            changed.append((key, diff_ticket(old, t)))
            kept.append(t)
    gone = sorted((present or set()) - set(tickets), key=key_order)
    returned = sorted(k for k in tickets if not baseline and k in state and k not in present)

    write_csv(os.path.join(args.dir, f"{snap_date}.csv"), kept)
    with open(os.path.join(args.dir, f"{snap_date}.keys"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(tickets, key=key_order)) + "\n")

    since = f" since {prior[-1]}" if prior else ""
    out = [
        "---",
        f'date: "[[{snap_date[:10]}]]"',
        "tags:",
        "  - ai-generated",
        "---",
        f"Jira snapshot from `{os.path.basename(args.export)}`: {len(tickets)} tickets in the export.",
        "",
    ]
    if baseline:
        out.append(f"**Baseline.** All {len(tickets)} tickets stored. Later snapshots store only what changes.")
    else:
        out.append(f"Changes{since}: {len(new_keys)} first seen, {len(changed)} changed, {len(gone)} gone.")
        if new_keys:
            out += ["", "## First seen", ""]
            out += [f"- {k} {tickets[k]['summary']} ({tickets[k]['status']}, {tickets[k]['assignee'] or 'unassigned'})" for k in new_keys]
        if changed:
            out += ["", "## Changed", ""]
            for k, lines in changed:
                out.append(f"- {k} {tickets[k]['summary']}")
                out += lines
        if gone:
            out += ["", "## Gone (deleted or moved out of the project)", ""]
            out += [f"- {k} {state[k]['summary']}" for k in gone]
        if returned:
            out += ["", "## Back after being gone", ""]
            out += [f"- {k}" for k in returned]
    report = "\n".join(out) + "\n"
    with open(os.path.join(args.dir, f"{snap_date}.md"), "w", encoding="utf-8") as f:
        f.write(report)
    print(report, end="")


def current(args):
    state, present, dates = load_state(args.dir, args.as_of)
    if not dates:
        sys.exit(f"No snapshots in {args.dir}.")
    keys = [k.upper() for k in args.keys] or sorted(state, key=key_order)
    missing = [k for k in keys if k not in state]
    if missing:
        print("Not in any snapshot: " + ", ".join(missing), file=sys.stderr)
    rows = [dict(state[k], gone="yes" if k not in present else "") for k in keys if k in state]
    if args.csv:
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=SLIM_FIELDS + ["gone"])
        w.writeheader()
        w.writerows(rows)
        print(buf.getvalue(), end="")
        return
    print(f"State as of snapshot {dates[-1]}")
    for r in rows:
        flag = " [GONE]" if r["gone"] else ""
        print(f"{r['key']}{flag} | {r['status']} | {r['assignee'] or 'unassigned'} | "
              f"{r['sprints'].split('; ')[-1] if r['sprints'] else '-'} | upd {r['updated']} | {r['summary']}")
        if args.keys:
            for f in ("parent", "labels", "links", "story_points"):
                if r[f]:
                    print(f"    {f}: {r[f]}")
            if r["description"]:
                print("    description: " + one_line(r["description"], 600))
            for c in split_comments(r["comments"]):
                print("    comment: " + one_line(c, 400))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("ingest", help="store a new export as a delta")
    pi.add_argument("export")
    pi.add_argument("--dir", required=True)
    pi.add_argument("--date", help="snapshot date (default today)")
    pc = sub.add_parser("current", help="print the latest state")
    pc.add_argument("keys", nargs="*")
    pc.add_argument("--dir", required=True)
    pc.add_argument("--as-of")
    pc.add_argument("--csv", action="store_true")
    args = p.parse_args(argv)
    {"ingest": ingest, "current": current}[args.cmd](args)


if __name__ == "__main__":
    main()
