---
name: sync-guide
description: Build and maintain a piece's guide.md from its brief and the vault sources it draws on.
---

# Sync Guide

Triggered by: "sync guide", "sync the guide", "update the guide", "build the guide"

Builds `guide.md` from `brief.md`, and keeps it in sync as new vault material becomes relevant. This workflow only ever touches `guide.md` — it never reads or writes `output.md`, and it doesn't set up the brief itself.

See `_AI/shared/snippets/piece-folder.md` for the file structure, brief.md fields, and location convention.

## Prerequisite: the brief

`brief.md` isn't built by this workflow — that's an ad hoc conversation, whenever the user wants help with it. If `brief.md` doesn't exist yet when this workflow is called, say so and offer to help draft it in chat, then stop. Don't start the guide until the brief exists.

## The guide template

`guide.md` is not prose — it's a structured scaffold, one heading per document section. It is **extractive, not abstractive**: a bullet is a lifted (verbatim or lightly trimmed) span, carried over with its own citation — never a freshly-composed sentence inspired by one. Freshly-composed sentences are where inaccuracy creeps in; copied ones can't drift from their source.

Lift from the **primary source**, not from the wiki page's prose. A wiki page is a map to sources, not itself a source — its own sentences can already be a synthesis across multiple sources, and lifting one faithfully just carries that synthesis into the guide with a false stamp of fidelity. Use the wiki page to find *which* source backs a claim (its footnote if the page cites more than one source, or its header `**Sources**:` field if it cites only one), then go read that source and lift from there.

If the wiki sentence can't actually be found in the source it's attributed to — the wiki has drifted, blended two sources, or the citation is stale — don't lift it anyway. Flag it to the user as a likely conflation and either fix the wiki page first or leave the point out of the guide until it's resolved. Finding one of these is a sign the fix is working, not a distraction from the guide-building task.

Under each heading:

**Extracted points** — one bullet per atomic claim, each with its own source:
- `"lifted sentence or clause, trimmed but not reworded" — [[primary-source]]`, where `primary-source` is the curated file, debrief note, or external source the wiki page cites for that claim — not the wiki page itself
- If the source sentence carries a hedge, caveat, or correction (an inline qualifier like "unconfirmed," "likely a misspeak," or a `> [!caution]` callout), the bullet must carry it too. Never cite a claim while dropping the caveat attached to it in the source.
- One citation per bullet. If a point can't be traced to a specific sentence in a specific source, it doesn't belong here — put it under Synthesis, or leave it out until a source exists.

**Synthesis** — reasoning, design implications, or Andy's own read, built on top of the extracted points above but not lifted from any source. No citation, because none exists — that absence is the label. Keep this visually separate from Extracted points; never let a synthesis bullet sit unmarked among sourced ones.

**Assets** — any assets needed, tied to their purpose.

Don't pool sources at the bottom of a section. Per-bullet citation makes the section's source list a byproduct (derivable by scanning the bullets), not something authored separately that can drift out of sync or omit a source in use.

## Building (no guide.md yet)

Read the brief, search the relevant knowledge bases, and write the scaffold — one heading per section. For each key point, find the wiki page, follow its citation to the primary source, and lift the sentence from there — never paraphrase from memory of the wiki page or the source. Where a point is genuinely the writer's own reasoning rather than something a source says, place it under Synthesis instead of inventing a citation for it.

## Syncing (guide.md exists)

On request, or when new vault material becomes relevant: expand a section, add newly-relevant extracted points, surface more vault material. Update in place — don't rebuild from scratch. Resist the urge to add a bullet just because a sync was requested — if a source genuinely has nothing new for a section, say so rather than manufacturing a point to fill the update.

Same rule applies on a sync as on a build: trace each new bullet to its primary source through the wiki page's citation, don't lift the wiki page's own wording as if it were the source.

## What this workflow doesn't do

Doesn't check a draft against the guide — that's `_AI/local/workflows/gap-check.md`.
