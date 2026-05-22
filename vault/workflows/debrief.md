---
name: debrief
description: Process first-hand material (site visit, conversation, observation) where accuracy is paramount.
---

# Debrief Workflow

Use this workflow when the user has first-hand material to process — a site visit, a conversation with someone, a memory, an observation, or a thought they've worked out. The source is the user themselves. Truth and accuracy are paramount.

## Step 0: Establish the source

Check `inbox/` for any notes, field notes, or transcripts the user has dropped in. Read them fully before proceeding.

If `inbox/` is empty, proceed with a chat-based debrief — the user will tell you directly.

## Step 1: Grill relentlessly

Before writing a single word of wiki content, grill the user until you are **95–97% certain** you have the facts right. Follow the approach in [[grill-me]]: walk down each branch of the subject, resolving dependencies one-by-one before moving on to the next branch.

Rules:
- Ask one question at a time. Wait for the answer. Resolve it. Then move to the next.
- For each uncertain claim, offer your best interpretation and ask the user to confirm or correct — don't fire blank questions. Example: *"You mentioned the south wall — do you mean the boundary wall running east–west, or the wall of the building itself?"*
- Resolve dependencies before moving on: if a claim depends on an undefined term or unclear context, resolve that first.
- Work through every claim: are the specifics right? Names spelled correctly? Numbers verified? Dates confirmed? Context clear?
- If a term is ambiguous, resolve it before moving on.
- If a claim cannot be resolved in this conversation (needs checking with a person or on site), do not guess — log it as an outstanding question (see Step 2).
- Do not stop early. If something feels vague, push on it.

**Glossary checks**: if the user uses a term already in `GLOSSARY.md` and it's unclear whether they mean the same thing, challenge them inline: *"You said [term] — do you mean [glossary definition]?"* Resolve before continuing.

## Step 2: Maintain QUESTIONS.md

If any questions cannot be resolved during the debrief, add them to `QUESTIONS.md` at the project root. Create the file if it doesn't exist.

Format:
```markdown
- [ ] Q1 · YYYY-MM-DD · Ask [person]: [question]
- [ ] Q2 · YYYY-MM-DD · Check on site: [question]
```

Rules:
- Q-numbers are sequential and never reused — check the file for the last number used and continue from there.
- Always include: checkbox, Q-number, date raised, who/what to check with, and the question.
- When an inbox note later answers a question (by Q-number or obvious content), process the answer into the wiki and delete the resolved question from `QUESTIONS.md`.

## Step 3: Maintain GLOSSARY.md and SPATIAL.md

**Inline (during grilling):** if a term already in `GLOSSARY.md` is used ambiguously, challenge it: *"You said [term] — do you mean [glossary definition]?"* Resolve before continuing.

**Closing pass (after wiki writing is complete):** scan everything written and propose adding any term, named feature, or concept not yet in `GLOSSARY.md`. Do this as a named step — don't skip it. Propose additions one at a time. Only add with the user's confirmation.

Create `GLOSSARY.md` at the project root if it doesn't exist. Keep entries as a flat alphabetical list — no letter headings.

Format:
```markdown
**south wall** — the boundary wall running east–west along the southern edge of the churchyard. Excludes the gate pier.
```

**SPATIAL pass:** if `SPATIAL.md` exists in this KB, check whether any location claims made during the debrief need adding or correcting. If `SPATIAL.md` doesn't exist but the debrief produced location claims about a physical site, offer to create it. Format: see [[_AI/core/AI.md]].

## Step 4: Create debrief note

Always create a debrief note and save it directly to `curated/` — it is already verified.

Filename: `debrief-YYYY-MM-DD-[brief-description].md`

**If no inbox notes exist**: write a compact factual summary of everything established during the debrief — verified facts in plain prose, dense and complete. This is the primary citable source for wiki pages.

**If inbox notes exist**: write a shorter document capturing only what the grilling *added* — clarifications, corrections, additional context, and anything the user said that wasn't in the raw notes. The inbox note remains the primary record; this captures the verified delta. Label it clearly at the top:

```markdown
> Debrief note — clarifications and additions to [inbox filename]. Not a full summary.
```

## Steps 5–9: Write wiki content and close

> **Page format**: defined in [[ingest]] — apply it to every wiki page written from a debrief without exception.

1. Create a summary page in `wiki/` named after the subject
2. Create or update concept pages in `wiki/` for each major idea or entity
3. Add wikilinks `[[page-name]]` to connect related pages
4. If you see a person's name, wikilink it — do not create a note for them
5. Update `INDEX.md` with new pages and one-line descriptions
6. Append a log entry: `bash _AI/core/scripts/log-write.sh "DEBRIEF: <brief summary>"`
7. Move any inbox files to `curated/`

## Citation rules

Follow the citation rules in [[ingest]]. Every wiki claim must reference its source — either an inbox file or the synthetic debrief note from Step 4. Use `[!caution]` callouts for any claim that remains uncertain after grilling.
