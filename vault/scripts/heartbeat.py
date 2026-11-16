#!/usr/bin/env python3
"""Do the mechanical parts of a vault's heartbeat: list what's owed, stamp notes, commit. No AI involved.

Usage (from anywhere):
    python3 heartbeat.py <vault> [--now YYYY-MM-DD] [--config PATH]
    python3 heartbeat.py mark <vault> <note>... [--config PATH]
    python3 heartbeat.py migrate <vault> [--apply] [--config PATH]
    python3 heartbeat.py finish <vault> --swept <note>... [--files <file>...] [--config PATH]
    python3 heartbeat.py --check-config [--config PATH]

Input notes are what a vault takes in day to day: log notes, or daily journal
notes. A vault that uses this has an entry under `heartbeat:` in the layer's
shared/config.yml, keyed by its root folder:

    heartbeat:
      ~/path/to/vault:
        inputs: "YYYY-MM-DD *.md"
        cutoff: 2026-11-10
        steps: [propagate, sweep-tasks]

A step is `propagate` (heartbeat's own) or the name of a vault workflow. It
can't be `minute`: that's a shortcut that runs heartbeat on one note.

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

Swept
  `swept: <hash>` in a note's frontmatter says heartbeat has looked at the note
  as it stands: the hash is the first 12 hex digits of the sha256 of its body
  (everything below the frontmatter), with CRLF read as LF, leading and trailing
  whitespace ignored, and every wikilink, embed and relative markdown link target
  reduced to its last path segment ([[a/b/c#h|x]] reads as [[c#h|x]]). So moving
  a note, and the link rewrites a move causes, leave it swept; editing its body,
  ticking a task included, doesn't. Only `mark`, `migrate` and `finish` write it.

Status
  `status:` holds only what's still owed once a note is swept: `needs-debrief`.
  A note is listed under
    Owes a debrief   status needs-debrief and a matching stamp
    To process       no stamp ("new"), a stamp that doesn't match its body, or
                     any status other than needs-debrief (shown as written)

Listing output
  First the vault's steps and any problems in its config entry, then the two
  lists, one line per note: "- <date> · <path from the vault root> · <why>".
  Then each note to process in full, its changed lines marked "+" (added) and
  "-" (removed) against the version last swept, which is found by walking the
  note's git history (following renames) for a body matching its stamp. The
  change is labelled `tasks ticked` when every changed line differs only in a
  checkbox, otherwise `content`, or `edited` when no swept version can be found.
  A note over 80 lines shows only its changes, with 3 lines around each (or
  its first 40 lines when there's nothing to compare with).
  Each note also gets its home (the nearest folder above it holding radar/ or
  _wayfinder/) and its linked surfaces: radar items, _wayfinder/ notes,
  _greenhouse/ entries and questions/ notes it links to or that link to it.
  Links resolve by path suffix, preferring the match nearest the linking note.
  Then each home once: its open radar items (with `latest:`) and wayfinder maps.
  Notes and surfaces with uncommitted changes are flagged `uncommitted`, and
  every other uncommitted file in the vault (bar NEXT.md) is listed at the end.
  Sorted by date, then path, with no timestamps, so a run with nothing changed
  prints the same. Outside a git repo the change marks are left out and the
  output says so.

mark
  Stamps each named input note (a path from the vault root, or any path to it).

migrate
  The one-off move to stamps. Lists the input notes whose status is `done`
  (stamped, status removed), `needs-debrief` with no stamp (stamped, status
  kept) or `unprocessed` (status removed); --apply makes the changes.

finish
  Stamps the --swept notes, rebuilds NEXT.md with frontier.py (next to this
  script), then, in a git repo, stages by name the --swept notes, the --files
  and every NEXT.md inside the vault that's now changed, and commits only those
  as "heartbeat: N notes, M files". Hooks run; if one blocks the commit, the
  files are left staged and the exit status is 1. With nothing to commit, there
  is no commit.

--check-config prints one line per problem in the config's `heartbeat:`
entries (an unusable entry, a step that isn't `propagate` or a vault workflow,
a vault with no `frontier: folders:` entry inside it) and always exits 0.
"""
import argparse, datetime as dt, difflib, hashlib, os, re, subprocess, sys
from pathlib import Path
from urllib.parse import unquote

