---
tags: [ai-layer-docs]
sources:
  - vault/workflows/sync-guide.md
  - vault/workflows/interview.md
  - vault/workflows/elicit.md
  - vault/workflows/beats.md
  - vault/workflows/polish.md
  - vault/workflows/scribe.md
  - vault/workflows/sanity.md
  - vault/workflows/gap-check.md
  - vault/workflows/diploma-ready.md
  - shared/snippets/piece-folder.md
checked: 2026-09-26
---

# Writing workflows: index

Every page under the writing docs, one line each. For how they fit together, start at [[writing/README|Writing workflows]].

## Workflows

- [[sync-guide workflow]]: build and update a piece's `guide/` from the vault sources its brief names.
- [[interview workflow]]: interview you thread by thread, check your answers against the record, and save them verbatim to `guide/`.
- [[elicit workflow]]: a one-shot burst of angles and questions from a section's notes, shown in chat.
- [[beats workflow]]: an ordered list of a section's moves, written into the draft to write against.
- [[polish workflow]]: fix the spelling, punctuation and structure of your own words, never the meaning.
- [[scribe workflow]]: carry out an instruction left in a file and reply in place.
- [[sanity workflow]]: flag contradictions and passages that don't hold up. Never edits.
- [[gap-check workflow]]: report what the draft misses from its guide, and record coverage on each note.
- [[diploma-ready workflow]]: check a design against the Diploma rubric and give a Yes / Nearly / Not Yet verdict.

## Concepts

- [[piece folder]]: the folder a piece lives in, holding `brief.md`, `guide/`, `output.md` and `assets/`.
- [[multi-part piece]]: one deliverable assembled from several piece folders under `parts/`.
- [[piece brief]]: `brief.md`, which says what the piece is, who it's for and where its material comes from.
- [[brief outline]]: the brief's `Format` and `Outline` fields, whose headings become each note's `section:`.
- [[guide folder]]: `guide/`, the material a piece is written from.
- [[gathered note]]: one note in `guide/`, with its five-field contract and `status` values.
- [[guide view]]: `guide.base`, the Obsidian view of a guide grouped by section.
- [[triage log]]: `triaged.md`, the append-only list of sources and threads a gatherer has finished with.
- [[interview timeline]]: `timeline.md`, the dated evidence interview checks answers against.
- [[interview thread]]: one line of questioning, and how its note shows it open, closed or reopened.
- [[output draft]]: `output.md`, the prose you always write yourself.
- [[coverage verdict]]: the `coverage` field that gap-check writes, `full`, `thin` or `missing`.
- [[assessment rubric]]: a hand-kept checklist in `standards/` that workflows read by heading.
- [[scribe marker]]: the `% scribe` block syntax.
- [[polish marker]]: the `%P` … `%` block syntax.
- [[beats block]]: the format of the Beats block that beats writes.
- [[gatherer]]: any workflow that fills `guide/`, and the contract that makes them interchangeable.
