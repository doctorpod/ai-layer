---
tags: [ai-layer-docs]
sources:
  - vault/workflows/beats.md
checked: 2026-09-26
---

# beats workflow

*Turns a section's [[gathered note|gathered notes]] into an ordered list of moves, a [[beats block]], for you to draft against.*

## When to reach for it

You know what a section has to cover but not what order it should move in. You want a spine before you write a sentence.

## How to invoke

- `/beats`, or say "beats", "beats section `<N>`" or "beat sheet for `<section>`".
- From a [[scribe marker]] wrapped around rough draft, note stubs or a half-built passage: `% scribe beats`.

## What it reads

- **Standalone:** every gathered note whose `section:` matches the named section, skipping `rejected` ones. Or just the notes you name.
- **From a scribe marker:** the wrapped text defines the part, with the section's notes as supporting context.

## What it writes

- **Standalone:** one [[beats block]] in the [[output draft]], directly under the section's heading. It replaces any existing block for that section. If `output.md` or the heading doesn't exist, the block is shown in chat instead.
- **From a scribe marker:** the block goes into `% **comments**`, without checkboxes.

## What it never touches

- The prose in `output.md`. It writes only the block.
- The notes in `guide/`. It never sets `status` or `coverage`, because which notes get used is decided when you write.

## How it works

1. It reads everything in scope, treating each note's whole body as one unit.
2. **It decides the beats.** This isn't one note per beat. It **merges** notes that make one move, **demotes** a detail to a sub-point, **cuts** a note that doesn't earn its place or belongs elsewhere, and adds a **gap** beat for a move no note covers, such as a transition or a "so what", marked as connective.
3. It orders the beats so each sets up the next, based on what the reader needs when rather than on topic.
4. It phrases each beat as what it *does* ("pivot from what's there to what the design should do"), not as its subject.
5. It does one pass, with no back-and-forth.

Every non-rejected note in scope ends up either in a beat or on the **Not beats** line. None is dropped silently.

## Worked example

You say "beats section 02" on the Hollin Lane client part. It reads the three `02 Observation` notes and writes this under `## 02 Observation` in `parts/client/output.md`:

```
**Beats** — section 02 Observation (framework; delete once written)

1. [ ] **Set up: the site looks dry** — …  ← [[South bed shaded by the neighbour's hedge until noon]]
2. [ ] **Complicate: except the north gate** — …  ← [[Wet corner by the north gate floods every winter]]
3. [ ] **Pivot: water as a resource** — …  *(connective — no note covers this)*

Not beats: [[Heavy clay under the wet corner]] — a detail inside beat 2.
```

You write the section, ticking beats as you go, then delete the block.

## Compared with…

- **[[elicit workflow|elicit]]**: angles to spark a sentence, shown in chat. beats gives structure and writes it into the draft.
- **[[gap-check workflow|gap-check]]**: checks *after* you've written whether the draft covers the notes. beats plans the section *before* you write.

## Related

- [[beats block]] · [[output draft]] · [[scribe marker]]
- Workflow file: `_AI/local/workflows/beats.md`
