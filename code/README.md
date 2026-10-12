# Code Workflows

How a change moves from a ticket to merged PRs in a code repo, and which workflow does each step.

- `AI.md` is the machine-facing trigger table and the rules Claude routes on — not meant for browsing.
- This file is the human-facing companion: the same process, laid out as the steps you follow.
- Keep both in sync — if a workflow, path or rule changes, update this file and `AI.md` together.

---

## The pieces

- **Ticket** — a snapshot of a ticket someone else owns (e.g. Jira), kept in `delivery/tickets/`. Optional: personal work often has none.
- **Work folder** — `delivery/work/<key>/`: everything about delivering one ticket or change. It lives in the vault and stays there.
- **Key** — the work folder's name: a ticket ID on gigs (`ABC-123`), a plain slug otherwise (`nested-layers`). Put it in your branch names as a segment (`feat/abc-123/totals`) and workflows find the folder on their own.
- **Init** — `init.md`: your framing beyond the ticket. With no ticket, the request itself.
- **Plan** — `plan.md`: what holds for the whole ticket (goal, acceptance criteria, context, architecture notes, anti-patterns), the list of slices, and the close-out checklist.
- **Slice** — one independently mergeable change, delivered as one PR. `slices/NN name.md`: metadata and checklist on top, its own blueprint below. Its `state` runs `planned → in progress → PR open → merged`.

```
<vault>/<gig or project>/delivery/     ← linked into each repo as _AI/delivery
  tickets/                             ← optional
    ABC-123.md
  templates/                           ← optional
    slice.md
  work/
    ABC-123/
      init.md
      DECISIONS.md
      QUESTIONS.md
      GLOSSARY.md                      ← optional
      QA-FAILURES.md                   ← when QA fails
      plan.md
      slices/
        01 add-model.md
        02 show-total.md
```

---

## One-time setup

**Per repo**

1. Install the layer: `bash ~/Dev/ai-layer/scripts/install-target.sh --code`.
2. Link the delivery folder: `ln -s <vault>/<gig or project>/delivery _AI/delivery`, and make sure `delivery/work/` exists in the vault. For a repo with no vault home, create a real folder instead: `mkdir -p _AI/delivery/work`.
3. Gitignore it: `_AI/` (or at least `_AI/delivery`) in `.gitignore`.
4. Let Claude Code reach the vault folder: add it to `additionalDirectories` in `.claude/settings.local.json`:
   ```json
   { "permissions": { "additionalDirectories": ["<vault>/<gig or project>/delivery"] } }
   ```
5. Run `/validate-ai-setup` — it checks the link resolves, `work/` exists, `_AI/delivery` is gitignored, and warns about a leftover legacy planning folder.

**Per vault**

- Add `slices.base` to `lib/`, so every `plan.md` can show its slices with `![[slices.base]]`:
  ```yaml
  filters:
    and:
      - file.inFolder(this.file.folder + "/slices")
  views:
    - type: table
      name: Slices
      order:
        - file.name
        - repo
        - depends-on
        - state
        - link
  ```

**Per gig (optional)**

- Add `delivery/templates/slice.md` to replace the default slice checklist with the gig's own (linters, ticket transitions, reviewers). Plain text only — no Templater syntax. Everything in it sits above a horizontal rule; the workflows write the blueprint below it. Without one, the layer's default `templates/slice.md` (a solo branch → PR → merge checklist) is used.

---

## Working a ticket

1. **you** — Snapshot the ticket into `delivery/tickets/<KEY>.md` (gigs only).
2. **you** — Write `delivery/work/<key>/init.md`: your framing, with `ticket: "[[<KEY>]]"` in its frontmatter when there's a ticket. With no ticket, write the request itself, including any acceptance criteria.
3. **`/grill-me <key>`** — reads init and the ticket, grills you on the gaps, and captures decisions into `DECISIONS.md`. Creates the work folder if it doesn't exist yet.
4. **`/create-plan`** — proposes the approach and a list of slices; **you** approve or adjust them. It then writes `plan.md` and every slice note, each with its blueprint.
5. For each slice, in dependency order:
   1. **you** — Branch off main, with the key in the branch name.
   2. **`/execute-plan <key> <NN>`** — implements only that slice and sets its `state: in progress`. Fresh session.
   3. **`/review`** — checks the diff against the slice's steps and success criteria. Fresh session. Diagnostic only.
   4. **you** — Work through the slice's checklist: open the PR (or merge straight to main), set `link:`, move `state` to `PR open`.
   5. **you** — Once merged, set `state: merged`.
6. If QA fails: **`/qa-failure`** — logs the failure in `QA-FAILURES.md`, diagnoses it with you, then writes and implements a fix slice on its own branch. Fresh session. Continue from step 5.4 for that slice.
7. **you** — Work through the close-out checklist in `plan.md`: all slices merged; durable decisions promoted to the repo `wiki/`; durable terms promoted to vault concept notes; ticket `status: inactive` (if there's a ticket).

---

## Other code workflows

| Workflow | Use when |
|---|---|
| **Teach me** | You want to learn how part of the codebase works, using the code itself as the material. |
| **Strict review** | You want a harsh maintainability pass — abstraction quality, giant files, tangled conditionals. |
| **Readback** | You've just built something and want to check your own explanation of it against the diff and the slice. |
| **Rubber duck** | You want to talk a problem through with honest, brief pushback and no file changes. |
| **Greenhouse** | An idea is worth keeping but not acting on now. |
