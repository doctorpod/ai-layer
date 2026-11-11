---
name: minute
description: Shortcut for "log it and apply it now". Capture a log note (or take the one pointed at), then run heartbeat on just that note.
---

# Minute

Triggered by: "minute this", "minute that", "minute it"

minute has no rules of its own. Everything about processing the note is in `_AI/local/workflows/heartbeat.md`.

## Step 1: Get the note

If the owner pointed at an existing note, use it. Otherwise capture one per `_AI/local/workflows/capture-log-note.md`.

## Step 2: Run heartbeat on it

Run `_AI/local/workflows/heartbeat.md` in single-note mode on that note.
