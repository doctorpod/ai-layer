# Workflow: Create PRP

Create a PRP (Product Requirements Prompt) — a complete implementation brief that allows a coding session to implement a set of changes in one pass.

## Example usage

> [!quote] Create a PRP called CVT-123 to add a button that shows the invoice total

## Step 0: Resume or start fresh

Check whether `_AI/PRPs/[ticket-name]/GRILLING.md` exists.

- **If yes**: read `GRILLING.md` and `QUESTIONS.md`. Resume from the first unresolved question in GRILLING.md, or move to Step 2 if all questions are answered.
- **If no**: create the folder `_AI/PRPs/[ticket-name]/` and create empty `GRILLING.md` and `QUESTIONS.md` files. Start at Step 1.

## Step 1: Grill the user

Follow the grill-me workflow (`_AI/core/workflows/grill-me.md`). Aim to understand:
- What is being built and why
- Constraints and known gotchas
- Which files are expected to change
- What's out of scope

As you go, persist the context into the PRP folder:

- After each resolved question, append to `GRILLING.md`:

```markdown
## Q: [the question]
**Recommended:** [your recommendation]
**Agreed:** [what was decided]
```

- If a question cannot be resolved now, add it to `QUESTIONS.md` and move on:

```markdown
- [ ] [the question — include why it's blocked and what's needed to resolve it]
```

Keep asking until you have sufficient knowledge to write the PRP.

## Step 2: Resolve the parking lot

Review `QUESTIONS.md`. If any items remain unchecked:
- Ask the user to resolve them before proceeding
- If items genuinely cannot be resolved yet, the PRP cannot be finalised — inform the user and stop

Once all items are resolved, mark them `[x]` in `QUESTIONS.md`.

## Step 3: Generate the PRP

Write `prp.md` from the knowledge in `GRILLING.md`. Use this structure:

---

**Goal** — one sentence: what does this implement?

**Why** — the business reason

**Success criteria** — how will we know it's done? (observable, testable)

**Context**

List the key files involved with a one-line note on each. Reference any `_AI/` docs that apply.

**Architecture notes**

Any codebase-specific constraints that apply to this ticket (from `_AI/OVERVIEW.md`). Repeat the relevant anti-patterns here so execution cannot miss them.

**Implementation blueprint**

Step-by-step implementation plan in dependency order:
- Use keywords: `create`, `modify`, `add`, `remove`, `migrate`, `move`
- One step = one logical change
- Include: migrations, model changes, service changes, query changes, controller changes, view changes, locale strings, spec changes

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

## Step 5: Completion

Once `prp.md` is saved and approved, delete `GRILLING.md` and `QUESTIONS.md`. The PRP folder is now ready for execution:

```
_AI/PRPs/[ticket-name]/
  prp.md    ← ready for execute-prp
```

> [!note] If you need to pause mid-grilling, move the PRP folder out of `_AI/PRPs/` to keep it away from coding sessions. Move it back when resuming.
