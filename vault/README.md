# Vault Workflows

Grouped by what you're trying to do, this is your map of the AI workflows available in this vault.

- `AI.md` is the machine-facing trigger table Claude routes on — not meant for browsing.
- This file is the human-facing companion: the same workflows, organized by scenario instead of trigger phrase.
- Keep both in sync — if a workflow is added, renamed, or removed, update this file and `AI.md` together.

---

## Bringing material in

| Workflow | Use when |
|---|---|
| **Debrief** | You have first-hand material — a site visit, a conversation, a memory, a thought you've worked out. Accuracy is paramount; the source is you. |
| **Ingest** | You've dropped something external into `inbox/` — an article, transcript, YouTube video, book extract, or web-stub. |
| **Capture log note** | You just want something logged to today's dated note — no wiki processing, no classification, just written down. |

Debrief vs. capture-log-note is a judgment call: first-hand material you want fully processed into wiki pages goes through debrief; a quick note-to-self goes through capture-log-note.

---

## Writing a piece

Every piece lives in the same `brief.md` / `themes/` / `output.md` / `assets/` folder (see `_AI/shared/snippets/piece-folder.md`). The brief itself is ad hoc — just ask for help drafting it in chat, no dedicated workflow owns that step.

| Workflow | Use when |
|---|---|
| **Sync-guide** | Build or update the piece's `themes/` folder from the brief and vault sources. Only ever touches `themes/` — never reads or writes `output.md`, never drafts prose. |
| **Elicit** | Stuck on a section — want a burst of odd angles and questions to kick a sentence loose. Reads `guide.md`'s bullets, throws out ideas in chat (or into a `scribe` block), then stops. One pass, no back-and-forth, never touches `output.md`. *(Not yet updated for `themes/` — still assumes the old flat `guide.md`.)* |
| **Polish** | The text is already yours (typed or dictated) — clean up spelling/punctuation/structure only, never rephrase. Works on any file, not just `output.md` in a piece-folder — see `%P`/`%` markers in `polish.md`. |
| **Scribe** | Leave a `% scribe <instruction>` marker inline in any file — I carry out the instruction and write the response into a `% comments` block in place, without stripping the marker. Works on any file, not just `output.md` in a piece-folder. |
| **Sanity** | Check your own writing for contradictions or passages that don't hold together. Diagnostic only, never edits. |
| **Gap-check** | Compare a draft against its `themes/` (or any named reference) and report what's missing. Never edits target or reference content, but does record a coverage verdict on each checked theme, every run. No overall score — just a gap list. |
| **Diploma-ready** | Same read-only-target shape as gap-check, but checked against the fixed Diploma assessment rubric specifically, with a Yes/Nearly/Not Yet verdict — before showing a tutor. *(Still reads `guide.md` directly — not yet updated for `themes/`.)* |

**You always write `output.md` yourself — `sync-guide` scaffolds and stays out of it.** **Calling `sync-guide` on a piece already in progress** only ever touches `themes/`, regardless of whether your draft so far came from typing, dictating + polish, or ideas sparked by `elicit` — it can't clash with any of them. When you want to know whether the draft actually covers the themes, that's a separate step: call `gap-check` explicitly.

`polish` and `scribe` are unrelated to this pipeline — both are marker-driven and work on any vault file, whether or not a piece-folder is involved.

---

## Keeping track of things worth remembering

| Workflow | Use when |
|---|---|
| **Add to radar** | A situation worth watching — no action implied, just awareness. |
| **Greenhouse** | A concrete idea you like and want to do — deliberately not now. |
| **Post-mortem** | Something went wrong; investigate why and propose a specific fix. (Greenhouse is one *possible outcome* of a post-mortem, not a substitute for it.) |

---

## Reviewing what's happened

| Workflow | Use when |
|---|---|
| **Reflect** | Review a scope of notes (last N days, since the last reflection, etc.) and surface patterns, momentum, surprises, and open loops as a chat response. Diagnostic by default — can capture as a reflection note or feed open loops into `add-to-radar` on request. |

---

## Auditing and maintaining the vault

| Workflow | Use when |
|---|---|
| **Lint** | Automated structural check — orphan pages, broken links, pending cautions — via script. |
| **Process notes** | Convention-based: proposes folder moves and category fixes, applies on confirmation. |
| **Connect** | Cross-knowledge-base pass to surface new connections between KBs. |
| **State of play** | On-demand, full reconciliation sweep across a gig's live projects, radar, triage, and wayfinder waypoints — interrogates you on each, updates the underlying notes, then writes a plain-language digest to `DASHBOARD.md`. |
| **Create summaries** | Pulls mentions from linking notes into a target note's `## Summary` section. |
| **Link components** | Wikilinks PRP decision notes to technical component pages (code-adjacent KBs only). |

---

## Talking something through

| Workflow | Use when |
|---|---|
| **Rubber duck** | You want to think out loud — no file changes, honest pushback. |
| **Grill me** | You want to be interrogated until the decisions are captured in a durable ADR-style record. |

---

## Crossing a session boundary

| Workflow | Use when |
|---|---|
| **Handoff** | Save state so this conversation can be resumed later. |
| **Resume** | Pick up from a saved handoff. |
| **Fetch** | Different mechanism — async message passing via a dated chat file, not a session-boundary save. |

---

## Setup and meta

| Workflow | Use when |
|---|---|
| **Validate AI setup** | Check the AI layer is correctly installed in this vault. |
| **Save** | Commit recent changes with a summary and log entry. |
