---
name: threads
description: Capture, update, and review ongoing threads — things worth tracking that may or may not require action.
---

# Threads Workflow

Triggered by: "threads", "capture as a thread", "update thread", "review threads"

A thread is something worth keeping an eye on — an unresolved situation, a decision pending elsewhere, a dynamic worth monitoring. Not necessarily a task, and not necessarily yours to act on.

## Scope

Threads are scoped to the current gig, project, or knowledge base. Derive scope from context. If unable, ask before proceeding.

Thread notes live in a `threads/` subfolder within the scoped project.

## Note format

Filename: `[short-descriptive-title].md` (kebab-case, no date prefix)

```
---
categories: ["[[Thread]]"]
status: watching
opened: YYYY-MM-DD
updated: YYYY-MM-DD
latest: "[one-line current status]"
tags:
  - ai-generated
---

## Context
[Background — what this is and why it matters]

## Log
- YYYY-MM-DD: [entry]
```

**Status values:**
- `watching` — live and worth monitoring
- `dormant` — not active right now but unresolved
- `not-mine` — acknowledged; someone else's to act on
- `resolved` — closed

---

## Mode: Capture

Use when a review, debrief, or conversation surfaces something thread-worthy.

1. **Scan first** — find all existing thread notes in the scoped `threads/` folder and read their `latest:` frontmatter. Do not create a duplicate; if a matching thread exists, switch to Update mode instead.
2. **Assess** — is this genuinely worth tracking, or just noise? Prefer fewer, sharper threads over comprehensive coverage.
3. **Create the note** — write context and an opening log entry. Set status to `watching` unless clearly otherwise.
4. **Confirm** — tell the user the filename and one-line summary.

## Mode: Update

Use when there is new information about an existing thread.

1. Update the `latest:` frontmatter field.
2. Append a dated entry to the log.
3. Update the `updated` frontmatter field.
4. Reassess status — has anything changed? Should this become `dormant`, `not-mine`, or `resolved`?

## Mode: Review

Use when the user asks to review threads, or as a closing step in the `review` workflow.

1. Read all thread notes in scope.
2. Respond in chat with a scannable summary — status, `latest:` value, and any threads that look stale or ready to close.
3. Invite the user to update or close any items.
