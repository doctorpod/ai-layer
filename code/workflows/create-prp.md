---
name: create-prp
description: Synthesize a PRP from captured decisions (DECISIONS.md) — no interview.
---

# Workflow: Create PRP

Synthesize a `prp.md` (Product Requirements Prompt) from captured decision files. No grilling — that's `grill-me`'s job.

## Example usage

> [!quote] Create a PRP called CVT-123 to add a button that shows the invoice total

## Step 0: Resolve the topic folder

Determine the slug from the user's invocation. Look for `_AI/PRPs/<slug>/DECISIONS.md` and `QUESTIONS.md`.

- **If the slug is ambiguous or unstated**, list in-progress folders under `_AI/PRPs/` and ask the user which to use.
- **If `DECISIONS.md` is present**, read it. Also read the glossary named by the pointer line at the top of `DECISIONS.md` (tolerate its absence — the user may have chosen "none").
- **If `DECISIONS.md` is absent**, synthesize from the current conversation context. If context is thin, suggest running `grill-me` first to capture decisions before proceeding.
- **Check for `init.md`** in the same topic folder. If it's absent, proceed with no signal — this is expected and not a flag. If it's present, search it for a heading whose text contains "acceptance criteria" (case-insensitive) and extract everything under that heading verbatim for use in Step 3. If `init.md` is present but no such heading is found, record a pending flag to raise at Step 2 — don't raise it here.

## Step 1: Parking-lot gate

Check `QUESTIONS.md` (if present). If any items are unchecked (`- [ ]`):
- Present them to the user and ask for resolution.
- The PRP **cannot be finalised** until all items are marked `[x]`.

## Step 2: Validation checkpoint

Present to the user:
- The proposed module structure and implementation blueprint sketch
- Which modules need tests

Confirm with the user. Adjust based on feedback. This is the **one and only** checkpoint — do not conduct a relentless interview.

If Step 0 recorded a present-but-empty-AC-section flag, fold it into this same checkpoint rather than opening a second one: ask inline, "`init.md` found, but no Acceptance Criteria section detected — does this ticket have ACs to carry forward?"

## Step 3: Generate `prp.md`

Write `prp.md` into `_AI/PRPs/<slug>/`. Use this structure:

---

**Goal** — one sentence: what does this implement?

**Why** — the business reason

**Success criteria** — how will we know it's done? (observable, testable)

**Acceptance criteria (from ticket, verbatim)**

The AC text extracted from `init.md` in Step 0, carried through unchanged. Omit this section entirely — no placeholder, no "N/A" — when Step 0 extracted nothing.

**Context**

List the key files involved with a one-line note on each. Reference any `_AI/` docs that apply.

**Architecture notes**

Any codebase-specific constraints that apply to this ticket (from `_AI/OVERVIEW.md`). Describe the blueprint through a "deep modules" lens — simple interface, substantial behaviour. Repeat the relevant anti-patterns here so execution cannot miss them.

**Implementation blueprint**

Step-by-step implementation plan in dependency order:
- Use keywords: `create`, `modify`, `add`, `remove`, `migrate`, `move`
- One step = one logical change
- Include: migrations, model changes, service changes, query changes, controller changes, view changes, locale strings, spec changes
- Spec/test steps must appear **immediately before** the implementation step they cover — never after

**Validation gates**

The agent must run these in order and loop until each passes before moving on. The validation commands for this project are defined in `_AI/VALIDATION.md`.

**Anti-patterns for this ticket**

List the anti-patterns from `_AI/OVERVIEW.md` most likely to be violated given what this ticket touches.

**Confidence score**

Rate 1–10: how confident are you that a single execution pass will complete this correctly? Note what, if anything, would lower that score.

---

## Step 4: Self-review before saving

Before saving `prp.md`, verify:
- Does the blueprint match the project's architecture (as described in `_AI/OVERVIEW.md`)?
- Are all validation gates executable by the agent?
- Is the confidence score honest?
- If the PRP has an "Acceptance criteria" section, does every verbatim AC map to at least one Implementation blueprint step? If a gap is resolvable by a mechanical blueprint edit, revise the blueprint now — no second user round-trip. If a gap needs real judgment, add an unchecked item to `QUESTIONS.md` and treat the PRP as not-yet-finalized, per the Step 1 parking-lot rule.

## Step 5: Completion

Once `prp.md` is saved and approved, the folder is ready for execution. **Do not delete** `DECISIONS.md`, `QUESTIONS.md`, or `GLOSSARY.md`. The complete folder migrates to Obsidian after execute + review:

```
_AI/PRPs/[ticket-name]/
  prp.md         ← ready for execute-prp
  DECISIONS.md   ← permanent history
  QUESTIONS.md   ← all [x], permanent history
  GLOSSARY.md    ← if created locally (optional)
```
