---
tags: [ai-layer-docs]
sources:
  - shared/snippets/piece-folder.md
checked: 2026-09-26
---

# piece folder

*The folder a piece of writing lives in, with the same four things inside every time.*

A piece folder is any folder holding a `brief.md`, a `guide/` folder, an `output.md` and an `assets/` folder. The folder name is yours to choose.

```
hollin-lane/design-doc/parts/client/
  brief.md     ← what the piece is and who it's for
  guide/       ← the material you'll write from
  output.md    ← the prose itself
  assets/      ← images, maps, diagrams
```

- `brief.md` is the [[piece brief]]. You write it.
- `guide/` is the [[guide folder]]. [[gatherer|Gatherers]] fill it.
- `output.md` is the [[output draft]]. You write it.
- `assets/` holds images, maps and diagrams. [[gap-check workflow|gap-check]] checks that each one is referenced in the draft.

Some workflows keep their own working files alongside these four: the [[triage log]] (`triaged.md`) and the [[interview timeline]] (`timeline.md`). They sit beside `brief.md`, not inside `guide/`.

**Where piece folders go.** Project deliverables such as design reports and client documents sit inside the project folder, e.g. `projects/hollin-lane/design-doc/`. General writing (articles, posts, essays) goes in a `writing/` folder at the vault root, if there is one.

**One deliverable, several parts.** When a document is assembled from several self-contained parts, each part is its own piece folder. See [[multi-part piece]].

Every writing workflow acts on a piece folder. Pointing a workflow at a part of a multi-part piece is the same as pointing it at a single piece.

## Related

- [[multi-part piece]]
- [[piece brief]]
- [[guide folder]]
- [[output draft]]
- [[writing/README|Writing workflows]]
