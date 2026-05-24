A portable AI workflow layer that installs into any project via symlink. It gives your AI assistant a structured set of workflows for two contexts: **coding repos** and **Obsidian vaults**.

Inspired by [Matt Pocock](https://www.mattpocock.com) - Thanks Matt!.

---

## Contexts

### Code workflows

Drop the `code/` layer into any coding repo and get:
- **Grill me** — relentless interrogation to surface assumptions before writing a line of code
- **Create PRP** — a complete implementation brief built from that shared understanding
- **Execute PRP** — a disciplined implementation pass in a clean context
- **Review** — a post-implementation check against the brief before raising a PR
- **Teach me** — guided learning from the codebase

### Vault workflows

Drop the `vault/` layer into any Obsidian vault and get:
- **Ingest** — add new sources to your knowledge base
- **Lint** — audit KB structure for orphans, broken links, and pending cautions
- **Connect** — discover cross-KB insights and write bidirectional links
- **Compose** — draft prose in your own voice
- **Debrief** — process first-hand notes into wiki pages
- **Write** — structured brief → guide → output pattern
- **Save** — commit with a 12-word summary and log entry
- **Fetch** — async message passing via dated chat logs

Both contexts also include **Grill me** and **Validate AI setup** (from `shared/`).

---

## Install — coding repos

Run from the root of your coding repo:

```bash
mkdir -p _AI/PRPs
bash ~/Dev/ai-layer/scripts/install-target.sh --code
```

> **Symlink vs copy:** The symlinks mean all your repos share one layer — updates propagate instantly. That's ideal for personal use. For shared team repos, copy the folders instead or use a git submodule.

Make the AI boot file (e.g. `CLAUDE.md`) in your repo root:
```markdown
See `_AI/local/AI.md` for project context and available workflows.
```

Create `_AI/OVERVIEW.md` — project description, architecture, key files, and anti-patterns.

Optionally create `_AI/CODEX.md` — personal coding preferences and domain glossary for AI workflows.

Create `_AI/VALIDATION.md` — the commands to run at each validation gate. Use this format:
```markdown
## Validation gates
1. `npm run lint` — after any JS/TS change
2. `npm test` — after each logical unit of change
3. `npm test` — full suite, must pass before done
```

---

## Install — Obsidian vaults

Run from the root of your vault:

```bash
bash ~/Dev/ai-layer/scripts/install-target.sh --vault
```

Make the AI boot file (`CLAUDE.md` or `AGENTS.md`) in the vault root:
```markdown
See `_AI/local/AI.md` for vault context and available workflows.
```

Create `_AI/GOALS.md` — the vault's purpose and focus areas.

Optionally create `_AI/VOICE.md` — a writing voice reference for the Compose workflow.

To block accidental commits of sensitive content, install the pre-commit hook:
```bash
cp _AI/local/scripts/pre-commit-sensitivity-check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

## Claude Code users — native skills (optional)

Instead of relying on trigger phrase matching, install native slash commands that delegate to the workflows:

```bash
bash ~/Dev/ai-layer/scripts/install-skills.sh
```

This scans `code/workflows/`, `vault/workflows/`, and `shared/workflows/` and writes skill stubs into `~/.claude/skills/`. You get:

| Skill | Routes to |
|-------|-----------|
| `/grill-me` | `_AI/shared/workflows/grill-me.md` |
| `/validate-ai-setup` | `_AI/shared/workflows/validate-ai-setup.md` |
| `/create-prp` | `_AI/local/workflows/create-prp.md` |
| `/execute-prp` | `_AI/local/workflows/execute-prp.md` |
| `/review` | `_AI/local/workflows/review.md` |
| `/teach-me` | `_AI/local/workflows/teach-me.md` |
| `/ingest` | `_AI/local/workflows/ingest.md` |
| `/lint` | `_AI/local/workflows/lint.md` |
| `/connect` | `_AI/local/workflows/connect.md` |
| `/compose` | `_AI/local/workflows/compose.md` |
| `/debrief` | `_AI/local/workflows/debrief.md` |
| `/write` | `_AI/local/workflows/write.md` |
| `/save` | `_AI/local/workflows/save.md` |
| `/fetch` | `_AI/local/workflows/fetch.md` |

Skills are thin wrappers — all logic stays in the workflow files. Context-specific skills resolve via `_AI/local` (which symlinks to either `code/` or `vault/` depending on the target). Shared skills resolve via `_AI/shared`.
