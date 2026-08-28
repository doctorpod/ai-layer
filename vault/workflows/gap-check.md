---
name: gap-check
description: Check a draft against its themes (or another named reference), report what's missing, and record coverage on the checked themes.
---

# Gap Check

Triggered by: "gap check `<file>`", "gap check `<file>` against `<reference>`", "check gaps in `<file>`", "does `<file>` cover `<reference>`"

Compares a document against a reference and reports what's missing. Never edits target or reference content — the one write it makes is `coverage` on the checked theme notes (see Step 5), every run, not opt-in.

## Step 1: Establish target and reference

- **Target**: the document being checked (usually `output.md`).
- **Reference**: what it's checked against.
  - If the user names one, use it.
  - If they don't, and the target sits in a piece-folder, default to that folder's `themes/` — every theme note inside it.
  - If the piece-folder still has a flat `guide.md` instead of `themes/` (not yet migrated — see `sync-guide.md`), use that, treating each `PENDING`/`USED`/`REJECTED`-tagged bullet as the reference item.
  - If neither applies, ask.

## Step 2: Compare themes

Read every theme note in the reference (skip any with `status: rejected` — deliberately excluded, not a gap). For each remaining theme, treat its Quotes and Synthesis together as one unit — matching `status`'s per-theme atomicity — and check it against the target: **covered**, **thin**, or **missing**.

This verdict is independent of the theme's own `status` field. A theme marked `used` can still come back `thin` or `missing` if `output.md` has since changed — that drift is exactly what this check exists to catch. A theme marked `pending` coming back `covered` is also worth surfacing — it may mean the writer forgot to update `status`, or covered it unknowingly.

## Step 3: Check assets

List every file in the piece-folder's `assets/`. For each, check whether target references or embeds it (`![[filename]]`, a plain link, or an explicit mention). Report any with no reference.

## Step 4: Report

Chat response only, by default — two short lists:
- One line per theme gap: the theme's name, and whether it's `thin` or `missing` in the target (skip anything `covered`, unless it's a `pending` theme that turned up covered — flag that too, differently, as noted above).
- One line per unused asset.

No verdict, no score. Don't fix anything. Don't write the gap list itself anywhere unless the user asks — this is about the chat report only; recording `coverage` (Step 5) happens regardless.

## Step 5: Recording coverage

Every run: write the Step 2 verdict into each checked theme's `coverage` frontmatter field (`full`, `thin`, or `missing`). Skip `rejected` themes entirely — never write their `coverage`. Never touch `status` — that stays the writer's own call, exactly as `sync-guide.md` leaves it alone.

## What this workflow doesn't do

Doesn't fix anything, in target or reference. Doesn't judge whether the writer has a personal basis for a theme — that's the writer's own call via `status`. Doesn't touch `status`, ever. Doesn't manage `assets/` contents — only checks that what's already there is referenced.
