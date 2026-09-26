---
tags: [ai-layer-docs]
sources:
  - shared/snippets/piece-folder.md
  - vault/workflows/sync-guide.md
  - vault/workflows/interview.md
  - docs/PATTERNS.md
checked: 2026-09-26
---

# gatherer

*A workflow that fills a [[guide folder]] with [[gathered note|gathered notes]], so that writing can happen.*

A gatherer is defined by what it produces (notes that meet the gathered-note contract), not by how it gathers. The workflows that read `guide/` never need to know which gatherer ran.

There are two:

| Gatherer | Gathers by | Material comes from |
|---|---|---|
| [[sync-guide workflow\|sync-guide]] | extracting quotes | vault sources, via the `curated/` folders of the knowledge bases in `Draw from` |
| [[interview workflow\|interview]] | eliciting answers | you, checked against the [[interview timeline]] |

The readers are [[beats workflow|beats]], [[elicit workflow|elicit]], [[gap-check workflow|gap-check]] and the [[guide view]].

A part can use both gatherers. They share the [[triage log]], each reading only its own lines.

For why the writing tools are shaped this way, see the Gatherer pattern in [[PATTERNS]].

## Related

- [[gathered note]]
- [[guide folder]]
- [[multi-part piece]]
