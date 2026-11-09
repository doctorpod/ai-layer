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

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_output_matches_expected(self):
        r = run(str(self.folder), "--now", NOW)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.maxDiff = None
        self.assertEqual(self.out.read_text(encoding="utf-8"), EXPECTED.read_text(encoding="utf-8"))

    def test_second_run_leaves_file_unchanged(self):
        run(str(self.folder), "--now", NOW)
        first = self.out.read_bytes()
        r = run(str(self.folder), "--now", NOW)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.out.read_bytes(), first)

    def test_stdout_equals_file(self):
        r = run(str(self.folder), "--now", NOW)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, self.out.read_text(encoding="utf-8"))

    def test_no_write_leaves_folder_alone(self):
        r = run(str(self.folder), "--now", NOW, "--no-write")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(self.out.exists())
        self.assertEqual(r.stdout, EXPECTED.read_text(encoding="utf-8"))


class FrontierConfig(unittest.TestCase):
    def test_no_folder_and_no_config_file_exits_with_message(self):
        with tempfile.TemporaryDirectory() as d:
            r = run("--config", str(Path(d) / "missing.yml"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("frontier_folders", r.stderr)

    def test_no_folder_and_no_config_key_exits_with_message(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = Path(d) / "config.yml"
            cfg.write_text("compass_file: ~/Compass.md\n", encoding="utf-8")
            r = run("--config", str(cfg))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("frontier_folders", r.stderr)


if __name__ == "__main__":
    unittest.main()
