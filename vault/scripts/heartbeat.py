#!/usr/bin/env python3
"""List a vault's input notes that still owe something. No AI involved.

Usage (from anywhere):
    python3 heartbeat.py <vault> [--now YYYY-MM-DD] [--config PATH]
    python3 heartbeat.py --check-config [--config PATH]

--check-config prints one line per problem in the config's `heartbeat:`
entries (an unusable entry, a step that isn't a vault workflow, a vault with no
`frontier: folders:` entry inside it) and always exits 0.

Input notes are what a vault takes in day to day: log notes, or daily journal
notes. A vault that uses this has an entry under `heartbeat:` in the layer's
shared/config.yml, keyed by its root folder:

    heartbeat:
      ~/path/to/vault:
        inputs: "YYYY-MM-DD *.md"
        cutoff: 2026-11-10
        steps: [...]          # not read here

Inputs pattern
  YYYY-MM-DD stands for a date, * for any run of characters within a name and
  ? for one character. With no "/", the pattern matches a filename anywhere in
  the vault; with a "/", it matches a path from the vault root. A note's date
  comes from its filename, and a note dated before `cutoff` is never an input.
  When the pattern's filename is only the date (YYYY-MM-DD.md), the inputs are
  daily notes: one is listed only once its day has passed, so today's never is.

Skipped folders
  wiki/, _AI/, .obsidian/ and templates/ at any depth (and .git/ and .trash/).
  Everything else is searched, including notes tagged ai-generated.

State
  A note's `status:` records what's still owed to it. No status means nothing
  has been done yet. `done` means nothing is owed, and `needs-debrief` has its
  own section. Any other value counts as still owed and is shown as written.

Edited since the last heartbeat
  For a note with a status, the script finds the last commit of it whose
  message starts "heartbeat:" (following renames), and compares the note's body
  (everything below the frontmatter) then with its body now, uncommitted edits
  included. A changed body puts the note back in "To process", whatever its
  status. Frontmatter edits and moves don't count. With no heartbeat commit,
  the comparison is with the first commit in which the note already had a
  status (one set when the note was written, then committed by something
  else). A note with neither can't be checked, so it's listed under "No
  heartbeat commit yet", for the next heartbeat commit to include. Outside a
  git repo, nothing is checked and that section is left out.

Output
    ## Owes a debrief         status needs-debrief, body unchanged
    ## To process             no status, any other status that isn't done, or
                              edited since the last heartbeat (with the reason)
    ## No heartbeat commit yet
  Each line is "- <date> · <path from the vault root>", sorted by date, then
  path. There are no timestamps, so a run with nothing changed prints the same.
"""
import argparse, datetime as dt, os, re, subprocess, sys
from pathlib import Path

from vaultyaml import load_config, parse_yaml, read_note, split_frontmatter

HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG = HERE.parent.parent / "shared" / "config.yml"
WORKFLOWS = HERE.parent / "workflows"
SKIP_DIRS = {"wiki", "_AI", ".obsidian", "templates", ".git", ".trash"}
DATE_TOKEN = "YYYY-MM-DD"
COMMIT_PREFIX = "heartbeat:"
DONE, DEBRIEF = "done", "needs-debrief"


# ---- which notes are inputs ----------------------------------------------------
def entry_problem(entry):
    """What's wrong with a config entry, or None if it's usable."""
    if not isinstance(entry, dict):
        return "the entry isn't a mapping of inputs, cutoff and steps"
    inputs = str(entry.get("inputs") or "").strip()
    if DATE_TOKEN not in inputs:
        return "inputs must be a filename or path pattern containing %s" % DATE_TOKEN
    if not inputs.endswith(".md"):
        return "inputs must end in .md"
    try:
        dt.date.fromisoformat(str(entry.get("cutoff") or "")[:10])
    except ValueError:
        return "cutoff must be a date, YYYY-MM-DD"
    return None


