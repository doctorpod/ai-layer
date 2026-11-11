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

LOG_ENTRY = '    inputs: "YYYY-MM-DD *.md"\n    cutoff: 2026-11-10\n    steps: [minute, sweep-tasks]\n'
JOURNAL_ENTRY = '    inputs: "journal/YYYY-MM-DD.md"\n    cutoff: 2026-11-10\n    steps: [sweep-tasks]\n'


class VaultRepo(unittest.TestCase):
    """A fresh copy of the fixture vault, committed once with a non-heartbeat message."""

    entry = LOG_ENTRY

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.vault = self.tmp / "vault"
        shutil.copytree(FIXTURE, self.vault)
        # _AI/ is git-ignored in this repo, so this fixture note is made here.
        (self.vault / "_AI" / "logs").mkdir(parents=True)
        (self.vault / "_AI" / "logs" / "2026-11-10 session.md").write_text("Layer log, never an input.\n")
        self.git("init", "-q", "-b", "main")
        self.commit("add notes")
        self.config = self.tmp / "config.yml"
        self.config.write_text("heartbeat:\n  %s:\n%s" % (self.vault, self.entry), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

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

    def output(self, now=NOW):
        r = self.run_script(now=now)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def section(self, out, title):
        """The lines of one output section."""
        body = out.split("## " + title + "\n", 1)[1].split("\n## ", 1)[0]
        return [l for l in body.splitlines() if l.startswith("- ")]

    def note(self, rel):
        return self.vault / rel

    def set_status(self, rel, status):
        p = self.note(rel)
        raw, body = vaultyaml.split_frontmatter(p.read_text(encoding="utf-8"))
        lines = [l for l in (raw or "\n").strip("\n").splitlines() if l and not l.startswith("status:")]
        lines.append("status: %s" % status)
        p.write_text("---\n%s\n---%s" % ("\n".join(lines), body if raw is not None else "\n" + body),
                     encoding="utf-8")


class LogVault(VaultRepo):
    def test_output_matches_expected(self):
        self.maxDiff = None
        self.assertEqual(self.output(), EXPECTED.read_text(encoding="utf-8"))

    def test_two_runs_are_byte_identical(self):
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
        self.assertEqual(self.section(out, "Owes a debrief"),
                         ["- 2026-11-11 · gig/lib/2026/2026-11-11 owes debrief.md"])
        process = self.section(out, "To process")
        self.assertIn("- 2026-11-10 · gig/lib/2026/2026-11-10 kickoff call.md · no status", process)
        self.assertIn("- 2026-11-12 · gig/lib/2026/2026-11-12 half done.md · minuted", process)
        self.assertNotIn("all done", "\n".join(process))

    def test_swept_note_with_no_heartbeat_commit_is_listed(self):
        rel = "gig/notes/2026-11-13 stray log.md"
        self.set_status(rel, "done")  # set, but not committed yet
        self.assertEqual(self.section(self.output(), "No heartbeat commit yet"), ["- 2026-11-13 · %s" % rel])
        self.commit("heartbeat: sweep")
        self.assertEqual(self.section(self.output(), "No heartbeat commit yet"), [])

    def test_status_committed_by_something_else_is_the_baseline(self):
        rel = "gig/lib/2026/2026-11-12 all done.md"  # committed with status: done, never by heartbeat
        out = self.output()
        self.assertNotIn(rel, out)
        with self.note(rel).open("a", encoding="utf-8") as f:
            f.write("One more thing.\n")
        self.commit("save: one more thing")
        self.assertIn("- 2026-11-12 · %s · edited since last heartbeat" % rel,
                      self.section(self.output(), "To process"))

    def test_body_edit_after_heartbeat_commit_requeues(self):
        rel = "gig/lib/2026/2026-11-10 kickoff call.md"
        self.set_status(rel, "done")
        self.commit("heartbeat: sweep")
        self.assertNotIn(rel, self.output())
        with self.note(rel).open("a", encoding="utf-8") as f:
            f.write("Something added later.\n")
        line = "- 2026-11-10 · %s · edited since last heartbeat" % rel
        self.assertIn(line, self.section(self.output(), "To process"))  # uncommitted
        self.commit("save: later notes")
        self.assertIn(line, self.section(self.output(), "To process"))  # committed by something else

    def test_edited_note_that_owed_a_debrief_moves_to_process(self):
        rel = "gig/lib/2026/2026-11-11 owes debrief.md"
        with self.note(rel).open("a", encoding="utf-8") as f:
            f.write("More from the visit.\n")
        out = self.output()
        self.assertEqual(self.section(out, "Owes a debrief"), [])
        self.assertIn("- 2026-11-11 · %s · edited since last heartbeat" % rel, self.section(out, "To process"))

    def test_frontmatter_only_edit_does_not_requeue(self):
        rel = "gig/lib/2026/2026-11-10 kickoff call.md"
        self.set_status(rel, "done")
        self.commit("heartbeat: sweep")
        p = self.note(rel)
        p.write_text(p.read_text(encoding="utf-8").replace("---\n", "---\nlast-ingested: 2026-11-15\n", 1),
                     encoding="utf-8")
        self.commit("ingest: frontmatter")
        self.assertNotIn(rel, self.output())

    def test_move_and_frontmatter_edit_does_not_requeue(self):
        rel = "gig/lib/2026/2026-11-10 kickoff call.md"
        moved = "gig/curated/2026-11-10 kickoff call.md"
        self.set_status(rel, "done")
        self.commit("heartbeat: sweep")
        self.git("mv", rel, moved)
        p = self.note(moved)
        p.write_text(p.read_text(encoding="utf-8").replace("---\n", "---\nlast-ingested: 2026-11-15\n", 1),
                     encoding="utf-8")
        self.commit("ingest: file the kickoff call")
        out = self.output()
        self.assertNotIn("kickoff call", out)

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


class JournalVault(VaultRepo):
    entry = JOURNAL_ENTRY

    def test_path_pattern_and_today_excluded(self):
        out = self.output(now="2026-11-11")
        self.assertEqual(self.section(out, "To process"), ["- 2026-11-10 · journal/2026-11-10.md · no status"])
        self.assertEqual(self.section(out, "Owes a debrief"), [])

    def test_yesterday_is_listed_once_its_day_has_passed(self):
        out = self.output(now="2026-11-12")
        self.assertEqual(self.section(out, "To process"), [
            "- 2026-11-10 · journal/2026-11-10.md · no status",
            "- 2026-11-11 · journal/2026-11-11.md · no status"])


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
                                       "steps": ["minute", "sweep-tasks"]},
                                "/w": {"inputs": "journal/YYYY-MM-DD.md", "cutoff": "2026-11-10",
                                       "steps": ["sweep_tasks"]}}}
        self.assertEqual(heartbeat.config_problems(config), [
            "heartbeat: /w: step 'sweep_tasks' isn't a vault workflow",
            "heartbeat: /w: no frontier: folders: entry inside this vault, so its tasks reach no NEXT.md"])

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
                           '    steps: [minute]\n', encoding="utf-8")
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
               "    steps: [minute, sweep-tasks]\n")
        self.assertEqual(vaultyaml.parse_fallback(raw), {
            "compass": {"file": "~/Compass.md"},
            "frontier": {"folders": ["~/a", "~/b"]},
            "heartbeat": {"~/vault": {"inputs": "YYYY-MM-DD *.md", "cutoff": "2026-11-10",
                                      "steps": ["minute", "sweep-tasks"]}}})

    def test_frontmatter_shape(self):
        raw = 'date: "[[2026-11-10]]"\ntime: "10:30"\ntags:\n- ai-generated\nstatus: done\nempty:\n'
        self.assertEqual(vaultyaml.parse_fallback(raw), {
            "date": "[[2026-11-10]]", "time": "10:30", "tags": ["ai-generated"], "status": "done", "empty": None})


if __name__ == "__main__":
    unittest.main()
