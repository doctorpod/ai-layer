---
tags: [ai-layer-docs]
sources:
  - vault/workflows/interview.md
checked: 2026-09-26
---

# interview thread

*One line of questioning in an [[interview workflow|interview]], ending in one conclusion, and recorded as one [[gathered note]].*

## The note

A thread lives in `guide/` as a note named with its two-digit number and a short topic, e.g. `01 choosing the framework.md`. On top of the five contract fields, it carries `date`, `thread` (its number) and `topic` (the question it chases).

The body is a record of the conversation:

```markdown
## Evidence (Claude)        ← optional: timeline entries bearing on the thread
## Q1 (Claude)              ← a question
## A1 (<your name>, 2026-09-12)     ← your answer, verbatim
## Evidence check (Claude)  ← only when the record disagrees or is silent
## Observations raised (Claude)
## Where thread 1 lands (Claude)   ← the conclusion
```

- **Your answers are saved verbatim.** The only changes allowed are removing duplicated dictation and fixing punctuation, noted in italics under the answer when made. Once saved, an answer is never edited. A correction goes in as a new answer (`A3 … — correction to A1`) and the original stays.
- **Every heading the assistant writes is labelled `(Claude)`.** That's how you tell its words from yours. The note isn't tagged `ai-generated`, because it's mostly your words.
- **Cross-section material** gets lifted into its own short note for the other section, with your words copied exactly and a link back to the thread. The assistant proposes this and does it only on your yes.

## Numbering

Threads are numbered for good. New proposals carry on from the highest number already used in the notes and the [[triage log]], so a dropped thread 3 is never reused.

## Open, closed, dropped

State is read from the note, never stored:

- **Open**: the latest `##` heading is anything short of a conclusion, usually an answer.
- **Closed**: the latest `##` heading is the conclusion, `Where thread <N> lands (Claude)`, its revised form, or any hand-worded heading starting `Where` and labelled `(Claude)`. On closing, one line goes into the [[triage log]].
- **Dropped**: you dropped the thread before it had a note. There's no note, just a line in the triage log so it isn't proposed again.

**Reopening.** Come back to a closed thread and the new Q&A is appended below the old conclusion, then closed again with `Where thread <N> lands — revised (Claude)`. The old conclusion stays; the latest wins. No new triage log line. If the note was `status: used`, it goes back to `pending`, and you're told why.

## Example

Thread 2 of the Hollin Lane reflection is still open: its latest heading is `## A2 (<your name>, 2026-09-19)`. When you next say "resume the interview", it's offered first.

## Related

- [[interview workflow]]
- [[interview timeline]]
- [[triage log]]
