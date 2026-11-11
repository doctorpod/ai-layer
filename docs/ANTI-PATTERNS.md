---
name: ANTI-PATTERNS
description: Shapes that have failed in this layer, with how to spot them and the fix. Design-time reference, not walked at runtime.
---

# Workflow Anti-Patterns

Shapes that have gone wrong in this layer, written down so the next workflow doesn't repeat them.

This sits beside [[PRINCIPLES]] and [[PATTERNS]]. The principles say what a workflow must never do; the patterns say what tends to work; this file says what tends to fail. An anti-pattern isn't automatically a transgression, but finding one in a design is a reason to stop and fix it before it ships. Checked at design time (via AI.md) and fed by `post-mortem`.

Each entry gives the **shape**, **why it fails**, **how to spot it**, **the fix**, and **where it's happened** in the layer.

---

## 1. Dead-end state (aka roach motel)

**Shape** — A process writes something, and nothing ever acts on it or moves it on. Things check in, but they don't check out. It takes two forms, often together:
- **No reader.** A file, log, field, tag or status is written, but no workflow, script or named human moment reads it and acts on it.
- **No exit.** An item is put into a pending state, and nothing moves it out when the pending thing is done.

**Why it fails** — Nothing breaks, so nothing complains. The item looks handled because it has a status, which is worse than having none: it hides that the work is still owed. Pending states pile up, any list built from them fills with stale entries, and the owner learns to ignore that list.

**How to spot it** — For every state, field, file or tag a design writes, ask two questions:
1. Who reads this, and what do they do with it? Name the workflow, script, or the human and when they look.
2. If it means "still owed", what moves it on, and who writes the next state?

If either answer is "nothing" or "someone will notice", it's a dead end. A state may be terminal only if it's meant to be the end, like `done`.

**The fix** — Whoever defines the state names its reader and its exit, in the same place it's defined. Wire both in the same change that adds the state. Writing for a human is fine when the human reader is named, such as the journal read at stand-up.

**Where it's happened**
- `status: needs-debrief` (2026-11): `minute` and `heartbeat` set it and heartbeat lists it, but `debrief` only looks in `inbox/` and never sets it back. Notes parked there would be listed forever. Fix pending: debrief also offers `needs-debrief` notes, and sets `done` when it finishes.

---

## 2. Stored derived state

**Shape** — A value that could be worked out from other files is stored instead, and then the files it came from change. The stored copy is now wrong, and nothing says so. It's a cache with no invalidation.

**Why it fails** — The failure is silent: a stale copy looks exactly like a fresh one, so it keeps being trusted. Every edit to the source is a chance for the copy to drift, and keeping it true depends on someone remembering to update it.

**How to spot it** — For every stored summary, verdict, count, or "latest" field, ask: could this be computed from the files at read time? If so, what refreshes it when the source changes, and how would anyone tell it's stale?

**The fix** — Derive at read time where you can (see [[PATTERNS]] #3, "Log inputs, derive the rest"). Where that costs too much, store what the value was derived from alongside it (a date, a commit, a hash), so staleness can be detected, and name the refresh. `heartbeat` does this: it uses git to notice a note "edited since last swept", so its stored `status:` can't silently go stale.

**Where it's happened**
- `coverage`: `gap-check` stores its verdict on each guide note because rerunning the check just to fill a view costs too much. It goes stale when the draft changes; rerunning `gap-check` refreshes it.
- `DASHBOARD.md` copies state from radar, wayfinder and projects. Its refresh is named (`state-of-play`), but it's stale between runs.
- Radar `latest:` repeats the newest Context entry, and wiki `INDEX.md` lines summarise their pages. Both drift unless whatever edits the source updates them too.
