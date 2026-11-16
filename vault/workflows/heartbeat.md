---
name: heartbeat
description: Sweep every new input note in the vault (log notes, or journal notes), deal with each one completely, record what's still owed in its status, commit, and end by rebuilding NEXT.md.
---

# Heartbeat

Triggered by: "heartbeat", "run the heartbeat", "sweep the logs"

Input notes are what makes things change in a vault: log notes, or journal notes in a vault that keeps a journal. heartbeat makes sure every new or edited one is dealt with completely: tracking surfaces updated, tasks threaded, any debrief it owes kept in view. It's run by hand several times a day, or on one note straight after it's written ("minute this" runs it in single-note mode), and ends by rebuilding `NEXT.md`.

Every rule for processing an input note lives here. Other workflows point here and keep no copy.

heartbeat runs a vault's `steps` on each note: `propagate` (below) or a vault workflow, followed in full with its own confirmations. Everything mechanical is done by `_AI/local/scripts/heartbeat.py`; spend effort only on judgement.

## States

Two frontmatter fields on an input note, both defined here and nowhere else:

| Field | Means | Written by | Cleared by |
|---|---|---|---|
| `swept: <hash>` | heartbeat has looked at the note as it stands. A hash of its body, ignoring link paths, so moves don't count but any edit (a ticked task included) does. No stamp, or one that no longer matches, puts the note in "To process". | `heartbeat.py` only (`finish` or `mark`) | an edit to the body, which makes it stop matching |
| `status: needs-debrief` | It changes what's true about a subject, so it owes a debrief. The only value `status:` takes. | heartbeat, when `propagate` stops for a debrief | `debrief`, which removes `status:` once it has taken the note as a source |

A note with a matching stamp and no `status:` owes nothing. A skipped or stopped note gets no stamp, so it stays listed. Neither field describes the note's tasks: Frontier keeps an input note's open tasks in play whatever its frontmatter.

## Step 1: Open with what's owed

Run `python3 _AI/local/scripts/heartbeat.py .` from the vault root. Its output is everything this run needs:

- **`Steps:`** the vault's steps, then any `Config:` problems. If it exits saying there's no config or no entry for this vault, stop (in single-note mode, take its fallback) and tell the owner to add one from the commented example in `_AI/shared/config.example.yml`.
- **Owes a debrief** and **To process**, each note with why it's listed: `new`, `content` or `tasks ticked` (changed lines marked `+` and `-`), `edited` (changes unknown), or a status as written.
- Each note's body, its **Home** and its **Linked** surfaces; then each home's open radar items and wayfinder maps. Don't re-read a note unless it's shown in part and you need the rest.
- **`uncommitted`** flags, and **Uncommitted elsewhere** at the end: the owner's changes, which Step 3 asks about.

Open with the debrief pile, one line per note, so parked work is the first thing seen on every run. Then give the count to process. Don't start on the debriefs: a debrief is the owner's call, run separately.

If there's nothing to process, say so in one line and stop: no finish, no further report.

## Step 2: Work through each note

Take the notes to process one at a time, oldest first. For each:

1. Name the note, its date and why it's listed, and say if it's tagged `ai-generated` (written by a past session, not the owner).
2. Run the vault's steps on it in order. For an edited note, work from the marked changes; earlier propagation covers the rest.
   - Run `sweep-tasks` whenever it's a step and the note has dangling tasks (open tasks with no thread link, as `_AI/local/FRONTIER.md` defines them).
   - The steps' own `NEXT.md` rebuilds wait for Step 3.
   - If `propagate` stops for a debrief, carry on with the remaining steps, but don't run the debrief.
3. Record the outcome, changing no other frontmatter:
   - `propagate` stopped for a debrief: set `status: needs-debrief`, and the note is swept.
   - every step ran to the end (for sweep-tasks, the owner answered its table, even if some tasks were kept dangling): the note is swept.
   - otherwise it isn't swept.

The owner can answer any note with:

- **"skip":** move to the next note; it isn't swept.
- **"nothing needed":** the note is swept without running the steps.
- **"stop":** end the loop here and go to Step 3 with what's done so far.

Keep two running lists: the notes swept, and every other file heartbeat or its steps touched.

### The `propagate` step

Work out where else the note belongs, and apply it there.

1. Start from the surfaces in the script's output: the note's linked surfaces, then its home's open radar items and wayfinder maps. For each, decide whether the note changes it, and how:
   - `radar/` items: bump `updated:`, rewrite `latest:`, add a dated entry to the Context section
   - `_wayfinder/` maps (per `_AI/local/workflows/wayfinder.md`) and `_greenhouse/` entries (per `_AI/shared/workflows/greenhouse.md`)
   - question notes in the `questions/` of the knowledge base the note's subject belongs to: answer, dismiss, or open one, per `_AI/shared/snippets/questions.md`. Only linked ones are listed, so look further only when the note bears on a knowledge base's open questions.
2. Cross-link both ways: the note names the places it fed; those places cite the note.
3. If the edits touch four or more files, confirm the plan with the owner before applying. Otherwise apply them.

**Boundary: propagate never touches the wiki.** No `wiki/` pages, no concept notes, no `INDEX.md`. It moves logistics and status, the small facts that live on the surfaces above ("John moved the meeting to Wednesday", "the quote came back at £4k"). If the note changes what's true about a subject (correcting a fact, adding a claim, not just moving a status), stop: keep the edits already made, and the note gets `needs-debrief` in Step 2.3. Debrief carries it into the wiki against a source. Don't run it.

## Single-note mode

Given one note ("minute this", or the owner pointing at a note), run Step 1 without its opening report and take only that note's block, then Step 2 on that note alone, then Steps 3 and 4.

If the vault has no `heartbeat:` entry, or the note isn't one of its input notes, run `propagate` and then `sweep-tasks` on it (if it has dangling tasks), set no `status:`, then run `python3 _AI/local/scripts/frontier.py --vault .` from the vault root and finish with Step 4. Nothing is stamped or committed.

## Step 3: Finish

If any file in either list was flagged `uncommitted` or listed under Uncommitted elsewhere in Step 1, list those and ask before including them. Leave out any the owner says no to. Then run, from the vault root:

`python3 _AI/local/scripts/heartbeat.py finish . --swept <note> ... --files <file> ...`

It stamps the swept notes, rebuilds every `NEXT.md` in the vault, then commits only the named files and rebuilt `NEXT.md` files. Run it whenever there was something to process, even if every note was skipped (no `--swept`). If the commit is blocked, report why; the files stay staged.

## Step 4: Report

Brief and structured:

- One line per note handled: its name and what it reached (swept, owes a debrief, or skipped).
- The files touched, and the commit (or why there wasn't one).
- What's still owed: the debrief pile, and any notes skipped or stopped on.
- One line pointing at `NEXT.md` for what to do next.
