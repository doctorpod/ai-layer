---
name: minute
description: Capture something that happened as a log note, then propagate it to every vault note that should reflect it.
---

# Minute

Triggered by: "minute this", "minute that", "minute it"

## Step 1: Get the record straight

- If the user pointed at an existing note, that is the record. Go to Step 2.
- Otherwise create a dated log note per `capture-log-note` (correct gig `log/YYYY/` folder, `date`/`time` frontmatter, `ai-generated` tag, 3–6 word lower-case title).
- The log note is a faithful record plus light context. Interpretation happens in Step 2.

## Step 2: Work out where else it belongs

Go through these homes. For each, decide whether this changes it, and how:

- `radar/` items — bump `updated:`, rewrite `latest:`, add a dated entry to the Context section
- `questions/` notes — answer, dismiss, or open a new one; bump `status` and `updated:`
- `wiki/` pages in the relevant KB — Summary, body, Evidence, Sources, Last updated
- `_wayfinder/` maps and `_greenhouse/` entries
- concept notes and `INDEX.md`

Stay on these synthesised surfaces. Update the underlying notes and leave `DASHBOARD.md` for `state-of-play` to reconcile.

Cross-link: the log note names the places it fed; those places cite the log note.

## Step 3: Apply

- Apply the log note now.
- Apply the propagation edits.
- If the plan touches four or more files, confirm the plan with the user before applying.

## Step 4: Report

Lead with a tight changelist: note created or used, then each file touched with a one-line reason, then any diffs handed back. "Logged, nothing else needed" is a valid outcome.
