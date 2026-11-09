# Frontier convention (all vaults)

How a vault records its live work so `scripts/frontier.py` can list what's yours to do now, with no per-vault config. This doc is for whatever writes the notes: workflows, and the owner typing by hand. How the list is laid out and sorted is the script's business, documented in its docstring.

The script writes the list to `<folder>/NEXT.md`. Anything it can't read is never dropped silently: it goes under "Needs a look".

## Words

- **Thread**: one line of work with its own history: a wayfinder, a work folder, a ticket with no work folder, or a project.
- **Step**: one thing to do next inside a thread: an Open waypoint, the next line of a checklist, a project checkbox, or a task.
- **Task**: a `- [ ]` or `- [/]` line in an ordinary note (a meeting note, a stand-up, a log note). A task that links to a thread joins that thread.
- **Dangling task**: a task with no thread link. Dangling tasks are listed together, after the threads.
- **Checklist**: the checkboxes in a ticket, plan or slice, read in order as a series of reminders. A checklist adds one step at a time: its first unticked line.

## Where the script looks

Every `.md` file in the folder the list covers, except `templates/`, `_AI/` and `.obsidian/` folders, notes with `ignore_tasks: true` in frontmatter, and notes whose `status:` means parked or done (their tasks are out of play). Checkboxes inside fenced code blocks are ignored.

## Status

Thread and ticket notes use `status:` with either vault words or words copied from Jira. Both are fine. Matching ignores case.

| Means | Words |
|---|---|
| live | active, to do, in progress, ready, open |
| waiting | waiting, needs review, in review, blocked |
| parked | inactive, backlog, parked, paused |
| done | done, closed, resolved |

Any other word goes under "Needs a look". A note with no `status:` counts as live.

Jira's "Blocked" means waiting, because in Jira it means held up by someone else.

## Threads

### Wayfinder

- **Found at:** `**/_wayfinder/<slug>/map.md`.
- **Steps:** each waypoint under **Open** is a step (map format in `workflows/wayfinder.md`). Blocked, Parked and Resolved waypoints aren't on the list; a waypoint's section says what it is.
- **Due:** `Due: YYYY-MM-DD` on the line.
- **Started:** the wayfinder workflow adds `Started YYYY-MM-DD` to an Open waypoint's line when work on it begins.

### Work folder

- **Found at:** every folder directly under `delivery/work/`, with or without `slices/`. The thread is named by the folder (`CVT-344`).
- **Status:** from its ticket, linked by `ticket:` in the folder's `init.md` or `plan.md`; with no `ticket:` there, the ticket whose name or alias is the folder's name. No ticket means live. If the ticket is parked or done, the whole folder is out.
- **Steps:** from the checklists of the ticket, the plan and the slices (see **Checklists**). A slice in `planned` whose `depends-on` slices aren't all merged is blocked and isn't on the list.
- **Internal notes:** every other note inside the folder (`init.md`, `QUESTIONS.md`, `DECISIONS.md` and the rest) is internal. Its checkboxes are never tasks.

Slice `state:` is one of `planned`, `in progress`, `PR open`, `merged`. Any other value goes under "Needs a look".

### Ticket with no work folder

A note with `categories:` including `[[Tickets]]`, no work folder, and at least one checkbox. A ticket with no checkboxes is a reference copy and isn't a thread. Its steps come from its checklist.

### Project

A note with `categories:` including `[[Projects]]`. Every open checkbox is its own step; a project isn't a checklist.

### Waiting threads

A ticket, work folder or project whose status means waiting shows one line under "Waiting on others", using its `latest:`, instead of its steps. Put what it's waiting on in `latest:`.

A live thread with no open step goes under "Needs a look". Record the next step rather than leaving the thread empty.

## Checklists

- The checkboxes in a ticket, a plan and a slice are read in order. Only the first unticked line (`[ ]` or `[/]`) is a step. Write checklists in the order the lines get done.
- In a work folder the checklists take turns: before any slice exists, the ticket's next line; while any slice is open, each open slice's next line; once every slice is merged, the ticket's next line and the plan's next line.
- A next line containing `PR review OK`, `QA` or `Merged` (as written, with that case) means waiting on someone else.
- Tick a line with `✅ YYYY-MM-DD`. The last ✅ date in a checklist is when it was last touched.

## Tasks in ordinary notes

Tasks stay in the note where they were written, usually a meeting or stand-up note. Every open task is on the list. Facts about a task are plain words, a colon and a link, appended after the task's own words:

```
- [ ] Prod MG for meeting [[cdp data ingest]] Expected by: [[Michael Greenall]] 📅 2026-11-09
```

| Part | Meaning |
|---|---|
| link to a thread note | the thread the task joins: a wayfinder map (by alias), a ticket (by alias, such as `[[CVT-344]]`, joining its work folder) or a project. No thread link makes it a dangling task. |
| `Expected by: [[person]]` | someone is expecting this from the owner, whether they asked or the owner offered. Only a link counts: "expected by Friday" is ordinary text. |
| `Waiting on: [[person]]` | the task waits on someone else, so it goes under "Waiting on others". |
| `Blocked by: [[note]]` | off the list while that note's `status:` means live, waiting or parked; back once it means done. A linked note with no `status:`, or one that doesn't exist, goes under "Needs a look". Only notes can block a task. |
| 📅 date | due by this date. |

`- [/]` is started, `- [x]` with a ✅ date is done, and `- [-]` (dropped) is ignored. The Tasks plugin's own fields (⛔, 🆔, ⏫ and the rest) aren't read.

A task's date is its note's date: frontmatter `date:`, or a date in the filename.

## Fields any thread can carry

| Field | Where | Meaning |
|---|---|---|
| `latest:` | thread and ticket frontmatter | one line on what's happening; shown for a waiting thread |
| `due:` | thread and ticket frontmatter | every step in the thread is due by this date |
| `priority: high` | thread and ticket frontmatter | marks the thread on the list; doesn't change the order |
