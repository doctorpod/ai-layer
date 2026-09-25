Every piece of writing lives in a named folder with four predictable contents:

```
[piece-folder]/
  brief.md     ← the seed
  guide/       ← gathered material — notes of a fixed shape, however they were gathered (INDEX.md + one file per note)
  output.md    ← the finished prose
  assets/      ← images, maps, diagrams
```

## Multi-part pieces

When one deliverable is assembled from several parts (e.g. a client document plus an assessment-only section), each part is its own self-contained piece-folder, and the root holds only the assembly:

```
[piece-root]/
  Makefile         ← joins the parts' output.md files into deliverables/
  deliverables/    ← the assembled documents
  parts/
    client/        ← a piece-folder: brief.md, guide/, output.md, assets/
    reflection/    ← another piece-folder
```

- No top-level `brief.md` or `guide/` — each part has its own.
- Tools act on a piece-folder and never need to know it's nested. Pointing a workflow at `parts/reflection/` is the same as pointing it at a single-part piece.
- A single-deliverable piece stays a plain piece-folder at the root, as above.

## brief.md fields

- **What** — working title and format
- **For** — audience and context
- **Angle** — point of view, argument, or tone
- **Draw from** — which knowledge bases or vault pages to pull from. May name another part's `guide/` when two parts need the same material — share by reference rather than copying. May also say *how* material is gathered as well as where from (e.g. "interview, anchored on `timeline.md`"); that's for people to read, and no workflow dispatches on it.
- **Must haves** — key points that must appear
- **Must nots** — things to avoid
- **Format** — structure or framework the piece follows, if any (e.g. "headed sections loosely following GOBRADIMET")
- **Outline** — required if `Format` names a structured framework: the resolved list of section headings, each tagged with its position in that framework. Omit entirely for freeform pieces. See `_AI/local/workflows/sync-guide.md`, which reads this to know what sections to build.

The user writes this. A workflow may help draft it on request — by asking questions or tidying rough notes into these fields — but does not own it.

## Gathered material (`guide/`)

`guide/` holds the material a piece is written from. A workflow that fills it is a **gatherer**; every gatherer writes notes to the same contract, so the workflows that read `guide/` (`beats`, `gap-check`, `elicit`, and the `guide.base` view) never need to know which gatherer produced a note.

Every gathered note carries this frontmatter:

```yaml
---
categories: "[[Themes]]"
guide: "[[full/path/to/piece-folder/guide/INDEX|alias]]"
section: <Outline heading text>
status: pending
coverage:
---
```

- `categories` and `guide` are what `guide.base` filters on — a note without them is invisible in the view. `guide:` uses the full path to this piece-folder's `guide/INDEX.md`, never a bare `[[INDEX]]`.
- `section` is the `Outline` heading the note belongs to, in the same form `sync-guide` writes it. **One note, one section** — material that belongs to two sections goes in two notes.
- `status` is `pending` on creation. `used` and `rejected` are the writer's own call, set by hand — see `sync-guide.md` for the full semantics, including when a gatherer reverts `used` to `pending`.
- `coverage` is left blank on creation and written only by `gap-check`. The blank line must be there: `gap-check`'s script only replaces an existing `coverage:` line.
- The body, and any fields beyond these five (e.g. `tags`, `date`, `thread`), belong to the gatherer. Consumers read the note's whole body as its content.

Current gatherers: `_AI/local/workflows/sync-guide.md` (extracts quotes from vault sources) and `_AI/local/workflows/interview.md` (elicits verbatim answers from the writer).

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

Some workflows keep additional working files inside the piece-folder beyond the four above. These aren't part of the core convention — see the owning workflow for format and lifecycle.

- `triaged.md` — an append-only log of inputs a gatherer has finished with. Shared by both gatherers, each with its own line format and each reading only its own lines: `_AI/local/workflows/sync-guide.md` lists the `curated/` files it's considered; `_AI/local/workflows/interview.md` lists the threads it's closed or dropped.
- `timeline.md` — dated evidence mined from the record, which `_AI/local/workflows/interview.md` checks answers against. Evidence, not gathered material: it lives beside `brief.md`, not in `guide/`, and nothing reads it as a note.
