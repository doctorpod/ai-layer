---
name: write-design
description: Grill on one guide.md point at a time, filter for what's actually worth writing, then turn Andy's own spoken answers into design-document prose — never AI-drafted, always extracted from his own words.
---

# Workflow: Write Design

Help draft permaculture design-document prose (`output.md`) without ever writing it *for* Andy. The prose always comes from his own words — spoken in the grilling conversation, then extracted and lightly cleaned up, never composed fresh by Claude.

## Origin

This exists because a flat list of facts to write from is a genuinely hard writing task — atomised, no order, no personal hook, performed for an audience. A live conversation isn't: answering "how did you find that out, what did you make of it" comes out in Andy's own natural voice, the same register his journaling already works in. The method exploits that gap rather than fighting it. See `lib/log/2026/2026-08-14 grilled-drafting compose variant.md` for the design history.

## Usage

> "write-design", "let's write section `<N>`", "grill me on section `<N>` of the guide"

## Prerequisites

Same piece-folder convention as `compose.md` (`_AI/shared/snippets/piece-folder.md`): `brief.md`, `guide.md`, `output.md`, `assets/`. If `brief.md` or `guide.md` don't exist yet, don't improvise — point to compose's Steps 1–3 first.

Also read `lib/atlas/teaching/wiki/design-assessment-form.md` once per session if this piece might ever become Diploma material — its criteria ground the filter in Step 2, particularly Section 1 (ethics/principles applied *and legible*), Section 2.1 (solutions relevant to the brief, clearly explained), and Section 3 (the apprentice's own reflective account — not inferable from the design content alone, which is exactly what this workflow's grilling produces when it works).

## Step 1: Pick a section, cluster its points

Read the target section's `guide.md` entry. Its "Extracted points" are atomic, sourced bullets — don't grill bullet-by-bullet. Group related bullets into threads first (e.g. one design idea, its origin, and the stakeholder reaction to it are one thread, even if guide.md lists them as three separate bullets).

## Step 2: Filter each thread before grilling it

A thread only gets the grilling treatment if it passes **both**:

1. **Leads somewhere** — it results in (or already is) a concrete design decision, recommendation, or observation relevant to the brief. Inert facts with no design consequence (an admin decision that's someone else's call, a measurement whose exact value doesn't matter) fail this and should be dropped or, if genuinely needed for completeness, just stated plainly — no grilling, no personal narrative built around them.
2. **Andy has a real basis for it** — he noticed it, reacted to it, or holds a genuine view (experiential *or* professional). If he simply never engaged with something firsthand, don't manufacture a personal angle for it — that's fabrication, not a writing-block problem. Write it as a plainly cited fact instead, honestly sourced, with a recommendation only if Andy is actually willing to make one in a professional-judgement capacity (distinct from a personal-encounter capacity).

Two misses in the first live test both failed criterion 1 (an admin decision, an exact measurement). A third apparent miss initially looked like it failed criterion 2, then turned out to pass it once Andy realised he did have a professional view — worth actually asking before assuming a topic is dead, not just guessing from the guide text alone.

## Step 3: Grill the threads that pass

One thread at a time. Technique is `debrief.md` Step 1, not a checklist:
- Offer a best interpretation and ask Andy to confirm, correct, or push back — never a blank open question.
- Frame around *his encounter* with the material — how he learned it, what he made of it, whether he agrees — not "confirm this fact." This is what produces first-person, easily-written material instead of a report.
- Push past flat statements toward the reasoning or tension underneath, one question at a time, resolving each before moving to the next.
- "Enough" is a bidirectional signal — either Claude or Andy can suggest it, but only proceed once both agree.

## Step 4: Extract and assemble — not polish, not compose

This is a third technique, distinct from both:
- **Not `compose.md`**: never invent new phrasing. Nothing gets written that Andy didn't actually say.
- **Not `polish.md`**: polish explicitly forbids reordering and cutting. This workflow needs both — a real conversation isn't already in document order, and has dialogue-only asides ("isn't it", meta-remarks addressed to Claude) that don't belong in the prose.

The actual rule: **select and reorder Andy's own exact words and phrases; fix only clear surface/dictation slips (spelling, an obviously mis-transcribed word inconsistent with the same term used correctly elsewhere in the same answer); never introduce a word or phrase Andy didn't say.** Drop meta-commentary directed at Claude. Minimal connective tissue only where genuinely needed to join two of his sentences, and prefer punctuation (a dash) over invented linking words.

If a filter-passing point from Step 2 has no personal hook to weave it into naturally, don't silently draft a sentence for it — flag it to Andy explicitly and let him decide whether and how to include it. He may fold it into his own next answer, as happened live in testing (an ecological citation got woven into his own dictated sentence rather than added by Claude).

## Step 5: Compose-style approval loop

Show the assembled passage. Andy responds with one of:
- **"Good"** — done, move to Step 6
- **"Change X"** — Claude may re-cut or re-order further, but any genuinely new wording must come from Andy, not be invented to fix it
- **"It should say..."** — Andy dictates the replacement directly; use it as given

Repeat until approved.

## Step 6: Write it in

Insert the approved passage into `output.md`'s matching section. If a filter-passing-but-hookless fact was flagged in Step 4 and Andy wants it included, add it as a plainly cited fact near the passage, not folded into the personal narrative.

## Step 7: Update guide.md status

Once a section's grillable threads are all resolved (including any deliberately dropped per Step 2 — that's a resolution too, not a gap), update its `⚠ needs revision` marker to `✓` in `guide.md`, same as `compose.md` does at the end of its drafting loop. If some threads remain open, leave the `⚠` with a note on what's left.

## Step 8: Log

Append a log entry: `bash _AI/local/scripts/log-write.sh "WRITE-DESIGN: [section] — [brief summary]"`.

## Caveats

- This is a live, conversational workflow, not a file-watcher — no marker protocol, no background `Monitor`. It runs for as long as the chat session does.
- Don't batch multiple threads' approvals before writing — write each one in as it's approved, the way testing actually happened, so nothing sits unsaved if the session ends.
- The Step 2 filter is a judgement call, not a mechanical test — when genuinely unsure whether a point passes, ask rather than guessing silently in either direction.
