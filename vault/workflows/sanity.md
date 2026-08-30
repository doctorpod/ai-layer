---
name: sanity
description: Read a body of the user's own writing and flag contradictions, non-sequiturs, and passages that don't hold up. Diagnostic only — never edits prose.
---

# Sanity Workflow

Use this workflow when the user wants a body of their own writing checked for internal coherence — not spelling or punctuation (that's `_AI/local/workflows/polish.md`), but whether it actually makes sense: contradictions, things that don't follow, passages that are just confusing or badly argued.

## The rule

**Polish never comments on content; sanity never touches prose.** Sanity is read/flag-only. It never rewrites, fixes, or improves a flagged passage — it names the problem and leaves the fix to the user, in their own words.

## Step 1: Establish scope

Parse whatever scope the user gives at call time — there is no default. Typical forms:

- **A named document**: "sanity this document", "sanity `output.md`"
- **Multiple named documents**
- **A time or count range**: "sanity all my log notes from the last three weeks", "sanity the last 5 entries"

Most invocations will name a single document — don't assume a temporal frame the way `_AI/local/workflows/reflect.md` does. If the scope isn't stated or is ambiguous, ask before proceeding.

## Step 2: Gather the material

Read everything in scope fully — don't skim.

## Step 3: Analyse

Look for whatever is actually present rather than forcing a fixed checklist. Candidates:

- **Contradictions** — claims or facts that conflict with each other, within the scope or against something the scope explicitly references
- **Non-sequiturs** — conclusions that don't follow from what precedes them
- **Confusing or unclear passages** — writing that doesn't communicate, regardless of correctness
- **Plain bad writing** — anything that just doesn't hold up on a careful read

Only surface what's genuinely there. One sharp finding beats a padded list.

## Step 4: Report

Deliver findings as a chat response — a short numbered list, each with a one-line pointer to where it is (file and line number, plus a short quote to anchor it) and what's wrong. Point at line numbers, not paragraph or section numbers ("¶2", "the third para") — they're exact and clickable. This holds wherever the findings land, including a scribe `% **comments**` block. Default: chat only, nothing written anywhere. If the user asks to capture the findings (e.g. as a log note, or fed into `_AI/local/workflows/add-to-radar.md`), do that on request — not automatically.

Do not fix anything found. If a finding is itself a spelling/punctuation issue, that's out of scope here — mention it only if it's tangled up in a content problem worth flagging anyway.
