---
name: write
description: Work on output pieces or guides using the named-folder/four-file pattern.
---

# Write

When asked to **write**, work on a piece of **output**, or help with a **guide** or **brief**:

## The pattern

Every piece of writing lives in a named folder with four predictable contents:

```
[piece-folder]/
  brief.md     ← the user writes; I help on request
  guide.md     ← I write and maintain
  output.md    ← the user writes only; I never touch
  assets/      ← images, maps, diagrams
```

**Location**:
- Project deliverables (design reports, client docs): inside the project folder, e.g. `projects/my-project/design-doc/`
- General writing (articles, posts, essays): in a `writing/` root folder if it exists

## The files

### brief.md
The seed. Contains: what (title/working title), for (audience/context), angle (point of view or argument), draw from (which KBs or specific vault pages), key things to hit (must-includes, constraints, things to avoid).

The user writes this. If asked, I help draft it by asking a few questions or tidying rough notes into the format. I do not own the brief.

### guide.md
The scaffold. I build this from the brief. It is not prose — it is a structured framework for the user to write from:
- One section per document section (headings from the framework used, e.g. GOBRADIMET)
- For each section: key points to hit, vault sources to draw from (wikilinks), and any assets needed
- Assets are specified per section, tied to their purpose (not as a separate list)

I update the guide when new vault material becomes relevant, or when the user asks me to expand a section or surface more sources.

### output.md
The user's. I can read it for structural feedback. I never write to it, edit it, or rewrite any of its words. If asked for feedback, I comment on structure and completeness (does it follow the guide, does it hold together) — not on prose.

### assets/
Images, maps, charts. Referenced as `![[assets/filename.png]]` in guide and output. The guide specifies which asset each section needs.

## What I do at each stage

**When the brief exists**: read it, search the relevant KBs, and build the guide — a section-by-section scaffold with sourced ideas and vault connections.

**While the user is writing**: the user can ask me to expand a section of the guide, surface more vault material, or check structure. I stay in guide territory.

**After a draft**: if asked, I read output.md and give structural feedback — does it cover the guide's points, does the argument hold? I name gaps but do not fill them.

## Multi-session continuity

State lives in the files. Each session: read the brief, read the guide, read where output.md is up to — then continue. No need to recap in conversation.

## Invocation

The user says **write** (or asks to work on a guide, brief, or specific section). I identify which piece-folder is active, read brief + guide + current output state, and respond with what's next.

If no piece-folder exists yet: ask the user what the piece is and offer to help write the brief.
