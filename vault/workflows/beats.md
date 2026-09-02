---
name: beats
description: Read a set of guide theme notes and lay out a beat sheet — an ordered list of moves the section makes — for the user to draft prose against.
---

# Beats Workflow

Triggered by: "beats", "beats section `<N>`", "beat sheet for `<section>`" — standalone in chat/CLI, or invoked by name from inside a `% scribe` marker (`_AI/local/workflows/scribe.md`), same as `polish` and `elicit`.

A **beat** is one discrete move in the section — set up, refine, complicate, pivot, illustrate, pay off, or connect. Not a topic; a function. This workflow turns a pile of guide notes into an ordered sequence of those moves, so the writing has a spine before a single sentence is drafted. Unlike `elicit` (angles to spark a sentence) and `gap-check` (coverage report), beats produces structure.

## Prerequisites

Piece-folder convention (`_AI/shared/snippets/piece-folder.md`): `brief.md`, `guide/`, `output.md`. If `brief.md` doesn't exist yet, that's an ad hoc conversation. If `brief.md` exists but `guide/` doesn't, point to `_AI/local/workflows/sync-guide.md` to build it first.

## Scope

Two ways in:

- **Whole section, from the guide notes** — standalone. Read every theme note (not `INDEX.md`) whose `section:` frontmatter matches the named section (skip any `status: rejected`, as `gap-check` does). Or, if the user names specific theme notes, use just those.
- **Part of a section, from draft material** — invoked from a `% scribe` marker wrapping rough draft prose, pasted note-stubs, or a half-assembled passage. The wrapped body defines the part. Work the beats for *that material*, pulling in the section's guide notes as supporting context.

## Doing the work

1. Read everything in scope — each theme note's Quotes and Synthesis together are the unit; plus the wrapped body, if invoked from scribe.
2. Decide the beats. This is the work, and it is not one-note-one-beat:
   - **Merge** — several notes that make one move become one beat.
   - **Demote** — a note that's a detail, not a move, becomes a sub-point under the beat it belongs to.
   - **Cut** — a note that doesn't earn a place, or belongs in another section, is named and set aside.
   - **Gap** — a move the section needs that no note covers (a transition, a "so what", a pivot from observation to recommendation) is added as a beat with no source note, marked as connective.
3. Order the beats for momentum — each should set up the next. Group by what the reader needs when, not by topic.
4. Phrase each beat as *what it does*, not just its subject: "pivot from what's there to what the design should do", not "the design section".
5. One pass. No follow-up questions, no back-and-forth.

Read-only on `guide/`: never write `status` or `coverage` on the theme notes — beats is a planning aid, and which notes get used is a writing-stage decision.

## Output

A single **Beats** block.

- **Standalone**: written into `output.md` directly under the section's heading, for the user to draft against and delete. Replace any existing Beats block for that section — never leave two. If `output.md` or that heading doesn't exist yet, show the block in chat instead of creating them.
- **From a `% scribe` marker**: into that block's `% **comments**`, per scribe's own convention.

Format:

```
**Beats** — section 6 (framework; delete once written)

1. **Principle: habitat is mostly hidden** — most insect life is larval, out of sight; it's the rough stuff that counts.  ← [[Insect life cycle — mostly larval, out of sight]]
2. **Refine: variety beats quantity** — lumps and bumps, a mosaic of microclimates.  ← [[Habitat design principles — heterogeneity and a sand pile]]
3. **Reality: the site is neat** — little organic debris; the log pile and bug hotel are the exceptions.  ← [[Volunteer-installed wildlife infrastructure]], site observation
4. **To action: cheap additions** — a sand pile; bug-hotel rules.  ← [[Habitat design principles — heterogeneity and a sand pile]], [[Bug hotel design — natural materials, spacing, and letting it rot]]
5. **Land the gap: water** — no water body anywhere; hands back to the cistern idea.  ← [[Water bodies — the clearest insect-habitat opportunity]]  *(connective — ties to the section opening)*

Not beats: [[Masonry bees — present three years]] — fold into the bees paragraph. [[Pond design — avoid a straight, uniform edge]] — a detail inside beat 4 if a pond is ever proposed.
```

Rules for the block:
- `**bold** ` = what the beat does (function + short label). Plain text after the em-dash = the gist.
- `← ` = the source note(s) as `[[wikilinks]]`, plus non-note sources ("site observation", "brief") in plain text.
- `*(...)*` = notes to self: a gap/connective beat, a sequencing risk, a call the user needs to make.
- A trailing **Not beats:** line lists every merged-away, demoted, or cut note, each with one clause saying where it went.
- Every non-`rejected` note in scope appears exactly once — in a beat's `←` list or on the **Not beats:** line. Nothing silently dropped.
