# Vault Workflows — by scenario

A human-facing guide, grouped by what you're trying to do rather than by trigger phrase. For the machine-readable trigger table Claude actually routes on, see `AI.md`. **If you add, rename, or remove a workflow, update both files.**

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

These chain — draft, then clean, then check, roughly in this order:

| Workflow | Use when |
|---|---|
| **Write** | General-purpose: brief → guide → output, the four-file pattern. |
| **Compose** | Same territory, but I draft the prose *in your voice* and you approve section-by-section. |
| **Polish** | The text is already yours — clean up spelling/punctuation/structure only, never rephrase. |
| **Sanity** | Check your own writing for contradictions or passages that don't hold together. Diagnostic only, never edits. |
| **Diploma-ready** | Same diagnostic shape as sanity, but checked against the Diploma assessment rubric specifically, before showing a tutor. |

---

## Keeping track of things worth remembering

| Workflow | Use when |
|---|---|
| **Add to radar** | A situation worth watching — no action implied, just awareness. |
| **Greenhouse** | A concrete idea you like and want to do — deliberately not now. |
| **Post-mortem** | Something went wrong; investigate why and propose a specific fix. (Greenhouse is one *possible outcome* of a post-mortem, not a substitute for it.) |

---

## Auditing and maintaining the vault

| Workflow | Use when |
|---|---|
| **Lint** | Automated structural check — orphan pages, broken links, pending cautions — via script. |
| **Process notes** | Convention-based: proposes folder moves and category fixes, applies on confirmation. |
| **Connect** | Cross-knowledge-base pass to surface new connections between KBs. |
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
