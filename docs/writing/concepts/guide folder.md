---
tags: [ai-layer-docs]
sources:
  - shared/snippets/piece-folder.md
  - vault/workflows/sync-guide.md
  - vault/workflows/interview.md
checked: 2026-09-26
---

# guide folder

*The `guide/` folder in a [[piece folder]]: the material the piece is written from, as one note per idea.*

`guide/` holds two kinds of file:

- `guide/INDEX.md`, which embeds the [[guide view]] so you can browse the notes grouped by section.
- One [[gathered note]] per idea, each filed under one section of the [[brief outline]].

## Who writes it

Only [[gatherer|gatherers]] create notes here: [[sync-guide workflow|sync-guide]], which lifts quotes from vault sources, and [[interview workflow|interview]], which records your own answers. A gatherer creates notes and appends to them. The only other change it makes is to put a note's `status` back from `used` to `pending` when it adds new material.

You own `status` (`used`/`rejected`). [[gap-check workflow|gap-check]] owns `coverage`. Nothing else writes here.

## Who reads it

[[beats workflow|beats]], [[elicit workflow|elicit]], [[gap-check workflow|gap-check]] and the [[guide view]] read every note the same way, whichever gatherer made it. That's the point of the [[gathered note]] contract.

## Creating `guide/INDEX.md`

sync-guide creates it when it first builds a guide:

```markdown
---
aliases:
  - guide - <piece name>
---
![[guide.base]]
```

interview doesn't create it. If it's missing, interview asks you to create it (with the same content) and then carries on.

Because every piece folder has its own `guide/INDEX.md`, never link to one as a bare `[[INDEX]]`. Use its full path, as the `guide:` field on each note does.

## Example

After a sync and a couple of interview threads, the two Hollin Lane parts look like this:

```
parts/client/guide/
  INDEX.md
  Wet corner by the north gate floods every winter.md
  South bed shaded by the neighbour's hedge until noon.md
  Heavy clay under the wet corner.md
  Fruit for the school kitchen, not a showpiece.md
  Swale above the wet corner.md
parts/reflection/guide/
  INDEX.md
  01 choosing the framework.md
  02 the wet corner surprise.md
```

## Related

- [[gathered note]]
- [[guide view]]
- [[gatherer]]
