---
name: capture-log-note
description: Capture content as a dated log note in the correct gig log folder.
---

# Capture Log Note Workflow

Triggered by: "capture log note", "capture as a log note", or "log this"

## Step 1: Determine where to put the note

Try to derive the correct log folder from context — recently mentioned files, the knowledge base being discussed, or the subject matter of the content. Look for a `log/` subfolder near relevant project or gig folders, and place the note inside a `YYYY/` subfolder matching the current year.

If you cannot confidently determine the location, ask the user before proceeding.

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
tags: ["ai-generated"]
---

[content]
```

- Substitute real values for date and time
- Preserve the content faithfully — do not summarise or rewrite unless the user asks
- Wikilink any names, concepts, or entities that are likely to have pages in this vault

## Step 5: Confirm

Tell the user the full file path of the note created.
