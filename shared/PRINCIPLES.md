---
name: PRINCIPLES
description: The invariants every workflow in this layer must hold. Checked against during workflow-design sessions, not walked at runtime.
---

# Workflow Principles

The fixed points of this AI layer. When a workflow is being written or revised, the
test is: **does this comply, or does it transgress?** A workflow may do many things
these don't mention — but it may not break one of these to do them.

This is the automation-facing counterpart to the vault owner's personal
[[My AI commandments]]. Where a principle descends from one, it's noted.

Two rules about this list itself:

- **It stays near ten.** A principles doc that grows past what you can hold in your
  head becomes noise nobody checks against. New candidates displace weak ones; they
  don't just accrete.
- **It is not `standards/`.** The `standards/` folder holds long, detailed,
  operational rubrics that a single workflow walks step by step (e.g.
  `diploma-design.md`). This file is short, general, and consumed by humans deciding
  how a workflow should behave.

---

1. **The owner decides — AI drafts** *(personal #3)* — A workflow proposes; it never
   commits the owner to a change they haven't seen. Where judgement or preference is
   involved, surface the options and let the owner pick.

2. **Diagnostic means diagnostic** — A workflow whose job is to assess (sanity,
   gap-check, diploma-ready, review, reflect) never edits the thing it assesses, or
   anything else. It names gaps; it doesn't fill them.

3. **Propose, then apply on confirmation** — For workflows that do change files: make
   the change legible before making it. When something is ambiguous, ask one
   question, wait for the answer, act, then ask the next — don't batch guesses.

4. **Write only where you're allowed** — The write allowlist in `AI.md` is
   exhaustive. If a task seems to need writing outside it, stop and ask — don't route
   around it.

5. **Hand-owned files change only on an explicit say-so** — Rubrics in `standards/`,
   `CONVENTIONS.md`, `SPATIAL.md`, this file. Never fold new material into one as a
   side effect of another workflow, and never treat the offer to update one as a
   formality.

6. **Every wiki claim traces to its source** — A heading claim, an evidence section,
   footnotes pointing to the sources the claim derives from. One source per sentence;
   never blend two sources into one sentence. Full mechanics live in `ingest.md`'s
   citation rules — this is the principle they serve.

7. **Be honest about what's AI-generated** *(personal #6, #9)* — The workflow's own
   synthesis is a lead, not a finding: keep uncertainty visible (`[!caution]` for
   unverified claims, "speculating" vs "confirmed"). And content authored by past AI
   sessions (`ai-generated` in frontmatter) is never surfaced as the owner's own
   thinking, memory, or lived experience — exclude it or flag it.

8. **Fix what you find, not just what you touched** — When a workflow surfaces a
   pre-existing problem, resolve it in the same pass. Don't gate old findings behind
   a "was this in scope?" check.

9. **Keep the planning layer out of the product** — `_AI/` is a planning workspace.
   Nothing in shipped code, commits, or output ever references `_AI/` paths, PRP
   files, or workflow names. A rationale worth keeping gets restated on its own terms.

10. **Shape output for the reader** *(personal #10)* — Reports are brief and
    structured. Long or complex output is the workflow's problem to make accessible,
    not the reader's to wade through.

---

## Maintenance

Changes to this file go through the same gate as any hand-owned file (principle 5):
explicit say-so, never a side effect. If a workflow edit seems to require bending a
principle, that's the signal to stop and discuss the principle directly — not to
quietly weaken it.
