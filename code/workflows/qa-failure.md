---
name: qa-failure
description: Log a QA failure against a work folder, diagnose the root cause, and deliver the fix as a new slice.
---

# Workflow: QA Failure

Take a QA tester's failure report, record it in the work folder, and fix only what's broken — delivered as a new slice, without re-running the whole implementation.

## Usage

```
Follow the workflow in _AI/local/workflows/qa-failure.md for [key] using this QA report: [report or path]
```

Run in a **fresh context**, once per QA failure report.

## Steps

### 1. Resolve the work folder

Resolve the work folder (see **Work folders** in `_AI/local/AI.md`).

### 2. Capture the failure

Take the QA tester's report (pasted in, or a file path) and append an entry to `QA-FAILURES.md` in the work folder (create it if it doesn't exist yet). Each entry:

- **Date**
- **Expected** — quote the relevant line(s) from the success criteria of the slice it most likely belongs to, or from `plan.md`'s success criteria if no slice fits; don't paraphrase from memory
- **Actual** — QA's repro steps and evidence, kept verbatim
- **Implicated slice** — best guess at which slice this traces to, flagged as a guess if uncertain, or "none" if it spans the ticket

`QA-FAILURES.md` is permanent history, same status as `DECISIONS.md` / `QUESTIONS.md` — only ever appended to, never overwritten or pruned.

### 3. Re-read context

Read the ticket (via the wikilink rule, if `init.md` has `ticket:`), the full `plan.md`, the implicated slice, and the new `QA-FAILURES.md` entry. Do not rely on recollection of the earlier execution session — read the actual files.

### 4. Diagnose before touching code

State a hypothesis for the root cause, tied to a specific slice step or file. If the failure doesn't map cleanly onto anything in the plan or its slices, say so explicitly rather than forcing a mapping — that's a signal the plan itself was wrong, not just the implementation.

Present the hypothesis and the intended fix to the user before changing anything. Wait for confirmation. If the diagnosis points to the plan being wrong rather than the implementation, say so here and let the user decide how to proceed — don't quietly patch around it.

### 5. Write the fix slice

Create `slices/NN fix-<thing>.md` in the work folder, using the next free number. Start from the slice template (see **Work folders** in `_AI/local/AI.md`) and fill its frontmatter: `repo`, `depends-on` (the implicated slice, if any), `state: planned`, `link` left empty, `plan` as `create-plan` sets it: `plan: "[[work/<key>/plan|plan]]"`.

Below the template's horizontal rule, write the fix's blueprint under `## Blueprint`, in the same shape `create-plan` uses: goal; success criteria (resolving the captured failure); implementation steps, scoped to the confirmed diagnosis; validation gates from `_AI/VALIDATION.md`.

### 6. Fix, scoped

The fix goes on its own branch, off main, with the key in its name. If you're not on one, propose a branch name and create it once the user confirms. Set the fix slice's `state: in progress`.

Implement only the fix slice's steps. This is not a re-run of any earlier slice. Run the relevant validation gate from `_AI/VALIDATION.md` for the area touched.

Never skip a validation gate. Never mark the fix done while a gate is failing.

### 7. Mini re-review

Run the check from `review.md` against the fix slice (`git diff main...HEAD`, full diff). Focus verification on: the fix resolves the QA failure captured in step 2, and nothing the fix touches has regressed.

### 8. Report

- Which `QA-FAILURES.md` entries this pass addresses
- Root cause found
- The fix slice created, and its branch
- What changed (file-by-file)
- Validation gates run and result
- Verdict: ready for re-QA once the fix slice is merged / still failing, and why
