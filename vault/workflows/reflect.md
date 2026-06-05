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

If the scope is ambiguous, ask before proceeding.

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

## Step 6: Thread capture

If the findings include open loops, offer to run the threads workflow (`_AI/local/workflows/threads.md`) in Capture mode for each one. Scan existing threads first — only propose genuinely new threads, not things already being tracked.
