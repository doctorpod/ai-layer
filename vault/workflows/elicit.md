---
name: elicit
description: Read a section's theme notes and spit out tickler ideas and questions to spark writing — a single-shot brainstorm, not drafted prose.
---

# Elicit Workflow

Triggered by: "elicit", "elicit section `<N>`", "grill me on section `<N>` of the guide" — standalone in chat, or invoked by name from inside a `% scribe` marker (`_AI/local/workflows/scribe.md`), same as `polish`.

## Prerequisites

Piece-folder convention (`_AI/shared/snippets/piece-folder.md`): `brief.md`, `guide/`, `output.md`. If `brief.md` doesn't exist yet, that's an ad hoc conversation (see `_AI/local/workflows/sync-guide.md`'s own Prerequisite note). If `brief.md` exists but `guide/` doesn't (and there's no flat `guide.md` either), point to `_AI/local/workflows/sync-guide.md` to build it first.

If the piece-folder still has a flat `guide.md` instead of a `guide/` folder (not yet migrated — see `sync-guide.md`), read its bullets in scope instead of theme notes; everything else below applies the same way.

## Doing the work

1. Read the theme notes in scope — every theme in the named `guide/` section, or the specific theme notes pointed to. Each theme's Quotes and Synthesis together are the material to work from.
2. Produce a single-shot brainstorm: odd angles, provocations, questions that might spark a sentence. Bullet points only.
3. One pass. No follow-up questions, no back-and-forth.

## Output

Elicit never writes a file itself. Show the ideas in chat when invoked directly. When invoked from a `% scribe` marker, the result goes into that block's `% **comments**`, per scribe's own convention.
