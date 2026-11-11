---
name: state-of-play
description: On-demand, full reconciliation sweep across a home's radar items and wayfinder waypoints — interrogates you to confirm what's still true, updates the underlying notes, then gives a plain-language digest in chat.
---

# Workflow: State of Play

Triggered by: "state of play", "where are we", "sweep the gig"

A deliberate, on-demand audit — not a scheduled or scoped-to-stale check. Every live item gets asked about, every time, because the value is in you choosing when to pay the cost, not in automating it away. Don't run this proactively; only when explicitly triggered.

## Scope

Scoped to a single home (a gig or project folder). Derive the home from context; ask before proceeding if ambiguous.

## Step 1: Gather the live set

Collect every item currently considered active — nothing closed, resolved, or archived:

- **Radar** — run `python3 _AI/local/scripts/list-radar.py <home>/radar` for every item with `status: watching`. Skip `dormant`, `not-mine`, and `resolved` — those have already been triaged out of your attention.
- **Wayfinder** — `<home>/_wayfinder/*/map.md` where `status: active`; only the Open/frontier waypoints, not Blocked or Resolved.

If a category has no live items, skip it silently — don't ask about an empty set.

## Step 2: Interrogate, one item at a time

Follow `_AI/shared/workflows/grill-me.md` interview style: one question at a time, offer your best-guess read before asking, and explore first (recent log notes, linked notes, ticket state) rather than asking anything answerable from the files.

**Source discipline.** The note being swept (radar/wayfinder) and any reflection or digest note along the way are themselves AI-authored synthesis — a lead, not verified fact, however confident their wording sounds. Before presenting a best-guess to the user, trace the claim back to a primary source: a dated log note with no `ai-generated` tag, i.e. the owner's own first-hand capture, or an artefact outside the vault (a ticket, a PR) if that's what the user points to. If a claim only traces back to another AI-generated note with no primary corroboration found, say so explicitly when presenting it — never present secondhand synthesis as settled.

For each item, the question is always some form of "is this still true, and is it still yours to watch?" Concretely:

- **Radar** — does `latest:` still hold? Has it moved to `dormant`, `resolved`, or turned out to be `not-mine` after all?
- **Wayfinder waypoint** — resolved, still open, or has it grown its own map or radar note and should now just be a status pointer rather than an independent item?

## Step 3: Apply confirmed updates immediately

Update each note using its own existing convention as you go — don't batch this to the end:

- **Radar** → `_AI/local/workflows/add-to-radar.md`, Mode: Update.
- **Wayfinder** → `_AI/local/workflows/wayfinder.md`, Mode: Work the frontier (move to Resolved, log the decision, update frontmatter, unblock dependents).

## Step 4: Synthesize the digest

Once every live item has been reconciled, write a plain-language digest of the whole home — not partitioned by note type, blended into a single read of "what's actually going on."

- Maximum 6 bullets.
- Caveman-simple: short, blunt sentences, no hedging register.
- Strip interpersonal colour (frustration, blame, tone) unless it's actually decision-relevant — someone's frustration with another team only belongs in the digest if it changes what happens next.
- Lead with what's blocked or moving, not with process detail.

## Step 5: Report

Tell the user which notes were updated and give the digest in chat. Don't write it to a file: `NEXT.md` is the page the owner looks at, and it derives itself from the notes.
