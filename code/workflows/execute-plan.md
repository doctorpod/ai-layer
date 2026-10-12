---
name: execute-plan
description: Implement one slice of a plan.
---

# Workflow: Execute Plan

Implement one slice of a validated plan.

## Usage examples

> [!quote] Examples of what the user may say:
> - Execute plan CVT-358 02
> - Implement slice `_AI/delivery/work/CVT-358/slices/02 add-totals.md`

This must be run in a **fresh context**. Do not run in the same session as plan creation.

## Steps

### 1. Resolve the slice

Resolve the work folder (see **Work folders** in `_AI/local/AI.md`). Then find the slice in its `slices/` folder, by number or name, or by the path given. If it's ambiguous or unstated, list the slices with their `state` and ask which one.

### 2. Read and internalise the plan and the slice

Read `plan.md` in full, then the slice in full. Do not begin implementation until you have read both completely. Pay particular attention to:
- The plan's architecture notes and anti-patterns
- The slice's implementation steps (step order matters)
- The slice's validation gates

### 3. Re-read relevant context

Read `_AI/OVERVIEW.md` and any other files referenced in the plan's context section. Do not rely on training knowledge for project-specific patterns — read the actual files.

### 4. Mark the slice in progress

Set the slice's frontmatter `state: in progress`. Change nothing else in the slice.

### 5. Implement in step order

Work through the slice's implementation steps in sequence. Do not jump ahead, and do not implement steps from any other slice.

For each step:
1. Make the change
2. Run the relevant validation gate (see below)
3. Fix any failures before moving to the next step

Never skip a validation gate. Never mark a step done while a gate is failing.

Do not reference `_AI/` paths, plan or slice files, or this workflow in any code, comment, docstring, or commit message you write — see `_AI/local/AI.md`. Those are planning artifacts; the shipped code must read as if they never existed.

### 6. Validation gates

Run the gates at the points specified in the slice. The validation commands for this project are defined in `_AI/VALIDATION.md`. Never skip a gate. Never mark a step done while a gate is failing.

### 7. When complete

Report:
- What was implemented (file-by-file summary)
- Which validation gates were run and passed
- Slice state set to `in progress` — the rest of the slice's checklist (review, PR, merged) is the user's
- Anything that deviated from the slice's blueprint, and why
- Any follow-up work that surfaced but is out of scope for this slice