from vaultyaml import load_config, radar_item, radar_open, read_note, set_field, split_frontmatter

HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG = HERE.parent.parent / "shared" / "config.yml"
WORKFLOWS = HERE.parent / "workflows"
FRONTIER = HERE / "frontier.py"
SKIP_DIRS = {"wiki", "_AI", ".obsidian", "templates", ".git", ".trash"}
DATE_TOKEN = "YYYY-MM-DD"
COMMIT_PREFIX = "heartbeat:"
OWN_STEP = "propagate"  # heartbeat's own step; every other step is a vault workflow
SHORTCUT = "minute"  # runs heartbeat on one note, so it can't be one of heartbeat's steps
STAMP, DEBRIEF = "swept", "needs-debrief"
LONG, CONTEXT, HEAD = 80, 3, 40  # a note over LONG lines shows only its changes
HISTORY_DEPTH = 100  # commits of a note searched for its swept version
SURFACES = {"radar": "radar", "_wayfinder": "wayfinder", "_greenhouse": "greenhouse", "questions": "question"}
HOME_MARKERS = ("radar", "_wayfinder")


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


def vault_files(root):
    """Every .md file in the vault outside the skipped folders, as paths from the root, sorted."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        rel_dir = Path(dirpath).relative_to(root).as_posix()
        for f in sorted(filenames):
            if f.endswith(".md"):
                out.append(f if rel_dir == "." else rel_dir + "/" + f)
    return out


# ---- the swept stamp -----------------------------------------------------------
WIKILINK = re.compile(r"(!?\[\[)([^\]|#\n]*)")
MDLINK = re.compile(r"(\]\()(<[^>\n]*>|[^)\s]+)")
SCHEME = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*:")
CHECKBOX = re.compile(r"^(\s*(?:[-*+]|\d+[.)])\s+\[).(\])")


def last_segment(path):
    return path.rsplit("/", 1)[-1]


def _md_link(m):
    target = m.group(2)
    angle = target.startswith("<")
    inner = target[1:-1] if angle else target
    if not inner or inner.startswith("#") or SCHEME.match(inner):
        return m.group(0)
    path, hash_, frag = inner.partition("#")
    inner = last_segment(path) + hash_ + frag
    return m.group(1) + ("<%s>" % inner if angle else inner)


def reduce_links(text):
    """Every link target cut to its last path segment, so a move's link rewrites read as no change."""
    text = WIKILINK.sub(lambda m: m.group(1) + last_segment(m.group(2)), text)
    return MDLINK.sub(_md_link, text)


def body_lines(body):
    body = body.replace("\r\n", "\n").strip()
    return body.split("\n") if body else []


def body_hash(body):
    """The stamp for a note body: see "Swept" above."""
    normalised = reduce_links("\n".join(body_lines(body)))
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()[:12]


def stamp_of(fm):
    return str(fm.get(STAMP) or "").strip()


