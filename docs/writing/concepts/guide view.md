---
tags: [ai-layer-docs]
sources:
  - shared/snippets/piece-folder.md
  - vault/workflows/sync-guide.md
checked: 2026-09-26
---

# guide view

*The `guide.base` file: an Obsidian Bases view that shows a piece's [[gathered note|gathered notes]], grouped by section.*

Each `guide/INDEX.md` embeds it with `![[guide.base]]`. The view groups notes by their `section:` field, so you don't need to scaffold headings in the index. It finds a note by its `categories` and `guide` fields, which is why every gathered note must carry both.

**You create `guide.base` once, by hand.** No workflow makes it. Obsidian finds it by filename, so it can live anywhere in the vault. If [[sync-guide workflow|sync-guide]] can't find one when it builds a new guide, it warns you and carries on. Until you add it, the embed just shows nothing; nothing breaks.

The view is one of the readers of the [[guide folder]], alongside [[beats workflow|beats]], [[elicit workflow|elicit]] and [[gap-check workflow|gap-check]]. Like them, it doesn't care which [[gatherer]] made a note.

## Related

- [[guide folder]]
- [[gathered note]]
