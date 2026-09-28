A `RELATED.md` lists the repos and sister vault that belong to the same group as the one you're working in, so you know where to look beyond the current folder.

## Where to find it

- **Code repo:** `_AI/RELATED.md`, if present. It's usually a symlink to the group's file in the sister vault. It's optional; don't alert if it's missing.
- **Vault:** any `RELATED.md` inside the folder you're working in or near. There's no vault-wide index.

## Format

A one-line note on how to use the file, then one `## <name>` heading per member with labelled bullets:

```markdown
Browse these on demand, read-only unless asked.

## gca-cvt-backend
- Kind: repo
- Path: `~/Dev/gca-cvt-backend`
- Role: Rails API; owns the DB, exposes `/api/v1/...`
- Look here when: a frontend ticket touches a backend endpoint — the merged code is the real contract.

## notes-work
- Kind: vault
- Path: `~/Obsidian/notes-work/gigs/2026-02-CCS/`
- Role: gig notes, repo overviews, PRPs, PR write-ups
- Look here when: you need the why behind a decision or anything discussed but not in code.
```

- `Kind` is `repo` or `vault`.
- `Path` may start with `~`. A vault's `Path` points to the relevant subfolder, not the vault root.
- No tables — headings and bullets are easier to edit by hand.

## Rules

- **Browse on demand, read-only.** Go to a listed location when an entry's "Look here when" applies. Read it; don't write to it unless the user asks.
- **Hand-owned.** Only the owner edits `RELATED.md`. Never change it as a side effect of another task; if it looks wrong or out of date, say so.
- **Repo in two groups.** Keep a small local `_AI/RELATED.md` that points to each group's file instead of symlinking one.
