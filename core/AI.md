Read `_AI/OVERVIEW.md` first. This will give you an overview of the project. If it's missing, alert the user.

## Workflows

Workflows live in `_AI/core/workflows/`. When the user's request matches a trigger below, read and follow the corresponding workflow file.

> **Fresh context warning:** before starting any workflow marked ⚠️, check whether this session already contains PRP creation work or implementation work. If it does, stop and tell the user to start a new session before proceeding.

| Trigger | Workflow |
|---|---|
| "create a PRP", "plan [ticket]", "write a PRP" | `_AI/core/workflows/create-prp.md` |
| "execute PRP", "implement PRP", "run PRP" | `_AI/core/workflows/execute-prp.md` ⚠️ fresh context required |
| "review", "post-execution review", "check the implementation" | `_AI/core/workflows/review.md` ⚠️ fresh context required |
| "grill me", "interview me", "question me about" | `_AI/core/workflows/grill-me.md` |
| "teach me", "teach me on how this works", "help me learn" | `_AI/core/workflows/teach-me.md` |
| "validate AI setup", "check AI setup", "is the AI layer installed correctly" | `_AI/core/workflows/validate-ai-setup.md` |
