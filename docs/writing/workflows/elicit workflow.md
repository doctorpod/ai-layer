---
tags: [ai-layer-docs]
sources:
  - vault/workflows/elicit.md
checked: 2026-09-26
---

# elicit workflow

*Reads a section's [[gathered note|gathered notes]] and throws out a quick burst of odd angles and questions to get you writing.*

## When to reach for it

You're stuck on a section. The material is in the guide, but no first sentence will come. You want provocations, not structure and not prose.

## How to invoke

- `/elicit`, or say "elicit", "elicit section `<N>`" or "grill me on section `<N>` of the guide".
- From a [[scribe marker]]: `% scribe elicit`.

You can also point it at specific notes rather than a whole section.

## What it reads

The notes in the named `guide/` section, or the notes you name.

## What it writes

Nothing. The ideas appear in chat, or in the scribe block's `% **comments**` when it's called from a marker.

## What it never touches

- The [[output draft]].
- Any gathered note, or any of its fields.

## How it works

1. It reads the notes in scope.
2. It produces a single bulleted brainstorm of odd angles, provocations, and questions that might spark a sentence.
3. It stops. That's one pass, with no follow-up questions and no back-and-forth.

It needs a brief and a `guide/`. If there's no guide yet, it points you to [[sync-guide workflow|sync-guide]] to build one first.

## Worked example

You've drafted `01 Goals` for Hollin Lane, but `02 Observation` won't start. You say "elicit section 02". It reads `Wet corner by the north gate floods every winter` and `South bed shaded by the neighbour's hedge until noon`, and replies with bullets such as:

- What would the site look like to someone who only visited in August?
- The hedge and the water are both on the site's edges. Is the interesting stuff all at the boundary?
- Which of these did Maggie mention first, and which did you notice yourself?

Nothing is written anywhere. You pick one and start typing.

## Compared with…

- **[[beats workflow|beats]]**: both read a section's notes, do one pass and stop. elicit gives you angles to spark a sentence. beats gives the section a spine, an ordered list of moves, and writes it into `output.md`. elicit writes nothing.
- **[[interview workflow|interview]]**: elicit brainstorms once from notes that already exist. interview runs over several sessions and *produces* notes from your answers.

## Related

- [[gathered note]] · [[scribe marker]]
- Workflow file: `_AI/local/workflows/elicit.md`
