#!/usr/bin/env python3
"""List what's yours to do now across a vault folder's threads. No AI involved.

Usage (from anywhere):
    python3 frontier.py [folder] [--now YYYY-MM-DD] [--no-write] [--config PATH]

Reads <folder> as described in ../FRONTIER.md (the convention: how notes
record threads, checklists and tasks), prints the list, and writes it to
<folder>/NEXT.md. With no folder, it does this for every folder listed under
`frontier_folders:` in the layer's shared/config.yml.

The output is stable: no timestamps, dates rather than ages, and every sort
has an explicit tie-break, so a run with nothing changed in the notes leaves
NEXT.md byte-identical (and the file isn't rewritten).

Listing rules (layout and sorting; how notes are written is the convention's):

  Sections
    ## Yours now         live steps, grouped under a bold header per thread,
                         with "Dangling tasks" (tasks with no thread link) last.
    ## Waiting on others one flat list: checklist lines with a waiting word,
                         tasks with `Waiting on:`, and waiting threads (one
                         line each, showing `latest:`).
    ## Needs a look      a live thread with no open step, a `Blocked by:` whose
                         note has no status or doesn't exist, an unrecognised
                         status or slice state, a slice depending on a slice
                         that isn't there.
    Blocked and parked steps are left out. Every line is a plain bullet that
    links to the note it came from, never a checkbox, so the Tasks plugin
    doesn't pick the list up as duplicate tasks.

  Lines
    - [[note|step text]] · reason · untouched since YYYY-MM-DD
    Reasons are "due D" ("overdue, due D" once D is before today) from a 📅
    date, a waypoint's `Due:` or the thread's `due:`, and "expected by
    [[person]]". On a waiting line, "in [[thread]]" names the thread and
    "waiting on [[person]]" the person.

  Sort order
    Within a thread: due date first (earliest first, so overdue at the top),
    then `Expected by:`, then the rest; inside each group the oldest untouched
    first, undated last, then note path and line. Threads are ordered by their
    top step with the same key; Dangling tasks always go last. Waiting on
    others is oldest untouched first, then path. Needs a look is by path.

  Untouched
    waypoint        the latest date on its line, ignoring `Due:`
    checklist line  the last ✅ date in its checklist, else the file's last
                    commit, else none
    task            its note's date (`date:` or a date in the filename), else
                    the file's last commit, else none
    waiting thread  its note's last commit
    Uncommitted edits don't count, so the date only moves with a commit.

  Checklist turn-taking in a work folder
    no slices yet        the ticket's next line
    any slice not merged each open slice's next line (a planned slice whose
                         depends-on aren't all merged is blocked, left out)
    every slice merged   the ticket's next line and the plan's next line
    A waiting thread (its ticket's status means waiting) shows only its one
    waiting line.
"""
import argparse, datetime as dt, os, re, subprocess, sys
from pathlib import Path

try:
    import yaml
except ImportError:  # minimal fallback: flat keys and simple lists
    yaml = None

HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG = HERE.parent.parent / "shared" / "config.yml"
OUTPUT = "NEXT.md"
HEADER = "%% Written by frontier.py from the notes in this folder. Edits here are overwritten: change the source notes instead. %%"

STATUS = {
    "live": {"active", "to do", "in progress", "ready", "open"},
    "waiting": {"waiting", "needs review", "in review", "blocked"},
    "parked": {"inactive", "backlog", "parked", "paused"},
    "done": {"done", "closed", "resolved"},
}
SLICE_STATES = {"planned", "in progress", "pr open", "merged"}
WAITING_WORDS = re.compile(r"\b(PR review OK|QA|Merged)\b")  # as written, case matters
SKIP_DIRS = {"templates", "_AI", ".obsidian", ".git", ".trash"}
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]")
TASK = re.compile(r"^\s*[-*] \[(.)\] (.*)$")
WAYPOINT = re.compile(r"^- \[[ /]\] \*\*(.+?)\*\*(.*)$")
DONE_DATE = re.compile(r"✅\s*(\d{4}-\d{2}-\d{2})")
DUE_EMOJI = re.compile(r"📅\s*(\d{4}-\d{2}-\d{2})")
DUE_WORD = re.compile(r"Due:\s*(\d{4}-\d{2}-\d{2})")
FIELD = re.compile(r"(Expected by|Waiting on|Blocked by):\s*(\[\[[^\]]+\]\])")
TASKS_FIELDS = re.compile(r"[📅⏳🛫➕✅❌]\s*\d{4}-\d{2}-\d{2}|[🆔⛔]\s*\S+|🔁[^📅⏳🛫➕✅❌🆔⛔]*|[⏫🔼🔽🔺⏬]")
FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^#{1,6} ")


