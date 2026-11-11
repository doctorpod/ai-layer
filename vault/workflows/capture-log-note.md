---
name: capture-log-note
description: Capture content as a dated log note in the correct gig log folder.
---

# Capture Log Note Workflow

Triggered by: "capture log note", "capture as a log note", or "log this"

## Step 1: Determine where to put the note

Try to derive the correct log folder from context — recently mentioned files, the knowledge base being discussed, or the subject matter of the content. Look for a `log/` subfolder near relevant project or gig folders, and place the note inside a `YYYY/` subfolder matching the current year.

If no `log/` folder exists anywhere relevant, stop and tell the user this vault doesn't appear to use log files — don't invent one or fall back to another surface (e.g. the journal) on your own judgement.

If `log/` folders exist but it's ambiguous which one applies, ask the user which to use.

## Step 2: Get current timestamp

Run `date +"%Y-%m-%d %H:%M"` to get the current date and time.

## Step 3: Infer a title

Derive a short, descriptive title from the content (3–6 words, lower case). Prefer noun phrases over sentences.

## Step 4: Create the file

Filename: `YYYY-MM-DD [title].md`

```
---
date: "[[YYYY-MM-DD]]"
time: "HH:MM"
tags:
  - ai-generated
---

[content]
```

- Substitute real values for date and time
- Never add a `status:` field. In a vault that heartbeat sweeps, a log note with no `status:` is one nothing has been done to yet, so heartbeat picks it up (or minute runs it at once).
- Preserve the content faithfully — do not summarise or rewrite unless the user asks
- Wikilink any names, concepts, or entities that are likely to have pages in this vault

## Step 5: Confirm

Tell the user the full file path of the note created.
