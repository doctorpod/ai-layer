---
name: create-plan
description: Synthesize a plan and its slices from captured decisions (DECISIONS.md) — no interview.
---

# Workflow: Create Plan

Synthesize a `plan.md` and its slice notes from captured decision files. The plan holds what applies to the whole ticket; each slice is one independently mergeable change, delivered as one PR, carrying its own blueprint. No grilling — that's `grill-me`'s job.

## Example usage

> [!quote] Create a plan for CVT-123 — add a button that shows the invoice total

## Step 0: Resolve the work folder

Resolve the work folder (see **Work folders** in `_AI/local/AI.md`). Then read what's in it:

- **If `DECISIONS.md` is present**, read it. Also read the glossary named by the pointer line at the top of `DECISIONS.md` (tolerate its absence — the user may have chosen "none").
- **If `DECISIONS.md` is absent**, synthesize from the current conversation context. If context is thin, suggest running `grill-me` first to capture decisions before proceeding.
- **Read `init.md`** if present. If its frontmatter has `ticket:`, read the ticket snapshot via the wikilink rule.
- **Extract the acceptance criteria** for use in Step 3. The source is the ticket snapshot when init has `ticket:`, otherwise `init.md`. Search the source for a heading whose text contains "acceptance criteria" (case-insensitive) and extract everything under that heading verbatim. If there's no source at all, proceed with no signal — this is expected and not a flag. If the source is present but no such heading is found, record a pending flag to raise at Step 2 — don't raise it here.

## Step 1: Parking-lot gate

Check `QUESTIONS.md` (if present). If any items are unchecked (`- [ ]`):
- Present them to the user and ask for resolution.
- The plan **cannot be finalised** until all items are marked `[x]`.

## Step 2: Validation checkpoint

Present to the user:
- The ticket-wide approach: proposed module structure and an implementation sketch
- Which modules need tests
- The proposed slices, in order: `NN name`, repo, depends-on, and a one-line goal for each. There is always at least one slice. Each slice should merge to main on its own; if one can't, re-split rather than stacking branches.

Confirm with the user. Adjust based on feedback. This is the **one and only** checkpoint — do not conduct a relentless interview. Write nothing until the user approves the slices.

If Step 0 recorded a present-but-empty-AC-section flag, fold it into this same checkpoint rather than opening a second one: ask inline, "Ticket (or `init.md`) found, but no Acceptance Criteria section detected — does this ticket have ACs to carry forward?"

## Step 3: Write `plan.md`

Write `plan.md` into the work folder. Use this structure:

---

**Goal** — one sentence: what does this ticket deliver?

**Why** — the business reason

**Success criteria** — how will we know the whole ticket is done? (observable, testable)

**Acceptance criteria (from ticket, verbatim)**

The AC text extracted in Step 0, carried through unchanged. Omit this section entirely — no placeholder, no "N/A" — when Step 0 extracted nothing.

**Context**

List the key files involved with a one-line note on each. Reference any `_AI/` docs that apply.

**Architecture notes**

Any codebase-specific constraints that apply to this ticket (from `_AI/OVERVIEW.md`). Describe the approach through a "deep modules" lens — simple interface, substantial behaviour. Repeat the relevant anti-patterns here so execution cannot miss them.

**Anti-patterns for this ticket**

List the anti-patterns from `_AI/OVERVIEW.md` most likely to be violated given what this ticket touches.

**Slices**

The approved slice list, in order. One line each: `NN name` — repo — depends-on — one-line goal.

`![[slices.base]]`

**Close-out**

- [ ] All slices `merged`
- [ ] Durable decisions promoted to the repo `wiki/`
- [ ] Durable terms promoted to vault concept notes
- [ ] Ticket `status: inactive` *(only when there's a ticket)*

---

## Step 4: Write the slices

For each approved slice, create `slices/NN name.md` in the work folder, numbered from `01` in the approved order.

Start from the slice template (see **Work folders** in `_AI/local/AI.md`). Copy it as-is and fill its frontmatter: `repo`, `depends-on` (the names of the slices it depends on, empty if none), `state: planned`, `link` left empty. Everything above the template's horizontal rule comes from the template.

Below the rule, write the slice's blueprint:

---

## Blueprint

**Goal** — one sentence: what does this slice deliver?

**Success criteria** — how will we know this slice is done? (observable, testable)

**Implementation steps**

Step-by-step plan in dependency order:
- Use keywords: `create`, `modify`, `add`, `remove`, `migrate`, `move`
- One step = one logical change
- Include: migrations, model changes, service changes, query changes, controller changes, view changes, locale strings, spec changes
- Spec/test steps must appear **immediately before** the implementation step they cover — never after

**Validation gates**

The agent must run these in order and loop until each passes before moving on. The validation commands for this project are defined in `_AI/VALIDATION.md`.

**Confidence score**

Rate 1–10: how confident are you that a single execution pass will complete this slice correctly? Note what, if anything, would lower that score.

---

Write every slice's blueprint now, so they're reviewed together. A blueprint can be revised before execution if an earlier slice changes things.

## Step 5: Self-review before finishing

Before reporting, verify:
- Does the approach match the project's architecture (as described in `_AI/OVERVIEW.md`)?
- Can each slice merge to main on its own?
- Are all validation gates executable by the agent?
- Are the confidence scores honest?
- If the plan has an "Acceptance criteria" section, does every verbatim AC map to at least one slice's implementation steps? If a gap is resolvable by a mechanical blueprint edit, revise the blueprint now — no second user round-trip. If a gap needs real judgment, add an unchecked item to `QUESTIONS.md` and treat the plan as not-yet-finalized, per the Step 1 parking-lot rule.

## Step 6: Completion

Once the plan and slices are written and approved, the work folder is ready for execution, one slice at a time. **Do not delete** `DECISIONS.md`, `QUESTIONS.md`, or `GLOSSARY.md` — the work folder is permanent history and stays where it is:

```
_AI/delivery/work/<key>/
  init.md
  DECISIONS.md       ← permanent history
  QUESTIONS.md       ← all [x], permanent history
  GLOSSARY.md        ← optional
  plan.md            ← the whole ticket, plus the slice list
  slices/
    01 <name>.md     ← ready for execute-plan
    02 <name>.md
```
