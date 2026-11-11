"""Tests for jira-snapshot.py using small synthetic Jira exports.

Run from the repo root: python3 -m unittest discover tests
"""
import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "vault" / "scripts" / "jira-snapshot.py"

# The shape of a real export: repeated columns, account ids in comments.
HEADER = ["Summary", "Issue key", "Issue Type", "Status", "Assignee", "Assignee Id",
          "Reporter", "Reporter Id", "Created", "Updated", "Description",
          "Sprint", "Sprint", "Labels", "Labels", "Parent key", "Parent summary",
          "Inward issue link (Relates)", "Comment", "Comment", "Custom field (Rank)"]


def ticket(key, summary="A ticket", status="To Do", assignee="Ann", updated="01/Nov/26 9:00 AM",
           sprints=("", ""), comments=("", ""), rank="0|a", description="Words"):
    return [summary, key, "Story", status, assignee, "id-ann" if assignee == "Ann" else "id-bob",
            "Bob", "id-bob", "01/Oct/26 10:00 AM", updated, description,
            sprints[0], sprints[1], "data", "", "EPIC-1", "The epic",
            "", comments[0], comments[1], rank]


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, encoding="utf-8")


class JiraSnapshot(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.snaps = self.tmp / "jira"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def export(self, name, rows):
        path = self.tmp / name
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(HEADER)
            w.writerows(rows)
        return str(path)

    def ingest(self, export, day):
        r = run("ingest", export, "--dir", str(self.snaps), "--date", day)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def rows(self, day):
        with open(self.snaps / f"{day}.csv", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def test_baseline_stores_everything_and_names_people(self):
        out = self.ingest(self.export("a.csv", [
            ticket("CVT-2", comments=("05/Nov/26 2:00 PM;id-bob;Hi [~accountid:id-ann]", ""),
                   sprints=("Sprint 1", "Sprint 2")),
            ticket("CVT-1")]), "2026-11-01")
        self.assertIn("Baseline", out)
        rows = self.rows("2026-11-01")
        self.assertEqual([r["key"] for r in rows], ["CVT-1", "CVT-2"])
        self.assertEqual(rows[1]["comments"], "2026-11-05 14:00 Bob: Hi @Ann")
        self.assertEqual(rows[1]["sprints"], "Sprint 1; Sprint 2")
        self.assertEqual(rows[0]["updated"], "2026-11-01 09:00")
        self.assertNotIn("Rank", (self.snaps / "2026-11-01.csv").read_text())

    def test_unchanged_and_rank_only_tickets_are_not_stored(self):
        self.ingest(self.export("a.csv", [ticket("CVT-1"), ticket("CVT-2")]), "2026-11-01")
        out = self.ingest(self.export("b.csv", [
            ticket("CVT-1", rank="0|b", updated="02/Nov/26 9:00 AM"),
            ticket("CVT-2", status="Done")]), "2026-11-08")
        self.assertEqual([r["key"] for r in self.rows("2026-11-08")], ["CVT-2"])
        self.assertIn("status: To Do → Done", out)
        self.assertIn("0 first seen, 1 changed, 0 gone", out)

    def test_new_comment_new_ticket_and_gone(self):
        self.ingest(self.export("a.csv", [ticket("CVT-1"), ticket("CVT-2")]), "2026-11-01")
        out = self.ingest(self.export("b.csv", [
            ticket("CVT-1", comments=("09/Nov/26 9:00 AM;id-ann;Looks good", "")),
            ticket("CVT-3", summary="Brand new")]), "2026-11-08")
        self.assertIn("new comment: 2026-11-09 09:00 Ann: Looks good", out)
        self.assertIn("## First seen", out)
        self.assertIn("CVT-3 Brand new", out)
        self.assertIn("## Gone", out)
        self.assertIn("CVT-2", out.split("## Gone")[1])
        keys = (self.snaps / "2026-11-08.keys").read_text().split()
        self.assertEqual(keys, ["CVT-1", "CVT-3"])

    def test_current_rebuilds_latest_state_and_marks_gone(self):
        self.ingest(self.export("a.csv", [ticket("CVT-1"), ticket("CVT-2")]), "2026-11-01")
        self.ingest(self.export("b.csv", [ticket("CVT-1", status="Done")]), "2026-11-08")
        r = run("current", "--dir", str(self.snaps), "--csv")
        rows = {row["key"]: row for row in csv.DictReader(r.stdout.splitlines())}
        self.assertEqual(rows["CVT-1"]["status"], "Done")
        self.assertEqual(rows["CVT-2"]["gone"], "yes")
        r = run("current", "--dir", str(self.snaps), "--as-of", "2026-11-01", "--csv")
        rows = {row["key"]: row for row in csv.DictReader(r.stdout.splitlines())}
        self.assertEqual(rows["CVT-1"]["status"], "To Do")
        self.assertEqual(rows["CVT-2"]["gone"], "")

    def test_refuses_to_overwrite_or_go_backwards(self):
        a = self.export("a.csv", [ticket("CVT-1")])
        self.ingest(a, "2026-11-08")
        self.assertNotEqual(run("ingest", a, "--dir", str(self.snaps), "--date", "2026-11-08").returncode, 0)
        self.assertNotEqual(run("ingest", a, "--dir", str(self.snaps), "--date", "2026-11-01").returncode, 0)

    def test_second_export_same_day_gets_a_suffix(self):
        today = date.today().isoformat()
        self.ingest(self.export("a.csv", [ticket("CVT-1")]), today)
        r = run("ingest", self.export("b.csv", [ticket("CVT-1", status="Done")]), "--dir", str(self.snaps))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([x["key"] for x in self.rows(f"{today}-2")], ["CVT-1"])
        self.assertIn(f'date: "[[{today}]]"', r.stdout)
        r = run("current", "--dir", str(self.snaps), "--csv")
        self.assertEqual(next(csv.DictReader(r.stdout.splitlines()))["status"], "Done")
        r = run("current", "--dir", str(self.snaps), "--as-of", today, "--csv")
        self.assertEqual(next(csv.DictReader(r.stdout.splitlines()))["status"], "To Do")

if __name__ == "__main__":
    unittest.main()
