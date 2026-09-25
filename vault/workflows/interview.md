---
name: interview
description: Interview the writer one thread at a time, checking answers against the record, and save verbatim answers as gathered notes in a part's guide/.
---

# Interview

Triggered by: "interview `<part>`", "start an interview", "resume the interview". Not "interview me" — that's `grill-me`.

The *eliciting* gatherer. Where `sync-guide` extracts quotes from vault sources, this workflow draws material out of the writer: it asks questions one thread at a time, checks each answer against a dated timeline of the record, and saves the answers verbatim as gathered notes in the piece-folder's `guide/`. The notes follow the gathered-material contract in `_AI/shared/snippets/piece-folder.md`, so `beats`, `gap-check`, `elicit` and `guide.base` read them like any other guide notes.

The writer's own words are the material. This workflow asks, checks and records — it never drafts prose.

## Prerequisites

A piece-folder (a single piece, or one part of a multi-part piece — see `piece-folder.md`) with a `brief.md` that includes an `Outline`. If `brief.md` is missing, or has no `Outline`, say so and stop — the Outline is what gives each note its `section:`.

If `guide/INDEX.md` is missing, tell the owner to create it with the `guide.base` embed (the same file `sync-guide` creates — see "Building" in `sync-guide.md`), then continue. This workflow doesn't create it.

## Step 1: Timeline

The timeline is the record answers get checked against. It lives at `timeline.md` in the piece-folder, beside `brief.md` — not in `guide/`. It's evidence, not gathered material: no `section:`, and nothing reads it as a note.

**If `timeline.md` exists**, reuse it. When a thread turns up new evidence (a log or chat the timeline missed), add it as a new entry in date order.

**If it's missing**, build it from the sources named in the brief's `Draw from` — logs, curated notes, chats — mining for dated events in how the work actually went. Then show the owner the entries and take any corrections before the first thread.

Format:

```markdown
---
date: "[[YYYY-MM-DD]]"
tags:
  - ai-generated
---
# <Piece>: how it actually went

Timeline mined from <sources>, as evidence for the interview. Entries marked † come from `ai-generated` sources — Claude's past summaries, not the owner's words. Treat them as prompts, not evidence.

## <Phase heading>

- **2025-07-18** — gist of what happened, in a sentence or two. [[source note]]
- **2026-06-30†** — gist from an `ai-generated` log. [[source log]]
```

