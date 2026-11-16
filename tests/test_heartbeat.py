"""Tests for heartbeat.py against a fixture vault, built into a temporary git repo per test.

Run from the repo root: python3 -m unittest discover tests
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "vault" / "scripts"
SCRIPT = SCRIPTS / "heartbeat.py"
FIXTURE = HERE / "heartbeat" / "vault"
EXPECTED = HERE / "heartbeat" / "expected" / "log-vault.md"
NOW = "2026-11-20"

sys.path.insert(0, str(SCRIPTS))
import heartbeat  # noqa: E402
import vaultyaml  # noqa: E402

# Keep the owner's git config (signing, hooks, default branch) out of the test repos.
GIT_ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
               GIT_AUTHOR_NAME="Test", GIT_AUTHOR_EMAIL="test@example.com",
               GIT_COMMITTER_NAME="Test", GIT_COMMITTER_EMAIL="test@example.com")

LOG_ENTRY = '    inputs: "YYYY-MM-DD *.md"\n    cutoff: 2026-11-10\n    steps: [propagate, sweep-tasks]\n'
JOURNAL_ENTRY = '    inputs: "journal/YYYY-MM-DD.md"\n    cutoff: 2026-11-10\n    steps: [sweep-tasks]\n'
KICKOFF = "gig/lib/2026/2026-11-10 kickoff call.md"
DEBRIEF_NOTE = "gig/lib/2026/2026-11-11 owes debrief.md"
ALL_DONE = "gig/lib/2026/2026-11-12 all done.md"


class Vault(unittest.TestCase):
    """A fresh copy of the fixture vault, committed once with a non-heartbeat message."""

    entry = LOG_ENTRY
    use_git = True

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.vault = self.tmp / "vault"
        shutil.copytree(FIXTURE, self.vault)
        # _AI/ is git-ignored in this repo, so this fixture note is made here.
        (self.vault / "_AI" / "logs").mkdir(parents=True)
        (self.vault / "_AI" / "logs" / "2026-11-10 session.md").write_text("Layer log, never an input.\n")
        if self.use_git:
            self.git("init", "-q", "-b", "main")
            self.commit("add notes")
        self.config = self.tmp / "config.yml"
        self.write_config(self.entry)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write_config(self, entry, extra=""):
        self.config.write_text("frontier:\n  folders:\n    - %s\nheartbeat:\n  %s:\n%s%s"
                               % (self.vault, self.vault, entry, extra), encoding="utf-8")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.vault), *args], env=GIT_ENV,
                              capture_output=True, text=True, check=True).stdout

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)

    def run_script(self, *args, now=NOW):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.vault), "--now", now,
                               "--config", str(self.config), *args],
                              capture_output=True, text=True, encoding="utf-8", env=GIT_ENV)

    def run_command(self, command, *args):
        return subprocess.run([sys.executable, str(SCRIPT), command, str(self.vault),
                               "--config", str(self.config), *args],
                              capture_output=True, text=True, encoding="utf-8", env=GIT_ENV)

    def output(self, now=NOW):
        r = self.run_script(now=now)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def section(self, out, title):
        """The list lines of one output section."""
        body = out.split("## " + title + "\n", 1)[1].split("\n## ", 1)[0].split("\n### ", 1)[0]
        return [l for l in body.splitlines() if l.startswith("- ")]

    def listed(self, out):
        return "\n".join(self.section(out, "To process"))

    def note(self, rel):
        return self.vault / rel

    def text(self, rel):
        return self.note(rel).read_text(encoding="utf-8")

    def append(self, rel, line):
        with self.note(rel).open("a", encoding="utf-8") as f:
            f.write(line)

    def replace(self, rel, old, new):
        self.note(rel).write_text(self.text(rel).replace(old, new, 1), encoding="utf-8")

    def mark(self, *rels):
        r = self.run_command("mark", *rels)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def write_note(self, rel, text):
        self.note(rel).parent.mkdir(parents=True, exist_ok=True)
        self.note(rel).write_text(text, encoding="utf-8")


# ---- the stamp -----------------------------------------------------------------
class BodyHash(unittest.TestCase):
    h = staticmethod(heartbeat.body_hash)

    def test_is_twelve_hex_digits(self):
        self.assertRegex(self.h("Hello"), r"\A[0-9a-f]{12}\Z")

    def test_link_targets_reduced_keeping_heading_and_alias(self):
        self.assertEqual(self.h("See [[a/b/c#h|x]]."), self.h("See [[c#h|x]]."))
        self.assertEqual(self.h("![[assets/2026/pic.png]]"), self.h("![[pic.png]]"))
        self.assertEqual(self.h("[x](../radar/vendor%20quote.md#now)"), self.h("[x](vendor%20quote.md#now)"))
        self.assertEqual(self.h("[x](<a/b c.md>)"), self.h("[x](<b c.md>)"))
        self.assertNotEqual(self.h("[[c#h|x]]"), self.h("[[c#g|x]]"))
        self.assertNotEqual(self.h("[[c#h|x]]"), self.h("[[c#h|y]]"))
        self.assertNotEqual(self.h("[[a/c]]"), self.h("[[a/d]]"))

    def test_external_links_are_kept_whole(self):
        self.assertNotEqual(self.h("[x](https://a.com/page)"), self.h("[x](https://b.com/page)"))

    def test_crlf_and_edge_whitespace_ignored(self):
        self.assertEqual(self.h("\n  a\r\nb  \n\n"), self.h("a\nb"))

    def test_a_tick_changes_it(self):
        self.assertNotEqual(self.h("- [ ] Send it"), self.h("- [x] Send it"))


class SetField(unittest.TestCase):
    def test_adds_a_field_leaving_the_rest_byte_for_byte(self):
        text = '---\ndate: "[[2026-11-10]]"\ntags:\n  - a\n---\nBody\n---\nmore\n'
        self.assertEqual(vaultyaml.set_field(text, "swept", "abc"),
                         '---\ndate: "[[2026-11-10]]"\ntags:\n  - a\nswept: abc\n---\nBody\n---\nmore\n')

    def test_replaces_in_place(self):
        text = "---\nswept: old\nstatus: done\n---\nBody\n"
        self.assertEqual(vaultyaml.set_field(text, "swept", "new"), "---\nswept: new\nstatus: done\n---\nBody\n")

    def test_removes_a_field_and_its_block_lines(self):
        text = "---\na: 1\nstatus:\n- x\n- y\nb: 2\n---\nBody\n"
        self.assertEqual(vaultyaml.set_field(text, "status", None), "---\na: 1\nb: 2\n---\nBody\n")
        self.assertEqual(vaultyaml.set_field("---\na: 1\n---\nB\n", "status", None), "---\na: 1\n---\nB\n")

    def test_gives_a_note_frontmatter(self):
        self.assertEqual(vaultyaml.set_field("Body\n", "swept", "abc"), "---\nswept: abc\n---\nBody\n")
        self.assertEqual(vaultyaml.set_field("Body\n", "swept", None), "Body\n")

    def test_keeps_crlf(self):
        self.assertEqual(vaultyaml.set_field("---\r\na: 1\r\n---\r\nB\r\n", "swept", "abc"),
                         "---\r\na: 1\r\nswept: abc\r\n---\r\nB\r\n")

    def test_numeric_looking_values_read_back_as_written(self):
        for value in ("012345678901", "123456789012", "0b1101100110", "abc123def456"):
            text = vaultyaml.set_field("---\n---\nB\n", "swept", value)
            self.assertEqual(str(vaultyaml.parse_yaml(vaultyaml.split_frontmatter(text)[0])["swept"]), value)


# ---- listing -------------------------------------------------------------------
class LogVault(Vault):
    def test_output_matches_expected(self):
        self.maxDiff = None
        self.assertEqual(self.output(), EXPECTED.read_text(encoding="utf-8"))

    def test_two_runs_are_byte_identical(self):
        self.append(KICKOFF, "Edited.\n")
        first = self.run_script()
        second = self.run_script()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout.encode(), second.stdout.encode())

    def test_dated_names_match_anywhere_and_built_in_folders_are_skipped(self):
        out = self.output()
        self.assertIn("gig/notes/2026-11-13 stray log.md", out)
        self.assertIn("gig/curated/2026-11-14 filed log.md", out)
        self.assertIn("gig/lib/2026/2026-11-15 ai note.md", out)
        for skipped in ("wiki/", "_AI/", ".obsidian/", "templates/", "before cutoff", "Undated", "2026-11-10.md"):
            self.assertNotIn(skipped, out)

    def test_states(self):
        out = self.output()
        self.assertEqual(self.section(out, "Owes a debrief"), ["- 2026-11-11 · %s" % DEBRIEF_NOTE])
        process = self.section(out, "To process")
        self.assertIn("- 2026-11-10 · %s · new" % KICKOFF, process)
        self.assertIn("- 2026-11-12 · gig/lib/2026/2026-11-12 half done.md · on-hold", process)
        self.assertNotIn("all done", out)

    def test_output_starts_with_the_steps(self):
        self.assertTrue(self.output().startswith("Steps: propagate, sweep-tasks\n\n## Owes a debrief\n"))

    def test_config_problems_for_this_vault_follow_the_steps(self):
        self.write_config(LOG_ENTRY.replace("sweep-tasks", "sweep_tasks"),
                          '  /some/other/vault:\n    inputs: "x"\n')
        out = self.output()
        self.assertTrue(out.startswith("Steps: propagate, sweep_tasks\nConfig: heartbeat: %s: step 'sweep_tasks' "
                                       "isn't a vault workflow\n\n" % self.vault), out)
        self.assertNotIn("other/vault", out)

    def test_stamped_note_is_not_listed(self):
        self.assertIn(KICKOFF, self.listed(self.output()))
        self.mark(KICKOFF)
        self.assertNotIn(KICKOFF, self.listed(self.output()))

    def test_frontmatter_is_not_part_of_the_stamp(self):
        self.mark(KICKOFF)
        self.replace(KICKOFF, "---\n", "---\nlast-ingested: 2026-11-15\n")
        self.assertNotIn(KICKOFF, self.listed(self.output()))

    def test_move_with_link_rewrites_does_not_relist(self):
        self.write_note("gig/lib/2026/2026-11-17 moved.md",
                        "Feeds [[gig/radar/vendor quote|the quote]] and [map](../../_wayfinder/launch/map.md).\n")
        self.mark("gig/lib/2026/2026-11-17 moved.md")
        self.commit("heartbeat: 1 note, 1 file")
        self.git("mv", "gig/lib/2026/2026-11-17 moved.md", "gig/curated/2026-11-17 moved.md")
        self.replace("gig/curated/2026-11-17 moved.md", "[[gig/radar/vendor quote|", "[[radar/vendor quote|")
        self.replace("gig/curated/2026-11-17 moved.md", "(../../_wayfinder", "(../_wayfinder")
        self.commit("save: file it")
        self.assertNotIn("2026-11-17", self.output())

    def test_body_edit_relists_with_changes_marked(self):
        self.mark(KICKOFF)
        self.commit("heartbeat: 1 note, 1 file")
        self.append(KICKOFF, "Something added later.\n")
        out = self.output()
        self.assertIn("- 2026-11-10 · %s · content · uncommitted" % KICKOFF, self.section(out, "To process"))
        self.assertIn("\n  Kickoff with the client.\n  - [ ] Send the agenda\n+ Something added later.\n", out)

    def test_edit_committed_by_something_else_still_compares_with_the_swept_version(self):
        self.mark(KICKOFF)
        self.commit("heartbeat: 1 note, 1 file")
        self.replace(KICKOFF, "Kickoff with the client.", "Kickoff with the new client.")
        self.commit("save: fix")
        out = self.output()
        self.assertIn("- 2026-11-10 · %s · content" % KICKOFF, self.section(out, "To process"))
        self.assertIn("- Kickoff with the client.\n+ Kickoff with the new client.\n", out)

    def test_tick_is_labelled_tasks_ticked(self):
        self.mark(KICKOFF)
        self.commit("heartbeat: 1 note, 1 file")
        self.replace(KICKOFF, "- [ ] Send the agenda", "- [x] Send the agenda")
        self.commit("save: ticked")
        out = self.output()
        self.assertIn("- 2026-11-10 · %s · tasks ticked" % KICKOFF, self.section(out, "To process"))
        self.assertIn("- - [ ] Send the agenda\n+ - [x] Send the agenda\n", out)

    def test_no_swept_version_in_git_is_labelled_edited(self):
        rel = "gig/lib/2026/2026-11-17 never committed.md"
        self.write_note(rel, "First thoughts.\n")
        self.mark(rel)
        self.append(rel, "More.\n")
        out = self.output()
        self.assertIn("- 2026-11-17 · %s · edited · uncommitted" % rel, self.section(out, "To process"))
        self.assertIn("\n  First thoughts.\n  More.\n", out)

    def test_needs_debrief_with_a_matching_stamp_owes_a_debrief(self):
        self.assertEqual(self.section(self.output(), "Owes a debrief"), ["- 2026-11-11 · %s" % DEBRIEF_NOTE])

    def test_edited_note_that_owed_a_debrief_moves_to_process(self):
        self.append(DEBRIEF_NOTE, "More from the visit.\n")
        self.commit("save: more")
        out = self.output()
        self.assertEqual(self.section(out, "Owes a debrief"), [])
        self.assertIn("- 2026-11-11 · %s · content · needs-debrief" % DEBRIEF_NOTE, self.section(out, "To process"))

    def test_needs_debrief_with_no_stamp_is_to_process(self):
        self.note(DEBRIEF_NOTE).write_text(vaultyaml.set_field(self.text(DEBRIEF_NOTE), "swept", None))
        out = self.output()
        self.assertEqual(self.section(out, "Owes a debrief"), [])
        self.assertIn("- 2026-11-11 · %s · needs-debrief · uncommitted" % DEBRIEF_NOTE,
                      self.section(out, "To process"))

    def test_other_statuses_are_shown_as_written_even_when_stamped(self):
        self.mark("gig/lib/2026/2026-11-12 half done.md")
        self.assertIn("- 2026-11-12 · gig/lib/2026/2026-11-12 half done.md · on-hold · uncommitted",
                      self.section(self.output(), "To process"))

    def test_long_notes_show_only_their_changes(self):
        rel = "gig/lib/2026/2026-11-17 long.md"
        self.write_note(rel, "".join("line %d\n" % i for i in range(1, 101)))
        out = self.output()
        self.assertIn("Long note (100 lines): showing the first 40.", out)
        self.assertIn("  line 40\n\n", out)
        self.assertNotIn("line 41\n", out)
        self.mark(rel)
        self.commit("heartbeat: 1 note, 1 file")
        self.replace(rel, "line 50\n", "line 50 changed\n")
        out = self.output()
        self.assertIn("Long note (100 lines): showing the changed lines with 3 lines around them.", out)
        self.assertIn("  …\n  line 47\n  line 48\n  line 49\n- line 50\n+ line 50 changed\n"
                      "  line 51\n  line 52\n  line 53\n  …\n", out)
        self.assertNotIn("line 46\n", out)

    def test_uncommitted_notes_and_surfaces_are_flagged(self):
        self.assertNotIn("uncommitted", self.output())
        self.append(KICKOFF, "Edited.\n")
        self.append("gig/radar/vendor quote.md", "- 2026-11-16: chased.\n")
        out = self.output()
        self.assertIn("- 2026-11-10 · %s · new · uncommitted" % KICKOFF, self.section(out, "To process"))
        self.assertIn("- radar · gig/radar/vendor quote.md · Quote due Friday · uncommitted", out)
        self.assertIn("- radar · gig/radar/vendor quote.md · uncommitted\n", out)  # as a linked surface

    def test_other_uncommitted_files_are_listed_once_at_the_end(self):
        self.assertNotIn("## Uncommitted elsewhere", self.output())
        self.append(KICKOFF, "Edited.\n")
        self.write_note("gig/tickets/T-1 ticket.md", "Owner's edit.\n")
        self.write_note("gig/NEXT.md", "Generated.\n")
        out = self.output()
        self.assertTrue(out.endswith("## Uncommitted elsewhere\n\n- gig/tickets/T-1 ticket.md\n"), out)

    def test_ai_generated_notes_are_called_out(self):
        self.assertIn("ai note.md · new\n\nTagged ai-generated", self.output())


class Surfaces(Vault):
    def test_linked_surfaces_both_ways(self):
        out = self.output()
        self.assertIn("2026-11-16 quote back.md · new\n\nHome: gig\nLinked:\n"
                      "- question · gig/kb/questions/who signs off.md\n- radar · gig/radar/vendor quote.md\n", out)
        self.assertIn("2026-11-16 launch update.md · new\n\nHome: gig\nLinked:\n"
                      "- wayfinder · gig/_wayfinder/launch/map.md\n", out)

    def test_home_listed_once_with_open_radar_items_and_maps(self):
        out = self.output()
        self.assertEqual(out.count("## Home: gig"), 1)
        home = out.split("## Home: gig\n", 1)[1]
        self.assertEqual(home, "\n- radar · gig/radar/vendor quote.md · Quote due Friday\n"
                               "- wayfinder · gig/_wayfinder/launch/map.md\n")

    def test_closed_radar_items_and_unlinked_questions_are_left_out(self):
        out = self.output()
        self.assertNotIn("old permit", out)
        self.assertNotIn("unlinked question", out)

    def test_a_note_with_no_home(self):
        self.assertIn("### 2026-11-10 · journal/2026-11-10 not daily.md · new\n\n  Not a daily-note name.\n",
                      self.output())

    def test_map_links_resolve_by_path_suffix_to_the_nearest_match(self):
        links = heartbeat.Links(["gig/_wayfinder/launch/map.md", "other/_wayfinder/launch/map.md",
                                 "gig/lib/note.md"])
        self.assertEqual(links.resolve("gig/_wayfinder/launch/map", "x.md"), "gig/_wayfinder/launch/map.md")
        self.assertEqual(links.resolve("launch/map.md", "other/lib/x.md"), "other/_wayfinder/launch/map.md")
        self.assertEqual(links.resolve("map", "gig/lib/x.md"), "gig/_wayfinder/launch/map.md")
        self.assertIsNone(links.resolve("launch/map", "x.md"))  # ambiguous
        self.assertEqual(links.resolve("../lib/note.md", "gig/radar/x.md"), "gig/lib/note.md")
        self.assertIsNone(links.resolve("nothing", "x.md"))

    def test_map_link_from_a_note_is_linked(self):
        self.write_note("other/_wayfinder/launch/map.md", "Another launch.\n")
        self.write_note("gig/lib/2026/2026-11-17 map link.md", "Updates [[gig/_wayfinder/launch/map|launch]].\n")
        out = self.output()
        self.assertIn("map link.md · new · uncommitted\n\nHome: gig\nLinked:\n- wayfinder · gig/_wayfinder/launch/map.md\n", out)
        self.assertNotIn("other/_wayfinder/launch/map.md\n\n  Updates", out)


class Errors(Vault):
    def test_missing_entry_exits_with_message(self):
        self.config.write_text("heartbeat:\n  /some/other/vault:\n%s" % LOG_ENTRY, encoding="utf-8")
        r = self.run_script()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no heartbeat: entry", r.stderr)
        self.assertIn(str(self.vault), r.stderr)

    def test_missing_config_exits_with_message(self):
        self.config.unlink()
        r = self.run_script()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no config", r.stderr)

    def test_entry_without_inputs_exits_with_message(self):
        self.config.write_text("heartbeat:\n  %s:\n    cutoff: 2026-11-10\n" % self.vault, encoding="utf-8")
        r = self.run_script()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("inputs", r.stderr)


# ---- mark and migrate ----------------------------------------------------------
class Mark(Vault):
    def test_writes_the_stamp_and_nothing_else(self):
        before = self.text(KICKOFF)
        out = self.mark(KICKOFF)
        h = heartbeat.body_hash(vaultyaml.split_frontmatter(before)[1])
        self.assertEqual(out, "- %s · swept: %s\n" % (KICKOFF, h))
        self.assertEqual(self.text(KICKOFF), before.replace('\n---\n', '\nswept: %s\n---\n' % h, 1))

    def test_gives_a_bare_note_frontmatter(self):
        rel = "gig/notes/2026-11-13 stray log.md"
        self.mark(rel)
        self.assertEqual(self.text(rel), "---\nswept: %s\n---\nA log note filed outside the log folder.\n"
                         % heartbeat.body_hash("A log note filed outside the log folder."))

    def test_updates_an_old_stamp(self):
        self.append(DEBRIEF_NOTE, "More.\n")
        self.mark(str(self.note(DEBRIEF_NOTE)))  # an absolute path works too
        fm, body = vaultyaml.read_note(self.note(DEBRIEF_NOTE))
        self.assertEqual(fm["swept"], heartbeat.body_hash(body))
        self.assertEqual(fm["status"], "needs-debrief")
        self.assertEqual(self.text(DEBRIEF_NOTE).count("swept:"), 1)

    def test_refuses_notes_that_are_not_inputs_and_changes_nothing(self):
        r = self.run_command("mark", KICKOFF, "gig/lib/Undated note.md", "nowhere.md")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("gig/lib/Undated note.md: not one of the vault's input notes", r.stderr)
        self.assertIn("nowhere.md: no such file in the vault", r.stderr)
        self.assertNotIn("swept", self.text(KICKOFF))


class Migrate(Vault):
    def setUp(self):
        super().setUp()
        self.note(ALL_DONE).write_text("---\nstatus: done\n---\nNothing left to do here.\n", encoding="utf-8")
        self.note(DEBRIEF_NOTE).write_text(vaultyaml.set_field(self.text(DEBRIEF_NOTE), "swept", None))
        self.replace("gig/lib/2026/2026-11-12 half done.md", "on-hold", "unprocessed")
        self.commit("old statuses")

    def test_lists_without_changing(self):
        before = {p: p.read_bytes() for p in self.vault.rglob("*.md")}
        r = self.run_command("migrate")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout,
                         "- %s · status: needs-debrief → stamp it, keep status\n"
                         "- %s · status: done → stamp it, remove status\n"
                         "- gig/lib/2026/2026-11-12 half done.md · status: unprocessed → remove status\n"
                         "3 notes to change. Run again with --apply to change them.\n" % (DEBRIEF_NOTE, ALL_DONE))
        self.assertEqual(before, {p: p.read_bytes() for p in self.vault.rglob("*.md")})

    def test_apply(self):
        r = self.run_command("migrate", "--apply")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(r.stdout.endswith("Changed 3 notes.\n"))
        self.assertEqual(self.text(ALL_DONE), "---\nswept: %s\n---\nNothing left to do here.\n"
                         % heartbeat.body_hash("Nothing left to do here."))
        out = self.output()
        self.assertEqual(self.section(out, "Owes a debrief"), ["- 2026-11-11 · %s · uncommitted" % DEBRIEF_NOTE])
        self.assertIn("- 2026-11-12 · gig/lib/2026/2026-11-12 half done.md · new · uncommitted",
                      self.section(out, "To process"))
        self.assertNotIn("all done", self.listed(out))
        self.assertIn("- gig/lib/2026/2026-11-12 all done.md", self.section(out, "Uncommitted elsewhere"))
        self.assertEqual(self.run_command("migrate").stdout, "Nothing to migrate.\n")

    def test_the_four_stuck_shapes_stay_off_once_migrated(self):
        notes = {
            "move": ("gig/lib/2026/2026-11-17 move.md", "See [[gig/_wayfinder/launch/map|launch]].\n"),
            "links": ("gig/lib/2026/2026-11-17 links.md", "See [[gig/radar/vendor quote]].\n"),
            "ticks": ("gig/lib/2026/2026-11-17 ticks.md", "- [ ] One\n- [ ] Two\n"),
            "added": ("gig/lib/2026/2026-11-17 added.md", "Backup plan.\n"),
        }
        for rel, body in notes.values():
            self.write_note(rel, "---\nstatus: done\n---\n" + body)
        self.commit("heartbeat: 4 notes, 4 files")
        self.git("mv", notes["move"][0], "gig/curated/2026-11-17 move.md")
        self.replace("gig/curated/2026-11-17 move.md", "[[gig/_wayfinder/launch/map|", "[[_wayfinder/launch/map|")
        self.replace(notes["links"][0], "[[gig/radar/vendor quote]]", "[[radar/vendor quote]]")
        self.replace(notes["ticks"][0], "- [ ] One\n- [ ] Two", "- [x] One\n- [x] Two")
        self.append(notes["added"][0], "Re-copy steps.\n")
        self.commit("save: tidy")
        self.assertEqual(self.listed(self.output()).count("2026-11-17 · "), 4)
        self.assertEqual(self.run_command("migrate", "--apply").returncode, 0)
        self.commit("heartbeat: migrate")
        self.assertNotIn("2026-11-17", self.output())
        self.append(notes["added"][0], "Something new.\n")
        self.assertIn("2026-11-17 added.md · content", self.listed(self.output()))


# ---- finish --------------------------------------------------------------------
class Finish(Vault):
    def finish(self, *args):
        return self.run_command("finish", *args)

    def committed(self, ref="HEAD"):
        return [l for l in self.git("show", "--name-only", "--format=%s", ref).splitlines() if l]

    def test_stamps_rebuilds_and_commits_only_named_files_last(self):
        self.append("gig/radar/vendor quote.md", "- 2026-11-16: came back at £4k.\n")
        self.append("gig/lib/Undated note.md", "The owner's own edit.\n")
        r = self.finish("--swept", KICKOFF, "--files", "gig/radar/vendor quote.md")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.committed(), ["heartbeat: 1 note, 3 files", "NEXT.md", KICKOFF,
                                            "gig/radar/vendor quote.md"])
        self.assertIn("swept:", self.git("show", "HEAD:" + KICKOFF))
        self.assertIn("Send the agenda", self.git("show", "HEAD:NEXT.md"))
        status = self.git("status", "--porcelain")
        self.assertEqual(status, " M \"gig/lib/Undated note.md\"\n")  # NEXT.md was rebuilt before the commit
        self.assertNotIn(KICKOFF, self.output())

    def test_leaves_other_staged_files_out(self):
        self.append("gig/lib/Undated note.md", "Staged by the owner.\n")
        self.git("add", "gig/lib/Undated note.md")
        r = self.finish("--swept", KICKOFF)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("gig/lib/Undated note.md", self.committed())
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "gig/lib/Undated note.md\n")

    def test_nothing_to_commit_skips_the_commit(self):
        self.assertEqual(self.finish("--swept", KICKOFF).returncode, 0)
        head = self.git("rev-parse", "HEAD")
        r = self.finish("--swept", KICKOFF)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Nothing to commit.", r.stdout)
        self.assertEqual(self.git("rev-parse", "HEAD"), head)

    def test_a_blocking_hook_leaves_files_staged(self):
        hook = self.vault / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\necho 'blocked by the hook'\nexit 1\n")
        hook.chmod(0o755)
        r = self.finish("--swept", KICKOFF)
        self.assertEqual(r.returncode, 1)
        self.assertIn("blocked by the hook", r.stdout)
        self.assertIn(KICKOFF, self.git("diff", "--cached", "--name-only"))
        self.assertEqual(self.committed()[0], "add notes")

    def test_refuses_a_note_that_is_not_an_input(self):
        r = self.finish("--swept", "gig/lib/Undated note.md")
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(self.note("NEXT.md").exists())


# ---- without git ---------------------------------------------------------------
class NoGit(Vault):
    use_git = False

    def test_listing_works_and_says_so(self):
        out = self.output()
        self.assertTrue(out.startswith("Steps: propagate, sweep-tasks\nGit: not a git repo, so changed lines "
                                       "aren't marked and finish won't commit.\n\n"))
        self.assertIn("- 2026-11-10 · %s · new" % KICKOFF, self.section(out, "To process"))
        self.assertNotIn("uncommitted", out)

    def test_mark_and_edit(self):
        self.mark(KICKOFF)
        self.assertNotIn(KICKOFF, self.output())
        self.append(KICKOFF, "More.\n")
        self.assertIn("- 2026-11-10 · %s · edited" % KICKOFF, self.section(self.output(), "To process"))

    def test_finish_stamps_and_rebuilds_without_committing(self):
        r = self.run_command("finish", "--swept", KICKOFF)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Not a git repo, so no commit.", r.stdout)
        self.assertTrue(self.note("NEXT.md").is_file())
        self.assertNotIn(KICKOFF, self.output())


# ---- journal vault and config --------------------------------------------------
class JournalVault(Vault):
    entry = JOURNAL_ENTRY

    def test_path_pattern_and_today_excluded(self):
        out = self.output(now="2026-11-11")
        self.assertEqual(self.section(out, "To process"), ["- 2026-11-10 · journal/2026-11-10.md · new"])
        self.assertEqual(self.section(out, "Owes a debrief"), [])

    def test_yesterday_is_listed_once_its_day_has_passed(self):
        out = self.output(now="2026-11-12")
        self.assertEqual(self.section(out, "To process"), [
            "- 2026-11-10 · journal/2026-11-10.md · new",
            "- 2026-11-11 · journal/2026-11-11.md · new"])


class IsInput(unittest.TestCase):
    entry = {"inputs": "YYYY-MM-DD *.md", "cutoff": "2026-11-10"}

    def test_matches(self):
        root = Path("/v")
        self.assertTrue(heartbeat.is_input(root, root / "a/b/2026-11-10 call.md", self.entry))
        self.assertFalse(heartbeat.is_input(root, root / "a/wiki/2026-11-10 call.md", self.entry))
        self.assertFalse(heartbeat.is_input(root, root / "a/2026-11-09 call.md", self.entry))
        self.assertFalse(heartbeat.is_input(root, root / "a/Call.md", self.entry))
        self.assertFalse(heartbeat.is_input(root, Path("/elsewhere/2026-11-10 call.md"), self.entry))

    def test_config_entry_for(self):
        config = {"heartbeat": {"/v": self.entry}}
        self.assertEqual(heartbeat.config_entry_for(Path("/v"), config), self.entry)
        self.assertIsNone(heartbeat.config_entry_for(Path("/w"), config))
        self.assertIsNone(heartbeat.config_entry_for(Path("/v"), None))


class CheckConfig(unittest.TestCase):
    def test_reports_unknown_steps_and_missing_frontier_coverage(self):
        config = {"frontier": {"folders": ["/v/gig"]},
                  "heartbeat": {"/v": {"inputs": "YYYY-MM-DD *.md", "cutoff": "2026-11-10",
                                       "steps": ["propagate", "sweep-tasks"]},
                                "/w": {"inputs": "journal/YYYY-MM-DD.md", "cutoff": "2026-11-10",
                                       "steps": ["sweep_tasks"]}}}
        self.assertEqual(heartbeat.config_problems(config), [
            "heartbeat: /w: step 'sweep_tasks' isn't a vault workflow",
            "heartbeat: /w: no frontier: folders: entry inside this vault, so its tasks reach no NEXT.md"])
        self.assertEqual(heartbeat.config_problems(config, vault=Path("/v")), [])

    def test_propagate_is_a_step_and_minute_is_not(self):
        config = {"frontier": {"folders": ["/v"]},
                  "heartbeat": {"/v": {"inputs": "YYYY-MM-DD *.md", "cutoff": "2026-11-10",
                                       "steps": ["propagate", "minute"]}}}
        self.assertEqual(heartbeat.config_problems(config), [
            "heartbeat: /v: step 'minute' is a shortcut that runs heartbeat, so it can't be one of "
            "heartbeat's steps (use propagate)"])

    def test_reports_unusable_entry(self):
        config = {"frontier": {"folders": ["/v"]}, "heartbeat": {"/v": {"inputs": "*.md"}}}
        problems = heartbeat.config_problems(config)
        self.assertEqual(len(problems), 1)
        self.assertIn("YYYY-MM-DD", problems[0])

    def test_no_heartbeat_section_is_fine(self):
        self.assertEqual(heartbeat.config_problems({"frontier": {"folders": ["/v"]}}), [])
        self.assertEqual(heartbeat.config_problems(None), [])

    def test_command_line(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = Path(d) / "config.yml"
            cfg.write_text('heartbeat:\n  /w:\n    inputs: "YYYY-MM-DD *.md"\n    cutoff: 2026-11-10\n'
                           '    steps: [propagate]\n', encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPT), "--check-config", "--config", str(cfg)],
                               capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.splitlines(),
                         ["heartbeat: /w: no frontier: folders: entry inside this vault, so its tasks reach no NEXT.md"])


class FallbackYaml(unittest.TestCase):
    """The parser used when PyYAML isn't installed reads what PyYAML reads, for these files."""

    def test_config_shape(self):
        raw = ("# comment\ncompass:\n  file: ~/Compass.md\nfrontier:\n  folders:\n    - ~/a\n    - ~/b\n"
               "heartbeat:\n  ~/vault:\n    inputs: \"YYYY-MM-DD *.md\"  \n    cutoff: 2026-11-10  # day one\n"
               "    steps: [propagate, sweep-tasks]\n")
        self.assertEqual(vaultyaml.parse_fallback(raw), {
            "compass": {"file": "~/Compass.md"},
            "frontier": {"folders": ["~/a", "~/b"]},
            "heartbeat": {"~/vault": {"inputs": "YYYY-MM-DD *.md", "cutoff": "2026-11-10",
                                      "steps": ["propagate", "sweep-tasks"]}}})

    def test_frontmatter_shape(self):
        raw = 'date: "[[2026-11-10]]"\ntime: "10:30"\ntags:\n- ai-generated\nstatus: needs-debrief\nswept: "012345678901"\nempty:\n'
        self.assertEqual(vaultyaml.parse_fallback(raw), {
            "date": "[[2026-11-10]]", "time": "10:30", "tags": ["ai-generated"], "status": "needs-debrief",
            "swept": "012345678901", "empty": None})


if __name__ == "__main__":
    unittest.main()
