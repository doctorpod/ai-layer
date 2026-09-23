---
name: gratitude
description: Ground in recent journal notes, offer prompts to help the user write gratitude entries, polish each entry as it's written, and append approved entries to today's daily note (creating it from the daily template if missing).
---

# Gratitude Workflow

Triggered by: "gratitude", "help me write gratitude entries", "gratitude prompts"

The entries are the user's own words. I prompt, give feedback, and polish. I never write the gratitude for them.

## Step 1: Locate the journal

Read `.obsidian/daily-notes.json` at the vault root for:
- `folder`: where daily notes live
- `format`: the filename date format (e.g. `YYYY-MM-DD`)
- `template`: the daily note template (path without `.md`)

If the file is missing or has no `folder`, ask the user where their daily notes are. Don't guess.

## Step 2: Ground in recent notes

Read the last ~6 dated daily notes, counting by the notes that exist rather than by calendar days, and including today's note if there is one. Read them in full.

Follow the content-provenance rule in `AI.md`: skip or flag anything tagged `ai-generated`. The prompts must come from the user's own life, not from something a past session wrote.

Also check memory for recent context that shapes the tone, such as illness, bereavement or a family member in decline.

## Step 3: Offer prompts

Give 5–7 numbered prompts. Each one has:
- **A statement** in bold, grounded in something specific from the notes, with the concrete detail included (a date, a name, the user's own quoted phrase).
- **A question** (`→`) that pushes toward a particular moment or toward *why* it mattered. "What are you grateful for about X?" is too vague.

Guidelines:
- Cover a range of areas: people, place, body and health, work, small domestic pleasures, things that went better than feared.
- For painful subjects (illness, decline, loss), still offer a prompt, but say plainly that it's optional ("only if it feels right").
- Don't make up details or inflate what the notes say. If the notes don't say how something turned out, ask about it.

End by inviting the user to pick whichever prompts they like and write in their own words, however rough.

## Step 4: Respond to each entry

When the user writes an entry:

1. **Honest, brief feedback.** Say what works, especially specificity and the *why*. If the entry is thin, say so kindly. Don't flatter it.
2. **Optional deepening.** Ask one or two questions that could make the entry more specific (who, which moment, what it meant). Make clear the entry is fine as it stands. Point out anything that could be a separate entry, or that ties into a bigger thread, without taking over the entry.
3. **Polish.** Follow the rules in `_AI/local/workflows/polish.md`: fix spelling, punctuation and obvious dictation artifacts only. Don't rephrase, reorder, cut or change word choice. If a missing conjunction or article makes a sentence hard to read, add the smallest word that fixes it. **List every change made**, even small ones.
4. **Wikilinks.** Suggest a `[[link]]` only when the note already exists in the vault (check first). Say which links were added and offer to remove them.
5. **Show the result** in a code block as it would appear in the note:

   ```markdown
   ## Gratitude

   <entry>
   ```

6. **Offer to append.** Name the target file. Also offer to wait so several entries can go in together.

If the user revises the entry, go back to 4.1 with the new version. Always polish their latest wording, not an earlier draft.

## Step 5: Append on confirmation

Writing to the daily note is outside the `AI.md` write allowlist. The user's explicit "yes" in Step 4 is the permission for this one write. Don't append without it.

### 5a: Make sure today's note exists

Today's note is `<folder>/<today in format>.md`. If it doesn't exist:

1. Read the template (`<template>.md`).
2. Replace date tokens with today's date: `{{date:FORMAT}}` in the given moment.js format (`[...]` is literal text), a bare `{{date}}` in the daily-notes `format` from Step 1, `{{title}}` with the filename without `.md`, and `{{time}}` as `HH:mm`.
3. Keep everything else exactly as it is, including embeds, dataview blocks and placeholder markers that the user's own tooling fills in later.
4. Create the file, then tell the user it was created from the template.

If the template can't be found, ask before creating a bare note.

### 5b: Append

- If the note has no `## Gratitude` heading, add one at the end of the file with a blank line before it, then a blank line and the entry as a paragraph.
- If the heading already exists, add the entry as a new paragraph at the end of that section, separated by a blank line and placed before the next heading if there is one.
- Check the file ends with a newline before appending, so the heading doesn't join onto the last line.

Show the tail of the file to confirm the write, and say where the entry went.

## Step 6: Continue or close

Offer another prompt or another entry. Later entries in the same session go under the same heading. Don't prompt forever: after an entry is appended, one short offer is enough.
