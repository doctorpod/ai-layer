---
name: elicit
description: Turn a guide.md into prose in the writer's own words — live grilling or a portable prompts file — never AI-drafted, always extracted from what was actually said or written.
---

# Elicit Workflow

Generic to any guide.md-driven piece. Never drafts prose from scratch — every sentence traces back to something the writer said (live) or wrote (portable).

Triggered by: "elicit", "elicit section `<N>`", "let's elicit section `<N>`", "grill me on section `<N>` of the guide"

## Prerequisites

Piece-folder convention (`_AI/shared/snippets/piece-folder.md`): `brief.md`, `guide.md`, `output.md`, `assets/`. If `brief.md` or `guide.md` don't exist, point to compose's Steps 1–3 first.

If `brief.md` indicates Diploma-relevance, also read `lib/atlas/teaching/wiki/design-assessment-form.md` once per session — grounds the Step 2 filter (Sections 1, 2.1, 3).

## The working file

One file per section: `section-<N>.md` in the piece-folder. Holds everything until published to `output.md`:

```markdown
## Threads
- [ ] Thread name — passes filter, not started
- [x] Thread name — answered & assembled YYYY-MM-DD
- [-] Thread name — dropped, plain fact in Boring facts

## Boring facts
- Plainly stated fact, cited.

## Prompts               <!-- portable mode only -->
### Thread name
[prompt text]

## Draft
[assembled prose accumulates here, thread by thread]
```

## Step 0: Choose mode

Default **interactive**. Ask "interactive or portable?" if unclear.

## Step 1: Pick a section, cluster its points

Check `section-<N>.md`'s Threads checklist first — if it exists, resume from it, don't re-derive.

Otherwise, read the section's `guide.md` "Extracted points" and group related bullets into threads (don't grill bullet-by-bullet). Write the Threads checklist into `section-<N>.md` before grilling or writing any prompts.

## Step 2: Filter each thread

Passes only if **both**:

1. **Leads somewhere** — a concrete decision, recommendation, or observation relevant to the brief. Otherwise drop it, or, if worth keeping, state it plainly (→ Boring facts).
2. **The writer has a real basis for it** — noticed it, reacted to it, holds a genuine view. Otherwise don't manufacture a personal angle — state it plainly (→ Boring facts) instead, with a recommendation only if they're actually willing to make one professionally.

Threads that fail go into **Boring facts** as plainly cited sentences — not questions. Mark the thread `[-]` in the Threads checklist (same convention as `debrief.md`'s dismissed questions) — a resumed session must be able to tell "dropped" apart from "not started" without re-deriving it.

## Step 3: Elicit answers

**Interactive**: grill one surviving thread at a time, in chat — core technique from `debrief.md` Step 1 (offer a best interpretation, ask to confirm or correct, one question at a time, resolve before moving on), plus two additions specific to this workflow: push past flat statements toward the reasoning or tension underneath, and treat "enough" as a bidirectional signal — either side can call it, only stop once both agree. Go straight to Step 4 once resolved.

**Portable**: write an open, inviting prompt per surviving thread into the Prompts block — styled to draw out the personal account, self-contained enough to copy into Keep or read back cold. Populate Boring facts too. Then stop.

When the writer returns with pasted material (same or fresh session): match it to open threads (ask if ambiguous), then go to Step 4 for whichever threads now have material.

## Step 4: Extract and assemble

Not compose (never invent phrasing), not polish (this needs reordering, polish doesn't). Select and reorder the writer's own exact words; fix only clear surface slips; never introduce a word or phrase they didn't say or write. Drop meta-commentary. Minimal connective tissue, prefer punctuation over invented linking words.

## Step 5: Approval loop

Show the assembled passage:
- **"Good"** — move to Step 6
- **"Change X"** — re-cut/reorder; new wording must come from the writer
- **"It should say..."** — dictated replacement, used as given

Repeat until approved.

## Step 6: Write into the working file

Insert into `section-<N>.md`'s `## Draft`. Check off the thread with today's date. A related Boring facts item goes in as a plainly cited sentence, not folded into the narrative.

## Step 7: Once every thread is resolved — batch pipeline

Dropped threads count as resolved.

1. **Polish** the Draft in place — apply `_AI/local/workflows/polish.md`'s guarantee (spelling, punctuation, and structure only; nothing rephrased).
2. **Sanity-check** the Draft via `_AI/local/workflows/sanity.md`. It's diagnostic-only — it reports, it never fixes. Findings → report, ask fix-now-or-override (always ask, never remember a prior override). A "fix now" is never Claude patching the sentence to resolve it: take it back to the writer — a quick question, not a full re-grill — and use only the words they give, same rule as Step 4. Loop until clean or overridden.
3. **Gap-check** against the section's `guide.md` entry via `_AI/local/workflows/gap-check.md`. Same fix-or-override loop and the same rule: a genuine gap gets filled by eliciting it (back to Step 3 for that point), never by writing filler to cover it.
4. Check `output.md` for existing content in this section: none → show the Draft, ask for go-ahead, append; existing → ask append or overwrite.
5. Update `guide.md`'s marker to `✓`.
6. Leave `section-<N>.md` in place — it's the record of how the section was derived (dropped threads, prompts used in portable mode). `output.md` is authoritative for the prose itself once published.

## Step 8: Log

`bash _AI/local/scripts/log-write.sh "ELICIT: [section] — [brief summary]"`

## Step 9: Learnings

Follow `_AI/shared/snippets/learnings.md`, substituting `ELICIT` for `[WORKFLOW]`.

## Caveats

- Interactive mode is live/conversational only — no file-watcher, no background Monitor.
- Write each approved thread into `section-<N>.md` as it's approved, don't batch approvals.
- The Step 2 filter is a judgement call — ask when genuinely unsure.
