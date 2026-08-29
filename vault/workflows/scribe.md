---
name: scribe
description: Carry out an inline instruction left in a file via a % scribe marker, and write the response back into the same block.
---
# Scribe Workflow

Trigger: a `% scribe <instruction>` marker found in a file (while reading it for another reason, or because the user points at it / says "read again"/"again"/"repeat"/"r").

## Marker syntax

```
% scribe <instruction>
Prose the instruction applies to. Can span several paragraphs.

% **comments**
(my response goes here)
%
```

- `% scribe`, `% **comments**`, and the closing `%` each sit alone on their own line
- `% **comments**` gets a blank line above it, to stand out from the prose
- `% **comments**` doesn't need to exist yet — add it (with the blank line) before the closing `%` when responding.
- Don't strip the markers once answered. A scribe block is a standing annotation the user may revisit (edit the prose, ask "read again") — leave the block in place, update `% **comments**` in place on each pass.
- If a block already has `% **comments**` filled in, don't reprocess it just because it was encountered while reading the file for another reason — that's stale, not new. Only reprocess when the user explicitly asks ("read again"/"again"/"repeat"/"r") or when the prose above it has visibly changed since the comment was written.

## Doing the work

1. If the file being edited sits in a piece-folder (`_AI/shared/snippets/piece-folder.md`), its `brief.md` and `guide/` siblings are fair game as context for the instruction — check for them. No piece-folder, no problem: proceed from the file alone.
2. The instruction can be anything — a question, an edit request, "polish", etc. If it names another workflow (e.g. "polish"), follow that workflow's own rules/guarantee for the edit itself.
3. If the instruction implies a direct fix (typo, punctuation, small correction), make it in place in the prose. Don't duplicate the corrected prose into `% **comments**` — that's redundant.
4. `% **comments**` is for what doesn't belong in the prose itself: brief notes, flagged issues, structural observations left for the user to decide on. Bullet points. No fluff, no restating what the fix already shows.
5. If a file has multiple `% scribe` blocks, process each one found.
