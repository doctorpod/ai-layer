---
name: readback
description: Check the user's own explanation of something against the real evidence, correcting it until they've got it right.
---

# Workflow: Readback

Have the user write, unprompted, what they believe is true about a specific thing, then correct it against the real evidence until they've got it right.

## Example usage

> [!quote] Readback — explain the auth change we just built

## Before you start

- Ground yourself in the real evidence for the thing being explained before the user writes anything:
  - In a code project with a PRP just executed: read `git diff main...HEAD` and the PRP's `prp.md` (goal + success criteria).
  - Otherwise: use whatever is already in context — the files, discussion, or work the user is pointing at.
- If grounding requires exploring files not yet in context, explore them silently rather than asking the user to supply them.

## How to check

- Wait for the user to write their paragraph unprompted — don't ask them questions or supply your own summary first.
- Compare their paragraph against the evidence, then respond with:
  - A brief verdict on how close they are, in plain language ("mostly right", "close but missing X") — not a score.
  - A list of specific misunderstandings or gaps, each grounded in a file/line or concrete fact, not just "you're wrong."
- If their paragraph exposes a real mismatch between the evidence and its own stated intent (e.g. the code doesn't actually do what the PRP says), rather than a misunderstanding on their part, flag that explicitly as a likely code/PRP issue — distinct from a correction — instead of steering them to match their belief to something that looks wrong.
- The user revises and resubmits; repeat.

## When to stop

Stop when the explanation is fully accurate and the user is satisfied — say so plainly ("that's accurate now") rather than continuing to probe. This is a chat-only exercise: nothing is written to disk, and the final paragraph isn't assumed to be headed anywhere specific — it's whatever the user needs it for.
