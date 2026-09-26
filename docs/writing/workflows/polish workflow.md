---
tags: [ai-layer-docs]
sources:
  - vault/workflows/polish.md
checked: 2026-09-26
---

# polish workflow

*A light copy-edit of your own typed or dictated words: spelling, punctuation and structure only, never what you meant.*

## When to reach for it

The words are already yours and you want them cleaned up without any of them becoming the assistant's prose. It works on any file in the vault, not just a piece's `output.md`.

## How to invoke

- `/polish`, or say "polish", with a file that has a [[polish marker]] (`%P` … `%`) in it.
- In chat: dictate text straight into a message, with no file named. Tell it where the result goes, either up front ("polish this into the site-walk log: …") or afterwards.
- From a [[scribe marker]]: `% scribe polish`.

## What it reads

- **File mode:** every unstripped `%P` block in the file. If there are none, it asks whether to polish the whole body instead.
- **Chat mode:** your message.

## What it writes

The polished text, to the destination you choose:

- in place, replacing the marked block with the markers stripped;
- appended to an existing file;
- a new file;
- or held in chat until you name one.

## What it never touches

What you meant. That's the guarantee:

- **It fixes** spelling, punctuation, paragraph and heading structure, and dictation debris such as repeated words, "um" and "you know".
- **It never** rephrases, reorders, cuts, adds, changes a word choice, or smooths a sentence into something it wasn't.

If dictation has garbled a sentence beyond repair, it doesn't guess. It flags the sentence inline, e.g. `[unclear: …]`, and leaves it for you to fix in your own words.

## How it works

It finds the scope (the marked blocks, the whole file on your say-so, or your message), corrects the surface, and writes the result where you tell it.

## Worked example

On the Hollin Lane site you dictate into `parts/client/output.md`, under `## 02 Observation`:

```
%P
so the wet corner um the wet corner by the north gate its under water
most of the winter which is why the swale goes above it
%
```

You say "polish". The block becomes:

```
So the wet corner by the north gate, it's under water most of the winter, which is why the swale goes above it.
```

The markers and the repeated "the wet corner" are gone, and "its" is now "it's". "So" stays, and so does the sentence's shape, because those are yours, not dictation debris.

## Compared with…

- **[[sanity workflow|sanity]]**: polish never comments on content, and sanity never touches prose. Use polish for how it's written and sanity for whether it holds together.
- **[[scribe workflow|scribe]]**: both are driven by markers and work on any file. Polish has one fixed job and strips its markers. Scribe carries out whatever instruction you leave and keeps its marker as a standing note.

## Related

- [[polish marker]] · [[scribe marker]]
- Workflow file: `_AI/local/workflows/polish.md`
