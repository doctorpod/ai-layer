---
name: wayfinder
description: Map out a fuzzy, too-big-for-one-session project into a destination and a set of small decisions (waypoints), then work through them one at a time across sessions.
---

# Wayfinder Workflow

Triggered by: "wayfinder this", "map this out", "help me find a way forward", "chart a way forward"

Adapted from Matt Pocock's wayfinder skill (https://github.com/mattpocock/skills) for vault use. For a project that's too woolly or too large to just start doing — you don't know the order, there are several unresolved decisions, and it'll span more than one session — wayfinder builds a **map**: a destination statement plus a list of small decisions (**waypoints**) to resolve one at a time.

Don't confuse this with:
- `radar` — a situation to watch, no action implied.
- `greenhouse` — an idea you already understand, deliberately parked.
- `post-mortem` — investigates something that already went wrong.

Wayfinder is for active, unclear, multi-step efforts you actually want to move forward on.

## Scope

Each wayfinder project lives at `_wayfinder/<kebab-case-slug>/map.md`, nested inside the project's own folder when one already exists (e.g. `projects/2026-07-LondonRoadDover/_wayfinder/map.md`) — this keeps the map next to the rest of the project's material instead of needing every update made twice. Fall back to `_wayfinder/<slug>/map.md` at the vault root only when the subject has no existing project folder of its own (e.g. a household task like `chimney-water-ingress`).

## Map format

```
---
categories: ["[[Wayfinder]]"]
aliases:
  - [human-readable version of the slug, e.g. chimney-water-ingress -> chimney water ingress]
status: active
opened: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - ai-generated
---

## Destination
[One sentence: what "sorted" looks like. What's explicitly out of scope.]

## Decisions so far
- YYYY-MM-DD — [waypoint] → [resolution]

## Waypoints

### Open (the frontier)
- [ ] **[title]** — HITL/AFK. [one-line question this waypoint needs to answer]. Blocked by: none

### Blocked
- [ ] **[title]** — HITL/AFK. [one-line question]. Blocked by: [waypoint title]

### Resolved
- [x] **[title]** — [resolution]. YYYY-MM-DD
```

**HITL** (human in the loop) — needs the user directly: a call only they can make, someone they need to contact, information only they have.
**AFK** — something the assistant can research or draft, now or in the background, without the user needing to be present.

## Mode: Chart

Use the first time a project is mapped — no `map.md` exists yet for it.

1. **Scan first** — check `_wayfinder/` for a close match, and check whether an existing project folder for this subject already exists elsewhere (e.g. under `projects/`). If a matching wayfinder map exists, offer to add to it instead of starting a new one. If no map exists yet but a project folder does, place the new map inside that project folder (see Scope) rather than at the vault root.
2. **Name the destination.** This is the first act, before any waypoint exists. Use `grill-me` rules: one question at a time, offer a best-guess answer, ask the user to confirm or correct. Keep going until the destination is a single concrete sentence with a clear boundary (what's in, what's explicitly not).
3. **Surface the waypoints.** Same grilling approach: work out what's actually unknown or blocking — decisions, missing information, people to contact, things to research. Each becomes one waypoint: a short title, a one-line question it needs to answer, HITL/AFK classification, and any blocking dependency.
4. **Write `map.md`.** Destination, empty "Decisions so far", waypoints sorted into Open/Blocked/Resolved (Resolved starts empty). Set `aliases:` to the slug with hyphens replaced by spaces (e.g. `chimney-water-ingress` → `chimney water ingress`), so the map can be wikilinked in plain English from journal entries and project notes.
5. **Confirm** — tell the user the file path and read back the frontier (the open, unblocked waypoints) — that's what's actionable next.

## Mode: Work the frontier

Use when a `map.md` already exists and the user wants to keep moving (triggers: "next waypoint", "work the wayfinder", "wayfinder this" naming an existing project).

1. Read the map. List the frontier — open, unblocked waypoints.
2. Take one waypoint at a time, in conversation:
   - **HITL** — grill it out (`grill-me` rules) until it's actually resolved, not just discussed. Don't manufacture a decision on the user's behalf.
   - **AFK** — offer to research it now (WebSearch, past notes) or flag it for later; do the research and report findings.
3. **On resolution** — move the waypoint to Resolved with the outcome and date, append a line to "Decisions so far", update the `updated:` frontmatter, and check whether any Blocked waypoint is now unblocked (move it to Open if so).
4. Prefer resolving one or two waypoints per session over trying to clear the whole map — the discipline is incremental progress, not a single marathon session.

## Mode: Add waypoint

Use when a new decision or unknown surfaces mid-project.

1. Add it to Open or Blocked as appropriate, classified HITL/AFK.
2. Update the `updated:` frontmatter.

## Mode: Review

Use when the user asks to review wayfinder projects.

1. Read all `_wayfinder/*/map.md` files.
2. Summarize: destination + frontier size + last updated, per project.
3. Flag anything that looks stalled (no updates in a long time) or resolved-in-spirit (all waypoints resolved — offer to close it).

## Project sync

Applies only when a wayfinder map is nested inside a project folder (see Scope) — a root-level map with no owning project has nothing to sync with.

When resolving a waypoint establishes something true about the project itself — a fact, a decision, a contact made — not just bookkeeping on the map, offer to route it into the project properly: `debrief` if it's first-hand material worth verifying, `ingest` if there's source material to fold in. Don't let a real project fact live only in "Decisions so far" if the project's own wiki should know it too.
