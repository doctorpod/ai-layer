---
name: trace
description: Turn an exported app log into dynamics notes for a gig's codebase, with a sequence diagram per user journey plus what each class decides and why.
---

# Trace

Triggered by: "trace", "trace this journey", "trace these logs", "draw the flows from these logs"

## Outcome

One note per user journey showing how the running system behaves: who calls whom, in what order, what each class decides, and why. Its reader is the owner, rebuilding a mental model of the code well enough to answer "why does X do this instead of that?" in a review. Plus one system map per gig: every endpoint seen, on one page.

## Inputs

- **A log export.** Run `python3 _AI/local/scripts/trace-logs.py` on it: `summary` for the system map, `list` to find each journey's requests, `trace --from <time>` for the cleaned, interleaved lines. Never parse a raw export by hand. If the script rejects the format, stop and say so.
- **The repos**, found through the gig's `RELATED.md`. Read code only to fill branches the logs didn't exercise, and for the Decides layer. Note which branch each repo is on.
- **Sources for the Why layer:** the gig's `DECISIONS.md` and PRP files, PR write-ups, `wiki/` pages, and class doc comments (the navigator notes show these).

Ask which journeys to trace if the owner hasn't said. Suggest the ones `list` shows the most of.

## Output contract

- **Location:** `<gig>/repos/flows/`. One `<journey-slug>.md` per journey, plus `system-map.md`, which is updated in place, never duplicated.
- **Frontmatter:** `date`, `logs:` (the export file and the time window traced), `branches:` (each repo and the branch read), `tags: [ai-generated]`.
- **Body, in order:**
  1. Diagram: Mermaid `sequenceDiagram`, one per journey step that crosses a service boundary. Use `box` to group the services. Use `alt` for branches the code shows but the trace didn't take, and say which one the trace took.
  2. **Decides**: a table of Class | Decides | Based on. Every class is a wikilink to its navigator note: the per-class reference that `code-wiki` generates into `<gig>/repos/<repo>/navigator/`. Path-qualify the link where the same name exists in both repos. If a repo has no `navigator/` folder, use plain class names and suggest running `code-wiki`.
  3. **Why**: bullets. Each one cites a vault note or doc comment, or is marked as an open question.
  4. **Open questions**: whatever the code does that nobody has written a reason for.
- **System map:** a Mermaid `flowchart LR` of services, databases and external systems, with edges labelled by endpoint and call count from `summary`. A journey state diagram (`stateDiagram-v2`), where the code defines step transitions, also goes here.

## Must-nots

- Never present inferred rationale as recorded. If no source gives the reason, it goes under Open questions, or it is labelled *inferred from the code*.
- Never draw behaviour from a branch the logs didn't run without a `[!warning]` callout saying what differs and why.
- No partials, layouts, cached queries or auth boilerplate in diagrams. If a diagram needs scrolling, split it.
- No edits to the navigator, the repos, or the decision notes. This workflow only reads them.

## Known gotchas

- Mermaid `stateDiagram-v2`: a transition label can't contain a second colon (`:ocid` breaks it) or `<br/>`. Write `OCID` and use commas instead.
- Sequence and state diagram participants can't hold links. Links live in the Decides table.
- FE and BE lines are matched by timestamp, not request id. That's fine for one local user but unreliable under load. Say so if the log came from a shared environment.
- Local logs usually contain no external API calls (e.g. CDP) or background jobs. Name that gap in the system map rather than leaving it silent.
- A 200 where `list` shows other requests getting a 302 on the same step usually means a validation failure that re-rendered the form. It's worth a line in the note, not a diagram.

## Done when

- Every diagram renders in Obsidian. Open the note to check.
- Every Decides row is grounded in code, and every Why either cites a source or is an open question.
- Then offer `readback` on one scenario from a new note, so the owner can test what they've taken in rather than just recognising it.
