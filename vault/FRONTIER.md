# Frontier convention (all vaults)

How a vault records its live work so the frontier script can read it with no per-vault config. This doc is for whatever writes the notes: workflows, and the owner typing by hand. How the page draws what it reads is the script's business and is documented there.

Anything that doesn't follow these rules isn't silently dropped. The page lists it under "Needs a look".

## Words

- **Thread**: one line of work with its own history. One of: wayfinder, work folder, project. Asks with no thread share a pseudo-thread, **loose ends**.
- **Step**: one unit inside a thread: a waypoint, a slice, a project checkbox, or an ask.
- **Tip**: a step that isn't done. Its state is one of `started`, `could` (could start), `waiting` (on someone else), `blocked` (on another step), `parked`.
- **History**: steps that are done.

## Where the script looks

Every `.md` file in the vault except `templates/`, `_AI/`, `.obsidian/`, and notes with `ignore_tasks: true` in frontmatter.

## Status

Thread and ticket notes use `status:` with either vault words or words copied from Jira. Both are fine. Matching ignores case.

| Means | Words |
|---|---|
| live | active, to do, in progress, ready, open |
| waiting | waiting, needs review, in review, blocked |
| parked | inactive, backlog, parked, paused |
| done | done, closed, resolved |

Any other word shows as "status unknown, check it". A note with no `status:` counts as live.

Jira's "Blocked" means waiting, because in Jira it means held up by someone else. A step blocked by another step is shown by its own dependencies, not by status.

## Threads

### Wayfinder

- **Found at:** `**/_wayfinder/<slug>/map.md`. Live when `status:` means live.
- **Id:** the folder slug. **Title:** the first alias.
- **Steps:** waypoint lines, by section (map format in `workflows/wayfinder.md`):

| Section | State |
|---|---|
| Open (the frontier) | `started` if the line has `Started YYYY-MM-DD`, else `could` |
| Blocked | `blocked` (`Blocked by:` names the blocker) |
| Parked | `parked` |
| Resolved | history, dated by the last `YYYY-MM-DD` on the line |

- **Started:** the wayfinder workflow adds `Started YYYY-MM-DD` to an Open waypoint's line when work on it begins.
- **Mine or hand-off:** `HITL` (including `HITL + AFK`) is mine, `AFK` alone is hand-off.
- **Due:** `Due: YYYY-MM-DD` on the line.
- **Last touched:** the latest `YYYY-MM-DD` on the line, else the map's `updated:`.

### Work folder

- **Found at:** any folder holding a `slices/` folder of slice notes (frontmatter has `state:` and `depends-on:`). The thread id is the folder name (`CVT-344`).
- **Ticket:** `ticket:` in the folder's `init.md` or `plan.md`, or in a slice. The ticket note gives the thread its `status:`, `latest:`, `due:` and `priority:`.
- **Live** when any slice isn't merged, or the ticket's status means live or waiting.
- **Steps:** one per slice. Step id is the slice's number prefix (`02`).

| Slice `state:` | State |
|---|---|
| planned | `could` if every `depends-on` slice is merged, else `blocked` |
| in progress | `started` |
| PR open | `waiting`, unless the first unticked checklist line is the owner's move, then `started` |
| merged | history |

- **Whose move:** in a `PR open` slice, a first unticked line containing `PR review OK`, `QA` or `Merged` means waiting on someone else. Any other line (such as `Code review sought`) means it's still the owner's move.
- **Last touched:** the latest ✅ date on a ticked checklist line, else the file's last git commit.
- **A work folder with no slices** isn't a thread. It's listed under "Needs a look".

### Project

- **Found at:** notes with `categories:` including `[[Projects]]`. Live when `status:` means live or waiting.
- **Steps:** the project note's own checkboxes, read as tasks (see **Asks** for task states).

### Tickets and radar

A ticket isn't a thread on its own; it feeds its work folder. A ticket with open checkboxes and no work folder is read like a project.

Radar items aren't threads.

## Asks (tasks in any note)

Tasks stay in the note where they were written, usually a meeting or stand-up note. The tagging sweep adds the tags after the meeting, so they don't need typing at the time.

```
- [ ] Prod MG for meeting [[cdp data ingest]] [[Michael Greenall]] #asked #swept 📅 2026-11-09
```

| Part | Meaning |
|---|---|
| link to a thread note | the thread the ask joins: a wayfinder map (by alias), a ticket (by alias, such as `[[CVT-344]]`, joining its work folder) or a project. No thread link means it's a loose end. |
| `#asked` | someone asked for it or it was promised, so someone is waiting on the owner. |
| person link | on an `#asked` line, any link that isn't a thread link is the person who asked, whether or not they have a note. Elsewhere, links to people are just mentions. |
| `#handoff` | could be delegated. Without it, the ask is the owner's. |
| 📅 date | urgent, by this date. Added only for something urgent. |
| ⏫ | flagged: "don't lose this". Not urgency. |
| `#swept` | the tagging sweep has reviewed this task. An open task without it counts as untagged. |
| 🆔 / ⛔ | Tasks plugin id and dependency, used only when one task really depends on another. A task with ⛔ pointing at an open task is `blocked`. |

**Task states:** `- [ ]` is `could`, `- [/]` is `started`, `- [x]` with a ✅ date is history, `- [-]` (cancelled, for a task that's no longer live) is ignored.

**Step id:** short note name plus position among the note's open tasks, such as `SU 11-06 #1`.

**Last touched:** the note's date (frontmatter `date:`, or a date in the filename), unless the line has a later date.

## Fields any thread or step can carry

| Field | Where | Meaning |
|---|---|---|
| `latest:` | thread and ticket frontmatter | one line on what's happening; often the reason for a wait ("Awaiting QA") |
| `due:` / `Due:` / 📅 | frontmatter / waypoint line / task line | urgent, by this date |
| `priority: high` / ⏫ | frontmatter / task line | flagged |

There's no field for who a step is waiting on. Waiting is a state, and the reason goes in `latest:` or the linked note.
