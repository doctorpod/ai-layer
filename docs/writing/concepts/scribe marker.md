---
tags: [ai-layer-docs]
sources:
  - vault/workflows/scribe.md
checked: 2026-09-26
---

# scribe marker

*A `% scribe <instruction>` block left in any file, telling the assistant to do something to the text inside it and reply in place.*

```
% scribe does this paragraph say why the wet corner matters?
The north-gate corner floods every winter. We plan a swale above it
to hold the water back and slow it down.

% **comments**
- (the assistant's reply goes here)
%
```

## Syntax

- **Opening fence:** `% scribe <instruction>`, or the short form `%s <instruction>`. It must start at column 0, with no leading space, so a `%s` in the middle of a line is never mistaken for a marker.
- **Body:** the prose the instruction applies to. It can run to several paragraphs.
- **`% **comments**`:** on its own line with a blank line above it. You don't need to add it. The assistant adds it when it first replies.
- **Closing `%`:** alone on its own line.

## How it behaves

- **The marker stays.** A scribe block is a standing note. Answering it doesn't strip the markers, and each new pass updates `% **comments**` in place.
- **Fixes go in the prose, notes go in the comments.** A small fix such as a typo is made directly in the body and isn't repeated in the comments. The comments are brief bullets: notes, flagged issues, observations for you to decide on.
- **A block that already has comments isn't reprocessed** just because the file was read for another reason. Say "read again", "again", "repeat" or "r" to rerun it, or change the prose above it.
- Every scribe block in a file is processed.

## Calling other workflows from a marker

The instruction can be anything, including another workflow's name. The assistant then follows that workflow's rules:

- `% scribe polish`: edits within [[polish workflow|polish]]'s guarantee.
- `% scribe elicit` or `% scribe beats`: the brainstorm or [[beats block]] goes into the comments, without checkboxes.
- `% scribe gap check this section`: [[gap-check workflow|gap-check]] runs scoped to the section.
- `% scribe sanity`: [[sanity workflow|sanity]]'s findings, with line numbers.

## Related

- [[scribe workflow]]
- [[polish marker]]
