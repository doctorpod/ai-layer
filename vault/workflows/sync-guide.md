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

`guide.md` is not prose — it's a structured scaffold, one heading per document section. It is **extractive, not abstractive**: a bullet is a lifted (verbatim or lightly trimmed) span from a wiki page, carried over with its own citation — never a freshly-composed sentence inspired by one. Freshly-composed sentences are where inaccuracy creeps in; copied ones can't drift from their source.

Under each heading:

**Extracted points** — one bullet per atomic claim, each with its own source:
- `"lifted sentence or clause, trimmed but not reworded" — [[source-page]]`
- If the source sentence carries a hedge, caveat, or correction (an inline qualifier like "unconfirmed," "likely a misspeak," or a `> [!caution]` callout), the bullet must carry it too. Never cite a claim while dropping the caveat attached to it in the source.
- One citation per bullet. If a point can't be traced to a specific sentence in a specific source, it doesn't belong here — put it under Synthesis, or leave it out until a source exists.

**Synthesis** — reasoning, design implications, or Andy's own read, built on top of the extracted points above but not lifted from any source. No citation, because none exists — that absence is the label. Keep this visually separate from Extracted points; never let a synthesis bullet sit unmarked among sourced ones.

**Assets** — any assets needed, tied to their purpose.

Don't pool sources at the bottom of a section. Per-bullet citation makes the section's source list a byproduct (derivable by scanning the bullets), not something authored separately that can drift out of sync or omit a source in use.

## Building (no guide.md yet)

Read the brief, search the relevant knowledge bases, and write the scaffold — one heading per section. For each key point, find the specific source sentence and lift it rather than paraphrasing from memory of the source. Where a point is genuinely the writer's own reasoning rather than something a source says, place it under Synthesis instead of inventing a citation for it.

## Syncing (guide.md exists)

On request, or when new vault material becomes relevant: expand a section, add newly-relevant extracted points, surface more vault material. Update in place — don't rebuild from scratch. Resist the urge to add a bullet just because a sync was requested — if a source genuinely has nothing new for a section, say so rather than manufacturing a point to fill the update.

## What this workflow doesn't do

Doesn't check a draft against the guide — that's `_AI/local/workflows/gap-check.md`.
