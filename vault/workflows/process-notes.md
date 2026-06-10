---
name: process-notes
description: Scan a scope of notes, propose folder moves and category assignments based on vault conventions, then apply on confirmation.
---

Process notes by checking them against vault conventions and proposing moves and category changes before touching anything.

## Step 0: Vault check

Before anything else, confirm you are in an Obsidian vault by checking for a `.obsidian/` directory at the vault root.

If it is absent: **stop and tell the user** — this workflow is vault-specific and should not run elsewhere. Do not proceed.

## Step 1: Determine rules source

The rules source is the note that defines conventions for folders, categories, and note types.

- If the user passed a note path as an argument, use that.
- If the user said "this discussion" or "last discussion", extract the relevant conventions from the current conversation.
- Otherwise, default to the vault root `README.md`.

Read the rules source now. Extract the following if present:
- Category vocabulary and what each category means
- Which categories map to which folders
- Any deciding questions (e.g. domain vs touchpoint, field vs domain)
- Any note types that have fixed homes (e.g. `QUESTIONS`, `DECISIONS`, people, tickets)

If the rules source is a gig or project README rather than the vault root, also read the vault root `README.md` and treat the gig rules as layered on top — gig-specific rules override vault-wide ones where they conflict.

## Step 2: Determine scope

Scope must be explicit — there is no default. Derive it from the user's invocation:

- **Folder path** — scan that folder recursively
- **Gig name or path** — scan that gig's `lib/(year)/` folder
- **Time range** ("last week", "since Monday") — find notes with a `date` property matching the range across the vault or a specified folder
- **Combination** — folder + time range

If none of these is clear from the invocation, ask. Offer the three options above. Do not guess.

Structural notes, system folders, and already-processed KB content (`curated/`, `wiki/`) are excluded automatically by the scripts below.

Once scope is clear, run `list-notes.py` to confirm what's in it:

```bash
# Folder scope
python3 _AI/local/scripts/list-notes.py <folder>

# Time-range scope (filename date prefix)
python3 _AI/local/scripts/list-notes.py <folder> --since 7d
python3 _AI/local/scripts/list-notes.py <folder> --since 2026-06-03

# Undated strays only
python3 _AI/local/scripts/list-notes.py <folder> --undated
```

Tell the user how many notes were found and confirm the scope before proceeding.

## Step 3: Analyse notes

Run `scan-frontmatter.py` on the scoped file list to get a structured overview in one call:

```bash
# Pipe from list-notes.py
python3 _AI/local/scripts/list-notes.py <folder> --since 7d | python3 _AI/local/scripts/scan-frontmatter.py

# Or scan a folder directly
python3 _AI/local/scripts/scan-frontmatter.py <folder>
```

The output groups notes into **UNDATED (potential strays)** and **DATED CAPTURES**, showing categories and flagging any missing. Use this as your working list — do not read individual files unless a note needs further investigation to classify it (ambiguous title, unclear content).

Check each entry against the rules from Step 1:

**Folder check**: Is this note in a folder that matches its content type? Flag it if not.

**Category check**: Is the `categories` value present and correct per the vocabulary? The script flags missing ones; also check for mismatches against the rules.

**New notes implied**: For any note you do open, note whether it references concepts, people, or touchpoints that don't yet have their own note.

Keep a running list of findings grouped by type. Do not propose changes yet.

## Step 4: Present proposals

Present findings grouped into these sections — omit any section with nothing to report:

### Wrong folder
List each note, its current location, and where it should move. One line per note.

### Missing categories
List each note and which category or categories to add. One line per note.

### Category mismatch
List each note, its current category, and what it should be changed to. Include a brief reason if it's not obvious from the rules.

### New notes to create
List concepts, people, or touchpoints referenced in the scanned notes that don't yet have their own note. Include a suggested filename, category, and folder for each.

### Looks fine
List any notes that needed no changes, so the user can see they were checked.

---

After presenting, ask: **"Shall I make all of these changes, or go through them one group at a time?"**

Do not touch any file until the user confirms.

## Step 5: Apply changes

Apply only what the user has approved. For each approved change:

- **Folder move**: move the file to the proposed location. Update any `[[wikilinks]]` to the note if you can find them — search by filename.
- **Category add/change**: edit the `categories` frontmatter property. Preserve all other frontmatter.
- **New note**: create the note with the agreed filename, frontmatter (`categories`, `gig` if inside a gig), and a minimal stub body. Do not write content — that is the user's job.

## Step 6: Update INDEX

Read the nearest `INDEX.md` — for gig notes this is the gig root INDEX, for vault-level notes it is the vault root INDEX.

Use the existing structure as your guide. Add new entries that fit naturally under existing headings. Do not restructure sections or rename headings unless the current structure genuinely cannot accommodate the new content — if that happens, propose the restructure and wait for confirmation before making it.

What warrants an INDEX entry:
- **New stubs created** during this session (glossary terms, touchpoints, people) → add under the appropriate existing heading with a one-line description
- **Notes moved** → only if the note is significant enough that someone would navigate to it directly; skip routine captures
- **Person notes** → add if the INDEX has a people section; skip if not

What does not warrant an INDEX entry:
- Date-prefixed captures that were simply categorised in place
- Notes moved purely for housekeeping (e.g. strays corrected to their proper folder)

After updating INDEX, move to Step 7.

## Step 7: Update README

Read the nearest `README.md` — same scope as the INDEX in Step 6.

The README describes the gig's purpose, structure, and conventions. It should not list notes (that's INDEX's job) — only keep the structural description accurate.

Check only these things:

- **Folder structure section** — if new folders were created during this session (e.g. `people/` created for the first time), add them with a one-line description. If a folder was removed or renamed, update accordingly.
- **Gig-specific conventions** — if this session surfaced a new convention or clarified an existing one, add it.
- **Frontmatter accuracy** — if `ended-on` or other metadata looks stale, flag it with a `[!note]` callout rather than silently editing it. Let the user confirm dates.

Do not rewrite orientation prose unless it is factually wrong. Do not restructure sections. If the README needs significant rework, describe what and why, and wait for confirmation.

After updating README, log a summary line by running:
```
bash _AI/local/scripts/log-write.sh "PROCESS-NOTES: <brief summary, e.g. '5 notes moved, 3 categorised, 2 stubs created'>"
```

## Notes on the capture pattern

Almost all notes start life as date-prefixed captures (`YYYY-MM-DD name.md`) with `date` and `time` frontmatter, landing in `lib/(year)/`. This is the capture format — fast to create, no decision required at the time. The date prefix signals when it was captured, not what it is or where it lives permanently.

This workflow is the processing step that turns raw captures into properly typed, properly placed notes. A captured note may turn out to be:
- A pure capture that stays in `lib/(year)/` — assign the appropriate category
- A concept or touchpoint — assign `[[Glossary]]` or `[[Touchpoints]]` category
- A reference — assign `[[References]]` category
- An observation — assign `[[Observations]]` category
- A person — move to `people/`, assign `[[People]]` category
- A PR review — move to `repos/(name)/curated/`
- A mix — if a note contains both a dated log section and a stable concept, consider whether to split it
