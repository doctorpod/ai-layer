---
tags: [ai-layer-docs]
sources:
  - vault/workflows/sync-guide.md
  - shared/snippets/piece-folder.md
checked: 2026-09-26
---

# sync-guide workflow

*Builds a piece's [[guide folder]] from the vault sources its brief names, and keeps it up to date as new material lands.*

## When to reach for it

- You've written a [[piece brief]] and want the material for it gathered from your knowledge bases.
- New sources have been ingested or debriefed since the guide was built, and you want them triaged in.

This is the *extracting* [[gatherer]]. If the material has to come out of your own head, use [[interview workflow|interview]] instead.

## How to invoke

`/sync-guide`, or say "sync guide", "sync the guide", "update the guide" or "build the guide", naming the piece folder.

## What it reads

- The [[piece brief]]: `Draw from` decides which knowledge bases to use, and the [[brief outline]] decides which sections to file notes under.
- The `curated/` folder of each knowledge base named in `Draw from`, and nothing else. It uses a knowledge base's `wiki/` pages only to find the primary source behind a claim.
- The [[triage log]], to see which curated files it has already been through.

## What it writes

- New [[gathered note|gathered notes]] in `guide/`, always `status: pending`, and new quotes appended to existing notes.
- `guide/INDEX.md`, the first time it builds a guide.
- Its own lines in the [[triage log]].
- One `status` change: `used` back to `pending`, when it appends a quote to a note you've already used. It tells you when it does this.

## What it never touches

- The [[output draft]]. It never reads or writes it.
- The brief. If there's no brief, it offers to help you draft one in chat, then stops.
- `status` beyond the one revert above. `used` and `rejected` are your calls.
- `coverage`, which belongs to [[gap-check workflow|gap-check]].
- The `guide.base` file behind the [[guide view]]. You make that once, by hand.
- The structure of existing notes. It never merges two notes or splits one.

## How it works

1. **Checks the brief.** It stops if there's no brief, or if `Format` names a framework and there's no `Outline`.
2. **Counts the backlog**, meaning the curated files not yet in the triage log. If there are more than a handful, or some are long, it proposes a batch, largest first, and asks whether to run it now.
3. **Triages one file at a time, completely.** It pulls out every claim in the file and puts each through a **relevance filter**: does it lead to a decision, recommendation or observation that matters to the brief? Claims that don't are dropped and written nowhere. If a raw source has a paired debrief, it reads both together, because the debrief often corrects the raw source.
4. **Lifts quotes from the primary source, not the wiki.** A wiki page is a map to its sources. The assistant follows its citation to the source and quotes that. If the wiki's sentence can't be found in its cited source, it flags a likely conflation instead of quoting it.
5. **Files each quote.** A clear match to an existing note in the same section gets appended there. No match means a new note, which is the default. If it's ambiguous, it asks you.
6. **Logs the file** in the triage log once every claim in it is done. Stopping between files loses nothing.

On a later sync it does the same for files not yet in the log. If nothing new passes the filter, it says so rather than inventing a note.

## Worked example

You've written the brief for `projects/hollin-lane/design-doc/parts/client/`, with `Draw from: the hollin-lane knowledge base` and a GOBRADIMET outline. You say "build the guide for the Hollin Lane client part".

There's no `guide/` yet, so it creates `guide/INDEX.md`. It finds three untriaged curated files and triages them one at a time. From `debrief-2026-03-14-site-walk` it lifts the line about the north-gate corner flooding and files it as a new note, `Wet corner by the north gate floods every winter`, under `02 Observation`. A remark about the car park's opening hours fails the relevance filter and is dropped. From the transcript it creates `Fruit for the school kitchen, not a showpiece` under `01 Goals`. Each file gets a line in `triaged.md`.

Weeks later a new debrief records the wet corner staying wet into April. You've already marked the wet-corner note `used`. The next sync appends the new quote, puts the note back to `pending`, and tells you why.

## Compared with…

- **[[interview workflow|interview]]**: the other gatherer. sync-guide *extracts* quotes from sources already in the vault. interview *elicits* answers from you, over several sessions. Their notes meet the same contract, so everything downstream treats them alike.
- **[[gap-check workflow|gap-check]]**: sync-guide fills the guide, and gap-check checks the draft against it. Running sync-guide never tells you whether the draft is complete.

## Related

- [[gathered note]] · [[triage log]] · [[guide view]] · [[brief outline]]
- Workflow file: `_AI/local/workflows/sync-guide.md`
