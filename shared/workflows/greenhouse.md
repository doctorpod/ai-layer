---
name: greenhouse
description: Park early-stage ideas you like but don't want to act on now, for later review.
---

# Greenhouse Workflow

Triggered by: "greenhouse this", "park this in the greenhouse", "add to greenhouse", "review greenhouse"

A greenhouse item is an idea worth keeping but not acting on right now. It differs from a radar item: radar says *"here's a situation worth being mindful of, no action implied"*; greenhouse says *"here's a concrete thing I'd like to do, deliberately not now."* Don't put situations-to-watch here, and don't put radar items here — they stay in `radar/`.

## Scope

Greenhouse entries live in a `_greenhouse/` folder at the project root.

- Code project → `_greenhouse/` at the repo root.
- Vault → `_greenhouse/` at the vault root.

## Note format

Freeform markdown — this folder is for early-stage thinking, not durable decisions, so don't over-formalize it. Existing entries vary, but conventionally:

- Filename: kebab-case slug, descriptive, no date prefix (e.g. `default-stroke-width.md`)
- A title heading, optionally prefixed (`# Backlog: <title>`, `# Parked: <title>`, or just `# <title>`)
- A body explaining what the idea is, written so it can be picked up cold with no memory of the conversation it came from. Common headers seen in practice: "What / What it should do", "Why parked / Deferred because" — none of this is enforced, use what fits.
- If the idea has a clear origin (a review, a commandment, a post-mortem, a PRP that ran out of scope for it), reference it inline so the source isn't lost.

## Mode: Capture

Use when an idea comes up that's worth keeping but not worth acting on right now.

1. **Scan first** — check `_greenhouse/` for a close match. If one exists, offer to fold this into it instead of creating a duplicate.
2. **Write the idea in your own words** — enough context that future-you, cold, can understand what it is and why it was parked.
3. **Confirm** — tell the user the filename and one-line summary.

## Mode: Review

Use when the user asks to review the greenhouse, or as a closing step of a broader review.

1. Read all entries in `_greenhouse/`.
2. Summarize in chat: title + one-line gist per entry. Flag any that look resolved by since-completed work, or stale enough to be worth pruning.
3. Invite the user to resolve, prune, or promote (e.g. into a PRP) any item.

## Mode: Resolve

Use when a greenhouse idea has actually been acted on.

1. Prepend a blockquote at the top of the file noting what resolved it:
   ```
   > **Resolved** by <PRP name, commit, or decision>.
   ```
2. Leave the file in place — resolved entries stay as a record. Don't delete or archive them.