# ---- git, when there is one ----------------------------------------------------
class Git:
    """The vault's git repo; .top is None when there isn't one."""

    def __init__(self, root):
        try:
            self.top = Path(self.run("rev-parse", "--show-toplevel", cwd=root).stdout.strip()).resolve()
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            self.top = None

    def run(self, *args, cwd=None, check=True):
        return subprocess.run(["git", "-c", "core.quotepath=off", "-C", str(cwd or self.top), *args],
                              capture_output=True, text=True, encoding="utf-8", errors="replace", check=check)

    def dirty(self):
        """Absolute paths of every file with uncommitted changes, untracked included."""
        out = self.run("status", "--porcelain", "-z", "--untracked-files=all").stdout.split("\0")
        paths, i = set(), 0
        while i < len(out):
            entry = out[i]
            i += 1
            if len(entry) < 4:
                continue
            paths.add((self.top / entry[3:]).resolve())
            if entry[0] in "RC":
                i += 1  # the rename's old path; nothing's there now
        return paths

    def swept_body(self, path, stamp):
        """The note's body at its newest commit whose body matches the stamp, or None."""
        rel = path.resolve().relative_to(self.top).as_posix()
        try:
            log = self.run("log", "--follow", "-n", str(HISTORY_DEPTH), "--format=%x01%H", "--name-only",
                           "--", rel).stdout
        except subprocess.CalledProcessError:
            return None
        for record in log.split("\x01")[1:]:
            commit, _, names = record.partition("\n")
            name = next((n for n in names.splitlines() if n.strip()), None)
            if not name:
                continue
            shown = self.run("show", "%s:%s" % (commit.strip(), name), check=False)
            if shown.returncode == 0:
                body = split_frontmatter(shown.stdout)[1]
                if body_hash(body) == stamp:
                    return body
        return None


# ---- what each note owes -------------------------------------------------------
class Note:
    def __init__(self, date, rel, path, fm, body):
        self.date, self.rel, self.path, self.fm, self.body = date, rel, path, fm, body
        self.status = str(fm.get("status") or "").strip()
        self.stamp = stamp_of(fm)
        self.swept = self.stamp == body_hash(body)
        self.rows, self.label = None, None  # set for a listed note: what to show, and why

    def owes(self):
        """'debrief', 'process' or None."""
        if self.swept and self.status.lower() == DEBRIEF:
            return "debrief"
        if self.swept and not self.status:
            return None
        return "process"


def input_notes(root, inputs, today, files):
    notes = []
    for rel in files:
        date = inputs.date_of(rel)
        if date is None or (inputs.daily and date >= today):
            continue
        p = root / rel
        try:
            fm, body = read_note(p)
        except OSError:
            continue
        notes.append(Note(date, rel, p, fm, body))
    return sorted(notes, key=lambda n: (n.date, n.rel))


def untick(line):
    return CHECKBOX.sub(r"\1 \2", line)


def compare(old_body, new_body):
    """(rows, label): every line of the new body marked ' ', '+' or '-' against the old one."""
    old, new = body_lines(old_body), body_lines(new_body)
    sm = difflib.SequenceMatcher(None, [reduce_links(l) for l in old], [reduce_links(l) for l in new],
                                 autojunk=False)
    rows, changed, ticks_only = [], False, True
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            rows += [(" ", l) for l in new[j1:j2]]
            continue
        changed = True
        if tag != "replace" or i2 - i1 != j2 - j1 or any(
                reduce_links(untick(a)) != reduce_links(untick(b)) for a, b in zip(old[i1:i2], new[j1:j2])):
            ticks_only = False
        rows += [("-", l) for l in old[i1:i2]] + [("+", l) for l in new[j1:j2]]
    return rows, "tasks ticked" if changed and ticks_only else "content"


def explain(note, git):
    """Fill in what to show for a listed note, and its label."""
    if note.stamp and not note.swept:
        old = git.swept_body(note.path, note.stamp) if git.top else None
        if old is not None:
            note.rows, note.label = compare(old, note.body)
            return
        note.label = "edited"
    else:
        note.label = "new" if not note.status else None
    note.rows = [(" ", l) for l in body_lines(note.body)]


def why(note):
    return " · ".join(x for x in (note.label, note.status) if x)


# ---- candidate surfaces --------------------------------------------------------
def surface_kind(rel):
    for part in reversed(rel.split("/")[:-1]):
        if part in SURFACES:
            return SURFACES[part]
    return None


def link_targets(text):
    """Every wikilink, embed and relative markdown link target in the text, without #heading or |alias."""
    for m in WIKILINK.finditer(text):
        if m.group(2).strip():
            yield m.group(2).strip()
    for m in MDLINK.finditer(text):
        target = m.group(2)
        target = target[1:-1] if target.startswith("<") else target
        if target and not target.startswith("#") and not SCHEME.match(target):
            path = unquote(target.partition("#")[0])
            if path:
                yield path


