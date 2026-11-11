---
name: sweep-tasks
description: Tidy a note's dangling tasks (usually a meeting or stand-up note) by proposing a thread link and plain-word fields for each, then writing only what the user confirms. Run by heartbeat as part of processing a note, or by hand.
---

# Sweep tasks

Triggered by: "sweep tasks", "sweep this note", "tidy the tasks", "sweep" + a note. `heartbeat` runs it on each note it processes (including through "minute this").

> [!warning] Must not
> Never edit a note without the user's confirmation of the proposal table in this session. That holds when this workflow is run by another workflow: a change agreed there doesn't cover the edits proposed here.

Tasks stay in the note where they were written. This workflow only appends plain-word fields to their lines, so the frontier list can put each one in its thread. The fields and what they mean are in `_AI/local/FRONTIER.md` under **Tasks in ordinary notes**. Read that section first.

## Step 1: Find the dangling tasks

- **Scope:** the note the user named. Read the note itself; don't run the frontier script.
- **Dangling:** an open task (`- [ ]` or `- [/]`) with no link to a thread note (a wayfinder map or a ticket). Skip notes the convention skips (parked or done `status:`, `ignore_tasks: true`, templates, and notes inside a work folder). A heartbeat input note is never skipped for its `status:`, which there records what heartbeat still owes the note.
- None found: say so in one line and stop.

## Step 2: Know the threads

Find the live threads the tasks might belong to, so each can be matched to a thread and duplicates spotted: the wayfinder maps (`**/_wayfinder/*/map.md`, by alias), and the tickets and work folders (by ticket alias, such as `[[CVT-344]]`). Read their open waypoints and checklists for duplicates.

## Step 3: Propose, all at once

One table, one row per task. For each, propose:

| Column | Propose |
|---|---|
| Still live? | keep; done (if the vault shows it's done); or drop (if it's stale or no longer wanted) |
| Duplicate of | the existing waypoint, checklist line or task it repeats, if any. Suggest drop, with "covered by ..." |
| Thread | the thread link to add, or "dangling" |
| `Expected by:` | a person link, if the note shows someone is expecting this from the owner, whether they asked or the owner offered |
| `Waiting on:` | a person link, if the task is really waiting on someone else |
| `Blocked by:` | a note link, if the task can't start until that note's `status:` means done |
| 📅 | only if the note gives a deadline or an event. Then ask "by when?" for the date |

Base every proposal on the note's own words, links and context, and on the threads from Step 2. Don't invent people, deadlines or links. If unsure, leave the cell blank and say why.

The user confirms or corrects the whole table in one reply. Don't go task by task unless they ask.

**Stop. Write nothing until the user replies to the table. If they don't reply to it, nothing is written.**

## Step 4: Write what was confirmed

- **Never change the task's own words,** and never move a task out of its note.
- Append to the end of the description, before any Tasks plugin emoji fields: the thread link, then `Expected by: [[person]]`, `Waiting on: [[person]]`, `Blocked by: [[note]]`. The Tasks fields (⏫ 📅 🆔 ⛔ ✅) stay last, as the plugin needs; a new 📅 goes with them.
- **Done:** change `[ ]` to `[x]` and add `✅ YYYY-MM-DD` (today).
- **Dropped:** change `[ ]` to `[-]`. The list ignores dropped tasks.
- A task kept as dangling with nothing to add is left as it is.

Example:

```
- [ ] Prod MG for meeting
- [ ] Prod MG for meeting [[cdp data ingest]] Expected by: [[Michael Greenall]] 📅 2026-11-09
```

## Step 5: Report

One line per note: how many tasks got a thread or fields, how many were marked done, how many were dropped, and how many are still dangling.

## Step 6: Rebuild NEXT.md

If Step 4 changed any task line, run `python3 _AI/local/scripts/frontier.py --vault .` from the vault root, so the vault's `NEXT.md` files reflect it. Don't show its output. When the vault has no config or no `frontier: folders:` inside it, the script says so and does nothing; skip it silently.
