---
name: add-to-radar
description: Capture, update, and review ongoing things worth tracking that may or may not require action.
---

# Radar Workflow

Triggered by: "add to radar", "capture on radar", "update radar", "review radar"

A radar item is something worth keeping an eye on — an unresolved situation, a decision pending elsewhere, a dynamic worth monitoring. Not necessarily a task, and not necessarily yours to act on.

## Scope

Radar items are scoped to the current gig, project, or knowledge base. Derive scope from context. If unable, ask before proceeding.

Radar notes live in a `radar/` subfolder within the scoped project.

## Note format

Filename: `[short-descriptive-title].md` (kebab-case, no date prefix)

```
---
categories: ["[[Radar]]"]
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
![[logs.base]]
```

**Status values:**
- `watching` — live and worth monitoring
- `dormant` — not active right now but unresolved
- `not-mine` — acknowledged; someone else's to act on
- `resolved` — closed

---

## Mode: Capture

Use when a review, debrief, or conversation surfaces something radar-worthy.

1. **Scan first** — find all existing radar notes in the scoped `radar/` folder and read their `latest:` frontmatter. Do not create a duplicate; if a matching radar item exists, switch to Update mode instead.
2. **Assess** — is this genuinely worth tracking, or just noise? Prefer fewer, sharper radar items over comprehensive coverage.
3. **Create the note** — write context and set status to `watching` unless clearly otherwise.
4. **Confirm** — tell the user the filename and one-line summary.

## Mode: Update

Use when there is new information about an existing radar item.

1. Update the `latest:` frontmatter field.
2. Offer to capture a log note with a link to the radar item if appropriate - `_AI/local/capture-log-note.md`
3. Update the `updated` frontmatter field.
4. Reassess status — has anything changed? Should this become `dormant`, `not-mine`, or `resolved`?

## Mode: Review

Use when the user asks to review radar items, or as a closing step in the `review` workflow.

1. Read all radar notes in scope.
2. Respond in chat with a scannable summary — status, `latest:` value, and any radar items that look stale or ready to close.
3. Invite the user to update or close any items.
