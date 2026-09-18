---
name: qa-failure
description: Log a QA failure against a PRP, diagnose the root cause, and apply a scoped fix.
---

# Workflow: QA Failure

Take a QA tester's failure report, record it against the original PRP, and fix only what's broken — without re-running the whole implementation.

## Usage

```
Follow the workflow in _AI/local/workflows/qa-failure.md for [ticket-name] using this QA report: [report or path]
```

Run in a **fresh context**, once per QA failure report.

## Steps

### 1. Resolve the PRP folder

Take the ticket/PRP slug from the invocation. Locate `_AI/PRPs/<slug>/`. If the slug is ambiguous or unstated, list in-progress folders under `_AI/PRPs/` and ask which one.

### 2. Capture the failure

Take the QA tester's report (pasted in, or a file path) and append an entry to `_AI/PRPs/<slug>/QA-FAILURES.md` (create it if it doesn't exist yet). Each entry:

- **Date**
- **Expected** — quote the relevant line(s) from the PRP's success criteria directly; don't paraphrase from memory
- **Actual** — QA's repro steps and evidence, kept verbatim
- **Implicated blueprint step** — best guess at which implementation blueprint step this traces to, flagged as a guess if uncertain

`QA-FAILURES.md` is permanent history, same status as `DECISIONS.md` / `QUESTIONS.md` — only ever appended to, never overwritten or pruned.

### 3. Re-read context

Read the original ticket, the full `prp.md`, and the new `QA-FAILURES.md` entry. Do not rely on recollection of the earlier execution session — read the actual files.

### 4. Diagnose before touching code

State a hypothesis for the root cause, tied to a specific blueprint step or file. If the failure doesn't map cleanly onto anything in the PRP, say so explicitly rather than forcing a mapping — that's a signal the PRP itself was wrong, not just the implementation.

Present the hypothesis and the intended fix to the user before changing anything. Wait for confirmation. If the diagnosis points to the PRP being wrong rather than the implementation, say so here and let the user decide how to proceed — don't quietly patch around it.

### 5. Fix, scoped

Implement only what's needed to resolve the failure(s) captured in step 2, per the confirmed diagnosis. This is not a re-run of the full blueprint. Run the relevant validation gate from `_AI/VALIDATION.md` for the area touched.

Never skip a validation gate. Never mark the fix done while a gate is failing.

### 6. Mini re-review

Run the check from `review.md` (`git diff main...HEAD`, full diff — there's no stored reference point for "since the last review"). Most of that diff already passed review, so focus verification on: the fix just made resolves the QA failure captured in step 2, and nothing else in the diff has regressed.

### 7. Report

- Which `QA-FAILURES.md` entries this pass addresses
- Root cause found
- What changed (file-by-file)
- Validation gates run and result
- Verdict: ready for re-QA / still failing, and why
