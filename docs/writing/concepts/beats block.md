---
tags: [ai-layer-docs]
sources:
  - vault/workflows/beats.md
checked: 2026-09-26
---

# beats block

*A **Beats** block that [[beats workflow|beats]] writes under a section heading in the [[output draft]]: an ordered list of the moves the section makes, for you to draft against and then delete.*

A **beat** is one move the section makes (set up, refine, complicate, pivot, illustrate, pay off, connect), not a topic.

## Format

```
**Beats** — section 02 Observation (framework; delete once written)

1. [ ] **Set up: the site looks dry** — sloping, well-drained turf across most of the plot; only the hedge's shade limits the south bed.  ← site observation, [[South bed shaded by the neighbour's hedge until noon]]
2. [ ] **Complicate: except the north gate** — standing water November to March.  ← [[Wet corner by the north gate floods every winter]]
3. [ ] **Pivot: water as a resource** — the one reliable water on site; hands on to the design section.  *(connective — no note covers this)*

Not beats: [[Heavy clay under the wet corner]] — a detail inside beat 2.
```

- `1. [ ]`: a numbered checkbox, so you can tick beats off as you write them. Keep the numbers too, because beats refer to each other by number.
- **Bold**: what the beat does, as a function plus a short label. Plain text after the dash is the gist.
- `←`: the [[gathered note|gathered notes]] it draws on, plus any non-note source in plain text ("site observation", "brief").
- `*( … )*`: notes to you, such as a connective beat no note covers, a sequencing risk, or a call you need to make.
- **Not beats:** every note that was merged away, demoted to a detail, or cut, each with a clause saying where it went.

Every non-rejected note in scope appears exactly once, either in a beat or on the Not beats line. Nothing is dropped silently.

## Rules

- **One per section.** Rerunning beats on a section replaces its existing block.
- It's written only under an existing heading in an existing `output.md`. If either is missing, the block is shown in chat instead.
- It never touches the prose around it.
- **Inside a [[scribe marker]]** the same block goes into `% **comments**`, without the checkboxes, because a comments block is deleted as a whole rather than worked through.

## Related

- [[beats workflow]]
- [[output draft]]