class Links:
    """Resolves link targets against the vault's notes by path suffix."""

    def __init__(self, files):
        self.by_name = {}
        for rel in files:
            self.by_name.setdefault(last_segment(rel)[:-3].lower(), []).append(rel)

    def resolve(self, target, source):
        parts = [p for p in target.split("/") if p not in ("", ".", "..")]
        if not parts:
            return None
        if parts[-1].lower().endswith(".md"):
            parts[-1] = parts[-1][:-3]
        suffix = "/".join(parts).lower()
        found = [r for r in self.by_name.get(parts[-1].lower(), [])
                 if r[:-3].lower() == suffix or r[:-3].lower().endswith("/" + suffix)]
        if len(found) > 1:  # nearest to the linking note wins, as in Obsidian
            def shared(r):
                n = 0
                for a, b in zip(r.split("/")[:-1], source.split("/")[:-1]):
                    if a != b:
                        break
                    n += 1
                return n
            best = max(shared(r) for r in found)
            found = [r for r in found if shared(r) == best]
        return found[0] if len(found) == 1 else None


def home_of(root, rel):
    """The nearest folder above the note holding radar/ or _wayfinder/, as a path from the root ("" for the root)."""
    parts = rel.split("/")[:-1]
    for k in range(len(parts), -1, -1):
        d = root.joinpath(*parts[:k])
        if any((d / m).is_dir() for m in HOME_MARKERS):
            return "/".join(parts[:k])
    return None


def read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def linked_surfaces(root, notes, files):
    """{note rel: sorted surface rels it links to or that link to it}."""
    links = Links(files)
    surfaces = {r for r in files if surface_kind(r)}
    listed = {n.rel for n in notes}
    out = {n.rel: set() for n in notes}
    for n in notes:
        for t in link_targets(n.body):
            r = links.resolve(t, n.rel)
            if r in surfaces and r != n.rel:
                out[n.rel].add(r)
    for s in sorted(surfaces):
        for t in link_targets(read_text(root / s)):
            r = links.resolve(t, s)
            if r in listed and r != s:
                out[r].add(s)
    return {k: sorted(v) for k, v in out.items()}


def home_surfaces(root, home):
    """(kind, rel, latest) for the home's open radar items and its wayfinder maps."""
    base = root / home if home else root
    out = []
    for p in sorted((base / "radar").glob("*.md")):
        item = radar_item(p)
        if radar_open(item):
            out.append(("radar", p.relative_to(root).as_posix(), item["latest"]))
    for p in sorted((base / "_wayfinder").glob("*/map.md")):
        out.append(("wayfinder", p.relative_to(root).as_posix(), None))
    return out


# ---- listing -------------------------------------------------------------------
def shown_rows(rows, compared):
    """The rows to print, and a note on what was left out, if anything."""
    length = sum(1 for m, _ in rows if m != "-")
    if length <= LONG:
        return rows, None
    changed = [i for i, (m, _) in enumerate(rows) if m != " "]
    if not compared or not changed:
        return rows[:HEAD], "Long note (%d lines): showing the first %d." % (length, HEAD)
    keep = sorted({j for i in changed for j in range(i - CONTEXT, i + CONTEXT + 1) if 0 <= j < len(rows)})
    out, last = [], -1
    for j in keep:
        if j != last + 1:
            out.append((" ", "…"))
        out.append(rows[j])
        last = j
    if last != len(rows) - 1:
        out.append((" ", "…"))
    return out, "Long note (%d lines): showing the changed lines with %d lines around them." % (length, CONTEXT)


