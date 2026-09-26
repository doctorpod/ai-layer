---
tags: [ai-layer-docs]
sources:
  - shared/snippets/piece-folder.md
  - vault/workflows/sync-guide.md
  - vault/workflows/interview.md
  - vault/workflows/gap-check.md
  - vault/workflows/beats.md
checked: 2026-09-26
---

# gathered note

*One note in a [[guide folder]]: a single piece of material, filed under one section, in the shape every writing workflow can read.*

## The contract

Every gathered note starts with these five frontmatter fields, whichever [[gatherer]] made it:

```yaml
---
categories: "[[Themes]]"
guide: "[[projects/hollin-lane/design-doc/parts/client/guide/INDEX|guide - client]]"
section: 02 Observation
status: pending
coverage:
---
```

| Field | Meaning | Who sets it |
|---|---|---|
| `categories` | Always `"[[Themes]]"`. The [[guide view]] filters on it. | The gatherer |
| `guide` | Full path to this piece folder's `guide/INDEX.md`, never a bare `[[INDEX]]`. The guide view filters on this too. | The gatherer |
| `section` | The one [[brief outline]] heading the note belongs to. | The gatherer |
| `status` | `pending`, `used` or `rejected` (see below). | You, except for the one revert below |
| `coverage` | `full`, `thin` or `missing`: a [[coverage verdict]]. Left blank on creation, but the line must be there. | [[gap-check workflow|gap-check]] only |

A note without `categories` and `guide` doesn't show up in the guide view.

**One note, one section.** Material that belongs to two sections goes in two notes.

The body, and any extra frontmatter (`tags`, `date`, `thread`, `topic`), belong to the gatherer. The workflows that read notes treat the whole body as one unit.

## Status

- **`pending`**: every note starts here.
- **`used`**: you've drawn on it in the [[output draft]]. You set this by hand.
- **`rejected`**: you've looked and decided you don't have a real basis for it. You set this by hand. [[beats workflow|beats]] and [[gap-check workflow|gap-check]] skip rejected notes.

No workflow ever sets `used` or `rejected`. The one automatic change is a revert: when a gatherer adds new material to a note marked `used`, it sets `status` back to `pending` and tells you why. New material means your earlier use of the note needs another look.

`status` is your judgement and `coverage` is gap-check's measurement. They're independent. A `used` note can come back `thin` if the draft has changed since.

## What the body looks like

It depends on the gatherer.

- **From [[sync-guide workflow|sync-guide]]**: a **Quotes** list (lifted sentences, each cited to its primary source), optional **Synthesis** (reasoning built on those quotes, deliberately uncited), and an empty **Comments** heading. Tagged `ai-generated`.
- **From [[interview workflow|interview]]**: a thread of questions and your verbatim answers, with every assistant-written heading labelled `(Claude)`. Not tagged `ai-generated`, because the words are mostly yours. See [[interview thread]].

## Example

`parts/client/guide/Wet corner by the north gate floods every winter.md`:

```markdown
---
categories: "[[Themes]]"
guide: "[[projects/hollin-lane/design-doc/parts/client/guide/INDEX|guide - client]]"
section: 02 Observation
status: pending
coverage:
tags:
  - ai-generated
---

**Quotes**
- "the bottom corner by the north gate sits under water from November to about March" — [[debrief-2026-03-14-site-walk]]

**Synthesis**
- the wet corner is the site's one reliable water feature; a problem or an asset depending on the design

**Comments**
```

## Related

- [[guide folder]]
- [[gatherer]]
- [[coverage verdict]]
