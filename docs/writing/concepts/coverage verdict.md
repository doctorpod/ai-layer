---
tags: [ai-layer-docs]
sources:
  - vault/workflows/gap-check.md
  - vault/scripts/write-coverage.py
  - shared/snippets/piece-folder.md
  - docs/PATTERNS.md
checked: 2026-09-26
---

# coverage verdict

*The `coverage` field on a [[gathered note]]: whether the draft covers that note `full`, `thin` or `missing`, as last judged by [[gap-check workflow|gap-check]].*

- **`full`**: the draft covers the note.
- **`thin`**: the draft touches it, but not enough.
- **`missing`**: the draft doesn't cover it.
- Blank: gap-check hasn't judged it yet.

## How it's written

gap-check records a verdict on every note it checks, on every run. You don't opt in. It writes them all in one call to a script, `_AI/local/scripts/write-coverage.py`, which:

- replaces only the existing `coverage:` line, leaving the rest of the frontmatter as it was. That's why every new note must carry an empty `coverage:` line: a note without one is skipped;
- refuses to write onto a note marked `status: rejected`;
- accepts only `full`, `thin` or `missing`, and writes nothing at all if any argument is invalid.

No other workflow writes `coverage`, and gap-check writes no other field.

## What it tells you, and what it doesn't

The note is judged as a whole, never quote by quote, just as `status` applies to the whole note.

`coverage` is a measurement, and `status` is your judgement. They're independent, and it's worth noticing when they disagree:

- `used` but `thin` or `missing`: the draft has probably changed since you used the note.
- `pending` but `full`: you may have covered it without realising, or forgotten to mark it `used`.

A verdict can go stale as the draft changes. It's only as current as the last gap-check run, and rerunning refreshes it. It's stored rather than recalculated because rerunning the check just to fill the [[guide view]] would cost too much.

A run scoped to one section writes verdicts only for notes in that section, so a scoped run and a whole-document run agree on any note they both check.

## Related

- [[gap-check workflow]]
- [[gathered note]]
- [[PATTERNS]], where `coverage` is the named exception to "log inputs, derive the rest"
