---
name: create-summaries
description: Update a note's Summary section with brief, linked entries drawn from notes that reference it.
---

# Create Summaries Workflow

Triggered by: "update the summary in `<note>`", "update summary", "refresh the summary for `<note>`"

A **summary note** has a `## Summary` heading containing `### YYYY` / `#### Mon` subheadings, with one-line bullet entries underneath. Each entry is a link back to the note it was drawn from — a summary note never talks about a source without linking to it.

This workflow finds notes that reference the target, works out which of them aren't reflected in the Summary yet, and adds a one-line entry for each — written static, not as a Dataview/base query.

## Step 1: Find candidates

Run:

```bash
/Applications/Obsidian.app/Contents/MacOS/obsidian backlinks path=<target note> vault=<name>
```

This is Obsidian's live link index, not a text search — it won't catch plain-prose mentions that aren't actually wikilinked, and that's correct: this workflow only summarises real links.

## Step 2: Work out what's new

Read the target note's existing `## Summary` section (you're about to edit it anyway, so this costs nothing extra). Collect every link target already present under that heading.

Any backlink from Step 1 whose filename doesn't appear as a link target there is **new**. Anything that does appear is already summarised — skip it.

## Step 3: Determine the extraction lens

How aggressively you filter a source note down to one line depends on what kind of note the *target* is, not the source. Check in this order:

1. **Filename matches a bare year** (`journal/YYYY.md`) → **minimal-extraction mode**. Pull out the single most notable thing that happened that day. Don't filter by topic — there isn't one. The target's own link will usually already sit inside the relevant paragraph. A bare-year note is a summary in its entirety — it won't have a `## Summary` wrapper heading, and shouldn't get one (see Step 6).
2. **Otherwise, check the target's frontmatter for a topical/categorisation signal** (whatever the vault's current convention is — don't hardcode a specific tag scheme, since it's expected to change over time) → **aggressive mode**. Extract only the clause or sentence relevant to that topic; discard everything else in the source note, however interesting.
3. **Neither signal present** → ask the user which mode applies. Don't guess.

## Step 4: Write one-line entries

For each new candidate, read the source note and write a single bullet in the target's voice — see `_AI/local/STYLE.md` for tone (concrete, alive, no flattening into neutral summary-speak). Link the source with a piped display:

```
- [[YYYY-MM-DD|brief summary text]]
```

## Step 5: Work out where each entry goes

If the source is a dated daily note, the date is already in its filename — bucket under the matching year/month subheading, creating either heading if it doesn't exist yet. Match the heading depth already used elsewhere in the note; don't invent a new convention for this note. In a bare-year target (Step 3), there's no `### YYYY` level to nest under — bucket directly under the note's top-level month headings instead.

If the source has no date in its filename, **always ask** which year/month it belongs under — never bucket it silently, and never fall back to file creation/modified time (git and sync operations touch those without reflecting when the real-world event happened). If the source note's own frontmatter has a date field, suggest it as a default the user can accept.

## Step 6: Batch the merge check

Collect all new entries per month before writing anything. If a month ends up with more than one new entry, present all of them together once and ask whether any should be merged into a single bullet — don't interrupt separately for each one.

If the user asks for a merge: combine the prose into one bullet, but never drop a link — a merged entry keeps every source it's drawn from linked, e.g.:

```
- [[2026-04-23|Two visible]]; [[2026-04-24|now six]]
```

If the target has no `## Summary` heading at all yet, ask before creating one — that's a bigger structural change than appending to an existing section. Exception: a bare-year target (Step 3) is expected to have no `## Summary` wrapper, since the whole note already is one — don't ask, just append under its month headings.

## Step 7: Confirm

After writing, tell the user what was added — which entries, under which headings — so they can review the diff. No need to ask permission before writing single, unambiguous entries; the checkpoints in Steps 5 and 6 already cover the cases that need a decision.
