---
tags: [ai-layer-docs]
sources:
  - vault/workflows/diploma-ready.md
checked: 2026-09-26
---

# diploma-ready workflow

*Checks a permaculture design's `output.md` against the Diploma [[assessment rubric]], the way a tutor would, and gives a Yes / Nearly / Not Yet verdict. It never edits the design.*

## When to reach for it

A design is nearly done and you want to know whether it would likely pass tutor assessment before you show it to your tutor.

## How to invoke

`/diploma-ready`, or say "diploma ready", "is this diploma ready" or "check against the diploma rubric", naming the piece folder. It asks if you don't say which.

## What it reads

- The [[output draft]]. That's what's assessed, as a tutor would see it, not the guide or the wiki. It checks that the draft has real content first.
- The rubric, `standards/diploma-design.md`, fresh on every run.
- The [[brief outline]], and failing that the notes in `guide/`, but only to work out which design framework you used when the draft doesn't make it obvious.

## What it writes

Nothing, by default. The report is in chat. If you ask, it will save the findings as a log note or raise Questions for gaps that need someone else's input.

## What it never touches

`output.md`, `guide/`, the rubric, or anything else. If the rubric looks out of date against something you tell it, it mentions this but doesn't edit it. Rubric changes happen separately, and only when you say so.

## How it works

1. **Scope.** It confirms which piece folder, and that `output.md` has real content.
2. **Rubric.** It reads `standards/diploma-design.md` and checks that every heading it depends on is there, word for word. If one is missing or reworded, it stops and names it. It won't run a partial check.
3. **Framework.** It works out which framework you used, either a process framework such as GOBRADIMET or the Design Web, because that decides which branch of Part 2 applies. If it can't tell, it asks.
4. **Walk the rubric** in its own order: Clear beginning, Part 1, the matching Part 2 branch, Part 3, then the minor-criteria and craft tables. It marks each check present, thin or missing. It doesn't invent checks and doesn't skip any. **Part 3 is checked for presence and separation only**: whether evaluation and reflection both exist and are kept apart, never whether they're honest or deep. The report says so.
5. **Verdict.** It uses the rubric's own scale, Yes Ready, Nearly Ready or Not Yet Ready, never a score. The gaps behind the verdict are ranked by how much a tutor would weigh them.
6. **Reading.** For thin or missing checks, it suggests matching wiki pages as reading. These are help for you, not evidence for the verdict.
7. **Report**, shaped like a pre-filled Individual Design Assessment Form: ✓ for satisfied, ? for thin, *absent* for missing, one line each. It notes that a single-design check says nothing about the portfolio as a whole.

## Worked example

You say "is this diploma ready" on `projects/hollin-lane/design-doc/parts/client/`. It reads `output.md`, which states it follows GOBRADIMET, so it takes the process-framework branch of Part 2. The report ticks most of Part 1, puts a **?** against the base map's missing north arrow and scale, and marks the evaluation **absent** under Part 3.

That Part 3 result is expected here. diploma-ready assesses one piece folder's `output.md`, and in this two-part design the reflection lives in the sibling part, `parts/reflection/`. Read Part 3 results with the layout of your [[multi-part piece]] in mind.

The verdict is **Nearly Ready**, with the Part 3 gap ranked first and the thin map conventions after it.

## Compared with…

- **[[gap-check workflow|gap-check]]**: both leave the draft untouched. gap-check checks against the piece's own guide or a reference you name, gives a gap list with no verdict, and records `coverage`. diploma-ready walks the fixed Diploma rubric, gives a Yes / Nearly / Not Yet verdict, and writes nothing.
- **[[sanity workflow|sanity]]**: sanity checks whether the writing holds together. diploma-ready checks whether the design meets the assessment criteria.

## Related

- [[assessment rubric]] · [[output draft]] · [[brief outline]]
- Workflow file: `_AI/local/workflows/diploma-ready.md`
