---
name: sync-guide
description: Build and maintain a piece's themes/ folder from its brief and the vault sources it draws on.
---

# Sync Guide

Triggered by: "sync guide", "sync the guide", "update the guide", "build the guide"

Builds a piece's `themes/` folder from `brief.md` by triaging its `Draw from` KBs' `curated/` folders against a relevance filter, and keeps it in sync as new material lands. This workflow only ever touches `themes/` — it never reads or writes `output.md`, and it doesn't set up the brief itself.

See `_AI/shared/snippets/piece-folder.md` for the file structure, brief.md fields, and location convention.

## Prerequisite: the brief

`brief.md` isn't built by this workflow — that's an ad hoc conversation, whenever the user wants help with it. If `brief.md` doesn't exist yet when this workflow is called, say so and offer to help draft it in chat, then stop. Don't start until the brief exists.

If `brief.md`'s `Format` field names a structured framework (e.g. GOBRADIMET), it must also have an `Outline` field — the resolved list of section headings. If `Format` names a framework but `Outline` is missing, stop and ask the user to supply it rather than inventing headings. `Outline`-less pieces (freeform writing, no framework) are fine — sections emerge from wherever the writer decides, ungated by this workflow.

## The theme model

`themes/` holds one file per **theme** — a small cluster of related **quotes** (1–3, usually 1), scoped to a single `Outline` section, plus optional **synthesis**. It is **extractive, not abstractive**: a quote is a lifted (verbatim or lightly trimmed) span, carried over with its own citation — never a freshly-composed sentence inspired by one. Freshly-composed sentences are where inaccuracy creeps in; copied ones can't drift from their source.

Lift from the **primary source**, not from the wiki page's prose. A wiki page is a map to sources, not itself a source — its own sentences can already be a synthesis across multiple sources, and lifting one faithfully just carries that synthesis into the theme with a false stamp of fidelity. Use the wiki page to find *which* source backs a claim (its footnote if the page cites more than one source, or its header `**Sources**:` field if it cites only one), then go read that source and lift from there.

If the wiki sentence can't actually be found in the source it's attributed to — the wiki has drifted, blended two sources, or the citation is stale — don't lift it anyway. Flag it to the user as a likely conflation and either fix the wiki page first or leave the point out until it's resolved.

**Concrete check before writing any citation**: if the quote you're about to write ends in `— [[site-overview]]` (a page under `wiki/`), stop — that's the map, not the source. Resolve the footnote or `**Sources**:` field for *that specific sentence* first, and cite what it points to instead. A citation pointing at a `wiki/` page is always wrong in this workflow.

### Theme note format

```markdown
---
categories: "[[Themes]]"
guide: "[[full/path/to/piece-folder/themes/INDEX|alias]]"
section: <Outline heading text>
status: pending
coverage:
tags:
  - ai-generated
---

**Quotes**
- "lifted sentence or clause, trimmed but not reworded" — [[primary-source]]

**Synthesis**
- reasoning built on the quotes above, no citation

**Comments**
```

