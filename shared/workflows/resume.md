---
name: resume
description: Resume work from a saved handoff document.
---

# Resume Workflow

Resume from a saved handoff document in `~/.claude/handoffs/`.

## If arguments were provided

The user has specified a name or partial name. Scan `~/.claude/handoffs/` for files whose name contains that string.

- **One match** → load it (go to **Load**)
- **Multiple matches** → show a numbered list and ask the user to pick one, then load it
- **No match** → say so and list all available handoffs

## If no arguments were provided

List all files in `~/.claude/handoffs/`:

```
[1] 2026-05-22-auth-refactor
[2] 2026-05-20-api-rate-limiting
[3] 2026-05-18-db-migration-plan
```

If the directory is empty or doesn't exist: `No handoffs found in ~/.claude/handoffs/`

Ask the user which one to resume (by number or name), then load it.

## Load

1. Read the file in full
2. Give the user an explicit "here's where we left off" summary:
   - **Project** and working directory
   - **What was in progress** — the active task
   - **What was done** — key progress from last session
   - **Suggested next steps** — what to tackle now
3. Delete the file: `rm ~/.claude/handoffs/<filename>`
4. Ask: "How would you like to proceed?"
