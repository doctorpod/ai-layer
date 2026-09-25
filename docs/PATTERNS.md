---
name: PATTERNS
description: Reusable shapes for designing workflows — design-time reference, not walked at runtime.
---

# Workflow Patterns

Shapes that have held up across more than one workflow in this layer, written down so the next workflow can reuse them rather than rediscover them.

This sits beside [[PRINCIPLES]]. The principles say what a workflow must never do; the patterns say what tends to work. A workflow can ignore a pattern without transgressing — if it breaks a principle, it's wrong.

Each entry gives the **shape**, **why it works**, its **concrete forms** (the files and fields it shows up as), and **where it's used** in the layer.

---

## 1. Rubric

**Shape** — One file defines what "good" looks like. Everything that checks the work and everything that builds it reads the same file, through stable named headings.

**Why it works** — There's one place to change the standard, and checkers and builders can't drift apart because they're reading the same words. Stable headings let a workflow find the part it needs without parsing the whole file, and let it check its own reading: if a heading it expects is missing, it stops and says so rather than guessing.

**Concrete forms**
- A rubric file in the vault's `standards/` folder, hand-owned, with headings that workflows address by name.
- A piece's `brief.md` must-haves and must-nots — a small rubric for one piece.

**Where it's used** — `diploma-ready` walks a `standards/` rubric; `gap-check` checks a draft against a named reference, so any rubric can stand in as that reference; builders can draw questions from a rubric's prompt headings (see `interview`).

---

## 2. Gatherer

**Shape** — Any stage that collects material so writing can happen. A gatherer is defined by its **output contract** — notes of a known shape in a known place — not by how it gathers. Consumers depend only on the contract, never on which gatherer ran.

**Why it works** — New ways of gathering can be added without touching anything downstream. The consumers stay simple because they read one shape; the gatherers stay free to work however their material demands (extracting from sources, eliciting from the writer). Anyone building a new gatherer only needs to meet the contract.

**Concrete forms**
- A piece-folder's `guide/`: one folder name for gathered material, whatever produced it. The contract is five frontmatter fields (`categories`, `guide`, `section`, `status`, `coverage`); the body and any extra fields belong to the gatherer. Full contract in `_AI/shared/snippets/piece-folder.md`.
- The brief's `Draw from` field says where material comes from and, in words for people to read, how it's gathered. No tool dispatches on it.

**Where it's used** — Two gatherers: `sync-guide` (extracts quotes from vault sources) and `interview` (elicits verbatim answers from the writer). Consumers: `beats`, `gap-check`, `elicit`, and the `guide.base` view.

---

## 3. Log inputs, derive the rest

**Shape** — Store only finished events that would otherwise leave no trace, in an append-only log. Work out current state from the files themselves each time.

**Why it works** — A finished event can't go out of date, so the log never needs correcting. Current state read from the files is always right, even after a hand edit. What the log saves is the one thing the files can't show: an input that was considered and dropped leaves nothing behind, so without the log it would be proposed again.

**Concrete forms**
- `triaged.md` in a piece-folder: one line per input, written once when it's finished with (a source file triaged, a thread closed or dropped).
- Open state read from the notes: an `interview` thread is open if its note's latest heading is an answer rather than a conclusion. No stored thread list.
- **Known exception: `coverage`.** `gap-check` stores its verdict on each note rather than deriving it, because rerunning the check just to fill a view costs too much. It can go stale when the draft changes; rerunning `gap-check` refreshes it.

**Where it's used** — `sync-guide` and `interview` both keep `triaged.md`, each with its own line format; `interview` derives open threads from its notes.

---

## 4. Toolbox, not pipeline

**Shape** — When the order of work is a judgement call, build independent tools that never call each other and are linked only by plain files. When the order is fixed and part of the method, a pipeline is right.

**Why it works** — The writer picks the next tool based on what the work needs, not on what the sequence says comes next. Each tool stays small and can be added, changed or dropped without the others knowing. A tool can still follow another's rules internally (`interview` checks answers the way `readback` does) without calling it.

**Concrete forms**
- The files that link the tools: the brief, the gathered material in `guide/` (see Gatherer above), and `triaged.md`.
- **The boundary.** Writing and thinking are a toolbox: `beats`, `polish`, `sanity`, `scribe` and `gap-check` can be used in any order. Delivering code is a pipeline on purpose: `create-prp` → `execute-prp` → `review`, because each stage's output is the next stage's required input.
- **The caveat.** Because the order lives with the writer, a fresh session doesn't know "what's next" for the whole piece. Log inputs, derive the rest answers this for a single gatherer (open threads, triaged files), not for the piece as a whole.

**Where it's used** — The vault's writing workflows. A new gatherer (`interview`) was added without `beats` or `gap-check` changing, because the contract in `guide/` is the only link between them.
