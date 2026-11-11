A Question records something unknown about a subject. Questions live only in a knowledge base, in its `questions/` subfolder: never in a gig or project folder.

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
[The question prose — no separate `who:` field]
- [ ] Ask <who> <what>

## Answer
[Empty until resolved]
```

**Status values:**
- `pending` — open, unanswered, not yet load-bearing anywhere. Default starting state.
- `surmised` — still unanswered, but the assistant has written a provisional answer into a wiki page anyway.
- `confirmed` — answered, matches what was assumed.
- `rejected` — answered, contradicts what was assumed.
- `dismissed` — closed without ever getting an answer, because it stopped mattering.

**Chase task**: each `pending` Question carries exactly one task line under `## Question`, saying who to ask and what ("- [ ] Ask Stephen who Anne is"). Link it to a thread (a wayfinder map or a ticket) where one fits. This is how the Question reaches `NEXT.md`: chasing it is a task, and Frontier lists it while the Question is `pending`. When the answer comes, it's logged in a log note, and `debrief` carries it into the wiki.

**Inline reference**: a piped wikilink shortens the display form — `[[Qn - <slug>|Qn]]`. No `aliases:` frontmatter needed.

## Creating a Question

1. **Scan first** — run `python3 _AI/local/scripts/list-questions.py <questions-folder>` to see all existing Questions in scope with their status/opened/updated in one pass. Do not create a duplicate; if an existing open Question already covers the gap, reuse it instead.
2. **Create the note** — write the question prose and its chase task under `## Question`, and set `status: pending`.

## Closing a Question

Setting any status other than `pending` closes it. Fill in `## Answer`, bump `updated:`, and close the chase task: tick it (`[x]` with `✅ YYYY-MM-DD`) when the Question was answered (`confirmed`, `rejected`), or drop it (`[-]`) when it wasn't (`surmised`, `dismissed`).

## Dismissing a Question

If a Question isn't pertinent — at the moment it's raised, or later on review — set `status: dismissed`, write the reason into `## Answer`, and drop its chase task. Never delete a Question outright; dismiss it instead, so the reasoning stays on record.
