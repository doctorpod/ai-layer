---
tags: [ai-layer-docs]
sources:
  - shared/snippets/piece-folder.md
  - vault/workflows/sync-guide.md
  - vault/workflows/interview.md
  - vault/workflows/elicit.md
  - vault/workflows/beats.md
checked: 2026-09-26
---

# piece brief

*The `brief.md` file in a [[piece folder]]: the seed that says what the piece is, who it's for, and where its material comes from.*

You write the brief. No workflow owns it. If you want help, ask in chat and the assistant will ask questions or tidy your rough notes into the fields, but the brief stays yours.

## Fields

| Field | What goes in it |
|---|---|
| **What** | Working title and format |
| **For** | Audience and context |
| **Angle** | Point of view, argument or tone |
| **Draw from** | Which knowledge bases or vault pages to pull material from. It can name another part's `guide/` to share material, and it can say *how* material is gathered (e.g. "interview, anchored on `timeline.md`"). That second part is for people to read; no workflow acts on it. |
| **Must haves** | Key points that must appear |
| **Must nots** | Things to avoid |
| **Format** | The structure or framework the piece follows, if any |
| **Outline** | The resolved list of section headings. Required when `Format` names a framework. See [[brief outline]]. |

## Which workflows need it

[[sync-guide workflow|sync-guide]], [[interview workflow|interview]], [[elicit workflow|elicit]] and [[beats workflow|beats]] all expect the brief to exist, and stop if it doesn't. sync-guide also offers to help you draft it in chat. The checkers ([[gap-check workflow|gap-check]], [[sanity workflow|sanity]], [[diploma-ready workflow|diploma-ready]]) work on the draft and don't need a brief, although diploma-ready will read the Outline if it has to.

- [[sync-guide workflow|sync-guide]] reads `Draw from` to decide which knowledge bases' `curated/` folders to triage, and `Outline` to know which sections to file notes under. It stops if `Format` names a framework but `Outline` is missing.
- [[interview workflow|interview]] needs an `Outline`, full stop, because each thread note is filed under one of its sections. It builds the [[interview timeline]] from the sources in `Draw from`.

## Example

The brief for the Hollin Lane client part, in `projects/hollin-lane/design-doc/parts/client/brief.md`:

```markdown
- **What** — Hollin Lane community orchard: design report
- **For** — Maggie Thorne and the Hollin Lane Residents' Group; also my Diploma tutor
- **Angle** — a low-maintenance orchard the group can run with volunteers
- **Draw from** — the `hollin-lane` knowledge base
- **Must haves** — the wet corner; a plan the school kitchen can use
- **Must nots** — no pond (insurance won't cover it)
- **Format** — headed sections loosely following GOBRADIMET
- **Outline** — 01 Goals · 02 Observation · 06 Design · …
```

## Related

- [[brief outline]]
- [[piece folder]]
- [[assessment rubric]]