def render(root, entry, problems, notes, git, dirty, files):
    flagged = set()

    def flag(rel):
        flagged.add(rel)
        return " · uncommitted" if (root / rel).resolve() in dirty else ""

    steps = entry.get("steps")
    steps = steps if isinstance(steps, list) else [steps] if steps else []
    out = ["Steps: " + (", ".join(str(s) for s in steps) or "none set")]
    out += ["Config: " + p for p in problems]
    if not git.top:
        out.append("Git: not a git repo, so changed lines aren't marked and finish won't commit.")
    out.append("")
    debrief = [n for n in notes if n.owes() == "debrief"]
    process = [n for n in notes if n.owes() == "process"]
    for title, rows, reason in (("Owes a debrief", debrief, None), ("To process", process, why)):
        out += ["## " + title, ""]
        out += ["- %s · %s%s%s" % (n.date, n.rel, (" · " + reason(n)) if reason and reason(n) else "", flag(n.rel))
                for n in rows] or ["Nothing here."]
        out.append("")
    if not process:
        return "\n".join(out).rstrip("\n") + "\n"
    linked = linked_surfaces(root, process, files)
    homes = {}
    for n in process:
        home = home_of(root, n.rel)
        out += ["### %s · %s%s%s" % (n.date, n.rel, (" · " + why(n)) if why(n) else "", flag(n.rel)), ""]
        if n.fm.get("tags") and "ai-generated" in (n.fm["tags"] if isinstance(n.fm["tags"], list) else [n.fm["tags"]]):
            out.append("Tagged ai-generated: written by a past session, not by the owner.")
        if home is not None:
            homes.setdefault(home, None)
            out.append("Home: " + (home or "(vault root)"))
        if linked[n.rel]:
            out.append("Linked:")
            out += ["- %s · %s%s" % (surface_kind(s), s, flag(s)) for s in linked[n.rel]]
        rows, cut = shown_rows(n.rows, n.label in ("content", "tasks ticked"))
        if cut:
            out.append(cut)
        if out[-1] != "":
            out.append("")
        out += [("%s %s" % (m, l)).rstrip() for m, l in rows] or ["(empty)"]
        out.append("")
    for home in sorted(homes):
        out += ["## Home: " + (home or "(vault root)"), ""]
        items = home_surfaces(root, home)
        out += ["- %s · %s%s%s" % (kind, rel, (" · " + latest) if latest else "", flag(rel))
                for kind, rel, latest in items] or ["No open radar items or wayfinder maps."]
        out.append("")
    elsewhere = sorted(r for r in (relative(root, p) for p in dirty)
                       if r and r not in flagged and last_segment(r) != "NEXT.md")
    if elsewhere:
        out += ["## Uncommitted elsewhere", ""] + ["- " + r for r in elsewhere]
    return "\n".join(out).rstrip("\n") + "\n"


# ---- config check --------------------------------------------------------------
def config_problems(config, workflows=WORKFLOWS, vault=None):
    """One line per problem in the config's heartbeat: entries (only this vault's, if one is given)."""
    section = (config or {}).get("heartbeat")
    if section is None:
        return []
    if not isinstance(section, dict):
        return ["heartbeat: should map each vault's root to its entry"]
    known = {p.stem for p in Path(workflows).glob("*.md")} - {SHORTCUT} | {OWN_STEP}
    frontier = (config or {}).get("frontier")
    folders = frontier.get("folders") if isinstance(frontier, dict) else None
    folders = [Path(str(f)).expanduser().resolve() for f in (folders if isinstance(folders, list) else [folders] if folders else [])]
    out = []
    for key in sorted(section, key=str):
        entry = section[key] if section[key] is not None else {}
        root = Path(str(key)).expanduser().resolve()
        if vault is not None and root != Path(vault).resolve():
            continue
        problem = entry_problem(entry)
        if problem:
            out.append("heartbeat: %s: %s" % (key, problem))
        if isinstance(entry, dict):
            steps = entry.get("steps")
            for step in steps if isinstance(steps, list) else [steps] if steps else []:
                if str(step) == SHORTCUT:
                    out.append("heartbeat: %s: step '%s' is a shortcut that runs heartbeat, so it can't be one of "
                               "heartbeat's steps (use %s)" % (key, step, OWN_STEP))
                elif str(step) not in known:
                    out.append("heartbeat: %s: step '%s' isn't a vault workflow" % (key, step))
        if not any(f == root or root in f.parents for f in folders):
            out.append("heartbeat: %s: no frontier: folders: entry inside this vault, so its tasks reach no NEXT.md" % key)
    return out


