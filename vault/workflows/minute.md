---
name: minute
description: Capture a logistics or status change as a log note, then propagate it across the vault's tracking surfaces (radar, questions, wayfinder, greenhouse). Durable wiki knowledge is out of scope — that's a debrief.
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
- `_wayfinder/` maps and `_greenhouse/` entries

Stay on these synthesised surfaces. Update the underlying notes and leave `DASHBOARD.md` for `state-of-play` to reconcile.

Cross-link: the log note names the places it fed; those places cite the log note.

### Boundary: minute does not touch the wiki

No `wiki/` pages, no concept notes, no `INDEX.md`. minute is for logistics and status — the small facts that live on the tracking surfaces above ("John moved the meeting to Wednesday", "the quote came back at £4k"). Durable domain knowledge has a truth gate that minute deliberately doesn't.

### If it turns out to change durable knowledge, stop

If propagating this cleanly would mean editing a `wiki/` page or concept note — correcting a fact about the subject, adding a claim, not just moving a status — that is a debrief, not a minute. Stop there. Keep the log note and any tracking-surface edits already made, then tell the user this needs `debrief` to carry it into the wiki against a source. Don't switch workflows yourself — hand back and let the user decide.

## Step 3: Apply

- Apply the log note now.
- Apply the propagation edits.
- If the plan touches four or more files, confirm the plan with the user before applying.

## Step 4: Report

Lead with a tight changelist: note created or used, then each file touched with a one-line reason, then any diffs handed back. "Logged, nothing else needed" is a valid outcome — so is "logged and propagated across the tracking surfaces; the wiki side needs a debrief."
