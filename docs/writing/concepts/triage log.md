---
tags: [ai-layer-docs]
sources:
  - shared/snippets/piece-folder.md
  - vault/workflows/sync-guide.md
  - vault/workflows/interview.md
  - docs/PATTERNS.md
checked: 2026-09-26
---

# triage log

*The `triaged.md` file in a [[piece folder]]: an append-only list of the inputs a [[gatherer]] has finished with.*

It records the one thing the notes can't show you: an input that was looked at and dropped. Without the log, it would be offered again next time. Current state (what's in `guide/`, which threads are open) is always read from the notes themselves.

Both gatherers share the file. Each writes its own kind of line and reads only its own lines.

## sync-guide's lines: sources triaged

```markdown
- 2026-03-21 · [[debrief-2026-03-14-site-walk]]
- 2026-03-21 · [[Maggie Thorne interview 1 - transcript]]
```

One line per `curated/` file: the date and the file, nothing else. A file is either untouched or fully triaged, never partway through. Anything in a triaged file that isn't quoted somewhere in `guide/` was considered and dropped. [[sync-guide workflow|sync-guide]] never reconsiders a listed file, because curated files don't change. Corrections arrive as new debrief notes.

## interview's lines: threads closed or dropped

```markdown
- 2026-09-12 · thread 1 · [[01 choosing the framework]] · closed
- 2026-09-19 · thread 3 · working with volunteers · dropped
```

One line per thread, ever, written the first time it's closed or dropped. A reopened thread doesn't get a second line. [[interview workflow|interview]] never proposes a logged thread as a new one. See [[interview thread]].

## Related

- [[gatherer]]
- [[interview thread]]
- [[PATTERNS]], for the "log inputs, derive the rest" pattern behind this file
