---
name: handoff
description: Save a handoff document so this conversation can be resumed in a future session.
---

# Handoff Workflow

Save a handoff document so this conversation can be resumed in a future session.

## Steps

### 1. Generate a slug

Derive a 2–4 word kebab-case summary of what was worked on this session (e.g. `auth-refactor`, `api-rate-limiting`, `db-migration-plan`). Keep it specific enough to be recognisable later.

### 2. Build the file path

- Date: today in `YYYY-MM-DD` format
- Path: `~/.claude/handoffs/YYYY-MM-DD-<slug>.md`

### 3. Ensure the directory exists

```bash
mkdir -p ~/.claude/handoffs
```

### 4. Write the handoff document

Use this exact structure:

```markdown
# Handoff: <slug>
**Date:** YYYY-MM-DD
**Project:** <project name>
**Working directory:** <absolute path of cwd>

## What was in progress
<The active task or problem being solved — what the user was focused on>

## What was done
<Key decisions made, changes implemented, or meaningful progress achieved this session>

## Suggested next steps
<The most logical things to tackle when resuming — be specific and actionable>

## Relevant files and artifacts
<Paths or URLs relevant to the work — reference only, no duplicated content>

## Suggested skills
<Skills or tools that would be useful in the next session>
```

Rules:
- Do not reproduce content already captured in separate artifacts (PRDs, plans, diffs, commits)
- Redact sensitive data (API keys, passwords, PII)
- Reference files by path, not by copying their content

### 5. Save and confirm

Overwrite the file if it already exists at that path.

Confirm to the user: `Handoff saved: ~/.claude/handoffs/YYYY-MM-DD_<slug>.md`
