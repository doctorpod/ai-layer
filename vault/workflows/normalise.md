---
name: normalise
description: Periodic sizing pass over a KB's wiki — find near-duplicate, over-broad, and source-shaped pages and propose merges or splits.
---

# Normalise Workflow

A deliberate, on-demand pass over one knowledge base's `wiki/` to correct page sizing that has drifted over many ingest and debrief passes. This is schema-refactoring for the wiki — run it occasionally, never as part of ingest.

The goal is well-sized pages: each one makes a single general claim, is a natural thing for many sources and other pages to link to, and has a coherent set of backlinks (everything pointing at it points for roughly the same reason).

## Step 0: Scope

One KB per run. If the user named one, use it. If not, list the KBs (folders containing a `wiki/`) and ask which.

Read every page in the KB's `wiki/`, plus its `INDEX.md`, before proposing anything.

## Step 1: Find the three problems

**Propose only — never restructure without the user confirming each change, one at a time.**

### 1. Near-duplicate pages

Two or more pages making essentially the same claim at different levels of specificity — e.g. `Resilient planting`, `Designing for resilience`, `Resilience in the churchyard`.

- Identify the most general viable title.
- Propose merging the others into it: which paragraphs move, which become `## Evidence` bullets, which footnotes carry over.
- List every inbound link that needs redirecting.

### 2. Over-broad pages

A page whose inbound links point to it for clearly different reasons — the backlinks don't form a coherent set.

- List the distinct reasons things link to it.
- Propose splitting it into one page per claim, and say which inbound links move to which new page.

### 3. Source-shaped pages

A page with one inbound link that comes from its own source, or a page whose body is all `## Evidence` and no durable claim.

- Propose merging it up into a broader parent page, or generalising it into a real concept page if the parent doesn't exist yet.
- If nothing links to it and nothing should, propose deleting it.

## Step 2: Apply, one at a time

- Use the `obsidian` CLI for backlink queries where available (`_AI/local/OBSIDIAN-CLI.md`); otherwise grep the KB for `[[page-name]]`.
- Present one proposal. Wait for the user's decision. Apply it. Move on.
- After applying a merge or split, update `INDEX.md` and fix every redirected wikilink in the same step — don't leave dangling links.
- Respect the citation rules in `_AI/local/workflows/ingest.md`: never blend two sources into one sentence when merging; keep footnotes intact and pointing at the right source.
- Preserve the two-part page shape (durable idea, then `## Evidence`) on every page you touch.

## Step 3: Learnings

Follow `_AI/shared/snippets/learnings.md`, substituting `NORMALISE` for `[WORKFLOW]`.
