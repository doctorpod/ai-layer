A portable AI workflow layer that installs into any project via symlink. It gives your AI assistant a structured set of workflows for two contexts: **coding repos** and **Obsidian vaults**.

Inspired by [Matt Pocock](https://www.mattpocock.com).

---

## Contexts

### Code workflows

Drop the `code/core` layer into any coding repo and get:
- **Grill me** — relentless interrogation to surface assumptions before writing a line of code
- **Create PRP** — a complete implementation brief built from that shared understanding
- **Execute PRP** — a disciplined implementation pass in a clean context
- **Review** — a post-implementation check against the brief before raising a PR
- **Teach me** — guided learning from the codebase

### Vault workflows

Drop the `vault/core` layer into any Obsidian vault and get:
- **Ingest** — add new sources to your knowledge base
- **Lint** — audit KB structure for orphans, broken links, and pending cautions
- **Connect** — discover cross-KB insights and write bidirectional links
- **Compose** — draft prose in your own voice
- **Debrief** — process first-hand notes into wiki pages
- **Write** — structured brief → guide → output pattern
- **Save** — commit with a 12-word summary and log entry
- **Fetch** — async message passing via dated chat logs

Both contexts also include **Grill me** and **Validate AI setup**.

---

## Install — coding repos

```bash
mkdir -p _AI/PRPs
ln -s ~/Dev/code-ai-layer/code/core _AI/core
```

> **Symlink vs copy:** The symlink means all your repos share one `core/` — updates propagate instantly. That's ideal for personal use. For shared team repos, copy `code/core/` instead or use a git submodule.

Make the AI boot file (e.g. `CLAUDE.md`) in your repo root:
```markdown
See `_AI/core/AI.md` for project context and available workflows.
```

Create `_AI/OVERVIEW.md` — project description, architecture, key files, and anti-patterns.

Create `_AI/VALIDATION.md` — the commands to run at each validation gate:
```markdown
## Validation gates
1. `npm run lint` — after any JS/TS change
2. `npm test` — after each logical unit of change
3. `npm test` — full suite, must pass before done
```

---

## Install — Obsidian vaults

```bash
mkdir -p /path/to/vault/_AI
ln -s ~/Dev/code-ai-layer/vault/core /path/to/vault/_AI/core
```

Make the AI boot file (`CLAUDE.md` or `AGENTS.md`) in the vault root:
```markdown
See `_AI/core/AI.md` for vault context and available workflows.
```

Create `_AI/GOALS.md` — the vault's purpose and focus areas.

Optionally create `_AI/VOICE.md` — a writing voice reference for the Compose workflow.

To block accidental commits of sensitive content, install the pre-commit hook:
```bash
cp /path/to/vault/_AI/core/scripts/pre-commit-sensitivity-check.sh /path/to/vault/.git/hooks/pre-commit
chmod +x /path/to/vault/.git/hooks/pre-commit
```

---

## Claude Code users — native skills (optional)

Instead of relying on trigger phrase matching, install native slash commands that delegate to the workflows:

```bash
bash ~/Dev/code-ai-layer/scripts/install-skills.sh
```

This installs all skills from `shared/skills/`, `code/skills/`, and `vault/skills/` into `~/.claude/skills/`. You get:

| Skill | Context |
|-------|---------|
| `/grill-me` | Both |
| `/validate-ai-setup` | Both |
| `/create-prp` | Code |
| `/execute-prp` | Code |
| `/review` | Code |
| `/teach-me` | Code |
| `/ingest` | Vault |
| `/lint` | Vault |
| `/connect` | Vault |
| `/compose` | Vault |
| `/debrief` | Vault |
| `/write` | Vault |
| `/save` | Vault |
| `/fetch` | Vault |

Skills are thin wrappers — all logic stays in the workflow files inside the symlinked `core/`.
