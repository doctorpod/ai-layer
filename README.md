A portable AI workflow layer that installs into any codebase via symlink. It gives your AI assistant a structured approach to planning, implementing, and reviewing code changes — without baking any project-specific knowledge into the shared core.

Inspired by [Matt Pocock](https://www.mattpocock.com).

Drop it in, point your AI boot file at it, and get:
- **Grill me** — relentless interrogation to surface assumptions before you write a line of code
- **Create PRP** — a complete implementation brief built from that shared understanding
- **Execute PRP** — a disciplined implementation pass in a clean context
- **Review** — a post-implementation check against the brief before raising a PR

---

## Install instructions for humans

1. In your code repo:
```bash
mkdir -p _AI/PRPs
ln -s ~/Dev/code-ai-layer/core _AI/core
```

> **Symlink vs copy:** The symlink means all your repos share one `core/` — updates to this repo propagate everywhere instantly. That's ideal for personal use where you own all the repos. For shared team repos where others shouldn't be coupled to your local path, copy the `core/` folder instead or use a git submodule.

2. Make the AI boot file (e.g. CLAUDE.md) in the root of your code repo. At minimum it should contain:
```markdown
See `_AI/core/AI.md` for project context and available workflows.
```
3. Create `_AI/OVERVIEW.md` — project description, architecture, key files, and anti-patterns
4. Create `_AI/VALIDATION.md` — the commands to run at each validation gate, e.g.:
```markdown
## Validation gates
1. `npm run lint` — after any JS/TS change
2. `npm test` — after each logical unit of change
3. `npm test` — full suite, must pass before done
```

### Claude Code users (optional)

Instead of relying on trigger phrase matching, you can install native Claude skills that delegate to the workflows:

```bash
bash ~/Dev/code-ai-layer/scripts/install-skills.sh
```

This gives you explicit `/create-prp`, `/execute-prp`, `/grill-me`, `/review`, `/teach-me`, and `/validate-ai-setup` slash commands. The skills are thin wrappers — all logic stays in the workflow files.
