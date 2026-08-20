Every piece of writing lives in a named folder with four predictable contents:

```
[piece-folder]/
  brief.md     ← the seed
  guide.md     ← section-by-section scaffold, built from the brief
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

Some workflows keep additional working files inside the piece-folder beyond the four above. E.g. `_AI/local/workflows/elicit.md` keeps a `section-<N>.md` per section (threads, prompts, draft-in-progress) until it's published into `output.md`, then leaves it in place as a record. `_AI/local/workflows/sync-guide.md` keeps `triaged.md`, a running list of which `curated/` files it's already considered for this piece. These aren't part of the core convention — see the owning workflow for format and lifecycle.
