---
name: sync-guide
description: Build and maintain a piece's guide.md from its brief and the vault sources it draws on.
---

# Sync Guide

Triggered by: "sync guide", "sync the guide", "update the guide", "build the guide"

Builds `guide.md` from `brief.md` by triaging its `Draw from` KBs' `curated/` folders against a relevance filter, and keeps it in sync as new material lands. This workflow only ever touches `guide.md` — it never reads or writes `output.md`, and it doesn't set up the brief itself.

See `_AI/shared/snippets/piece-folder.md` for the file structure, brief.md fields, and location convention.

## Prerequisite: the brief

`brief.md` isn't built by this workflow — that's an ad hoc conversation, whenever the user wants help with it. If `brief.md` doesn't exist yet when this workflow is called, say so and offer to help draft it in chat, then stop. Don't start the guide until the brief exists.

## The guide template

`guide.md` is not prose — it's a structured scaffold, one heading per document section. It is **extractive, not abstractive**: a bullet is a lifted (verbatim or lightly trimmed) span, carried over with its own citation — never a freshly-composed sentence inspired by one. Freshly-composed sentences are where inaccuracy creeps in; copied ones can't drift from their source.

Lift from the **primary source**, not from the wiki page's prose. A wiki page is a map to sources, not itself a source — its own sentences can already be a synthesis across multiple sources, and lifting one faithfully just carries that synthesis into the guide with a false stamp of fidelity. Use the wiki page to find *which* source backs a claim (its footnote if the page cites more than one source, or its header `**Sources**:` field if it cites only one), then go read that source and lift from there.

If the wiki sentence can't actually be found in the source it's attributed to — the wiki has drifted, blended two sources, or the citation is stale — don't lift it anyway. Flag it to the user as a likely conflation and either fix the wiki page first or leave the point out of the guide until it's resolved. Finding one of these is a sign the fix is working, not a distraction from the guide-building task.

**Concrete check before writing any citation**: if the bullet you're about to write ends in `— [[site-overview]]` (a page under `wiki/`), stop — that's the map, not the source. Resolve the footnote or `**Sources**:` field for *that specific sentence* first, and cite what it points to instead, e.g. `— [[debrief-2026-02-19-ian-parrish-interview-1]]`. A citation pointing at a `wiki/` page is always wrong in this workflow — both examples above use `[[...]]` syntax, but only a source file (a curated file or debrief note) belongs on the right side of the dash.

Under each heading:

**Extracted points** — one bullet per atomic claim, each with its own source:
- `"lifted sentence or clause, trimmed but not reworded" — [[primary-source]]`, where `primary-source` is the curated file, debrief note, or external source the wiki page cites for that claim — not the wiki page itself
- If the source sentence carries a hedge, caveat, or correction (an inline qualifier like "unconfirmed," "likely a misspeak," or a `> [!caution]` callout), the bullet must carry it too. Never cite a claim while dropping the caveat attached to it in the source.
- One citation per bullet. If a point can't be traced to a specific sentence in a specific source, it doesn't belong here — put it under Synthesis, or leave it out until a source exists.

**Synthesis** — reasoning, design implications, or Andy's own read, built on top of the extracted points above but not lifted from any source. No citation, because none exists — that absence is the label. Keep this visually separate from Extracted points; never let a synthesis bullet sit unmarked among sourced ones.

**Assets** — any assets needed, tied to their purpose.

Don't pool sources at the bottom of a section. Per-bullet citation makes the section's source list a byproduct (derivable by scanning the bullets), not something authored separately that can drift out of sync or omit a source in use.

## Relevance filter

Before a claim earns an Extracted point, it has to pass one test: does it lead somewhere — a concrete decision, recommendation, or observation relevant to the brief? If not, drop it. Don't write it to `guide.md` at all, not even as a plain fact — a failing claim just doesn't appear. Admin decisions that aren't the writer's to make, and exact measurements nobody will act on, are the common failure case.

This filter applies to candidate Extracted points only. Synthesis bullets aren't sourced from `curated/` in the first place, so nothing to filter.

This is narrower than `_AI/local/workflows/elicit.md`'s own filter — elicit separately checks whether the *writer* has a real basis for a surviving point (noticed it, reacted to it, holds a genuine view). That's a live judgement call made during grilling; this workflow never grills, so it only ever applies the relevance half. Anything that reaches `guide.md` has already earned its place on relevance grounds — elicit doesn't need to re-check that.

## Tracking what's been triaged

`curated/` grows continuously; re-reading all of it on every sync doesn't scale. Scope is `brief.md`'s `Draw from` field — only the `curated/` folder of each KB listed there (one `curated/` per KB), never a KB the brief doesn't name. Track progress in `triaged.md`, a sibling file in the piece-folder (see `_AI/shared/snippets/piece-folder.md`):

```markdown
- 2026-08-19 · [[debrief-2026-08-05-ian-final-questions]]
- 2026-08-19 · [[Ian Parrish interview 3 - transcript]]
```

One line per curated file: filename and the date it was triaged, nothing else. `guide.md`'s own per-bullet citations already show what was accepted from a given file; anything from a triaged file that isn't cited anywhere in `guide.md` was considered and dropped — no reason needs recording separately.

Rules:
- A file is either untouched or fully triaged, never partway. Read it once, extract every atomic claim it contains, run each through the Relevance filter, write the passing ones to their matching section, then append the file to `triaged.md`. Don't stop partway through a file just because the section you're populating already has enough.
- Curated files are append-only by convention — a correction arrives as a new debrief note, not an edit to the old one (see `_AI/local/workflows/debrief.md`). So once a file is listed in `triaged.md`, it never needs reconsidering; only filenames in `curated/` that aren't yet listed are candidates for triage.
- **Migrating a `guide.md` that predates `triaged.md`**: don't backfill the manifest from the guide's existing citations — the old build process searched for key points rather than triaging every file exhaustively, so a citation there doesn't mean the rest of that file was ever considered. Start `triaged.md` empty and do one full sweep across each Draw-from KB's `curated/` instead. But leave the guide's already-accepted content alone while doing this — the filter only gates newly-discovered material on a migration pass, it doesn't retroactively strip what's already there (some of which may already be written into `output.md`).

## Building (no guide.md yet)

Read the brief and write the scaffold — one heading per section, no content yet. Then triage every file in each Draw-from KB's `curated/` (per "Tracking what's been triaged" above): for each extractable claim, run it through the Relevance filter, and if it passes, lift the sentence and place it under whichever section it belongs to — never paraphrase from memory of the source. Use a claim's wiki page as a map to help decide which section it belongs under, but always cite the primary source the wiki page points to, not the wiki page's own prose (see the citation rule above). Where a point is genuinely the writer's own reasoning rather than something a source says, place it under Synthesis instead of inventing a citation for it.

## Syncing (guide.md exists)

On request — including when `_AI/shared/snippets/cross-workflow-check.md` offers it after a debrief or ingest adds new material to `curated/`: check `triaged.md`, triage only the files not yet listed there, and add any newly-passing extracted points to their matching section. Update in place — don't rebuild from scratch. If nothing in the newly-triaged files passes the Relevance filter, say so rather than manufacturing a point to fill the update.

Same citation rule applies on a sync as on a build: trace each new bullet to its primary source through the wiki page's citation, don't lift the wiki page's own wording as if it were the source.

## What this workflow doesn't do

Doesn't check a draft against the guide — that's `_AI/local/workflows/gap-check.md`. Doesn't judge whether the writer has a personal basis for a point — see the Relevance filter section above for that boundary with `_AI/local/workflows/elicit.md`.
