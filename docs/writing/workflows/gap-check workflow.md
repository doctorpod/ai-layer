---
tags: [ai-layer-docs]
sources:
  - vault/workflows/gap-check.md
  - vault/scripts/write-coverage.py
  - vault/scripts/check-assets.py
checked: 2026-09-26
---

# gap-check workflow

*Checks a draft against its guide, or any reference you name, reports what's missing, and records a [[coverage verdict]] on each note it checked.*

## When to reach for it

- You've drafted some or all of a piece and want to know what from the guide hasn't made it in.
- You want to see whether notes you marked `used` are still covered after edits.
- You want to check that every image in `assets/` is actually used.

## How to invoke

- `/gap-check`, or say "gap check `<file>`", "gap check `<file>` against `<reference>`", "check gaps in `<file>`" or "does `<file>` cover `<reference>`".
- From a [[scribe marker]] under, or naming, one section, which runs it for just that section.

## What it reads

- **Target:** the document being checked, usually the [[output draft]].
- **Reference:** whatever you name. Otherwise, if the target is in a piece folder, every [[gathered note]] in that folder's `guide/`, skipping `rejected` ones. If neither applies, it asks.
- The piece's `assets/` folder.

## What it writes

The `coverage` field on each note it checked, on every run, whether or not you ask. It uses one script call (`_AI/local/scripts/write-coverage.py`) and writes no other field.

## What it never touches

- The content of the target or the reference.
- `status`. That's always your call.
- A `rejected` note. The script also refuses to write one.
- The contents of `assets/`. It only checks whether they're referenced.
- On a scoped run, any note outside the scope. It never records a verdict on a note whose section it didn't read.

## How it works

1. **Target and reference.** Usually `output.md` against its `guide/`.
2. **Compare.** For each non-rejected note, it judges the note's whole body against the target: `full`, `thin` or `missing`. That judgement is independent of the note's `status`.
3. **Assets.** It runs `_AI/local/scripts/check-assets.py`, which flags any file in `assets/` whose filename doesn't appear in the target. A miss is a strong hint, not proof, because the draft might describe an image without naming the file. Before reporting a flagged file, it glances through the target for a mention of it by description.
4. **Report**, in chat. There are two short lists: notes that are `thin` or `missing`, and unreferenced assets. It also flags any `pending` note that came back `full`, which may mean you forgot to mark it `used`. Where a gap points at a passage, it cites the line number. There's no score.
5. **Record** every verdict to `coverage`.

## Worked example

You say "gap check parts/client/output.md". It replies:

- `Wet corner by the north gate floods every winter` is **thin**. `output.md:12` mentions standing water but not that it lasts November to March.
- `Swale above the wet corner` is **missing**.
- `Fruit for the school kitchen, not a showpiece` came back **full** but is still `pending`. Did you mean to mark it `used`?
- Asset `swale-section.png` is unreferenced.

It writes `coverage: thin`, `coverage: missing` and `coverage: full` onto those notes, and `full` onto any others it found covered. Their `status` is untouched. Your guide view now shows where the draft stands.

## Compared with…

- **[[diploma-ready workflow|diploma-ready]]**: both read without editing the draft. gap-check compares against the piece's own guide (or a reference you name), gives no overall verdict, and records coverage. diploma-ready walks the fixed Diploma rubric, gives a Yes / Nearly / Not Yet verdict, and writes nothing.
- **[[sanity workflow|sanity]]**: sanity checks whether the draft holds together, and gap-check checks whether it's complete.
- **[[beats workflow|beats]]**: beats plans a section from the notes before you write. gap-check checks the notes against what you wrote.

## Related

- [[coverage verdict]] · [[gathered note]] · [[guide view]]
- Workflow file: `_AI/local/workflows/gap-check.md`
