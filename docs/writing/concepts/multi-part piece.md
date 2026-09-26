---
tags: [ai-layer-docs]
sources:
  - shared/snippets/piece-folder.md
checked: 2026-09-26
---

# multi-part piece

*One deliverable built from several parts, each of which is a complete [[piece folder]] of its own.*

A multi-part piece has a `parts/` folder at its root, with one piece folder per part, and a `Makefile` that joins each part's `output.md` into `deliverables/`:

```
projects/hollin-lane/design-doc/
  Makefile         ← joins the parts' output.md files
  deliverables/    ← the assembled documents
  parts/
    client/        ← brief.md, guide/, output.md, assets/
    reflection/    ← brief.md, guide/, output.md, assets/
```

- The root has **no** `brief.md` or `guide/`. Each part has its own.
- Workflows don't know a part is nested. `/beats` pointed at `parts/reflection/` behaves exactly as it would on a single-part piece.
- Parts can share material by reference. A part's [[piece brief]] can name another part's `guide/` in its `Draw from` field rather than copying the notes across.
- A piece with only one deliverable stays a plain piece folder at the root. You only need `parts/` when there's more than one.

**Why split a piece?** Different parts are usually gathered in different ways. In the running example, the Hollin Lane client document is built from the site-walk debrief and the client's transcript with [[sync-guide workflow|sync-guide]], while the reflection section comes from your own memory through [[interview workflow|interview]]. Keeping them apart gives each its own brief, [[brief outline|outline]] and guide.

## Related

- [[piece folder]]
- [[gatherer]]
- [[writing/README|Writing workflows]]
