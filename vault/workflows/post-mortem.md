---
name: post-mortem
description: Investigate something that went wrong, find the root cause, and propose a concrete tweak to the vault or its workflows to reduce recurrence.
---

# Post-Mortem Workflow

Triggered by: "post-mortem this", "run a post-mortem", "post-mortem on [thing]", "candidate for post-mortem?"

Either of us can flag something as a post-mortem candidate — a mistake, a near-miss, a recurring friction, anything that went worse than it should have. This is not a queue: run it live, at the point it's raised, against whatever conversation or work produced the incident.

Don't confuse this with `radar` (a situation worth watching, no fix implied) or `greenhouse` (an idea already known and wanted, just not now). Post-mortem investigates *why something went wrong* and produces *a specific proposed fix*. Greenhouse is one of its possible outcomes, not its purpose.

## Before starting

Check `_AI/learnings.md` if it exists. Several workflows already log lightweight one-line insights there. If this incident already has an entry, read it — the post-mortem is the deep-dive version of that same signal, not a duplicate of it.

## Step 1: Establish what happened

A mix of `grill-me` and `rubber-duck`:
- Ask one question at a time. Offer a best-guess answer each time and ask the user to confirm or correct it — don't fire blank questions.
- If the first theory of what went wrong looks shaky, say so plainly before going further. Rubber-duck's "push back, don't soften" rule applies here.
- Keep going until you reach an actual root cause, not just the symptom. "I forgot" is a symptom; "there was no checklist step for this" is a root cause.

Lazy capture: don't write anything until the root cause is genuinely established.

## Step 2: Name what worked

Before proposing a fix, say — specifically and honestly — what went right in this same incident. This is not padding and it isn't optional, but it must be true: name something that actually happened (caught it before it shipped, a check that worked as intended, a fast recovery), not a generic "good effort." If nothing genuinely went right, say that plainly rather than inventing something — but check hard before concluding that; it's rarely actually true.

## Step 3: Propose a tweak

Map the root cause to one of these targets and produce the actual concrete change, not a vague suggestion:

| Target | Typically lives at | Directly writable? |
|---|---|---|
| Skill/workflow tweak or new skill | `_AI/local/workflows/`, `_AI/shared/workflows/` | No — draft only |
| Checklist tweak | `templates/` | No — draft only |
| Vault structure tweak | folders, `CLAUDE.md`, `AI.md` | No — draft only |
| Gap in an existing KB | `wiki/`, `INDEX.md` within that KB | Usually yes, once agreed |
| Brand-new KB | new top-level folder + `inbox/` | No, folder scaffold needs permission — contents inside are writable once it exists |

"Directly writable" follows the write-access rules in `AI.md`. Most targets aren't on that list — the default is: draft the change, show it, don't apply it unasked.

### Exception: sourcing generic reference material

A vault's normal rules may exclude generic web material (only org-specific or personally-synthesised knowledge belongs). A post-mortem-driven KB fix is allowed to break that rule *only* when the note carries a `postmortem:` frontmatter field pointing back to this record — the provenance is what justifies the exception. Don't source generic material for any other reason.

## Step 4: Act on the outcome

Don't write anything durable by default — a post-mortem conversation is disposable unless the user wants it kept. Ask which of these it becomes:

- **Applied now** — if directly writable per Step 3's table, make the change; otherwise ask permission, make it.
- **Greenhouse** — run `greenhouse` Capture mode, referencing this incident.
- **Declined** — note it in chat and stop. Legitimate outcome, not a failure of the workflow.

## Step 5: Offer to capture, don't assume it

Once the outcome is settled, offer — don't auto-write:

- **Default: a log note.** Offer to run `capture-log-note` with a summary of what happened, the root cause, and the outcome. This is the lightweight path and covers most cases.
- **If the tweak is still open** (applied-later, or the greenhouse item needs its own status tracked over time — not a same-session apply or a clean decline), offer the fuller alternative instead: a dedicated record at `_AI/postmortems/<kebab-case-slug>.md`:

  ```markdown
  ---
  categories: ["[[Post-mortem]]"]
  status: proposed | applied | greenhouse | declined
  date: YYYY-MM-DD
  target: skill | checklist | vault-structure | kb-gap
  tags:
    - ai-generated
  ---

  ## What happened
  [factual account]

  ## Root cause
  [the actual why]

  ## What worked
  [specific, true, traceable to this incident]

  ## Proposed tweak
  [the concrete draft — diff, new line, stub]

  ## Outcome
  [applied and how / linked greenhouse entry / declined and why]
  ```

  Use this over a log note specifically when the status will need revisiting later — it's the only format built to change state over time.

If the user declines both, that's fine — the analysis and any applied change already happened; nothing else needs to persist.