# ---- writing stamps ------------------------------------------------------------
def write_field(path, key, value):
    text = path.read_text(encoding="utf-8")
    new = set_field(text, key, value)
    if new != text:
        path.write_text(new, encoding="utf-8")


def stamp(path):
    """Stamp a note as swept; returns the stamp."""
    h = body_hash(read_note(path)[1])
    write_field(path, STAMP, h)
    return h


def find_file(root, name):
    """A path named on the command line: from the vault root, or as given."""
    p = Path(name).expanduser()
    for candidate in ([p] if p.is_absolute() else [root / p, Path.cwd() / p]):
        if candidate.exists() and relative(root, candidate) is not None:
            return candidate.resolve()
    return None


def input_paths(root, entry, names):
    """The named notes as paths, or exit naming every one that isn't one of the vault's input notes."""
    inputs, paths, bad = Inputs(entry), [], []
    for name in names:
        p = find_file(root, name)
        if p is None or not p.is_file():
            bad.append("%s: no such file in the vault" % name)
        elif inputs.date_of(relative(root, p)) is None:
            bad.append("%s: not one of the vault's input notes" % name)
        else:
            paths.append(p)
    if bad:
        sys.exit("heartbeat: nothing done.\n" + "\n".join("- " + b for b in bad))
    return sorted(set(paths))


def mark(root, entry, names):
    for p in input_paths(root, entry, names):
        print("- %s · swept: %s" % (relative(root, p), stamp(p)))


def migrate(root, entry, apply):
    inputs, changes = Inputs(entry), []
    for rel in vault_files(root):
        if inputs.date_of(rel) is None:
            continue
        fm, body = read_note(root / rel)
        status = str(fm.get("status") or "").strip().lower()
        swept = stamp_of(fm) == body_hash(body)
        if status == "done":
            changes.append((rel, "status: done → stamp it, remove status", True, None))
        elif status == DEBRIEF and not swept:
            changes.append((rel, "status: needs-debrief → stamp it, keep status", True, "keep"))
        elif status == "unprocessed":
            changes.append((rel, "status: unprocessed → remove status", False, None))
    for rel, what, stamps, keep in changes:
        print("- %s · %s" % (rel, what))
        if apply:
            p = root / rel
            if stamps:
                stamp(p)
            if keep is None:
                write_field(p, "status", None)
    if not changes:
        print("Nothing to migrate.")
    elif apply:
        print("Changed %d note%s." % (len(changes), "" if len(changes) == 1 else "s"))
    else:
        print("%d note%s to change. Run again with --apply to change them." % (len(changes), "" if len(changes) == 1 else "s"))


