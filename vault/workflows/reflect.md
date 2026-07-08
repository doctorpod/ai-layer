---
name: reflect
description: Review a specified scope of notes and surface patterns, observations, and open loops as a chat response.
---

# Reflect Workflow

Triggered by: "reflect" + a scope (e.g. "last 3 days", "this week's log notes", "recent entries")

## Step 1: Establish scope

Parse the scope from the user's request. Typical forms:
- Time-based: "last N days/weeks"
- Count-based: "last N log notes"
- Explicit: named files or a date range

If the scope is phrased relative to a prior reflection (e.g. "since our last reflection"), find the most recent existing note with `categories: ["[[Reflections]]"]` and use its date as the start date — do not ask the user if one exists. If no such note exists yet, ask before proceeding.

If the scope is otherwise ambiguous, ask before proceeding.

## Step 2: Gather the notes

Find and read the relevant notes. Use `date` or file timestamps to anchor time-based scopes. Read fully — don't skim.

**Do not read anything inside `_AI/`.** That folder is AI layer infrastructure (workflow logs, ingestion records, config). It is not work content.

For time-based scopes, use `_AI/local/scripts/list-log-notes.sh YYYY-MM-DD` (run from the vault root) to get all log notes from that date to the latest. Calculate the start date from the scope before running it.

## Step 3: Analyse

Look for whatever is actually present and interesting. Do not force a fixed set of headings. Candidates include:

- **Patterns** — recurring themes, names, blockers, or dynamics
- **Momentum** — things gaining traction or stalling
- **Surprises** — anything that stands out as unexpected or significant
- **Open loops** — unresolved questions, decisions pending, threads dropped mid-conversation
- **Connections** — links between things that haven't been explicitly connected yet

Only surface categories that have genuine content. One sharp observation beats a padded list.

## Step 4: Clarify

If anything in the notes is ambiguous — an unclear outcome, a name without context, a thread you can't interpret — ask the user before presenting findings. Ask questions one at a time as per `_AI/shared/workflows/grill-me.md`.

## Step 5: Respond

Deliver findings as a chat response. Keep it dense and scannable — use short headers and bullets. No preamble.

Retain the findings in context: the user may follow up by asking to capture them (e.g. as a log note) or feed them into another workflow.

## Step 6: Radar capture

If the findings include open loops, offer to run the add-to-radar workflow (`_AI/local/workflows/add-to-radar.md`) in Capture mode for each one. Scan existing radar items first — only propose genuinely new items, not things already being tracked.

## Step 7: Capture as a reflection note

If the user asks to capture the reflection (e.g. "capture this reflection", "log this"), use this frontmatter instead of the generic `capture-log-note.md` format — it carries the `[[Reflections]]` category and its schema (see `templates/reflection.md`):

```
---
date: "[[YYYY-MM-DD]]"
time: "HH:MM"
categories:
  - "[[Reflections]]"
last_reflection: "[[<link to the previous reflection note>]]"
tags:
  - ai-generated
---
```

- `last_reflection` links to the reflection note used to establish scope in Step 1 (the most recent prior one found by category). Omit the field if this is the first reflection ever captured.
- Otherwise follow `capture-log-note.md` for filename, folder, and title conventions — only the frontmatter differs.
- Content is the findings delivered in Step 5, preserved faithfully.
