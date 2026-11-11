"""Tests for frontier.py against a small fixture vault.

Run from the repo root: python3 -m unittest discover tests
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "vault" / "scripts" / "frontier.py"
FIXTURE = HERE / "frontier" / "vault"
EXPECTED = HERE / "frontier" / "expected" / "NEXT.md"
NOW = "2026-11-10"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, encoding="utf-8")


class FrontierFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.vault = self.tmp / "vault"
        shutil.copytree(FIXTURE, self.vault)
        self.folder = self.vault / "gig"
        self.out = self.folder / "NEXT.md"
        # the fixture vault's input notes, so its debrief pile is read
        self.config = self.tmp / "config.yml"
        self.config.write_text('heartbeat:\n  %s:\n    inputs: "YYYY-MM-DD *.md"\n    cutoff: 2026-11-06\n'
                               '    steps: [propagate, sweep-tasks]\n' % self.vault, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_fixture(self, *args):
        return run(str(self.folder), "--now", NOW, "--config", str(self.config), *args)

    def test_output_matches_expected(self):
        r = self.run_fixture()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.maxDiff = None
        self.assertEqual(self.out.read_text(encoding="utf-8"), EXPECTED.read_text(encoding="utf-8"))

    def test_second_run_leaves_file_unchanged(self):
        self.run_fixture()
        first = self.out.read_bytes()
        r = self.run_fixture()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.out.read_bytes(), first)

    def test_stdout_equals_file(self):
        r = self.run_fixture()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, self.out.read_text(encoding="utf-8"))

    def test_no_write_leaves_folder_alone(self):
        r = self.run_fixture("--no-write")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(self.out.exists())
        self.assertEqual(r.stdout, EXPECTED.read_text(encoding="utf-8"))


class FrontierConfig(unittest.TestCase):
    def test_no_folder_and_no_config_file_exits_with_message(self):
        with tempfile.TemporaryDirectory() as d:
            r = run("--config", str(Path(d) / "missing.yml"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("frontier: folders:", r.stderr)

    def test_no_folder_and_no_config_key_exits_with_message(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = Path(d) / "config.yml"
            cfg.write_text("compass:\n  file: ~/Compass.md\nfrontier:\n  other: x\n", encoding="utf-8")
            r = run("--config", str(cfg))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("frontier: folders:", r.stderr)


class FrontierVault(unittest.TestCase):
    """--vault, and the tasks of a heartbeat vault's input notes."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.vault = self.tmp / "vault"
        self.other = self.tmp / "other"
        shutil.copytree(FIXTURE, self.vault)
        shutil.copytree(FIXTURE, self.other)
        self.config = self.tmp / "config.yml"
        lib = self.vault / "gig" / "lib"
        (lib / "2026-11-08 Sweep.md").write_text("---\nstatus: done\n---\n- [ ] Chase the invoice\n", encoding="utf-8")
        (lib / "2026-10-01 Old log.md").write_text("---\nstatus: done\n---\n- [ ] Never listed: before the cutoff\n", encoding="utf-8")
        (lib / "Finished note.md").write_text("---\nstatus: done\n---\n- [ ] Never listed: done note\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write_config(self, heartbeat=True):
        text = "frontier:\n  folders:\n    - %s\n    - %s\n" % (self.vault / "gig", self.other / "gig")
        if heartbeat:
            text += 'heartbeat:\n  %s:\n    inputs: "YYYY-MM-DD *.md"\n    cutoff: 2026-11-01\n    steps: [propagate, sweep-tasks]\n' % self.vault
        self.config.write_text(text, encoding="utf-8")

    def test_vault_rebuilds_only_its_own_folders(self):
        self.write_config()
        r = run("--vault", str(self.vault), "--now", NOW, "--config", str(self.config))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.vault / "gig" / "NEXT.md").exists())
        self.assertFalse((self.other / "gig" / "NEXT.md").exists())

    def test_vault_with_no_folders_inside_says_so_and_succeeds(self):
        self.config.write_text("frontier:\n  folders:\n    - %s\n" % (self.other / "gig"), encoding="utf-8")
        r = run("--vault", str(self.vault), "--now", NOW, "--config", str(self.config))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("no frontier: folders:", r.stderr)
        self.assertFalse((self.vault / "gig" / "NEXT.md").exists())

    def test_vault_with_no_config_says_so_and_succeeds(self):
        r = run("--vault", str(self.vault), "--now", NOW, "--config", str(self.tmp / "missing.yml"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("no config", r.stderr)

    def test_input_note_keeps_its_tasks_whatever_its_status(self):
        self.write_config()
        r = run(str(self.vault / "gig"), "--now", NOW, "--no-write", "--config", str(self.config))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Chase the invoice", r.stdout)
        self.assertNotIn("Never listed", r.stdout)

    def test_without_a_heartbeat_entry_done_notes_are_skipped(self):
        self.write_config(heartbeat=False)
        r = run(str(self.vault / "gig"), "--now", NOW, "--no-write", "--config", str(self.config))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("Chase the invoice", r.stdout)


if __name__ == "__main__":
    unittest.main()
