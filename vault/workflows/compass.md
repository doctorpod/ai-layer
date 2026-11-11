---
name: compass
description: Check an idea, opportunity or commitment against the owner's vocation compass — towards or away, and which part is theirs. Diagnostic only.
---

# Compass Workflow

Triggered by: "compass check this", "compass check", "check this against my compass", "towards or away?"

The compass is a short statement of the owner's vocational direction: a bearing, not a job title. This workflow tests one candidate (an idea, an offer, a project, a role) against it. It's diagnostic: it never edits the compass, or the thing it checks.

## The compass file

Its path is the `compass: file:` value in `_AI/shared/config.yml`. It lives in the owner's personal vault, and any vault may read it, read-only. The `## Compass` section is the version to check against; `## Pocket version` is a memory aid, not the test.

**Step 0, every time: find it.** Read `compass: file:` from `_AI/shared/config.yml`, then read that file, before anything else. Stop if:
- the config file or the `compass: file:` key is missing: tell the owner to set it, copying from `_AI/shared/config.example.yml`;
- the file it points to doesn't exist, or has no `## Compass` section: tell the owner the compass can't be found at that path and ask whether it has moved.

Don't carry on, don't work from a remembered or paraphrased version, and if another workflow called this one, don't let it carry on either until the owner has fixed the path or said to skip the check.

## Mode: Full check

Use on demand, or when the owner asks to expand a quick check.

1. **Pin down the candidate** in one sentence. If it's unclear what's being checked (an event, or a role within it?), ask one question.
2. **Gather context** from notes already in the vault about the candidate: log notes, debriefs, wiki pages. Don't search the web unless asked.
3. **Table.** One row per clause of the compass, scored against the candidate: ✓✓, ✓, ?, or ✗, each with a few words of evidence.
4. **Verdict:** strongly towards, towards, mixed, mostly away, or away. The tick count is a guide, not a formula.
5. **Which part is the owner's.** If the candidate splits into parts (doing it vs designing it; the admin vs the facilitating), name the part that points towards. This is often the most useful line.
6. **Flags:** at most two risks, taken from the owner's own record where possible (someone else's clock, alone in it too long, capacity).
7. **Ask whether the verdict matches their gut.** Their answer wins. If they push back on a row, change it.

Keep the output to the table plus a few lines.

## Mode: Quick check

Use when another workflow calls this one (`greenhouse` capture, `wayfinder` chart).

1. Step 0 as above.
2. Give one line: the verdict and the single strongest reason, plus a flag if there is one. For example: *Compass: towards. "Solve it, share it" fits. Flag: it would be a third project.*
3. Offer the full check; don't run it unprompted.

A quick check is information, not a gate. Apart from a missing compass file, it never stops the calling workflow.
