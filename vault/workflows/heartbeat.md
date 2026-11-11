---
name: heartbeat
description: Sweep every new input note in the vault (log notes, or journal notes), deal with each one completely, record what's still owed in its status, commit, and end by rebuilding NEXT.md.
---

# Heartbeat

Triggered by: "heartbeat", "run the heartbeat", "sweep the logs"

Input notes are what makes things change in a vault: log notes, or journal notes in a vault that keeps a journal. heartbeat makes sure every new one is dealt with completely: tracking surfaces updated, tasks threaded, and any debrief it owes kept in view. It's run by hand, several times a day. It ends by rebuilding the vault's `NEXT.md`, so the owner can see what to do next.

heartbeat is a loop over existing workflows. Each step keeps its own confirmations: heartbeat never batches changes or skips a step's own gate. What it adds is the opening report, the `status:` it writes on each note, a commit of its own files, and the Frontier run.

## States

An input note's `status:` records what's still owed to it. These values are defined here and nowhere else.

| `status:` | Means |
|---|---|
| `unprocessed` | Nothing done yet. A note dated on or after the cutoff with no `status:` counts as this. |
| `minuted` | Propagated to the tracking surfaces; the task sweep is still owed. |
| `needs-debrief` | Owes a debrief, which finishes it. |
| `done` | Nothing owed. |

The states describe what's owed, not steps taken, so a note can go straight from `unprocessed` to `done` or to `needs-debrief`. A vault whose steps don't include `minute` (a journal vault) never reaches `minuted` or `needs-debrief`.

A note's status describes the note, not its tasks: Frontier keeps an input note's open tasks on the list whatever its status.

## Step 0: Find this vault's entry

- Read `_AI/shared/config.yml` and find the `heartbeat:` entry whose key is this vault's root. It gives `inputs` (which notes are input notes), `cutoff` (notes dated before it are never swept) and `steps` (the workflows to run on each note, in order).
- If the config file or this vault's entry is missing, stop. Tell the owner to add one, copying the commented `heartbeat:` example from `_AI/shared/config.example.yml`.
- If the vault isn't a git repo, stop. heartbeat relies on git to notice notes edited after they were swept.
- Run `git status --porcelain` and note the files already uncommitted. They're the owner's, and Step 3 won't commit them without asking.

## Step 1: Open with what's owed

Run `python3 _AI/local/scripts/heartbeat.py .` from the vault root. It lists, oldest first:

- **Owes a debrief:** notes with `status: needs-debrief`.
- **To process:** notes with no status, any status other than `done`, or edited since they were last swept.
- **No heartbeat commit yet:** notes with a status that git hasn't recorded yet. Nothing is done to them; Step 3 includes them in the commit.

Open with the debrief pile, one line per note, so parked work is the first thing seen on every run. Then give the count to process. Don't start on the debriefs: a debrief is the owner's call, run separately.

If there's nothing to process, say so and go to Step 3.

## Step 2: Work through each note

Take the notes to process one at a time, oldest first. For each:

1. Name the note, its date and why it's listed (no status, its current status, or edited since last swept). If it's tagged `ai-generated`, say so: it was written by a past session, not by the owner.
2. Run the vault's `steps` on it in order, following each workflow in full, including its own confirmations. For an edited note, run them on the note as it stands; earlier propagation may already cover part of it.
   - While inside heartbeat, a step doesn't offer the next workflow (minute's sweep-tasks offer) when that workflow is the next step anyway, and the steps' own `NEXT.md` rebuilds wait for Step 4.
   - If a step hands back for a debrief, carry on with the remaining steps, but don't run the debrief.
3. Set the note's `status:` from what actually happened:
   - `needs-debrief` if a step handed back for a debrief
   - `done` if every step ran to the end (for sweep-tasks, the owner answered its table, even if some tasks were kept dangling)
   - `minuted` if `minute` ran but a later step didn't finish
   - otherwise leave `status:` as it was

   minute sets `status:` itself; check it matches the rules above once the later steps have run, and correct it if not.

The owner can answer any note with:

- **"skip":** move to the next note and leave its status unchanged.
- **"nothing needed":** set `status: done` without running the steps.
- **"stop":** end the loop here and go to Step 3 with what's done so far.

Keep a running list of every file heartbeat or its steps touched.

## Step 3: Commit heartbeat's own files

- The commit holds the files touched in Step 2, plus the notes listed under **No heartbeat commit yet**.
- If any of them was already uncommitted at Step 0, list those and ask before including them. Leave out any the owner says no to.
- Stage them by name (`git add -- <file> ...`). Never `git add -A`, `git add .`, or anything else that sweeps in files heartbeat didn't touch.
- Commit with a message starting `heartbeat:`, such as `heartbeat: 3 notes, 7 files`. That prefix is how the next run knows what was swept. Never skip the vault's pre-commit hook; if it blocks the commit, report why and leave the files staged.
- If there's nothing to commit, skip this step.

## Step 4: Rebuild NEXT.md

Run `python3 _AI/local/scripts/frontier.py --vault .` from the vault root. It rebuilds the `NEXT.md` of every `frontier: folders:` entry inside this vault. Run it even when Step 1 found nothing to process.

## Step 5: Report

Brief and structured:

- One line per note handled: its name and the state it reached (or "skipped").
- The files touched, and the commit (or why there wasn't one).
- What's still owed: the debrief pile, and any notes skipped or left `minuted`.
- One line pointing at `NEXT.md` for what to do next.