# ---- reading -------------------------------------------------------------------
def status_of(word):
    if word is None or str(word).strip() == "":
        return "live"
    w = str(word).strip().lower()
    for meaning, words in STATUS.items():
        if w in words:
            return meaning
    return "unknown"


def parse_yaml(raw):
    if yaml:
        try:
            v = yaml.safe_load(raw)
            return v if isinstance(v, dict) else {}
        except yaml.YAMLError:
            return {}
    out, key = {}, None
    for line in raw.splitlines():
        if line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([\w-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"')
            out[key] = val if val else []
        elif key and re.match(r"^\s+-\s+", line):
            if not isinstance(out[key], list):
                out[key] = []
            out[key].append(re.sub(r"^\s+-\s+", "", line).strip().strip('"'))
    return out


def read_note(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm, body = parse_yaml(text[3:end]), text[end + 4:]
    return fm, body


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def lines_outside_code(body):
    """(line number, line) for every line not inside a fenced code block."""
    fenced = False
    for n, line in enumerate(body.splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            yield n, line


def checkboxes(body):
    """(line number, mark, text) for every checkbox line, in order."""
    for n, line in lines_outside_code(body):
        m = TASK.match(line)
        if m:
            yield n, m.group(1), m.group(2)


def has_category(fm, name):
    return ("[[%s]]" % name) in " ".join(str(c) for c in as_list(fm.get("categories")))


def first_date(s):
    m = DATE.search(str(s or ""))
    return m.group(0) if m else None


# ---- the vault -----------------------------------------------------------------
class Vault:
    """Notes in the folder covered, plus a name index over the whole vault for links."""

    def __init__(self, root, scope):
        self.root, self.scope = root, scope
        self.notes = {}  # path -> (fm, body), read for every note in scope
        self.outside = {}  # path -> fm, read lazily for link targets elsewhere
        self.by_path, self.by_name = {}, {}
        in_scope = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            for f in sorted(filenames):
                if not f.endswith(".md"):
                    continue
                p = Path(dirpath) / f
                if p.parent == scope and f == OUTPUT:
                    continue
                if scope == p.parent or scope in p.parents:
                    in_scope.append(p)
                self.by_path.setdefault(self.rel(p).lower(), p)
        for p in in_scope:
            try:
                self.notes[p] = read_note(p)
            except OSError:
                continue
        # names: notes in scope first, so a clash resolves to the nearer note
        for p in in_scope:
            self.by_name.setdefault(p.stem.lower(), p)
            for a in as_list(self.notes.get(p, ({}, ""))[0].get("aliases")):
                self.by_name.setdefault(str(a).strip().lower(), p)
        for key, p in sorted(self.by_path.items()):
            self.by_name.setdefault(p.stem.lower(), p)
        self.commits = self._commit_dates()

    def rel(self, p):
        return p.relative_to(self.root).with_suffix("").as_posix()

    def fm(self, p):
        if p in self.notes:
            return self.notes[p][0]
        if p not in self.outside:
            try:
                self.outside[p] = read_note(p)[0]
            except OSError:
                self.outside[p] = {}
        return self.outside[p]

    def resolve(self, target):
        t = target.strip().lower()
        if t.endswith(".md"):
            t = t[:-3]
        return self.by_path.get(t) or self.by_name.get(t) or self.by_name.get(t.split("/")[-1])

    def _commit_dates(self):
        """Last commit date per file in scope. Uncommitted edits are ignored."""
        dates = {}
        try:
            top = subprocess.run(["git", "-C", str(self.scope), "rev-parse", "--show-toplevel"],
                                 capture_output=True, text=True, check=True).stdout.strip()
            out = subprocess.run(
                ["git", "-c", "core.quotepath=off", "-C", top, "log", "--format=@%cs", "--name-only",
                 "--", str(self.scope)], capture_output=True, text=True, check=True).stdout
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            return dates
        current = None
        for line in out.splitlines():
            if line.startswith("@"):
                current = line[1:]
            elif line.strip() and current:
                dates.setdefault((Path(top) / line.strip()).resolve(), current)
        return dates

    def committed(self, p):
        return self.commits.get(p.resolve())

    def note_date(self, p):
        return first_date(self.fm(p).get("date")) or first_date(p.stem) or self.committed(p)


# ---- the list being built ------------------------------------------------------
class Thread:
    def __init__(self, key, link, tid, title, fm):
        self.key, self.link, self.id, self.title = key, link, tid, title
        self.high = str(fm.get("priority") or "").strip().lower() == "high"
        self.due = first_date(fm.get("due"))

    def header(self):
        name = "**[[%s|%s]]**" % (self.link, self.id) if self.link else "**%s**" % self.id
        return name + (" " + self.title if self.title else "")


class Frontier:
    def __init__(self, vault, today):
        self.v, self.today = vault, today
        self.threads = {}  # key -> Thread
        self.thread_of = {}  # note path -> thread key, for tasks linking to a thread
        self.yours, self.waiting, self.look = [], [], []
        self.internal = set()  # notes whose checkboxes are never tasks
        self.ended = {}  # thread key -> ended-on date, for projects that have ended

    # -- helpers --
    def excluded(self, p):
        fm = self.v.fm(p)
        return str(fm.get("ignore_tasks")).strip().lower() == "true" or status_of(fm.get("status")) in ("parked", "done")

    def add_thread(self, key, notes, link, tid, title, fm):
        th = self.threads.setdefault(key, Thread(key, link, tid, title, fm))
        for n in notes:
            if n:
                self.thread_of.setdefault(n, key)
        return th

    def step(self, thread, note, line, text, untouched, due=None, expected=None, waiting_on=None, waiting=False):
        s = {"thread": thread, "note": self.v.rel(note), "line": line, "text": display(text),
             "untouched": untouched, "due": due, "expected": expected, "waiting_on": waiting_on}
        (self.waiting if waiting or waiting_on else self.yours).append(s)
        return s

    def needs_look(self, note, line, label, reason):
        self.look.append({"note": self.v.rel(note) if isinstance(note, Path) else note,
                          "line": line, "label": label, "reason": reason})

    def thread_look(self, th, reason, note):
        self.look.append({"note": self.v.rel(note), "line": 0, "label": th.header(), "reason": reason})

    def check_status(self, th, fm, note):
        if status_of(fm.get("status")) == "unknown":
            self.thread_look(th, "status '%s' not recognised" % fm.get("status"), note)

    def waiting_thread(self, th, fm, note):
        latest = str(fm.get("latest") or "").strip() or "status: %s" % fm.get("status")
        self.waiting.append({"thread": None, "whole": th, "note": self.v.rel(note), "line": 0,
                             "latest": " ".join(latest.split()), "untouched": self.v.committed(note)})

    def checklist_step(self, th, note, prefix=""):
        """The first unticked line of a note's checklist, as a step. True if there was one."""
        body = self.v.notes[note][1]
        items = list(checkboxes(body))
        ticked = [d for _, _, t in items for d in DONE_DATE.findall(t)]
        untouched = max(ticked) if ticked else self.v.committed(note)
        for n, mark, text in items:
            if mark in (" ", "/"):
                self.step(th.key, note, n, prefix + text, untouched,
                          waiting=bool(WAITING_WORDS.search(text)))
                return True
        return False

    # -- gather --
    def gather(self):
        self.gather_wayfinders()
        used = self.gather_work_folders()
        self.gather_tickets(used)
        self.gather_projects()
        self.gather_tasks()

    def gather_wayfinders(self):
        for p in sorted(self.v.notes):
            if p.name != "map.md" or p.parent.parent.name != "_wayfinder":
                continue
            fm, body = self.v.notes[p]
            aliases = as_list(fm.get("aliases"))
            th = self.add_thread(("wayfinder", p), [p], self.v.rel(p), p.parent.name,
                                 str(aliases[0]) if aliases else "", fm)
            self.internal.add(p)
            if self.excluded(p):
                continue
            self.check_status(th, fm, p)
            section = None
            for n, line in lines_outside_code(body):
                if HEADING.match(line):
                    words = line.lstrip("#").split()
                    section = words[0].lower() if line.startswith("### ") and words else None
                    continue
                m = WAYPOINT.match(line)
                if not m or section != "open":
                    continue
                rest = m.group(2)
                due = DUE_WORD.search(rest)
                dates = DATE.findall(DUE_WORD.sub("", line))
                self.step(th.key, p, n, m.group(1), max(dates) if dates else None,
                          due=due.group(1) if due else None)

    def ticket_of_folder(self, folder):
        for name in ("init.md", "plan.md"):
            fm = self.v.notes.get(folder / name, ({}, ""))[0]
            m = LINK.search(str(fm.get("ticket") or ""))
            if m:
                t = self.v.resolve(m.group(1))
                if t:
                    return t
        return self.v.resolve(folder.name)

    def gather_work_folders(self):
        used = set()
        scope = self.v.scope
        folders = sorted({q for p in self.v.notes for q in p.parents
                          if q.parent.name == "work" and q.parent.parent.name == "delivery"
                          and (q == scope or scope in q.parents)})
        for f in folders:
            notes = sorted(p for p in self.v.notes if f in p.parents)
            self.internal.update(notes)
            ticket = self.ticket_of_folder(f)
            tfm = self.v.fm(ticket) if ticket else {}
            plan = f / "plan.md" if (f / "plan.md") in self.v.notes else None
            if ticket:
                used.add(ticket)
                self.internal.add(ticket)
                title = ticket.stem[len(f.name):].strip() if ticket.stem.startswith(f.name) else ticket.stem
            else:
                title = ""
            link = self.v.rel(ticket) if ticket else (self.v.rel(plan) if plan else None)
            th = self.add_thread(("work", f), [ticket, plan], link, f.name, title, tfm)
            status = status_of(tfm.get("status"))
            if status in ("parked", "done"):
                continue
            home = ticket or plan or notes[0]
            self.check_status(th, tfm, home)
            if status == "waiting":
                self.waiting_thread(th, tfm, home)
                continue
            slices = sorted(p for p in notes if p.parent == f / "slices")
            states = {s.stem: str(self.v.notes[s][0].get("state") or "").strip().lower() for s in slices}
            open_slices = [s for s in slices if states[s.stem] != "merged"]
            found = False
            if not slices:
                found = bool(ticket and ticket in self.v.notes and self.checklist_step(th, ticket))
            elif open_slices:
                for s in open_slices:
                    found |= self.slice_step(th, s, states)
            else:
                if ticket and ticket in self.v.notes:
                    found |= self.checklist_step(th, ticket)
                if plan:
                    found |= self.checklist_step(th, plan, "plan: ")
            if not found and not self.has_blocked_slice(open_slices, states):
                self.thread_look(th, "live, but no open step recorded", home)
        return used

    def has_blocked_slice(self, open_slices, states):
        return any(states[s.stem] == "planned" and self.open_deps(s, states) for s in open_slices)

    def open_deps(self, s, states):
        deps = [str(d).strip() for d in as_list(self.v.notes[s][0].get("depends-on")) if str(d).strip()]
        return [d for d in deps if states.get(d) != "merged"]

    def slice_step(self, th, s, states):
        state = states[s.stem]
        if state not in SLICE_STATES:
            self.needs_look(s, 0, s.stem, "slice state '%s' not recognised" % (self.v.notes[s][0].get("state") or "missing"))
            return True
        if state == "planned":
            missing = [d for d in self.open_deps(s, states) if d not in states]
            if missing:
                self.needs_look(s, 0, s.stem, "depends on '%s', which isn't a slice in this folder" % "', '".join(missing))
                return True
            if self.open_deps(s, states):
                return False
        return self.checklist_step(th, s, "slice %s: " % s.stem.split(" ")[0])

    def gather_tickets(self, used):
        for p in sorted(self.v.notes):
            fm, body = self.v.notes[p]
            if not has_category(fm, "Tickets") or p in used:
                continue
            aliases = as_list(fm.get("aliases"))
            tid = str(aliases[0]) if aliases else p.stem.split(" ")[0]
            title = p.stem[len(tid):].strip() if p.stem.startswith(tid) else p.stem
            th = self.add_thread(("ticket", p), [p], self.v.rel(p), tid, title, fm)
            self.internal.add(p)
            if self.excluded(p) or not any(True for _ in checkboxes(body)):
                continue  # a ticket with no checkboxes is a reference copy, not a thread
            self.check_status(th, fm, p)
            if status_of(fm.get("status")) == "waiting":
                self.waiting_thread(th, fm, p)
            elif not self.checklist_step(th, p):
                self.thread_look(th, "live, but no open step recorded", p)

    def gather_projects(self):
        for p in sorted(self.v.notes):
            fm, body = self.v.notes[p]
            if not has_category(fm, "Projects"):
                continue
            tid, _, title = p.stem.partition(" - ")
            th = self.add_thread(("project", p), [p], self.v.rel(p), tid, title, fm)
            self.internal.add(p)
            ended = str(fm.get("ended-on") or "").strip()
            if ended:
                self.ended[th.key] = ended
            if self.excluded(p) or ended:
                continue  # an ended project is inactive, whatever its status says
            self.check_status(th, fm, p)
            if status_of(fm.get("status")) == "waiting":
                self.waiting_thread(th, fm, p)
            elif not self.tasks_in(p, th.key):
                self.thread_look(th, "live, but no open step recorded", p)

    def gather_tasks(self):
        for p in sorted(self.v.notes):
            if p in self.internal or self.excluded(p):
                continue
            self.tasks_in(p, None)

    def tasks_in(self, p, own_thread):
        """Every open task in a note becomes a step. True if there was one."""
        found = False
        untouched = self.v.note_date(p)
        for n, mark, text in checkboxes(self.v.notes[p][1]):
            if mark not in (" ", "/"):
                continue
            found = True
            fields = {k: v for k, v in FIELD.findall(text)}
            blocker = fields.get("Blocked by")
            if blocker:
                target = self.v.resolve(LINK.match(blocker).group(1))
                if target is None:
                    self.needs_look(p, n, display(text), "blocked by %s, which doesn't exist" % blocker)
                    continue
                bstatus = self.v.fm(target).get("status")
                meaning = status_of(bstatus)
                if bstatus is None or str(bstatus).strip() == "":
                    self.needs_look(p, n, display(text), "blocked by %s, which has no status" % blocker)
                    continue
                if meaning == "unknown":
                    self.needs_look(p, n, display(text), "blocked by %s, whose status '%s' isn't recognised" % (blocker, bstatus))
                    continue
                if meaning != "done":
                    continue  # still blocked: off the list until the blocker is done
            thread = own_thread
            words = FIELD.sub("", text)
            if thread is None:
                for m in LINK.finditer(words):
                    target = self.v.resolve(m.group(1))
                    if target in self.thread_of:
                        thread = self.thread_of[target]
                        words = words.replace(m.group(0), "", 1)
                        break
            if thread in self.ended and own_thread is None:
                th = self.threads[thread]
                self.needs_look(p, n, words, "linked to [[%s|%s]], which ended on %s"
                                % (th.link, th.id, self.ended[thread]))
                continue
            due = DUE_EMOJI.search(text)
            self.step(thread, p, n, words, untouched, due=due.group(1) if due else None,
                      expected=fields.get("Expected by"), waiting_on=fields.get("Waiting on"))
        return found

    # -- render --
    def sort_key(self, s):
        due = s["due"] or (self.threads[s["thread"]].due if s["thread"] else None)
        rank = (0, due) if due else ((1, "") if s.get("expected") else (2, ""))
        return rank + (s["untouched"] or "9999-99-99", s["note"], s["line"])

    def reasons(self, s):
        out = []
        due = s["due"] or (self.threads[s["thread"]].due if s["thread"] else None)
        if due:
            out.append(("overdue, due %s" if due < self.today else "due %s") % due)
        if s.get("expected"):
            out.append("expected by " + s["expected"])
        return out

    def line(self, s, waiting=False):
        parts = ["[[%s|%s]]" % (s["note"], s["text"])]
        if waiting and s["thread"]:
            th = self.threads[s["thread"]]
            parts.append("in " + ("[[%s|%s]]" % (th.link, th.id) if th.link else th.id))
        parts += self.reasons(s)
        if s.get("waiting_on"):
            parts.append("waiting on " + s["waiting_on"])
        if s["untouched"]:
            parts.append("untouched since " + s["untouched"])
        return "- " + " · ".join(parts)

    def render(self):
        out = [HEADER, "", "## Yours now", ""]
        groups = {}
        for s in self.yours:
            groups.setdefault(s["thread"], []).append(s)
        for g in groups.values():
            g.sort(key=self.sort_key)
        order = sorted((k for k in groups if k is not None),
                       key=lambda k: (self.sort_key(groups[k][0]), self.threads[k].link or self.threads[k].id))
        if None in groups:
            order.append(None)
        if not order:
            out += ["Nothing here.", ""]
        for k in order:
            if k is None:
                out.append("**Dangling tasks**")
            else:
                th = self.threads[k]
                out.append(th.header() + (" · high priority" if th.high else ""))
            out += [self.line(s) for s in groups[k]]
            out.append("")

        out += ["## Waiting on others", ""]
        waiting = sorted(self.waiting, key=lambda s: (s["untouched"] or "9999-99-99", s["note"], s["line"]))
        for s in waiting:
            if s.get("whole"):
                parts = [s["whole"].header(), s["latest"]]
                if s["untouched"]:
                    parts.append("untouched since " + s["untouched"])
                out.append("- " + " · ".join(parts))
            else:
                out.append(self.line(s, waiting=True))
        out += ([""] if waiting else ["Nothing here.", ""])

        out += ["## Needs a look", ""]
        look = sorted(self.look, key=lambda x: (x["note"], x["line"], x["reason"]))
        for x in look:
            label = x["label"] if x["line"] == 0 and x["label"].startswith("**") else "[[%s|%s]]" % (x["note"], display(x["label"]))
            out.append("- %s · %s" % (label, x["reason"]))
        if not look:
            out.append("Nothing here.")
        return "\n".join(out).rstrip("\n") + "\n"


def display(text):
    """Step text fit for a link's label: fields and Tasks emoji removed, links reduced to their words."""
    t = FIELD.sub("", text)
    t = TASKS_FIELDS.sub("", t)
    t = LINK.sub(lambda m: m.group(2) or m.group(1), t)
    t = re.sub(r"[`*\[\]]", "", t).replace("|", "/")
    return " ".join(t.split())


# ---- main ----------------------------------------------------------------------
def find_vault_root(start):
    for marker in ("_AI", ".obsidian"):
        for p in [start] + list(start.parents):
            if (p / marker).is_dir():
                return p
    return None


def configured_folders(config):
    if not config.is_file():
        sys.exit("frontier: no folder given, and no config at %s to read frontier_folders: from" % config)
    raw = config.read_text(encoding="utf-8")
    data = parse_yaml(raw) if yaml is None else (yaml.safe_load(raw) or {})
    folders = [str(f) for f in as_list(data.get("frontier_folders") if isinstance(data, dict) else None) if str(f).strip()]
    if not folders:
        sys.exit("frontier: no folder given, and %s has no frontier_folders: list" % config)
    return folders


def run(folder, today, write):
    scope = Path(folder).expanduser().resolve()
    if not scope.is_dir():
        print("frontier: %s is not a folder" % folder, file=sys.stderr)
        return False
    root = find_vault_root(scope)
    if root is None:
        print("frontier: no vault (an _AI or .obsidian folder) found above %s" % scope, file=sys.stderr)
        return False
    f = Frontier(Vault(root, scope), today)
    f.gather()
    text = f.render()
    sys.stdout.write(text)
    if write:
        out = scope / OUTPUT
        if not out.exists() or out.read_text(encoding="utf-8") != text:
            out.write_text(text, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("folder", nargs="?", help="folder to list, e.g. gigs/2026-02-CCS")
    ap.add_argument("--now", help="pretend today is this date, YYYY-MM-DD (for testing)")
    ap.add_argument("--no-write", action="store_true", help="print the list without writing NEXT.md")
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help=argparse.SUPPRESS)
    a = ap.parse_args()
    today = (a.now or dt.date.today().isoformat())[:10]
    folders = [a.folder] if a.folder else configured_folders(a.config)
    ok = True
    for folder in folders:
        ok &= run(folder, today, not a.no_write)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
