---
name: gap-check
description: Check a draft against its guide (or another named reference) and report what's missing. Diagnostic only — never edits.
---

# Gap Check

Triggered by: "gap check `<file>`", "gap check `<file>` against `<reference>`", "check gaps in `<file>`", "does `<file>` cover `<reference>`"

Compares a document against a reference and reports what's missing. Read-only — never edits either file, never fixes what it flags.

## Step 1: Establish target and reference

- **Target**: the document being checked (usually `output.md`).
- **Reference**: what it's checked against.
  - If the user names one, use it.
  - If they don't, and the target sits in a piece-folder, default to that folder's `guide.md`.
  - If neither applies, ask.

## Step 2: Compare

Read both in full. Extract the reference's key points or required sections. Check each against the target: covered, thin, or missing.

## Step 3: Report

Chat response only, by default — a short list, one line per gap: what the reference called for, and whether it's absent or underdeveloped in the target. No verdict, no score. This workflow only ever names gaps.

Don't fix anything. Don't write the gap list anywhere unless the user asks.
