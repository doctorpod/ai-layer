# Vault Workflows

Grouped by what you're trying to do, this is your map of the AI workflows available in this vault.

- `AI.md` is the machine-facing trigger table Claude routes on — not meant for browsing.
- This file is the human-facing companion: the same workflows, organized by scenario instead of trigger phrase.
- Keep both in sync — if a workflow is added, renamed, or removed, update this file and `AI.md` together. For the writing workflows, also update the matching page(s) in `_AI/docs/writing/` and bump their `checked:` date.

---

## Bringing material in

| Workflow | Use when |
|---|---|
| **Debrief** | You have first-hand material — a site visit, a conversation, a memory, a thought you've worked out. Accuracy is paramount; the source is you. |
| **Ingest** | You've dropped something external into the vault-root `inbox/` — an article, transcript, YouTube video, book extract, or web-stub. Ingest routes it to the right KB. |
| **Capture log note** | You just want something logged to today's dated note — no wiki processing, no classification, just written down. |
| **Heartbeat** | Run several times a day to make sure every new log note (or journal note) has been dealt with. Opens with the notes still owing a debrief, then works through each new or edited note one at a time, propagating it to radar, questions, wayfinder and greenhouse and threading its tasks, with the usual confirmations. Holds every rule for processing a note. Records what's still owed in each note's `status:`, commits only what it touched, and ends by rebuilding `NEXT.md` so you can see what to do next. Set up per vault under `heartbeat:` in `_AI/shared/config.yml`. |
| **Minute** | A logistics or status change — "John moved the meeting to Wednesday" — that you want applied now. A shortcut: captures a log note, then runs heartbeat on just that note. |

Debrief vs. capture-log-note is a judgment call: first-hand material you want fully processed into wiki pages goes through debrief; a quick note-to-self goes through capture-log-note. `minute` captures through capture-log-note, then has heartbeat propagate the change across the tracking surfaces — which stops at the wiki, which stays debrief-only.

---

## Writing a piece

Every piece lives in the same `brief.md` / `guide/` / `output.md` / `assets/` folder (see `_AI/shared/snippets/piece-folder.md`). The brief itself is ad hoc — just ask for help drafting it in chat, no dedicated workflow owns that step.

Full docs — the lifecycle of a piece, a page per workflow, and the concepts they share — start at `_AI/docs/writing/README.md`.

| Workflow | Use when |
|---|---|
| **Sync-guide** | Build or update the piece's `guide/` folder from the brief and vault sources. Only ever touches `guide/` — never reads or writes `output.md`, never drafts prose. |
| **Interview** | The material for a part has to come from you — a reflection, an evaluation, what you learned. Builds a dated timeline from your logs, then interviews you one thread at a time, checks each answer against the record, and saves your answers verbatim as notes in `guide/`. Runs across sessions; never drafts prose, never touches `output.md`. |
| **Elicit** | Stuck on a section — want a burst of odd angles and questions to kick a sentence loose. Reads the section's theme notes in `guide/`, throws out ideas in chat (or into a `scribe` block), then stops. One pass, no back-and-forth, never touches `output.md`. |
| **Beats** | Know what a section must cover but not what order the writing should move in. Reads the section's theme notes (or a `scribe`-wrapped passage) and lays out an ordered beat sheet — each beat phrased as the *move* it makes, not just its topic — written as a framework block under the section heading for you to draft against and delete. One pass; never alters existing prose. |
| **Polish** | The text is already yours (typed or dictated) — clean up spelling/punctuation/structure only, never rephrase. Works on any file, not just `output.md` in a piece-folder — see `%P`/`%` markers in `polish.md`. |
| **Scribe** | Leave a `% scribe <instruction>` marker (or the short form `%s <instruction>`, at column 0) inline in any file — I carry out the instruction and write the response into a `% comments` block in place, without stripping the marker. Works on any file, not just `output.md` in a piece-folder. |
| **Sanity** | Check your own writing for contradictions or passages that don't hold together. Diagnostic only, never edits. |
| **Gap-check** | Compare a draft against its `guide/` (or any named reference) and report what's missing. Never edits target or reference content, but does record a coverage verdict on each checked theme, every run. No overall score — just a gap list. |
| **Diploma-ready** | Same read-only-target shape as gap-check, but checked against the fixed Diploma assessment rubric specifically, with a Yes/Nearly/Not Yet verdict — before showing a tutor. |

