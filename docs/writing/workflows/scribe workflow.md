---
tags: [ai-layer-docs]
sources:
  - vault/workflows/scribe.md
checked: 2026-09-26
---

# scribe workflow

*Carries out an instruction you've left in a file inside a [[scribe marker]], and writes its reply back into the same block.*

## When to reach for it

You're working in a file and want to leave an instruction right where it applies, whether a question, an edit request or another workflow's name, without switching to chat to explain which paragraph you mean. It works on any file in the vault.

## How to invoke

Write a marker at column 0:

```
% scribe <instruction>
…the prose it applies to…
%
```

`%s <instruction>` is the short form. The assistant acts on a marker when it comes across one while reading the file, or when you point it at the file. Say "read again", "again", "repeat" or "r" to rerun a block that's already been answered.

## What it reads

- The marked block, and the rest of the file.
- If the file is in a [[piece folder]], its [[piece brief]] and [[guide folder]] as context. Without a piece folder, it works from the file alone.

## What it writes

- Small direct fixes (a typo, punctuation, a small correction) go straight into the prose inside the block.
- Everything else goes into the block's `% **comments**` as short bullets: notes, flagged issues, and structural points for you to decide on. It adds the comments line if it isn't there.

## What it never touches

- The markers. It never strips them, because a scribe block is a standing note you can come back to.
- A block that already has comments, unless you ask for a rerun or the prose above has visibly changed.
- It doesn't duplicate a fix into the comments, since the fix already shows it.

## How it works

1. It finds each scribe block in the file.
2. It reads the instruction. If it names another workflow, that workflow's rules govern the edit. `% scribe polish` stays within [[polish workflow|polish]]'s guarantee, and `% scribe beats` produces a [[beats block]] in the comments.
3. It makes any direct fix in place, and puts the rest in `% **comments**`.

## Worked example

In `parts/client/output.md` you've written the Design section's opening and aren't sure it earns the swale:

```
% scribe does this justify the swale, given the brief?
We'll dig a swale along the contour above the north gate.

% **comments**
- The brief's must-haves include the wet corner, but this doesn't say what the swale does for it. Hold water back? Feed the orchard?
- "north gate" here, "north-gate corner" in 02. Pick one.
%
```

You rewrite the sentence and say "r". The block's comments are updated in place.

## Compared with…

- **[[polish workflow|polish]]**: both are driven by markers and work on any file. Polish does one fixed job and strips its markers. Scribe does whatever you ask and keeps its marker.
- **Asking in chat**: a scribe marker says exactly which prose you mean, and the reply stays next to it.

## Related

- [[scribe marker]] · [[polish marker]] · [[beats block]]
- Workflow file: `_AI/local/workflows/scribe.md`
