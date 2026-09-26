---
tags: [ai-layer-docs]
sources:
  - vault/workflows/sanity.md
checked: 2026-09-26
---

# sanity workflow

*Reads your own writing and flags contradictions, non-sequiturs and passages that don't hold up. It never edits anything.*

## When to reach for it

You want to know whether a piece of writing actually makes sense: whether the claims agree with each other and the conclusions follow. Spelling and punctuation are [[polish workflow|polish]]'s job.

## How to invoke

- `/sanity`, or say "sanity", with a scope: one document ("sanity output.md"), several, or a range ("sanity my log notes from the last three weeks", "sanity the last 5 entries").
- From a [[scribe marker]]: `% scribe sanity`.

There's no default scope. If yours is unclear, it asks.

## What it reads

Everything in scope, read in full.

## What it writes

Nothing, by default. Findings come back in chat, or in the scribe block's comments. If you ask, it will record them as a log note or pass them to add-to-radar, but only on request.

## What it never touches

The writing it checks, or anything else. It names the problem and leaves the fix to you, in your own words.

## How it works

1. It settles the scope.
2. It reads everything in it.
3. It looks for what's actually there, without working through a fixed checklist: **contradictions** (within the scope, or against something the scope refers to), **non-sequiturs**, **confusing passages** and **plain bad writing**. It prefers one sharp finding to a padded list.
4. It reports a short numbered list. Each finding gives the file and **line number**, a short quote to anchor it, and what's wrong. It never refers to paragraph numbers.

## Worked example

You say "sanity parts/client/output.md". It replies:

1. `output.md:34` "the north gate stays dry in summer" contradicts `output.md:12` "standing water most of the year".
2. `output.md:58` "so a swale is the obvious choice": nothing before this rules out a pond or drainage, so the conclusion doesn't follow.

It doesn't touch the file. You fix both yourself.

## Compared with…

- **[[polish workflow|polish]]**: polish never comments on content, and sanity never touches prose.
- **[[gap-check workflow|gap-check]]**: sanity asks whether the draft holds together on its own terms. gap-check asks whether it covers the guide.
- **reflect**: also reviews a set of notes, but looks for patterns and open loops rather than faults. Sanity doesn't assume a time range the way reflect does.

## Related

- [[output draft]] · [[scribe marker]]
- Workflow file: `_AI/local/workflows/sanity.md`
