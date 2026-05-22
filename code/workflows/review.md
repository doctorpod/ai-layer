---
name: review
description: Review the implementation against the PRP before raising a PR.
---

# Workflow: Post-execution Review

Review the implementation against the PRP before raising a PR.

## Usage

```
Follow the workflow in _AI/core/workflows/review.md using: _AI/PRPs/[ticket-name]/prp.md
```

Run in a **fresh context** after execution is complete.

## Steps

### 1. Get the diff

```bash
git diff main...HEAD
```

Read it in full.

### 2. Read the PRP

Read the PRP at the path provided. Hold the success criteria and implementation blueprint in mind while reviewing the diff.

### 3. Run the full validation suite

Run all validation gates defined in `_AI/VALIDATION.md`. All must pass. If any fail, stop and report — do not continue the review.

### 4. Check the diff against the PRP

For each item in the PRP's implementation blueprint, verify it is present in the diff. Note any gaps.

Check the diff against the anti-patterns defined in `_AI/OVERVIEW.md`.

### 5. Report

Produce a structured report:

**Tests**: pass / fail (list failures if any)

**Coverage vs PRP**: list each blueprint step and whether it was implemented

**Issues found**:
- Critical: must fix before PR (wrong architecture, failing tests, missing functionality)
- Important: should fix (code quality, pattern violations)
- Minor: optional (style, naming)

**Verdict**: ready to PR / needs fixes
