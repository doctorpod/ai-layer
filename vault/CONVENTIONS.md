# Vault Conventions (all vaults)

Operating conventions that apply to every vault built from this template — not specific to any one vault's content. A vault's own content-specific conventions belong in that vault's `_AI/CONVENTIONS.md` instead (e.g. how it treats ticket notes, naming quirks in its own KBs).

## A folder's canonical entry file links to its orientation sibling

If a folder has both a canonical/forced-path file — the one a workflow or navigation system actually routes through, e.g. `INDEX.md` as a gig's MOC, or `AI.md` as Claude's trigger table — and a separate orientation file meant to be read by a human before anything else, e.g. `README.md`, the canonical file links to the orientation file whenever one exists.

- **One-directional.** Canonical → orientation, never the reverse. Whoever reaches the orientation file got there via the forced path, so it doesn't need a way back to the thing that led them there.
- **Conditional, not mandatory.** Don't create a `README.md` just to satisfy this rule — it only fires where the README/orientation file already exists for its own reasons.
- **Vault-tier only.** Codebases installed from this framework don't have this shape — `code/` has no README/INDEX split — so this rule doesn't apply there.

Known instances of this pattern: a gig's `INDEX.md` → its `README.md`; `_AI/local/AI.md` → `_AI/local/README.md`.