**You always write `output.md` yourself — `sync-guide` scaffolds and stays out of it.** **Calling `sync-guide` on a piece already in progress** only ever touches `guide/`, regardless of whether your draft so far came from typing, dictating + polish, or ideas sparked by `elicit` — it can't clash with any of them. When you want to know whether the draft actually covers the guide, that's a separate step: call `gap-check` explicitly.

`elicit` and `beats` both read a section's theme notes and stop, but do different jobs: `elicit` throws out angles and questions to spark a sentence; `beats` gives the section a spine — an ordered list of moves — before any sentence is drafted. `beats` writes a framework block into `output.md` under the heading; `elicit` never touches it. `interview` is a different kind of tool again: `elicit` is a single-shot brainstorm from notes that already exist, while `interview` is a multi-session elicitation that *produces* the notes — the other way of filling `guide/`, alongside `sync-guide`.

`polish` and `scribe` are unrelated to this pipeline — both are marker-driven and work on any vault file, whether or not a piece-folder is involved.

---

## Keeping track of things worth remembering

| Workflow | Use when |
|---|---|
| **Add to radar** | A situation worth watching — no action implied, just awareness. |
| **Greenhouse** | A concrete idea you like and want to do — deliberately not now. |
| **Wayfinder** | A project too woolly or too big to just start — unknown order, several open decisions, more than one session. Maps it into a destination plus small decisions (waypoints) you resolve one at a time. Distinct from radar (watch, no action), greenhouse (understood, parked), and post-mortem (already went wrong). |
| **Compass** | Is this idea, offer or commitment *towards* or *away* from my vocation? Checks it line by line against my compass (in the personal vault) and names which part of it is mine. Greenhouse and wayfinder run a one-line version automatically. |
| **Frontier** | See what's yours to do now across a folder's threads (wayfinder maps, work folders, tickets, and tasks in meeting notes), what owes a debrief, what's waiting on others, which watches have gone quiet, and what needs a look. Not a workflow: `python3 _AI/local/scripts/frontier.py <folder>` writes `<folder>/NEXT.md`, the one place to look for what to do next. `NEXT.md` is rebuilt at the end of `debrief`, `sweep-tasks` and `heartbeat` (for the folders listed under `frontier: folders:` in `_AI/shared/config.yml` inside the vault), or whenever you run the script. How notes are written for it: `_AI/local/FRONTIER.md`. |
| **Sweep tasks** | A meeting note left tasks with no thread. Proposes a thread link and plain-word fields (`Expected by:`, `Waiting on:`, `Blocked by:`, 📅) for each in one table, and writes only what you confirm. Heartbeat runs it as part of processing a note. |
| **Post-mortem** | Something went wrong; investigate why and propose a specific fix. (Greenhouse is one *possible outcome* of a post-mortem, not a substitute for it.) |

---

## Reviewing what's happened

| Workflow | Use when |
|---|---|
| **Reflect** | Review a scope of notes (last N days, since the last reflection, etc.) and surface patterns, momentum, surprises, and open loops as a chat response. Diagnostic by default — can capture as a reflection note or feed open loops into `add-to-radar` on request. |
| **Gratitude** | You want to write gratitude entries. Prompts come from your recent journal notes; each entry gets feedback and a light polish (never rephrased), and approved entries are appended to today's daily note, which is created from your daily template if it doesn't exist. |

---

## Auditing and maintaining the vault

| Workflow | Use when |
|---|---|
| **Lint** | Automated structural check — orphan pages, broken links, pending cautions — via script. |
| **Normalise** | Periodic sizing pass over a KB's `wiki/` — finds near-duplicate, over-broad, source-shaped, and full-prose pages and proposes merges, splits, or conversions. Propose-only. |
| **Process notes** | Convention-based: proposes folder moves and category fixes, applies on confirmation. |
| **Connect** | Cross-knowledge-base pass to surface new connections between KBs. |
| **State of play** | On-demand, full reconciliation sweep across a gig or project folder's radar and wayfinder waypoints — interrogates you on each, updates the underlying notes, then gives a plain-language digest in chat. |
| **Create summaries** | Pulls mentions from linking notes into a target note's `## Summary` section. |
| **Link components** | Wikilinks PRP decision notes to technical component pages (code-adjacent KBs only). |

---

## Understanding a codebase

| Workflow | Use when |
|---|---|
| **Trace** | You want to see how the running code actually behaves. Give it a log export from a local run; it writes a sequence diagram per user journey to `<gig>/repos/flows/`, with what each class decides and why, plus a system map of every endpoint seen. Pairs with the repo navigators (static, per class, generated by `code-wiki` into `<gig>/repos/<repo>/navigator/`) and `readback` (to test what you've taken in). |

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
