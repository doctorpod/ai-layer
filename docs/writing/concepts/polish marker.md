---
tags: [ai-layer-docs]
sources:
  - vault/workflows/polish.md
checked: 2026-09-26
---

# polish marker

*A `%P` … `%` block in any file, marking raw typed or dictated text for [[polish workflow|polish]] to clean up.*

```
%P
so the wet corner um the wet corner by the north gate its under water
most of the winter which is why the swale goes above it
%
```

## Syntax

- `%P` opens the block. It isn't case-sensitive, so `%p` works too. `%` closes it.
- **Both must sit alone on their own line.** That's what lets an ordinary `%` in prose ("50% done") pass through untouched.
- When polish runs, it cleans up the text and **strips the markers**. Compare the [[scribe marker]], which stays in place.

## Where you can use it

- **A new file:** dictate straight into a note wrapped in `%P`/`%`.
- **Appending:** add a block at the end of an existing file. Only the block is touched.
- **Editing in place:** go back into a polished file and wrap just the bit you changed.
- **Across sessions:** leave several blocks over several sessions. Polish processes every unstripped block it finds, not just the newest.

If a file has no block, polish tells you and asks whether to polish the whole body instead.

## Related

- [[polish workflow]]
- [[scribe marker]]
