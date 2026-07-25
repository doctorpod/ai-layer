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

`guide.md` is not prose — it's a structured scaffold, one heading per document section. Under each heading:
- Key points to hit
- Vault sources to draw from, as `[[wikilinks]]`
- Any assets needed, tied to their purpose

## Building (no guide.md yet)

Read the brief, search the relevant knowledge bases, and write the scaffold — one heading per section, sourced ideas and vault connections under each.

## Syncing (guide.md exists)

On request, or when new vault material becomes relevant: expand a section, add newly-relevant sources, surface more vault material. Update in place — don't rebuild from scratch.

## What this workflow doesn't do

Doesn't check a draft against the guide — that's `_AI/local/workflows/gap-check.md`.
