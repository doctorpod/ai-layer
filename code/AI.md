Read `_AI/OVERVIEW.md` first. This will give you an overview of the project. If it's missing, alert the user.

Also read `_AI/CODEX.md` if it exists — it defines coding conventions for this project. If absent, proceed without it.

## Never leak `_AI/` into shipped code

`_AI/` is a planning workspace invisible to the shipped codebase — it does not ship, and nothing in it should ever be referenced from something that does. When writing or editing code, comments, docstrings, commit messages, or strings, never reference `_AI/` paths, PRP files, workflow names (e.g. `execute-prp`, `grill-me`), or these instructions. If a rationale from a PRP or `_AI/OVERVIEW.md` is worth preserving in code, restate it in the comment on its own terms — don't cite the source file.

## Workflows

Workflows live in `_AI/local/workflows/` (code-specific) and `_AI/shared/workflows/` (shared). When the user's request matches a trigger below, read and follow the corresponding workflow file.

> **Fresh context warning:** before starting any workflow marked ⚠️, check whether this session already contains PRP creation work or implementation work. If it does, stop and tell the user to start a new session before proceeding.

| Trigger | Workflow |
|---|---|
| "create a PRP", "plan [ticket]", "write a PRP" | `_AI/local/workflows/create-prp.md` — synthesizes `prp.md` from captured decisions; no interview |
| "execute PRP", "implement PRP", "run PRP" | `_AI/local/workflows/execute-prp.md` ⚠️ fresh context required |
| "review", "post-execution review", "check the implementation" | `_AI/local/workflows/review.md` ⚠️ fresh context required |
| "grill me", "interview me", "question me about" | `_AI/shared/workflows/grill-me.md` — captures decisions into a durable ADR-style record |
| "teach me", "teach me on how this works", "help me learn" | `_AI/local/workflows/teach-me.md` |
| "rubber duck this", "let's rubber duck", "talk this through with me" | `_AI/shared/workflows/rubber-duck.md` — honest, brief conversation with no file changes |
| "greenhouse this", "park in greenhouse", "add to greenhouse", "review greenhouse" | `_AI/shared/workflows/greenhouse.md` — park early-stage ideas for later, distinct from radar |
| "validate AI setup", "check AI setup", "is the AI layer installed correctly" | `_AI/shared/workflows/validate-ai-setup.md` |