class Inputs:
    """A config entry, compiled."""

    def __init__(self, entry):
        problem = entry_problem(entry)
        if problem:
            raise ValueError(problem)
        pattern = str(entry["inputs"]).strip().lstrip("/")
        self.by_path = "/" in pattern
        self.daily = pattern.rsplit("/", 1)[-1] == DATE_TOKEN + ".md"
        self.cutoff = str(entry["cutoff"])[:10]
        self.regex = compile_pattern(pattern)

    def date_of(self, rel):
        """The note's date if the path (relative to the vault root) is an input, else None."""
        parts = rel.split("/")
        if any(d in SKIP_DIRS for d in parts[:-1]):
            return None
        m = self.regex.match(rel if self.by_path else parts[-1])
        if not m:
            return None
        try:
            dt.date.fromisoformat(m.group(1))
        except ValueError:
            return None
        return m.group(1) if m.group(1) >= self.cutoff else None


def compile_pattern(pattern):
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith(DATE_TOKEN, i):
            out += r"(\d{4}-\d{2}-\d{2})" if "(" not in out else r"\d{4}-\d{2}-\d{2}"
            i += len(DATE_TOKEN)
            continue
        c = pattern[i]
        out += "[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c)
        i += 1
    return re.compile(out + r"\Z")


def relative(vault_root, path):
    try:
        return Path(path).resolve().relative_to(Path(vault_root).resolve()).as_posix()
    except ValueError:
        return None


def is_input(vault_root, path, entry):
    """True if the note at path is one of the vault's input notes under this config entry."""
    rel = relative(vault_root, path)
    return rel is not None and Inputs(entry).date_of(rel) is not None


def config_entry_for(vault_root, config):
    """The `heartbeat:` entry for this vault, or None if the config has none."""
    section = (config or {}).get("heartbeat")
    if not isinstance(section, dict):
        return None
    root = Path(vault_root).expanduser().resolve()
    for key, entry in section.items():
        if Path(str(key)).expanduser().resolve() == root:
            return entry if entry is not None else {}
    return None


# ---- what each note owes -------------------------------------------------------
class History:
    """The vault's git history, if it has one."""

    def __init__(self, root):
        try:
            self.top = Path(self.git(root, "rev-parse", "--show-toplevel").strip()).resolve()
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            self.top = None

    @staticmethod
    def git(cwd, *args):
        return subprocess.run(["git", "-c", "core.quotepath=off", "-C", str(cwd), *args],
                              capture_output=True, text=True, encoding="utf-8", errors="replace",
                              check=True).stdout

    def baseline_body(self, path):
        """The note's body as last swept, or None if no commit records it.

        That's its body at the last heartbeat commit of it. A note that never had
        one (its status was set elsewhere and committed by something else) is
        compared with its body at the first commit that already had a status.
        """
        rel = path.resolve().relative_to(self.top).as_posix()
        try:
            log = self.git(self.top, "log", "--follow", "--format=%x01%H%x09%s", "--name-only", "--", rel)
        except subprocess.CalledProcessError:
            return None
        commits = []  # (commit, subject, path at that commit), newest first
        for record in log.split("\x01")[1:]:
            head, _, names = record.partition("\n")
            commit, _, subject = head.partition("\t")
            name = next((n for n in names.splitlines() if n.strip()), None)
            if name:
                commits.append((commit, subject, name))
        for commit, subject, name in commits:
            if subject.startswith(COMMIT_PREFIX):
                return self.body_at(commit, name)[1]
        for commit, _, name in reversed(commits):
            fm, body = self.body_at(commit, name)
            if str(fm.get("status") or "").strip():
                return body
        return None

    def body_at(self, commit, name):
        """(frontmatter, body) of a file at a commit; ({}, "") if it can't be read."""
        try:
            raw, body = split_frontmatter(self.git(self.top, "show", "%s:%s" % (commit, name)))
        except subprocess.CalledProcessError:
            return {}, ""
        return (parse_yaml(raw) if raw is not None else {}), body


def same_body(a, b):
    return a.replace("\r\n", "\n").strip() == b.replace("\r\n", "\n").strip()


