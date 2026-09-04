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

## Step 2: Maintain Questions

Follow `_AI/shared/snippets/questions.md` for creating and maintaining Questions.

## Step 3: Concept notes and SPATIAL.md

**Closing pass (after wiki writing is complete):** follow the concept note rules in `_AI/local/workflows/ingest.md` Step 9. Do this as a named step — don't skip it.

**SPATIAL pass:** if `SPATIAL.md` exists in this KB, check whether any location claims made during the debrief need adding or correcting. If `SPATIAL.md` doesn't exist but the debrief produced location claims about a physical site, offer to create it. Format: see `_AI/local/AI.md`.

## Step 3b: Cross-workflow check

Follow `_AI/shared/snippets/cross-workflow-check.md`, substituting `established during this debrief` for `[CONTEXT]`.

## Step 4: Create debrief note

**No inbox notes exist**: write a compact factual summary of everything established during the debrief — verified facts in plain prose, dense and complete. This is the primary citable source for wiki pages. Keep it a full prose summary even though wiki content is now spread across many small concept pages (ingest.md Step 2a): *because* it is spread thin, this note is the one place the whole picture stays coherent. Don't trim it to match the wiki's granularity. Save it directly to `curated/` — it is already verified. Filename: `debrief-YYYY-MM-DD-[brief-description].md`.

**Exactly one inbox file in scope**: append a `## Debrief (YYYY-MM-DD)` section to the end of that inbox file itself, capturing only what the grilling *added* — clarifications, corrections, additional context, and anything the user said that wasn't in the raw notes. The rest of the inbox file remains the primary record; this section is the verified delta, placed right next to what it's clarifying instead of in a sibling file. Do this before the file is moved to `curated/` in Step 7 of `wiki-write-steps.md` — that step just moves the now-enriched file, no change needed there.

No "has this been triaged" check is needed before appending: Step 0 only ever reads from `inbox/`, and a file can't be triaged by `sync-guide` until it's moved to `curated/`, which only happens after this step. So any inbox file reaching this step is always pre-triage by construction — the restriction is structural, not something to test for at runtime.

**Two or more inbox files in scope**: write a new debrief note capturing the session-wide delta — clarifications, corrections, additional context spanning the files, not tied to any one of them. Save it directly to `curated/` — it is already verified. Filename: `debrief-YYYY-MM-DD-[brief-description].md`. Label it clearly at the top, and list every inbox file it draws from via a `**Sources**:` field, matching the wiki page convention in `ingest.md`:

```markdown
> Debrief note — clarifications and additions to the inbox files below. Not a full summary.

**Sources**: [[inbox-file-one]], [[inbox-file-two]]
```

Don't add a forward link from the inbox files back to this note — Obsidian's backlinks panel already surfaces that direction for anyone who wants it.

## Steps 5–9: Write wiki content and close

> **Page format**: defined in `_AI/local/workflows/ingest.md` — apply it to every wiki page written from a debrief without exception.
> **Page sizing**: the existing-home check, the one-sentence sizing test, the two-part concept-page shape, and the pointer-style summary page (ingest.md Step 2a) all apply to debriefs too.

Follow `_AI/shared/snippets/wiki-write-steps.md`, substituting `subject` for `[NOUN]` and `DEBRIEF` for `[WORKFLOW]`.

## Citation rules

Follow the citation rules in `_AI/local/workflows/ingest.md`. Every wiki claim must reference its source — the inbox file (now carrying any appended debrief delta), or a separate debrief file when Step 4 created one (no inbox notes existed, or multiple were in scope). Use `[!caution]` callouts for any claim that remains uncertain after grilling.

The multi-source trigger in `ingest.md` applies here too: if this debrief is the *second* debrief (or an ingest) to touch an existing page — a follow-up conversation about something already written up — switch that page to per-claim footnotes rather than folding the new debrief note's claims into the earlier sentences.

## Step 10: Learnings

Follow `_AI/shared/snippets/learnings.md`, substituting `DEBRIEF` for `[WORKFLOW]`.
