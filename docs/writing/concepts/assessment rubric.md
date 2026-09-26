---
tags: [ai-layer-docs]
sources:
  - vault/workflows/diploma-ready.md
  - vault/workflows/interview.md
  - vault/workflows/gap-check.md
checked: 2026-09-26
---

# assessment rubric

*A file in the vault-root `standards/` folder that defines what "good" looks like for a kind of piece, which workflows read by its named headings.*

The one in use today is `standards/diploma-design.md`, the checklist for a permaculture Diploma design. You keep it by hand. The assistant edits a rubric only when you've explicitly said to, and never folds new material into one as a side effect of another workflow.

## Who reads it

- [[diploma-ready workflow|diploma-ready]] walks `standards/diploma-design.md` check by check. It reads the file fresh on every run, and first confirms that every heading it depends on is there, word for word. If one is missing or reworded, it stops and names it rather than running a partial check.
- [[interview workflow|interview]] can draw thread ideas from a rubric's elicitation-prompts heading, when the [[piece brief]] points to the rubric.
- [[gap-check workflow|gap-check]] can use a rubric as its reference instead of `guide/` if you name it: "gap check output.md against standards/diploma-design.md".

## Why headings matter

Workflows find the parts they need by exact heading text. Rewording a heading is a structural change. Expect diploma-ready to stop and tell you, and expect its own workflow file to need updating to match.

## Related

- [[diploma-ready workflow]]
- [[PATTERNS]], for the Rubric pattern
