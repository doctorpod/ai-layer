# Vault Conventions (all vaults)

Operating conventions that apply to every vault built from this template — not specific to any one vault's content. A vault's own content-specific conventions belong in that vault's `_AI/CONVENTIONS.md` instead (e.g. how it treats ticket notes, naming quirks in its own KBs).

## A folder's canonical entry file links to its orientation sibling

If a folder has both a canonical/forced-path file — the one a workflow or navigation system actually routes through, e.g. `INDEX.md` as a gig's MOC, or `AI.md` as Claude's trigger table — and a separate orientation file meant to be read by a human before anything else, e.g. `README.md`, the canonical file links to the orientation file whenever one exists.

- **One-directional.** Canonical → orientation, never the reverse. Whoever reaches the orientation file got there via the forced path, so it doesn't need a way back to the thing that led them there.
- **Conditional, not mandatory.** Don't create a `README.md` just to satisfy this rule — it only fires where the README/orientation file already exists for its own reasons.
- **Vault-tier only.** Codebases installed from this framework don't have this shape — `code/` has no README/INDEX split — so this rule doesn't apply there.

Known instances of this pattern: a gig's `INDEX.md` → its `README.md`; `_AI/local/AI.md` → `_AI/local/README.md`.

## Atomic thing + `categories:` + `status`

A recurring shape for tracking something that changes state over time: give each instance its own file, tag it `categories: ["[[Thing]]"]`, and put a `status` enum in its frontmatter — rather than tracking many instances as rows or bullets in one shared ledger file. This makes each instance independently linkable (wikilink straight to it) and lets its state live on the object itself instead of a separate index that can drift out of sync.

The listing mechanism depends on who the primary consumer is:
- **Radar** (`radar/` folder, `_AI/local/workflows/add-to-radar.md`) is listed by a Python script (`list-radar.py`) — the AI agent is the primary consumer, sweeping for open items programmatically.
- **Themes** (a guide's theme notes) are listed via an Obsidian Base — the human is the primary consumer, using it as a working to-do list while writing.
- **Questions** (`questions/` folder, `_AI/shared/snippets/questions.md`) follow the Radar shape: script-listed (`list-questions.py`), since the AI agent is the primary sweeper (dedup checks, surmise resolution).

## Question status enum

A Question's `status` frontmatter field is one of:

1. **pending** — open, unanswered, not yet load-bearing anywhere. Default starting state.
2. **surmised** — still unanswered, but the assistant has written a provisional answer into a wiki page anyway. Distinct from `pending` because it's now actively propping up wiki content.
3. **confirmed** — answered, matches what was assumed. Any paired surmise gets promoted to a normal cited claim.
4. **rejected** — answered, contradicts what was assumed. Any paired surmise needs correcting or removing.
5. **dismissed** — closed without ever getting an answer, because it stopped mattering. Kept distinct from `rejected`: they trigger different follow-up (rejected → go fix the surmise; dismissed → nothing to fix, it never mattered).
