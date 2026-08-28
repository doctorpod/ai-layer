Every piece of writing lives in a named folder with four predictable contents:

```
[piece-folder]/
  brief.md     ← the seed
  guide/       ← quote/theme/synthesis scaffold, built from the brief (INDEX.md + one file per theme)
  output.md    ← the finished prose
  assets/      ← images, maps, diagrams
```

## brief.md fields

- **What** — working title and format
- **For** — audience and context
- **Angle** — point of view, argument, or tone
- **Draw from** — which knowledge bases or vault pages to pull from
- **Must haves** — key points that must appear
- **Must nots** — things to avoid
- **Format** — structure or framework the piece follows, if any (e.g. "headed sections loosely following GOBRADIMET")
- **Outline** — required if `Format` names a structured framework: the resolved list of section headings, each tagged with its position in that framework. Omit entirely for freeform pieces. See `_AI/local/workflows/sync-guide.md`, which reads this to know what sections to build.

The user writes this. A workflow may help draft it on request — by asking questions or tidying rough notes into these fields — but does not own it.

## Location

- Project deliverables (design reports, client docs): inside the project folder, e.g. `projects/my-project/design-doc/`
- General writing (articles, posts, essays): in a `writing/` root folder if it exists

## output.md frontmatter

```yaml
---
title: [piece title]
status: in progress
last_updated: YYYY-MM-DD
---
```

## Workflow-owned scratch files

Some workflows keep additional working files inside the piece-folder beyond the four above. E.g. `_AI/local/workflows/sync-guide.md` keeps `triaged.md`, a running list of which `curated/` files it's already considered for this piece. These aren't part of the core convention — see the owning workflow for format and lifecycle.
