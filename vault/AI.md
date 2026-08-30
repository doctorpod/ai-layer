# AI Context

- This is the `_AI/local/` folder. I shall refer to the parent folder (the folder you've been given access to) as **the vault**.
- Chats live in `_AI/chats/`
- Logs live in `_AI/logs/`
- Scripts live in `_AI/local/scripts/`
- Workflows live in `_AI/local/workflows/` (vault-specific) and `_AI/shared/workflows/` (shared)

## Setup files

These files live in `_AI/` and are created by the vault owner during setup. Read them for context before starting work:

- `_AI/GOALS.md` — goals and focus areas for this vault
- `_AI/CONVENTIONS.md` — vault-specific operating conventions not covered elsewhere *(optional)*

If `_AI/GOALS.md` is missing, alert the user.

## Obsidian CLI

The `obsidian` CLI is available when the Obsidian app is running with this vault open. See `_AI/local/OBSIDIAN-CLI.md` for commands that are cheaper than Grep/Read/mv for search, link-graph queries, and file moves.

## Read & write access

- You may READ any file recursively in the vault
- Your WRITE access is limited to:
	- `_AI/chats/`
	- `_AI/logs/`
	- Any folder named `wiki/`
	- Any folder named `assets/`
	- Any file named `INDEX.md`
	- Any note with `categories: ["[[Glossary]]"]` in its frontmatter (concept notes)
	- The `coverage` frontmatter field *only* on guide theme notes (`categories: "[[Themes]]"`), and *only* via the gap-check workflow's `write-coverage.py` — never any other field, never `status`
	- Any file named `QUESTIONS.md`
	- Any file named `SPATIAL.md`
	- Any file named `DASHBOARD.md`
	- Any folder named `_greenhouse/`
	- Any folder named `_wayfinder/`
	- Any folder named `_AI/postmortems/`
	- Any file named `_AI/learnings.md`
	- The single `inbox/` at the vault root, but only to create web-stub files (`tags` includes `web-stub`) — not to write full ingest source content directly
	- You may move files to any folder named `curated/`
- If you ever need to write anywhere else, ask my permission first.

## Content provenance

- Any note carrying `ai-generated` in its frontmatter `tags` was authored by you (the assistant) in a past session — not by the vault owner.
- This is expected and by design wherever the workflow's job *is* to build AI-authored content (knowledge-base `wiki/` pages, guides, etc.) — no special handling needed there.
- The risk is specific to workflows that synthesize across the owner's *personal* notes (journal, reflections, radar, and similar) and report back what they contain. There, never surface `ai-generated` content as if it were the owner's own thinking, memory, or lived experience — either exclude it, or explicitly flag it as previously AI-generated when you draw on it.

## Knowledge bases

- Within this vault, there are folders which I call **knowledge bases**.
- You will help me build specific domain knowledge within these folders.
- Knowledge bases are any folder containing a `wiki/` subfolder — the lint script discovers them automatically.
- New sources are not filed per-KB. They all go into a single `inbox/` at the vault root; the ingest workflow routes each one to the KB it belongs in (see `_AI/local/workflows/ingest.md`, Step 0a).
- Knowledge bases contain the following subfolders and files:
	- `curated/` — You move files here once ingested
	- `wiki/` — You build a wiki here
	- `assets/` — Images downloaded during ingest; gitignored
	- `INDEX.md` — You keep this updated
	- `AI.md` — Optional: specific instructions for this knowledge base
	- concept notes — any note with `categories: ["[[Glossary]]"]` frontmatter; queryable via Dataview
	- `QUESTIONS.md` — Optional: outstanding questions requiring follow-up
	- `SPATIAL.md` — Optional: named-feature location index *(only for KBs with a physical site)*

### SPATIAL.md format

Flat alphabetical list. One-line header naming the reference point. Each entry:

```
**feature name** — [position relative to reference point]. One sentence of context.
```

Example:
```
All directions are relative to the church building.

**Celtic cross** — southwest boundary, near the fence. A ~4m carved stone cross; a strong positive sight line.
**vestry** — south flank of the church, eastern end. Shows signs of subsidence; a growing crack in the wall.
```

## Workflows

When my request matches a trigger below, read and follow the corresponding workflow file.

| Trigger | Workflow |
|---|---|
| "validate AI setup", "check AI setup" | `_AI/shared/workflows/validate-ai-setup.md` |
| "ingest" (optionally naming a knowledge base) | `_AI/local/workflows/ingest.md` |
| "lint" or "audit" + knowledge base name | `_AI/local/workflows/lint.md` |
| "process notes" + scope | `_AI/local/workflows/process-notes.md` — proposes folder moves and category fixes against vault conventions, applies on confirmation |
| "connect" or "find cross-knowledge base insights" | `_AI/local/workflows/connect.md` |
| "update the summary in `<note>`", "update summary", "refresh the summary for `<note>`" | `_AI/local/workflows/create-summaries.md` — pulls mentions from linking notes into a target note's Summary section |
| "sync guide", "sync the guide", "update the guide", "build the guide" | `_AI/local/workflows/sync-guide.md` — builds/maintains a piece's `guide/` folder from the brief and vault sources; never touches output.md |
| "polish" | `_AI/local/workflows/polish.md` — light copy-edit of the user's own text, never rephrases |
| a `% scribe <instruction>` marker found in a file | `_AI/local/workflows/scribe.md` — carries out an inline instruction left in a file marker, writes the response back into the same block |
| "sanity" | `_AI/local/workflows/sanity.md` — flags contradictions/confusing writing, never edits |
| "gap check `<file>`", "gap check `<file>` against `<reference>`", "does `<file>` cover `<reference>`" | `_AI/local/workflows/gap-check.md` — checks a draft against its `guide/` (or a named reference) and reports what's missing; never edits target or reference content, but does record a coverage verdict on each checked theme, every run |
| "diploma ready", "is this diploma ready", "check against the diploma rubric" | `_AI/local/workflows/diploma-ready.md` — checks a design's `output.md` against the fixed Diploma assessment rubric, Yes/Nearly/Not Yet verdict, never edits |
| "grill me" or "interview me" | `_AI/shared/workflows/grill-me.md` — captures decisions into a durable ADR-style record |
| "rubber duck this", "let's rubber duck", "talk this through with me" | `_AI/shared/workflows/rubber-duck.md` — honest, brief conversation with no file changes |
| "debrief" | `_AI/local/workflows/debrief.md` *(optional workflow)* |
| "save" | `_AI/local/workflows/save.md` |
| "fetch" | `_AI/local/workflows/fetch.md` *(optional workflow)* |
| "capture log note", "capture as a log note", "log this" | `_AI/local/workflows/capture-log-note.md` |
| "reflect" + scope | `_AI/local/workflows/reflect.md` |
| "add-to-radar", "capture radar item", "update radar list", "review radar items" | `_AI/local/workflows/add-to-radar.md` |
| "greenhouse this", "park in greenhouse", "add to greenhouse", "review greenhouse" | `_AI/shared/workflows/greenhouse.md` — park early-stage ideas for later, distinct from radar |
| "wayfinder this", "map this out", "help me find a way forward", "chart a way forward" | `_AI/local/workflows/wayfinder.md` — map a woolly, multi-session project into a destination + waypoints resolved one at a time |
| "state of play", "where are we", "sweep the gig" | `_AI/local/workflows/state-of-play.md` — on-demand reconciliation sweep across live projects, radar, triage, and wayfinder, then writes a plain-language digest to DASHBOARD.md |
| "post-mortem this", "run a post-mortem", "candidate for post-mortem?" | `_AI/local/workflows/post-mortem.md` — investigate what went wrong, propose a concrete tweak |
| "handoff" | `_AI/shared/workflows/handoff.md` — save a handoff document so this conversation can be resumed later |
| "resume" | `_AI/shared/workflows/resume.md` — resume from a saved handoff document |
| "link components" + knowledge base name, "sweep PRPs for components" | `_AI/local/workflows/link-components.md` — propose wikilinks from PRP decision notes to technical component pages |
| "elicit", "elicit section `<N>`", "grill me on section `<N>` of the guide" | `_AI/local/workflows/elicit.md` — one-shot brainstorm of angles and questions from a section's `guide/` theme notes, to spark writing; never drafts prose, never touches `output.md` |

## The fetch method *(optional)*

Sometimes, rather than typing into the chat, I'll use the _fetch_ method to send and receive messages. When I say "fetch", run the workflow at `_AI/local/workflows/fetch.md`.
