---
name: diploma-ready
description: Check a permaculture design's output doc against the Diploma design rubric. Diagnostic only — never edits the design.
---

# Diploma-Ready Workflow

Use this workflow when the user wants to know whether a design (a piece-folder — `brief.md` / `guide/` / `output.md`, see `_AI/shared/snippets/piece-folder.md`) would likely pass tutor assessment, before showing it to a tutor.

## The rule

Same shape as `sanity.md`: read-only, diagnostic. Never edit `output.md`, `guide/`, the rubric, or anything else. Name gaps; don't fill them.

## Step 1: Establish scope

Parse which piece-folder to check. If not stated or ambiguous, ask. Confirm `output.md` exists and has real content — this workflow assesses the document as a tutor would see it, not the guide or the underlying wiki.

## Step 2: Read the rubric

Read `standards/diploma-design.md` fresh, every run — don't rely on a cached memory of its contents. **That file is the checklist; this workflow is only the harness that walks it.** It is hand-maintained (see its own Maintenance section), so its checks and structure can change between runs — always follow the file as it currently stands, not this workflow's description of it.

If `standards/diploma-design.md` doesn't exist, stop and tell the user — this workflow can't run without it.

## Step 3: Detect the framework

Work through the rubric's **Framework check** section against `output.md`. If the framework isn't obvious from the output alone, check `brief.md`'s `Outline` field (the resolved framework breakdown, if the piece has one) before falling back to `guide/`'s theme notes. The framework determines which branch of the rubric's Part 2 applies (process-framework vs Design Web). If genuinely unclear which framework was used, ask before proceeding.

## Step 4: Work through the rubric

For every check in the rubric — Framework, Part 1, the matching Part 2 branch, Part 3, Minor criteria, and Craft checks — mark **present / thin / missing** against `output.md`, with a one-line pointer to where it's satisfied (or a note that it's absent).

Honour what the rubric says about each group. In particular: Part 3 is checked for **presence and separation only** — whether evaluation and reflection both exist and are kept distinct — never for whether the reflection is honest or deep. Say so in the report rather than implying a real check happened.

Do not invent checks the rubric doesn't contain, and don't skip ones it does.

## Step 5: Verdict

Roll up to the rubric's own scale — **Yes Ready / Nearly Ready / Not Yet Ready**, never a score or percentage — using the rubric's Verdict section. Justify it with the specific gaps found in Step 4, ranked by how much each would matter to a tutor (a missing Part 3 element outweighs thin captions).

The rubric's **Portfolio-level criteria** are out of scope here — this is a single-design check. Note in the report that a "Yes Ready" says nothing about diversity, progression, or implementation across the whole portfolio.

## Step 6: Point to reference reading

For any check marked **thin** or **missing**, offer the relevant wiki page as reference reading for the fix — only where the gap genuinely matches the page's subject:

- Brief unclear, or not revisited at the end → `[[design-brief-bookend]]`
- Plan conventions, Latin names, TOADS, undated stages, or blurred Needs/Functions/Systems/Elements → `[[design-write-up-craft]]`
- Evaluation reading as one generic section rather than addressing different stakeholders → `[[audience-tiered-evaluation]]`
- Whole-portfolio questions the user raises → `[[diploma-portfolio-criteria]]`

These are reading for the apprentice, not part of the rubric — never treat matching one as evidence for or against the verdict.

## Step 7: Report

Chat response only, by default:

**Framework detected**: process framework (which one) / Design Web

**Part 1**: present / thin / missing, one line each

**Part 2**: present / thin / missing, one line each (matching branch)

**Part 3**: present / thin / missing — with the presence-and-separation-only caveat

**Minor & craft**: the notable gaps only

**Verdict**: Yes Ready / Nearly Ready / Not Yet Ready, with the gaps driving it, and the portfolio-scope note

**Worth reading**: any pages from Step 6, next to the gap they relate to (omit if none)

If the user asks to capture the findings (e.g. as a log note, or as new Questions for gaps needing input from someone else — see `_AI/shared/snippets/questions.md`), do that on request — not automatically.

## Step 8: Rubric currency

If, while working through the design, you notice the rubric looks out of step with something the user says about current Diploma requirements, mention it — but don't edit `standards/diploma-design.md` here. Rubric changes go through the `cross-workflow-check` flow in an ingest or debrief, on the user's explicit say-so.