- Filename: a short descriptive phrase naming the theme (3–8 words), not the source.
- `guide:` uses the full path to the piece's `themes/INDEX.md`, never a bare `[[INDEX]]` — the filename is reused across the vault.
- One citation per quote. If a point can't be traced to a specific sentence in a specific source, it doesn't belong in Quotes — put it under Synthesis instead, or leave it out until a source exists.
- If the source sentence carries a hedge, caveat, or correction, the quote must carry it too.
- `status` is `pending` (default), `used` (the writer has drawn on it in `output.md`), or `rejected` (the writer checked and decided they don't have a real basis for it). This workflow only ever writes `pending` on a new theme. Moving a theme to `used` or `rejected` is the writer's own call, made by hand, never inferred or set by this workflow.
- `status` is atomic per theme, not per quote. If this workflow appends a new quote to a theme currently marked `used`, it must revert `status` to `pending` and tell the user why — new material invalidates a prior review, even when the append itself was a confident match.
- `coverage` is set only by `gap-check`, never by this workflow. Leave blank on every new theme.
- Synthesis has no citation — that absence is the label. A theme's own quotes are its evidence; synthesis is the writer's read built on top of them. If a piece of reasoning doesn't hang off any single theme's quotes (a whole-section framework application, e.g. a permaculture zone assignment spanning the section), give it its own theme file with no Quotes block, just Synthesis — still scoped to one `section`.
- No Assets tracking here. The canonical asset list is the piece's `assets/` folder itself; checking each file there has a reference in `output.md` is `gap-check`'s job, not this workflow's.

## Relevance filter

Before a claim earns a quote, it has to pass one test: does it lead somewhere — a concrete decision, recommendation, or observation relevant to the brief? If not, drop it. Don't write it anywhere, not even as a plain fact. Admin decisions that aren't the writer's to make, and exact measurements nobody will act on, are the common failure case.

This filter applies to candidate quotes only. Synthesis isn't sourced from `curated/` in the first place, so nothing to filter.

This is narrower than the writer's own filter, applied later and by hand — whether they have a real basis for a surviving theme (noticed it, reacted to it, holds a genuine view), marked directly via `status`. Anything that reaches `themes/` has already earned its place on relevance grounds.

## Clustering a new quote into a theme

For each quote that passes the relevance filter, decide where it lands:

1. **Clear match to an existing theme in the same section** (same narrow topic — the same fact, decision, or observation the existing theme's quotes are already about): append it there.
   - If that theme's `status` is `used`, revert to `pending` and flag it to the user.
   - If `pending` or `rejected`, append silently, no flag needed.
2. **No existing theme fits**: create a new theme note, one quote, `status: pending`. This is the default case, not a judgment call — don't ask.
3. **Ambiguous** — plausibly fits two or more existing themes, or a borderline fit that could reasonably be its own theme instead: stop and ask the user which it should be. Don't guess.

Never merge two existing themes into one, and never split one theme into two — both are the writer's own call.

## Tracking what's been triaged

`curated/` grows continuously; re-reading all of it on every sync doesn't scale. Scope is `brief.md`'s `Draw from` field — only the `curated/` folder of each KB listed there, never a KB the brief doesn't name. Track progress in `triaged.md`, a sibling file in the piece-folder:

```markdown
- 2026-08-19 · [[debrief-2026-08-05-ian-final-questions]]
- 2026-08-19 · [[Ian Parrish interview 3 - transcript]]
```

One line per curated file: filename and the date it was triaged, nothing else. Existing theme citations already show what was accepted from a given file; anything from a triaged file not cited anywhere in `themes/` was considered and dropped — no reason needs recording separately.

Rules:
- A file is either untouched or fully triaged, never partway. Read it once, extract every atomic claim it contains, run each through the Relevance filter and Clustering above, then append the file to `triaged.md`. Don't stop partway through a file just because the section you're populating already has enough.
- **If a paired debrief exists, triage it together with its raw source, not separately.** If the file being triaged is a raw inbox source rather than a debrief note, check `curated/` for a paired debrief note first. If none exists, triage the raw file on its own. If the debrief exists, read both before writing any quotes — it often corrects a misheard name, a misspoken fact, or an ambiguous claim in the raw source. Process the pair as one atomic pass, each still getting its own `triaged.md` line, but neither counts as triaged until both are done.
- Curated files are append-only by convention — a correction arrives as a new debrief note, not an edit to the old one. Once a file is listed in `triaged.md`, it never needs reconsidering.

## Batching a large backlog

Before triaging, count how many files across the Draw-from KBs' `curated/` folders aren't yet listed in `triaged.md`. If it's more than a handful, or several are large (a full interview transcript or article, not a short debrief), don't attempt them all in one pass — propose a batch and ask whether to run it now or pick up more later.

Order the batch largest/densest first — interview transcripts and long articles before short debriefs and reconfirmation notes.

Triage and write up one file completely before moving to the next, appending to `triaged.md` as each finishes. Stopping between files at the end of a batch loses nothing — only stopping mid-file does.

## Building (no themes/ yet)

Read the brief, including its `Outline`. Create `themes/INDEX.md` if it doesn't exist:

```markdown
---
aliases:
  - guide - <piece name>
---
![[themes.base]]
```

No per-section scaffolding needed — `themes.base` groups by each theme's `section` field automatically. Then triage every file in each Draw-from KB's `curated/` (per "Tracking what's been triaged" and "Batching a large backlog" above), running each extractable claim through the Relevance filter and Clustering above, filing it under whichever `Outline` section it belongs to.

## Syncing (themes/ exists)

On request: check `triaged.md`, then triage the files not yet listed there — following "Batching a large backlog" above if there are many — and cluster any newly-passing quotes per "Clustering a new quote into a theme." If nothing in the newly-triaged files passes the Relevance filter, say so rather than manufacturing a theme to fill the update.

Same citation rule applies on a sync as on a build.

## Migrating a piece from the old flat `guide.md`

Read `guide.md` in full. For each section, split its Extracted points into themes per "Clustering a new quote into a theme" above (existing adjacent bullets citing the same narrow fact are usually one theme already) — carry over each bullet's existing `PENDING`/`USED`/`REJECTED` tag as that theme's `status` (a theme is `used` only if every bullet folded into it was `USED`; if mixed, split rather than blend). Carry Synthesis bullets to whichever theme they reason about, or their own synthesis-only theme if section-wide. Drop the section's `Assets` line and its `✓`/`⚠` marker — the marker is superseded by `status`/`coverage` in `themes.base`; assets are tracked via the `assets/` folder instead. Once every section is migrated, delete `guide.md`.

## What this workflow doesn't do

Doesn't check a draft against the themes — that's `gap-check`. Doesn't judge whether the writer has a personal basis for a theme — that's the writer's own call, made directly via `status`, not a filter this workflow applies. Doesn't touch `coverage` — that's `gap-check`'s field. Doesn't track assets — that's the `assets/` folder plus `gap-check`.
