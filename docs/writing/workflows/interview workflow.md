---
tags: [ai-layer-docs]
sources:
  - vault/workflows/interview.md
  - shared/snippets/piece-folder.md
checked: 2026-09-26
---

# interview workflow

*Interviews you one thread at a time, checks each answer against the record, and saves your answers word for word as [[gathered note|gathered notes]].*

## When to reach for it

- The material for a part has to come from you: a reflection, an evaluation, what you learned, why you chose what you did.
- You want your own account checked against what your logs show actually happened, without being told what to conclude.

This is the *eliciting* [[gatherer]]. If the material is already in your knowledge bases, use [[sync-guide workflow|sync-guide]].

## How to invoke

`/interview`, or say "interview `<part>`", "start an interview" or "resume the interview". "Interview me" is a different workflow (grill-me).

## What it reads

- The [[piece brief]], which must have an `Outline`, and the sources named in its `Draw from`.
- The [[interview timeline]], if it exists.
- Existing thread notes in `guide/` and its own lines in the [[triage log]], to work out where you left off.
- A rubric's elicitation prompts, when the brief points to an [[assessment rubric]].

## What it writes

- The [[interview timeline]] (`timeline.md`), built on the first run and added to later.
- One note per [[interview thread|thread]] in `guide/`, plus short excerpt notes when you agree to lift material into another section.
- Its own lines in the [[triage log]], one per closed or dropped thread.
- One `status` change: `used` back to `pending`, when you reopen a thread whose note you've already used. It tells you when it does this.

## What it never touches

- The [[output draft]]. It never drafts prose.
- A saved answer. Corrections go in as new answers.
- An old conclusion. Reopened threads get a revised conclusion below it.
- `guide/INDEX.md`. If it's missing, it asks you to create it.
- `status` otherwise, and `coverage`.
- Other workflows. It checks answers the way readback does and tidies dictation within polish's limits, but it doesn't call either.

## How it works

1. **Timeline.** It reuses `timeline.md`, or builds one from `Draw from` and shows it to you for corrections first.
2. **Choose threads.** It proposes numbered threads in chat, each one question tied to one `Outline` section. The ideas come from the outline, from tensions or gaps in the timeline, and from rubric prompts. You pick, reorder, drop or add. On a resume it offers open threads first, never re-proposes a logged one, and only suggests new threads for sections with no notes yet.
3. **Run a thread**, one at a time. It asks one question and waits. It saves your answer verbatim, then checks the facts in it against the timeline. When the record disagrees, or is silent where you were confident, it adds an **Evidence check** with dates and sources. It points at the record and doesn't tell you what to conclude. Your answer stands as given.
4. **Close or drop.** When a thread has run its course, it asks whether to close it, writes the conclusion, and logs the thread.

It runs across as many sessions as you need.

## Worked example

The Hollin Lane reflection part (`parts/reflection/`) has an Outline of `01 Choosing a framework` and `02 What I'd do differently`, and `Draw from` names your Hollin Lane logs. You say "interview reflection".

There's no timeline, so it builds one, including a 22 January log that mentions standing water by the north gate. You correct one date. It proposes three threads, and you take 1 and 2 and drop 3 ("working with volunteers"). That drop is logged, so thread 3 never comes back.

Thread 1, `01 choosing the framework`, asks why you picked GOBRADIMET over the Design Web. After three answers you agree to close it. It writes `Where thread 1 lands (Claude)` and logs the thread.

In thread 2, `02 the wet corner surprise`, you say you first noticed the wet corner on the March site walk. It adds an Evidence check pointing to the 22 January log entry. Your answer stays exactly as you said it. You stop for the day with thread 2 open. Next session, "resume the interview" offers thread 2 first.

## Compared with…

- **[[sync-guide workflow|sync-guide]]**: the other gatherer, which extracts quotes from vault sources. Use interview when the source is you.
- **[[elicit workflow|elicit]]**: a one-shot brainstorm from notes that already exist. interview runs over several sessions and *produces* the notes.
- **grill-me** ("interview me"): records design decisions for a plan, and has nothing to do with a piece's `guide/`.

## Related

- [[interview thread]] · [[interview timeline]] · [[triage log]] · [[gathered note]]
- Workflow file: `_AI/local/workflows/interview.md`