def sweep(root, inputs, today, history):
    """The three lists, each of (date, path, reason)."""
    debrief, process, uncommitted = [], [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for f in sorted(filenames):
            p = Path(dirpath) / f
            rel = p.relative_to(root).as_posix()
            date = inputs.date_of(rel)
            if date is None or (inputs.daily and date >= today):
                continue
            try:
                fm, body = read_note(p)
            except OSError:
                continue
            status = str(fm.get("status") or "").strip()
            if status and history.top:
                then = history.baseline_body(p)
                if then is None:
                    uncommitted.append((date, rel, None))
                elif not same_body(then, body):
                    process.append((date, rel, "edited since last heartbeat"))
                    continue
            if not status:
                process.append((date, rel, "no status"))
            elif status.lower() == DEBRIEF:
                debrief.append((date, rel, None))
            elif status.lower() != DONE:
                process.append((date, rel, status))
    return sorted(debrief), sorted(process), sorted(uncommitted)


def render(debrief, process, uncommitted, git):
    out = []
    sections = [("Owes a debrief", debrief), ("To process", process)]
    if git:
        sections.append(("No heartbeat commit yet", uncommitted))
    for title, rows in sections:
        out += ["## " + title, ""]
        out += ["- " + " · ".join(x for x in row if x) for row in rows] or ["Nothing here."]
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


# ---- config check --------------------------------------------------------------
def config_problems(config, workflows=WORKFLOWS):
    """One line per problem in the config's heartbeat: entries."""
    section = (config or {}).get("heartbeat")
    if section is None:
        return []
    if not isinstance(section, dict):
        return ["heartbeat: should map each vault's root to its entry"]
    known = {p.stem for p in Path(workflows).glob("*.md")}
    frontier = (config or {}).get("frontier")
    folders = frontier.get("folders") if isinstance(frontier, dict) else None
    folders = [Path(str(f)).expanduser().resolve() for f in (folders if isinstance(folders, list) else [folders] if folders else [])]
    out = []
    for key in sorted(section, key=str):
        entry = section[key] if section[key] is not None else {}
        root = Path(str(key)).expanduser().resolve()
        problem = entry_problem(entry)
        if problem:
            out.append("heartbeat: %s: %s" % (key, problem))
        if isinstance(entry, dict):
            steps = entry.get("steps")
            for step in steps if isinstance(steps, list) else [steps] if steps else []:
                if str(step) not in known:
                    out.append("heartbeat: %s: step '%s' isn't a vault workflow" % (key, step))
        if not any(f == root or root in f.parents for f in folders):
            out.append("heartbeat: %s: no frontier: folders: entry inside this vault, so its tasks reach no NEXT.md" % key)
    return out


# ---- main ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("vault", nargs="?", help="the vault's root folder")
    ap.add_argument("--now", help="pretend today is this date, YYYY-MM-DD (for testing)")
    ap.add_argument("--check-config", action="store_true", help="report problems in the heartbeat: config entries")
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.check_config:
        for line in config_problems(load_config(a.config)):
            print(line)
        return
    if not a.vault:
        ap.error("give the vault's root folder")
    today = (a.now or dt.date.today().isoformat())[:10]
    root = Path(a.vault).expanduser().resolve()
    if not root.is_dir():
        sys.exit("heartbeat: %s is not a folder" % a.vault)
    config = load_config(a.config)
    if config is None:
        sys.exit("heartbeat: no config at %s to read heartbeat: from" % a.config)
    entry = config_entry_for(root, config)
    if entry is None:
        sys.exit("heartbeat: no heartbeat: entry for %s in %s" % (root, a.config))
    problem = entry_problem(entry)
    if problem:
        sys.exit("heartbeat: the heartbeat: entry for %s in %s: %s" % (root, a.config, problem))
    history = History(root)
    lists = sweep(root, Inputs(entry), today, history)
    sys.stdout.write(render(*lists, git=history.top is not None))


if __name__ == "__main__":
    main()
