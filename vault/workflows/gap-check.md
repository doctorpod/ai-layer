---
name: gap-check
description: Check a draft against its guide (or another named reference), report what's missing, and record coverage on the checked themes.
---

# Gap Check

Triggered by: "gap check `<file>`", "gap check `<file>` against `<reference>`", "check gaps in `<file>`", "does `<file>` cover `<reference>`"

Compares a document against a reference and reports what's missing. Never edits target or reference content — the one write it makes is `coverage` on the checked theme notes (see Step 5), every run, not opt-in.

## Step 1: Establish target and reference

- **Target**: the document being checked (usually `output.md`).
- **Reference**: what it's checked against.
  - If the user names one, use it.
  - If they don't, and the target sits in a piece-folder, default to that folder's `guide/` — every theme note inside it.
  - If neither applies, ask.

## Step 1a: Scoped runs

Usually the whole target is in play. Sometimes it isn't — most often a `% scribe` marker (`scribe.md`) sitting under, or naming, a single section. On a scoped run:

- **Read scope = write scope.** Compare (Step 2) and record `coverage` (Step 5) for *only* the theme notes whose `section:` frontmatter falls inside the part you actually read. Never write a verdict for a theme whose section you didn't look at — it would land as `missing` purely for being out of scope.
- Match theme to section on the `section:` field (e.g. `section: 03 What I Saw`).
- Nothing else changes: still skip `rejected`, still leave `status` alone, still a chat report.

This is by design: `coverage` is a per-theme progress signal, and each theme belongs to exactly one section, so a section-scoped run and a whole-doc run write the same value for any theme they share.

## Step 2: Compare themes

Read every theme note in the reference (skip any with `status: rejected` — deliberately excluded, not a gap; on a scoped run, also skip any whose `section:` is outside the scope — see Step 1a). For each remaining theme, treat its Quotes and Synthesis together as one unit — matching `status`'s per-theme atomicity — and check it against the target: **full**, **thin**, or **missing**.

This verdict is independent of the theme's own `status` field. A theme marked `used` can still come back `thin` or `missing` if `output.md` has since changed — that drift is exactly what this check exists to catch. A theme marked `pending` coming back `full` is also worth surfacing — it may mean the writer forgot to update `status`, or covered it unknowingly.

## Step 3: Check assets

Run `python3 _AI/local/scripts/check-assets.py <piece-folder> <target>`. It flags any asset whose filename doesn't appear anywhere in the target — that's a strong signal, not proof, since an asset can still be referenced by description alone with no filename in sight. Give each `unreferenced` result a quick glance against the target before reporting it as a real gap.

## Step 4: Report

Chat response only, by default — two short lists:
- One line per theme gap: the theme's name, and whether it's `thin` or `missing` in the target (skip anything `full`, unless it's a `pending` theme that turned up `full` — flag that too, differently, as noted above).
- One line per unused asset.

When a gap points at a specific passage in the target, cite its line number with a short quote to anchor it — not a paragraph or section number ("¶2", "the third para"). Line numbers are exact and clickable. This holds wherever the report lands, including a scribe `% **comments**` block.

No verdict, no score. Don't fix anything. Don't write the gap list itself anywhere unless the user asks — this is about the chat report only; recording `coverage` (Step 5) happens regardless.

## Step 5: Recording coverage

Every run: batch-write the Step 2 verdicts in one call — `python3 _AI/local/scripts/write-coverage.py <guide-folder> <theme-file>=<verdict> [<theme-file>=<verdict> ...]` — one `<theme-file>=<verdict>` pair per theme checked in Step 2. Don't include `rejected` themes in the call; the script also refuses to write `coverage` onto one if it slips through. Never touch `status` — that stays the writer's own call, exactly as `sync-guide.md` leaves it alone.

## What this workflow doesn't do

Doesn't fix anything, in target or reference. Doesn't judge whether the writer has a personal basis for a theme — that's the writer's own call via `status`. Doesn't touch `status`, ever. Doesn't manage `assets/` contents — only checks that what's already there is referenced.
