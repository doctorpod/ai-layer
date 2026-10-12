---
name: review
description: Review the implementation of a slice before raising a PR.
---

# Workflow: Post-execution Review

Review the implementation of a slice against its blueprint before raising a PR.

## Usage

```
Follow the workflow in _AI/local/workflows/review.md for slice [NN] of [key]
```

Run in a **fresh context** after execution is complete.

This review is diagnostic: it never edits the slice, the plan, or anything else. It reports; the user acts.

## Steps

### 1. Get the diff

```bash
git diff main...HEAD
```

Read it in full.

### 2. Read the slice and the plan

Resolve the work folder (see **Work folders** in `_AI/local/AI.md`), then the slice in its `slices/` folder (by number, name or path; ask if ambiguous). Read the slice in full. Hold its success criteria and implementation steps in mind while reviewing the diff.

Also read `plan.md` and `DECISIONS.md` from the work folder, tolerating the absence of `DECISIONS.md`.

### 3. Run the full validation suite

Run all validation gates defined in `_AI/VALIDATION.md`. All must pass. If any fail, stop and report — do not continue the review.

### 4. Check the diff against the slice

For each of the slice's implementation steps, verify it is present in the diff. Note any gaps. Then check the diff against the slice's success criteria.

Check the diff against the anti-patterns defined in `_AI/OVERVIEW.md` and in the plan.

If the plan has an "Acceptance criteria" section, check each verbatim AC for contradiction against the diff or `DECISIONS.md` — does the implementation actively override what the AC says? This is scoped to contradictions only; a missing AC (never implemented) is not this check's concern — that gap is caught upstream, during plan creation, and an AC may belong to a different slice.

### 5. Report

Produce a structured report:

**Tests**: pass / fail (list failures if any)

**Coverage vs slice**: list each implementation step and whether it was implemented, then each success criterion and whether it's met

**AC conflicts**: none / list — contradictions found between a verbatim AC and the diff or `DECISIONS.md`. This is a flag for human judgment, not a gate: it does not, by itself, change the Verdict below.

**Issues found**:
- Critical: must fix before PR (wrong architecture, failing tests, missing functionality)
- Important: should fix (code quality, pattern violations)
- Minor: optional (style, naming)

**Verdict**: ready to PR / needs fixes
