---
name: diploma-ready
description: Check a permaculture design's output doc against the Diploma assessment rubric. Diagnostic only — never edits the design.
---

# Diploma-Ready Workflow

Use this workflow when the user wants to know whether a design (a piece-folder — `brief.md` / `guide.md` / `output.md`, see `_AI/shared/snippets/piece-folder.md`) would likely pass tutor assessment, before showing it to a tutor.

## The rule

Same shape as `sanity.md`: read-only, diagnostic. Never edit `output.md`, `guide.md`, or anything else. Name gaps; don't fill them.

## Step 1: Establish scope

Parse which piece-folder to check. If not stated or ambiguous, ask. Confirm `output.md` exists and has real content — this workflow assesses the document as a tutor would see it, not the guide or the underlying wiki.

## Step 2: Read the rubric

Read `lib/atlas/teaching/wiki/design-assessment-form.md` fresh, every run — don't rely on a cached memory of its contents. The rubric can be revised; this workflow should always reflect whatever's currently in the wiki.

## Step 3: Detect the framework

Read `output.md` (and `guide.md` if the framework isn't obvious from the output alone) to determine which path applies:

- **Section 2.1** — the design follows a process framework (SADIM, OBREDIM, CEAP, or similar)
- **Section 2.2** — the design follows the Design Web

Apply only the matching section. If genuinely unclear which framework was used, ask before proceeding.

## Step 4: Check Section 1 (applies to both paths)

For each of the six checks — framework used accurately and completely, ethics applied, principles applied appropriately, variety of tools, coherent and meets client needs, documentation fit to present — mark **present / thin / missing** against `output.md`, with a one-line pointer to where (or a note that it's absent).

## Step 5: Check Section 2.1 or 2.2

Same present / thin / missing treatment, against whichever section Step 3 selected.

## Step 6: Check Section 3

Evaluation of effectiveness, critical reflection, evidence of skill progression — check for **presence only**. This section is the apprentice's own reflective account of themselves; the workflow can say whether it exists and how developed it looks on the page, but cannot judge whether the reflection is honest, deep, or correct. Say so explicitly in the report rather than implying a real check happened.

## Step 7: Verdict

Roll up to the form's own scale — **Yes Ready / Nearly Ready / Not Yet Ready** — never a score or percentage. Justify the verdict with the specific gaps found in Steps 4–6, ranked by how much each would matter to a tutor (a missing Section 3 outweighs thin documentation formatting).

## Step 7b: Cross-reference craft patterns

For any check marked **thin** or **missing** in Steps 4–6, check whether it matches one of these patterns from `lib/atlas/permaculture-design/wiki/`:

- Section 1e ("coherent, meets client needs") or 1f ("documentation appropriate") thin, specifically around the brief being unclear or not revisited at the end → `[[design-brief-bookend]]`
- Section 1d ("variety of tools") or 1f thin, specifically around plan conventions, Latin names, or vague Needs/Functions/Systems/Elements → `[[design-write-up-craft]]`
- Section 3 thin, specifically around evaluation reading as one generic section rather than addressing different stakeholders → `[[audience-tiered-evaluation]]`

Only cite a page when the gap actually matches its subject — don't force a pointer onto every thin/missing result. These are reference reading for the apprentice, not part of the rubric; never treat matching one as itself evidence for or against the verdict.

## Step 8: Report

Chat response only, by default:

**Framework detected**: [2.1 process framework / 2.2 Design Web], and which specific framework if named

**Section 1**: present / thin / missing, one line each

**Section 2.x**: present / thin / missing, one line each

**Section 3**: present / thin / missing — with the caveat from Step 6

**Verdict**: Yes Ready / Nearly Ready / Not Yet Ready, with the gaps driving it

**Worth reading**: any pages surfaced in Step 7b, next to the gap they relate to (omit this line if none matched)

If the user asks to capture the findings (e.g. as a log note, or as new `QUESTIONS.md` items for gaps that need input from someone else), do that on request — not automatically.
