A portable AI workflow layer that installs into any project via symlink. It gives your AI assistant a structured set of workflows for two contexts: **coding repos** and **Obsidian vaults**.

Inspired by [Matt Pocock](https://www.mattpocock.com) - Thanks Matt!.

---

## Contexts

### Code workflows

Drop the `code/` layer into any coding repo and get:
- **Create PRP** — synthesizes a complete implementation brief from decisions captured by Grill me
- **Execute PRP** — a disciplined implementation pass in a clean context
- **Review** — a post-implementation check against the brief before raising a PR
- **QA failure** — log a QA failure against a PRP, diagnose the root cause, and apply a scoped fix
- **Strict review** — a harsh maintainability review for abstraction quality, giant files, and tangled conditionals
- **Teach me** — guided learning from the codebase

### Vault workflows

Drop the `vault/` layer into any Obsidian vault and get:

**Knowledge base**
- **Ingest** — add new sources to your knowledge base
- **Debrief** — process first-hand notes into wiki pages
- **Lint** — audit KB structure for orphans, broken links, and pending cautions
- **Normalise** — find near-duplicate, over-broad, or source-shaped wiki pages and propose merges or splits
- **Connect** — discover cross-KB insights and write bidirectional links
- **Link components** — propose wikilinks from internal decision notes to the components they touch
- **Create summaries** — update a note's Summary section from the notes that reference it

**Writing**
- **Sync-guide** — build/maintain a piece's guide from its brief and vault sources
- **Interview** — interview the writer one thread at a time and save verbatim answers into the guide
- **Elicit** — a one-shot brainstorm of tickler ideas and questions from a section's theme notes
- **Beats** — lay out a beat sheet from guide notes to draft prose against
- **Gap-check** — check a draft against its guide (or any reference) and report what's missing
- **Sanity** — flag contradictions and non-sequiturs in your own writing, without editing it
- **Polish** — light copy-edit of your own prose: spelling, punctuation, structure only
- **Scribe** — carry out an inline `% scribe` instruction and write the response back in place

**Tracking and planning**
- **Capture log note** — file content as a dated log note in the right gig log folder
- **Minute** — log a logistics or status change and propagate it across radar, questions, wayfinder, and greenhouse
- **Add to radar** — capture, update, and review ongoing things worth tracking
- **Wayfinder** — map a too-big project into a destination and small decisions worked through across sessions
- **State of play** — a full reconciliation sweep across a gig, ending in a digest in `DASHBOARD.md`
- **Process notes** — propose folder moves and categories for a scope of notes, then apply on confirmation

**Reflection**
- **Reflect** — surface patterns, observations, and open loops across a scope of notes
- **Gratitude** — prompts grounded in recent journal notes, with approved entries appended to today's daily note
- **Post-mortem** — find the root cause of something that went wrong and propose a workflow tweak

**Specialist and housekeeping**
- **Diploma ready** — check a permaculture design against the Diploma design rubric
- **Save** — commit with a 12-word summary and log entry
- **Fetch** — async message passing via dated chat logs

### Shared workflows

Both contexts also include (from `shared/`):
- **Grill me** — relentless interrogation that captures decisions into a durable ADR-style record
- **Rubber duck** — talk a problem through with honest, brief pushback
- **Readback** — check your own explanation against the evidence until it's right
- **Greenhouse** — park early-stage ideas for later review
- **Handoff** / **Resume** — save a conversation's state and pick it up in a later session
- **Validate AI setup** — check the AI layer is correctly installed

---

## Principles

`docs/PRINCIPLES.md` holds the invariants every workflow must obey — read-only means read-only, every wiki claim traces to a source, hand-owned files change only on an explicit say-so, and so on. It's checked against when a workflow is written or revised, not walked at runtime. Kept deliberately short (~ten).

Design-time documentation for people writing workflows lives in [`docs/`](docs/): `PRINCIPLES.md` for what a workflow must never do, and `PATTERNS.md` for reusable shapes that tend to work (Rubric, Gatherer, Log inputs derive the rest, Toolbox not pipeline).

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

Optionally, if this repo belongs to a group of related repos with a sister vault, symlink the group's `RELATED.md` from the vault (format in `shared/snippets/related.md`):
```bash
ln -s <vault>/<group folder>/RELATED.md _AI/RELATED.md
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

To block accidental commits of sensitive content, install the pre-commit hook:
```bash
cp _AI/local/scripts/pre-commit-sensitivity-check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

If the vault is the sister vault for a group of related repos, keep the group's `RELATED.md` in the vault folder for that group (see `shared/snippets/related.md`).

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
| `/rubber-duck` | `_AI/shared/workflows/rubber-duck.md` |
| `/readback` | `_AI/shared/workflows/readback.md` |
| `/validate-ai-setup` | `_AI/shared/workflows/validate-ai-setup.md` |
| `/create-prp` | `_AI/local/workflows/create-prp.md` |
| `/execute-prp` | `_AI/local/workflows/execute-prp.md` |
| `/review` | `_AI/local/workflows/review.md` |
| `/teach-me` | `_AI/local/workflows/teach-me.md` |
| `/ingest` | `_AI/local/workflows/ingest.md` |
| `/lint` | `_AI/local/workflows/lint.md` |
| `/normalise` | `_AI/local/workflows/normalise.md` |
| `/connect` | `_AI/local/workflows/connect.md` |
| `/debrief` | `_AI/local/workflows/debrief.md` |
| `/sync-guide` | `_AI/local/workflows/sync-guide.md` |
| `/gap-check` | `_AI/local/workflows/gap-check.md` |
| `/save` | `_AI/local/workflows/save.md` |
| `/fetch` | `_AI/local/workflows/fetch.md` |

Skills are thin wrappers — all logic stays in the workflow files. Context-specific skills resolve via `_AI/local` (which symlinks to either `code/` or `vault/` depending on the target). Shared skills resolve via `_AI/shared`.
