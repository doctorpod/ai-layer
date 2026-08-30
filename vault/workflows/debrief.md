---
name: debrief
description: Process first-hand material (site visit, conversation, observation) where accuracy is paramount.
---

# Debrief Workflow

Use this workflow when the user has first-hand material to process — a site visit, a conversation with someone, a memory, an observation, or a thought they've worked out. The source is the user themselves. Truth and accuracy are paramount.

## Step 0: Establish the source

Check the single `inbox/` at the vault root for any notes, field notes, or transcripts the user has dropped in for *this* debrief. The inbox is shared across every KB and may hold unrelated items, so don't assume everything in it is in scope — match by filename, content, or the user pointing you at a specific file. Read the relevant ones fully before proceeding.

If nothing in `inbox/` is relevant, proceed with a chat-based debrief — the user will tell you directly.

## Step 1: Grill relentlessly

Before writing a single word of wiki content, grill the user until you are **95–97% certain** you have the facts right. Follow the approach in `_AI/shared/workflows/grill-me.md`: walk down each branch of the subject, resolving dependencies one-by-one before moving on to the next branch.

Rules:
- Ask one question at a time. Wait for the answer. Resolve it. Then move to the next.
- For each uncertain claim, offer your best interpretation and ask the user to confirm or correct — don't fire blank questions. Example: *"You mentioned the south wall — do you mean the boundary wall running east–west, or the wall of the building itself?"*
- Resolve dependencies before moving on: if a claim depends on an undefined term or unclear context, resolve that first.
- Work through every claim: are the specifics right? Names spelled correctly? Numbers verified? Dates confirmed? Context clear?
- If a term is ambiguous, resolve it before moving on.
- If a claim can't be resolved by the user but is externally verifiable (a definition, a public record, a company or place detail — not something only a person or the site itself could confirm), do a web search on the spot and present what you find for the user to confirm or correct. Don't write it into the wiki unconfirmed.
- If a claim still cannot be resolved (needs checking with a person or on site, or the search comes up empty or unreliable), do not guess — log it as an outstanding question (see Step 2).
- Do not stop early. If something feels vague, push on it.

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

### Dismissing a question

If the user says a question isn't pertinent — at the moment it's raised, or later when reviewing `QUESTIONS.md` — dismiss it rather than leaving it open or deleting it. Use `- [-]` (the vault's Tasks plugin "Cancelled" status, distinct from `- [x]` Done) and append the reason:

```markdown
- [-] Q4 · 2026-08-05 · Check with Ian / LPA: has the TPO status ever been established? ✗ Dismissed 2026-08-06: not relevant to current design scope.
```

Never delete a question outright — dismiss it instead, so the reasoning stays on record.

## Step 3: Concept notes and SPATIAL.md

**Closing pass (after wiki writing is complete):** follow the concept note rules in `_AI/local/workflows/ingest.md` Step 9. Do this as a named step — don't skip it.

**SPATIAL pass:** if `SPATIAL.md` exists in this KB, check whether any location claims made during the debrief need adding or correcting. If `SPATIAL.md` doesn't exist but the debrief produced location claims about a physical site, offer to create it. Format: see `_AI/local/AI.md`.

## Step 3b: Cross-workflow check

Follow `_AI/shared/snippets/cross-workflow-check.md`, substituting `established during this debrief` for `[CONTEXT]`.

## Step 4: Create debrief note

Always create a debrief note and save it directly to `curated/` — it is already verified.

Filename: `debrief-YYYY-MM-DD-[brief-description].md`

**If no inbox notes exist**: write a compact factual summary of everything established during the debrief — verified facts in plain prose, dense and complete. This is the primary citable source for wiki pages.

**If inbox notes exist**: write a shorter document capturing only what the grilling *added* — clarifications, corrections, additional context, and anything the user said that wasn't in the raw notes. The inbox note remains the primary record; this captures the verified delta. Label it clearly at the top:

```markdown
> Debrief note — clarifications and additions to [inbox filename]. Not a full summary.
```

## Steps 5–9: Write wiki content and close

> **Page format**: defined in `_AI/local/workflows/ingest.md` — apply it to every wiki page written from a debrief without exception.

Follow `_AI/shared/snippets/wiki-write-steps.md`, substituting `subject` for `[NOUN]` and `DEBRIEF` for `[WORKFLOW]`.

## Citation rules

Follow the citation rules in `_AI/local/workflows/ingest.md`. Every wiki claim must reference its source — either an inbox file or the synthetic debrief note from Step 4. Use `[!caution]` callouts for any claim that remains uncertain after grilling.

The multi-source trigger in `ingest.md` applies here too: if this debrief is the *second* debrief (or an ingest) to touch an existing page — a follow-up conversation about something already written up — switch that page to per-claim footnotes rather than folding the new debrief note's claims into the earlier sentences.

## Step 10: Learnings

Follow `_AI/shared/snippets/learnings.md`, substituting `DEBRIEF` for `[WORKFLOW]`.
