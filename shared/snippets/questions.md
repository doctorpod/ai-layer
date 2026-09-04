Questions are scoped to the current gig, project, or knowledge base, in a `questions/` subfolder within the scoped project.

## Note format

Filename: `Qn - <Short sentence-case description>.md` — `n` is sequential and never reused within that folder. Scan the folder's existing files for the highest leading `Qn` to find the next number.

```markdown
---
categories: ["[[Questions]]"]
status: pending
opened: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - ai-generated
---

## Question
[The question prose, including who to ask if relevant — no separate `who:` field]

## Answer
[Empty until resolved]
```

**Status values:**
- `pending` — open, unanswered, not yet load-bearing anywhere. Default starting state.
- `surmised` — still unanswered, but the assistant has written a provisional answer into a wiki page anyway.
- `confirmed` — answered, matches what was assumed.
- `rejected` — answered, contradicts what was assumed.
- `dismissed` — closed without ever getting an answer, because it stopped mattering.

**Inline reference**: a piped wikilink shortens the display form — `[[Qn - <slug>|Qn]]`. No `aliases:` frontmatter needed.

## Creating a Question

1. **Scan first** — run `python3 _AI/local/scripts/list-questions.py <questions-folder>` to see all existing Questions in scope with their status/opened/updated in one pass. Do not create a duplicate; if an existing open Question already covers the gap, reuse it instead.
2. **Create the note** — write the question prose under `## Question` and set `status: pending`.

## Dismissing a Question

If a Question isn't pertinent — at the moment it's raised, or later on review — set `status: dismissed` and write the reason into `## Answer`. Never delete a Question outright; dismiss it instead, so the reasoning stays on record.
