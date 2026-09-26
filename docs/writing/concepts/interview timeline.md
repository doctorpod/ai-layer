---
tags: [ai-layer-docs]
sources:
  - shared/snippets/piece-folder.md
  - vault/workflows/interview.md
checked: 2026-09-26
---

# interview timeline

*The `timeline.md` file in a [[piece folder]]: dated evidence from the record that [[interview workflow|interview]] checks your answers against.*

It lives beside `brief.md`, **not** in `guide/`. It's evidence, not material to write from: it has no `section:`, and no workflow reads it as a [[gathered note]].

## How it's built

On the first interview run, if there's no `timeline.md`, the assistant mines the sources named in the brief's `Draw from` (logs, curated notes, chats) for dated events in how the work actually went. It then shows you the entries and takes your corrections before the first [[interview thread|thread]] starts. Later, when a thread turns up evidence the timeline missed, it's added in date order.

The file is tagged `ai-generated`, because the assistant compiled it.

## Entry format

```markdown
## Survey

- **2026-01-22** — first note of standing water by the north gate, in passing. [[2026-01-22 log]]
- **2026-03-14** — site walk with Maggie; wet corner recorded as flooding Nov–Mar. [[debrief-2026-03-14-site-walk]]
- **2026-04-02†** — summary of the soil test results. [[2026-04-02 log]]
```

- Every entry has a **bold date** (a month or a range is fine), a short gist and a link to its source.
- **† marks an entry whose source is itself `ai-generated`**: the assistant's past summary rather than your own words. A † entry can prompt a question, but it can't contradict one of your answers on its own. The assistant has to go to the underlying source first.

## Related

- [[interview workflow]]
- [[interview thread]]