- Every entry has a **bold date** (a month or range is fine when that's all the record gives), a short gist, and a wikilink to its source.
- The file is tagged `ai-generated`: Claude compiled it.
- Mark an entry † when its source carries `ai-generated`. A † entry can prompt a question, but it can't contradict an answer on its own — go to what that source summarises before citing it in an evidence check.

## Step 2: Choose threads

A **thread** is one line of questioning that ends in one conclusion. Propose threads in chat, drawn from:

- the brief's `Outline`,
- the timeline (tensions, turning points, gaps between what was said and what happened),
- rubric prompts, if the brief points to a rubric (e.g. a `standards/` file with an elicitation-prompts heading).

Number each proposed thread, one line each: the question it chases and the `Outline` section it belongs to. The owner picks, reorders or drops them, and can name threads of their own. Numbers carry on from the highest already used in the notes and `triaged.md`, so a thread keeps its number for good. The proposals stay in chat — there's no stored thread list.

**On a resume**, work out state from the files before proposing anything:

1. **Open threads first.** List every thread note that's still open (see "Open or closed" below), and offer to carry on with one of them.
2. **Skip anything already logged.** A thread with a line in `triaged.md` has been closed or dropped — never propose it again as a new thread. A reopened thread still shows up under step 1, because its note says it's open.
3. **Fill empty sections.** Propose new threads only for `Outline` sections that have no notes yet.

One thread runs at a time.

## Step 3: Run a thread

### Create the note

Create the note in `guide/` when the thread starts. Filename: the thread number, two digits, then a short topic (`01 framework choice.md`).

```markdown
---
categories: "[[Themes]]"
guide: "[[full/path/to/piece-folder/guide/INDEX|alias]]"
section: <Outline heading text>
status: pending
coverage:
date: "[[YYYY-MM-DD]]"
thread: 1
topic: <the question this thread chases>
---
# <Short title>

<Owner>'s answers verbatim. Claude's questions and observations are marked as such; they are prompts, not <Owner>'s words.

## Evidence (Claude)

- **2026-04-18** — what the record shows that bears on this thread. [[source]]

## Q1 (Claude)

<question>

## A1 (<Owner>, YYYY-MM-DD)

<answer, verbatim>
```

- The first five fields are the contract; `date`, `thread` and `topic` are this workflow's own. `section` is the one `Outline` section the thread belongs to, in the same form `sync-guide` writes it.
- **No `ai-generated` tag.** The note is mostly the owner's verbatim words. Instead, every section Claude writes carries `(Claude)` in its heading: `Evidence`, `Q<n>`, `Evidence check`, `Observations raised`, and the conclusion. A Claude-authored section without that label is a provenance error.
- `## Evidence (Claude)` is optional: the timeline entries that bear on the thread, pulled up front when there are some.

### The loop

Ask one question at a time, write it to the note as `## Q<n> (Claude)`, and wait for the answer.

**Save the answer verbatim** as `## A<n> (<Owner>, YYYY-MM-DD)`. The only changes allowed: removing dictation that came through duplicated, and fixing punctuation. When either was done, say so in italics straight after the answer:

```markdown
*(Dictation duplicated; de-duplicated and lightly polished — punctuation only.)*
```

Once saved, an answer is never edited — not to fix a fact, not to tidy a phrase.

**Check the answer against the record.** After each answer, compare its factual claims (dates, who did what, what happened first) with the timeline and the sources behind it. Correct, don't teach: point at the specific dated entry or source line, never just "that's not right", and don't tell the owner what to conclude from it. When the record contradicts an answer, or is silent where the answer is confident, write an `## Evidence check (Claude)` section straight after the answer: what the record shows, each point with its date and source, and anything the record can't confirm said plainly as unconfirmed. The answer stands as given — a wrong memory is part of the record too. A follow-up question can put the evidence to the owner.

**Observations.** When an answer opens something worth following — a pattern, a tension, a link to another thread — note it under `## Observations raised (Claude)`. Mark speculation as speculation. Observations are prompts for the owner, not findings.

**Owner corrections.** When the owner revises an earlier answer, it goes in as a new answer — `## A<n> (<Owner>, YYYY-MM-DD) — correction to A<m>` — and the original stays untouched.

**Cross-section material.** A note belongs to one section. When an answer carries material for a different `Outline` section, propose lifting it: name the excerpt and the section it belongs to. On a yes, write a separate short note in `guide/` for that section — the contract frontmatter plus `date` and `topic` (no `thread`: it isn't a thread), and a body holding the copied verbatim excerpt with a link back to the thread note:

```markdown
## Excerpt from thread 3

> the owner's words, copied exactly as saved in A2

— <Owner>, YYYY-MM-DD, [[03 tools vs design]]
```

Copy the excerpt rather than just linking, so the note stands on its own in its section. Do it during the interview, while the context is fresh.

## Step 4: Close or drop

**Closing.** When a thread has run its course, say so and ask whether to close it. On a yes, write the conclusion under `## Where thread <N> lands (Claude)` — what the answers add up to, what's still open. Then append a line to `triaged.md` in the piece-folder:

```markdown
- 2026-09-23 · thread 1 · [[01 framework choice]] · closed
```

**Dropping.** When the owner drops a thread before it has a note, log it so a resume doesn't propose it again:

```markdown
- 2026-09-24 · thread 5 · learning through relationships · dropped
```

`triaged.md` gets **one line per thread, ever** — written once, when the thread is first closed or dropped, and never changed or repeated. It's append-only, and may also hold `sync-guide`'s lines for source files; read only the `thread` lines.

## Open or closed

Read from the note, never stored: a thread is **closed** if its latest `##` heading is its conclusion (`Where thread <N> lands (Claude)`, or the revised form below; a hand-worded conclusion — a heading starting `Where` and labelled `(Claude)` — counts too). If the latest heading is an answer — or anything else short of a conclusion — the thread is **open**.

## Reopening a thread

A closed thread reopens when the owner comes back to it — a new answer, a correction, a question they want to take further. Append the new Q&A below the existing conclusion, then close again with `## Where thread <N> lands — revised (Claude)`. The old conclusion stays where it is; the latest one wins.

- If the note is `status: used`, revert it to `pending` and tell the owner why: new material means the writer's earlier use of the note needs another look. That's the only change this workflow ever makes to `status`.
- No new `triaged.md` line — the thread is already logged.

## What this workflow doesn't do

- Never drafts prose, and never reads or writes `output.md`.
- Never tags thread notes `ai-generated`; labels Claude's sections instead.
- Never edits a saved answer, and never replaces an old conclusion.
- Never creates `guide/INDEX.md`.
- Never sets `status` to `used` or `rejected` (the writer's call), and never touches `coverage` (`gap-check`'s field).
- Doesn't call other workflows. It checks answers the way `readback` does and tidies dictation within `polish`'s limits, but those are its own steps, not handoffs.
