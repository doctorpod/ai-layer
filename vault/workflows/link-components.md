---
name: link-components
description: Sweep a knowledge base's internal decision notes (starting under PRPs/) and propose wikilinks connecting them to the technical components they touch.
---

Triggered by: "link components" + knowledge base name, "sweep PRPs for components", "link components in `<repo>`"

This is a **linking** workflow, not a summarising one. Its only durable output is wikilinks from source notes to component notes. History for a component is read live via a Base query embedded in the component note — this workflow never writes prose into a component note itself. See `Components` in `lib/categories/` and `Touchpoints` for the sibling pattern this follows.

## Precondition

The target KB (a `repos/<name>/` folder) must have a `wiki/` subfolder. Component notes are `wiki/` pages tagged `categories: ["[[Components]]"]` — the same wiki pages ingest would otherwise produce, just tagged.

If the KB's `AI.md` has a `Repo path:` line, the actual codebase is available for verification (see Step 3b). If it's missing, ask the user once, up front, whether they want to add it before proceeding — don't silently skip verification or nag mid-run. If they decline or don't have the repo checked out, proceed on text alone.

## Step 0: Bootstrap

- If `lib/categories/Components.md` doesn't exist at the vault root, offer to create it — one line, same shape as `Touchpoints.md`: e.g. *"Architectural pieces of a specific codebase — not the tools/frameworks it's built with."*
- If the target KB's `wiki/` folder has no `components.base` file, offer to create it:

  ```yaml
  filters:
    and:
      - file.hasLink(this.file)
      - file.folder != "templates"
  views:
    - type: table
      name: History
      order:
        - file.name
      sort:
        - property: file.name
          direction: ASC
      columnSize:
        file.name: 454
  ```

  Note: unlike `logs.base`, this doesn't group by `date` — PRPs/DECISIONS notes carry no date frontmatter. Sorted by filename (roughly ticket order) instead. If a date convention gets adopted for PRPs later, upgrade this query to group by date the way `logs.base` does.

## Step 1: Build the candidate list

Find every note in the target KB's `wiki/` tagged `categories: ["[[Components]]"]`. This is the bounded vocabulary for matching — never invent a component name that isn't either an existing match or a new note the user confirms in Step 4.

This is a plain `grep -l` over `wiki/*.md` frontmatter, not a script — the candidate list is short and the lookup is already as cheap as it gets.

## Step 2: Find unlinked decision blocks

Run `python3 _AI/local/scripts/find-unlinked-decisions.py <kb-path>`. It walks `<kb-path>/PRPs/` for `DECISIONS.md` (primary source; this is where the *why* lives) and `prp.md` (secondary; spec/plan framing) files — the only two decision sources, everything else in a PRP folder (`GLOSSARY.md`, `ponderings.md`, `key-aspects.md`, `init.md`/`initial.md`) is a working note, not a decision record, and linking from it would pollute a component's history with scratch material — and prints one `path: heading` line per `## heading` decision block that has no `**Component(s):**` line yet.

This is the only completeness check the workflow needs. There is no separate incremental/marker step: the script sweep is cheap enough to run in full every time, so first run and hundredth run take the same path — no state file to go stale, nothing to migrate.

- If the script prints nothing (just the trailing `0 unlinked decision block(s)...` line): report "nothing to do" and stop. Don't open any source file.
- If it prints entries: group them by file. These files — and only these — get opened in Step 3. Never Read a source file this script didn't flag.

Caveat: the script's notion of "linked" is mechanical — it looks for the literal `**Component(s):**` field, the only way Step 6 ever writes a link. A component mentioned only in prose, without that field, will still show up here and get re-evaluated. That's an acceptable false positive (costs a re-look at one block); it never causes a false negative, since a block once written by Step 6 always carries the field.

## Step 3: Infer per decision block

For each flagged `## heading` block, read its Decision / Why / Alternatives text and match against the Step 1 candidate list — by name, by class/file name mentioned in the text (e.g. `CpvPeerGroupComparison`, `ContractsController`), or by clear paraphrase. A block may match zero, one, or several components.

Match against the existing candidate list first. Do not free-associate a component name that isn't already a wiki page — that's Step 4's job, not this one.

If a block's connection to a component is genuinely unclear (vague paraphrase, no class/file named, could plausibly be several things), leave it unmatched rather than guessing — under-linking is recoverable, a wrong link silently pollutes that component's history table.

## Step 3b: Verify against the real repo, if available

Prose drifts — a decision can name a class that was later renamed, or propose one that was superseded by a different approach in a later PRP. If the KB's `AI.md` has a `Repo path:`, verify names against the actual codebase rather than trusting text alone:

- **Before proposing a new component (Step 4) — do this, don't skip it.** Grep the repo for the class/controller name. If it doesn't exist, search for what the decision's *outcome* actually was (a later PRP in the same ticket, or a different name) before assuming the name is right. A decision block proposing a class that was never built (superseded, abandoned) should not spawn a component page for a class that isn't real — note it as superseded instead, same as an unmatched block.
- **Before matching an existing candidate (Step 3) — best effort, not mandatory.** If a decision's phrasing is a paraphrase rather than a named class, a repo grep can confirm which existing component it actually touches instead of guessing from wording alone.
- If the repo path doesn't resolve (moved, not checked out), fall back to Step 3/4 as normal — this step only adds confidence, it isn't a hard gate.

## Step 4: No-match → propose a new component note

If a decision block clearly concerns a technical part of the system with no existing wiki page for it, propose creating one. Confirm with the user before creating — one at a time, same as ingest's glossary pass.

New component note format:

```markdown
---
categories:
  - "[[Components]]"
tags:
  - ai-generated
---

# Component Title

**Summary**: One to two sentences describing this component.
**Last updated**: Date of creation.

---

![[components.base]]

Body content: what it is, where it lives in the codebase.
```

## Step 5: Batch confirm

Collect all proposed links for the whole sweep run — existing-component matches from Step 3 and new-component proposals from Step 4 — and present them together before writing anything. Group by source file. Don't interrupt per decision block.

## Step 6: Write

On confirmation, add the link inline at the relevant decision block, not as a bulk list at the top of the file:

```markdown
**Decision:** ...
**Why:** ...
**Alternatives:** ...
**Component(s):** [[component-name]]
```

Note the Base query is file-level (`file.hasLink(this.file)`) — it can't reflect which specific decision block within a multi-decision file did the linking. Placing the link at the block level still matters for anyone reading the source file directly, even though the component's own History table will just show the file once.

## Step 7: Learnings

Reflect briefly: was there anything about this KB's structure, PRP conventions, or component-matching that would have been faster to know upfront? If yes, follow `_AI/shared/snippets/learnings.md`, substituting `LINK-COMPONENTS` for `[WORKFLOW]`.
