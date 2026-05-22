# AI Context

- This is the `_AI/core/` folder. I shall refer to the parent folder (the folder you've been given access to) as **the vault**.
- Chats live in `_AI/chats/`
- Logs live in `_AI/logs/`
- Scripts live in `_AI/core/scripts/`
- Workflows live in `_AI/core/workflows/`

## Setup files

These files live in `_AI/` and are created by the vault owner during setup. Read them for context before starting work:

- `_AI/GOALS.md` — goals and focus areas for this vault
- `_AI/VOICE.md` — writing voice reference, used by the compose workflow *(optional — only needed for vaults where prose drafting in the user's voice is a goal)*

If `_AI/GOALS.md` is missing, alert the user.

## Read & write access

- You may READ any file recursively in the vault
- Your WRITE access is limited to:
	- `_AI/chats/`
	- `_AI/logs/`
	- Any folder named `wiki/`
	- Any folder named `assets/`
	- Any file named `INDEX.md`
	- Any file named `GLOSSARY.md`
	- Any file named `QUESTIONS.md`
	- Any file named `SPATIAL.md`
	- You may move files to any folder named `curated/`
- If you ever need to write anywhere else, ask my permission first.

## Knowledge bases

- Within this vault, there are folders which I call **knowledge bases**.
- You will help me build specific domain knowledge within these folders.
- Knowledge bases are any folder containing a `wiki/` subfolder — the lint script discovers them automatically.
- Knowledge bases contain the following subfolders and files:
	- `inbox/` — I put stuff here for you to ingest
	- `curated/` — You move files here once ingested
	- `wiki/` — You build a wiki here
	- `assets/` — Images downloaded during ingest; gitignored
	- `INDEX.md` — You keep this updated
	- `AI.md` — Optional: specific instructions for this knowledge base
	- `GLOSSARY.md` — Optional: key terms and definitions
	- `QUESTIONS.md` — Optional: outstanding questions requiring follow-up
	- `SPATIAL.md` — Optional: named-feature location index *(only for KBs with a physical site)*

### SPATIAL.md format

Flat alphabetical list. One-line header naming the reference point. Each entry:

```
**feature name** — [position relative to reference point]. One sentence of context.
```

Example:
```
All directions are relative to the church building.

**Celtic cross** — southwest boundary, near the fence. A ~4m carved stone cross; a strong positive sight line.
**vestry** — south flank of the church, eastern end. Shows signs of subsidence; a growing crack in the wall.
```

## Workflows

Workflows live in `_AI/core/workflows/`. When my request matches a trigger below, read and follow the corresponding workflow file.

| Trigger | Workflow |
|---|---|
| "validate AI setup", "check AI setup" | `_AI/core/workflows/validate-ai-setup.md` |
| "ingest" + knowledge base name | `_AI/core/workflows/ingest.md` |
| "lint" or "audit" + knowledge base name | `_AI/core/workflows/lint.md` |
| "connect" or "find cross-knowledge base insights" | `_AI/core/workflows/connect.md` |
| "write", "guide", or "help with output" | `_AI/core/workflows/write.md` |
| "compose" | `_AI/core/workflows/compose.md` |
| "grill me" or "interview me" | `_AI/core/workflows/grill-me.md` |
| "debrief" | `_AI/core/workflows/debrief.md` *(optional workflow)* |
| "save" | `_AI/core/workflows/save.md` |
| "fetch" | `_AI/core/workflows/fetch.md` *(optional workflow)* |

## The fetch method *(optional)*

Sometimes, rather than typing into the chat, I'll use the _fetch_ method to send and receive messages. When I say "fetch", run the workflow at `_AI/core/workflows/fetch.md`.
