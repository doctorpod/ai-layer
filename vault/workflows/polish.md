---
name: polish
description: Light copy-edit of the user's own dictated or typed prose — spelling, punctuation, structure only. Never rephrase, reorder, cut, or add content.
---

# Polish Workflow

Use this workflow when the user wants their own dictated or typed words cleaned up without any of it becoming my prose. This is the opposite of `_AI/local/workflows/compose.md`: I never draft, I only correct the surface of what's already theirs.

## The guarantee

Polish makes one hard promise: **I will never touch what the user meant, only how it's spelled and punctuated.**

Fix: spelling, punctuation, paragraph and heading structure, obvious dictation artifacts (repeated words, stray filler like "um"/"you know").

Never: rephrasing, reordering, cutting or adding content, changing word choice, smoothing a sentence into something it wasn't.

If a sentence is genuinely broken — dictation garbled a clause beyond repair — do not guess at a fix. Flag it inline (e.g. `[unclear: ...]`) and leave it for the user to resolve in their own words.

## Three ways to invoke it

### 1. File markers

Raw, unpolished text sitting in a vault file is wrapped like this:

```
%P
Dictated paragraphs go here.
Can span several paragraphs.
%
```

Both `%P` (open, case-insensitive — `%p` works too) and `%` (close) must sit alone on their own line — this is what lets a stray `%` in ordinary prose (e.g. "50% done") pass through without being mistaken for a marker.

This one convention covers every mode of use:
- **New file**: the user dictates straight into a new note, wrapped in `%P`/`%`. Polish it, strip the markers.
- **Append**: the user adds a `%P`/`%` block at the end of an existing file. Only that block is touched.
- **In-place edit**: the user goes back into an already-polished file and wraps just the bit they changed. No need to be told which paragraph — the marker says so.
- **Accumulation across sessions**: the user can dictate across several sessions, each in its own `%P`/`%` block. When invoked, process every unstripped block found, not just the most recent.

If a file has no `%P`/`%` block, say so and ask whether the user wants the whole file body polished instead. If they confirm, treat the entire body as the scope (no markers to strip).

### 2. In-chat, ephemeral

The user dictates raw text directly into a message with no file named. The message itself is the scope — no markers needed. Polish it, hold the result, and wait for a destination: the user may give it in the same message, a later message, or may already have named it up front (e.g. "polish this into the wireframe-review log: ...").

### 3. Coverage-check (conditional)

Triggered when the user names a second, source document alongside the thing being polished (e.g. "polish X against Y", "check X covers Y").

After the normal light-touch edit:
1. Read the source document.
2. Extract its key points.
3. Compare against the polished text.
4. Report gaps as a short bullet list in the chat — appended after presenting the polished text, never blended into the prose itself.

Default: report gaps to chat only. Do not write the gap list anywhere unless the user asks.

Coverage-check never fills a gap in the user's voice — it only names what's missing. If this ever needs to grow into something heavier (structured alignment scoring, multi-document synthesis), that belongs in `compose` or a review-style workflow, not here.

## Destination

Once polished, the result goes to whichever the user specified:
- A new file
- Appended to an existing file
- In place, replacing the marked block (markers stripped)
- Held in memory until the user names a destination (ephemeral mode)
