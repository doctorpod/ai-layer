---
tags: [ai-layer-docs]
sources:
  - shared/snippets/piece-folder.md
  - vault/workflows/sync-guide.md
  - vault/workflows/interview.md
  - vault/workflows/diploma-ready.md
checked: 2026-09-26
---

# brief outline

*The `Format` and `Outline` fields of a [[piece brief]]: the framework a piece follows and its resolved list of section headings.*

- **`Format`** names the structure, e.g. "headed sections loosely following GOBRADIMET". Leave it empty for freeform writing.
- **`Outline`** is the list of actual section headings, each tagged with its place in the framework. It is required as soon as `Format` names a structured framework. Leave it out for freeform pieces.

## Why the headings matter

The Outline headings become the `section:` values on [[gathered note|gathered notes]], so they tie the whole piece together:

- [[sync-guide workflow|sync-guide]] files each note under one Outline section. If `Format` names a framework and there's no Outline, it stops and asks you for one rather than inventing headings. With no framework, sections emerge as you write.
- [[interview workflow|interview]] won't run without an Outline, because every thread note needs a section.
- [[beats workflow|beats]], [[elicit workflow|elicit]] and [[gap-check workflow|gap-check]] pick notes by matching `section:`, so "beats section 02" means "every note whose `section:` is the 02 heading".
- [[diploma-ready workflow|diploma-ready]] reads the Outline to work out which design framework you used when that isn't obvious from the draft.

Write the heading text the same way everywhere, e.g. `02 Observation`. The `section:` field on a note is matched against it exactly.

## Example

The Hollin Lane client part follows GOBRADIMET:

```markdown
- **Format** — headed sections loosely following GOBRADIMET
- **Outline**
  - 01 Goals (G)
  - 02 Observation (O)
  - 06 Design (D)
```

The reflection part is freeform in voice but still needs an Outline, because it's gathered by interview:

```markdown
- **Outline**
  - 01 Choosing a framework
  - 02 What I'd do differently
```

## Related

- [[piece brief]]
- [[gathered note]]