def plural(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


def finish(root, entry, config_path, swept, files):
    notes = input_paths(root, entry, swept)
    others = []
    for name in files:
        p = find_file(root, name)
        if p is None and not Path(name).is_absolute():
            p = (root / name).resolve()  # a deleted file still gets staged
        if p is None or relative(root, p) is None:
            sys.exit("heartbeat: nothing done. %s isn't in the vault." % name)
        others.append(p)
    for p in notes:
        print("- %s · swept: %s" % (relative(root, p), stamp(p)))
    r = subprocess.run([sys.executable, str(FRONTIER), "--vault", str(root), "--config", str(config_path)],
                       capture_output=True, text=True, encoding="utf-8")
    ok = r.returncode == 0
    print("NEXT.md rebuilt." if ok else "frontier.py failed:\n" + r.stderr.strip())
    git = Git(root)
    if not git.top:
        print("Not a git repo, so no commit.")
        return 0 if ok else 1
    nexts = sorted(p for p in git.dirty() if p.name == "NEXT.md" and relative(root, p) is not None)
    paths = []
    for p in notes + others + nexts:
        if p not in paths and (p.exists() or git.run("ls-files", "--", str(p)).stdout.strip()):
            paths.append(p)
    if not paths:
        print("Nothing to commit.")
        return 0 if ok else 1
    names = [str(p) for p in paths]
    add = git.run("add", "--", *names, check=False)
    if add.returncode:
        print("git add failed, so no commit:\n" + (add.stderr or add.stdout).strip())
        return 1
    staged = [n for n in git.run("diff", "--cached", "--name-only", "-z", "--", *names).stdout.split("\0") if n]
    if not staged:
        print("Nothing to commit.")
        return 0 if ok else 1
    message = "%s %s, %s" % (COMMIT_PREFIX, plural(len(notes), "note"), plural(len(staged), "file"))
    c = git.run("commit", "-q", "-m", message, "--", *names, check=False)
    if c.returncode:
        print("The commit was blocked, so the files are left staged:\n" + (c.stderr + c.stdout).strip())
        return 1
    print("Committed: " + message)
    return 0 if ok else 1


# ---- main ----------------------------------------------------------------------
def vault_entry(vault, config_path):
    """(root, config, entry), or exit saying what's missing."""
    root = Path(vault).expanduser().resolve()
    if not root.is_dir():
        sys.exit("heartbeat: %s is not a folder" % vault)
    config = load_config(config_path)
    if config is None:
        sys.exit("heartbeat: no config at %s to read heartbeat: from" % config_path)
    entry = config_entry_for(root, config)
    if entry is None:
        sys.exit("heartbeat: no heartbeat: entry for %s in %s" % (root, config_path))
    problem = entry_problem(entry)
    if problem:
        sys.exit("heartbeat: the heartbeat: entry for %s in %s: %s" % (root, config_path, problem))
    return root, config, entry


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    summary = __doc__.split("\n\n")[0]
    if argv and argv[0] in ("mark", "migrate", "finish"):
        ap = argparse.ArgumentParser(prog="heartbeat.py " + argv[0], description=summary)
        ap.add_argument("vault", help="the vault's root folder")
        ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help=argparse.SUPPRESS)
        if argv[0] == "mark":
            ap.add_argument("notes", nargs="+", help="input notes to stamp as swept")
        elif argv[0] == "migrate":
            ap.add_argument("--apply", action="store_true", help="make the changes, not just list them")
        else:
            ap.add_argument("--swept", nargs="+", default=[], help="input notes to stamp as swept")
            ap.add_argument("--files", nargs="+", default=[], help="other files to commit")
        a = ap.parse_args(argv[1:])
        root, _, entry = vault_entry(a.vault, a.config)
        if argv[0] == "mark":
            mark(root, entry, a.notes)
        elif argv[0] == "migrate":
            migrate(root, entry, a.apply)
        else:
            sys.exit(finish(root, entry, a.config, a.swept, a.files))
        return
    ap = argparse.ArgumentParser(description=summary)
    ap.add_argument("vault", nargs="?", help="the vault's root folder")
    ap.add_argument("--now", help="pretend today is this date, YYYY-MM-DD (for testing)")
    ap.add_argument("--check-config", action="store_true", help="report problems in the heartbeat: config entries")
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if a.check_config:
        for line in config_problems(load_config(a.config)):
            print(line)
        return
    if not a.vault:
        ap.error("give the vault's root folder")
    today = (a.now or dt.date.today().isoformat())[:10]
    root, config, entry = vault_entry(a.vault, a.config)
    git = Git(root)
    files = vault_files(root)
    notes = input_notes(root, Inputs(entry), today, files)
    for n in notes:
        if n.owes() == "process":
            explain(n, git)
    dirty = git.dirty() if git.top else set()
    sys.stdout.write(render(root, entry, config_problems(config, vault=root), notes, git, dirty, files))


if __name__ == "__main__":
    main()
