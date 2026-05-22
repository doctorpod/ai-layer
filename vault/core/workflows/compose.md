# Compose Workflow

Use this workflow when the user wants to produce written output — a design document, blog post, article, social media post, or any other piece. The key difference from [[write]]: I draft the prose in the user's voice; the user approves section by section by dictating reactions.

## Prerequisites: style reference

Check whether `_AI/VOICE.md` exists before drafting any prose.

- **If it exists**: read it before every drafting step. Write in the voice it describes.
- **If it is missing**: warn the user that drafting without it will produce generic prose, then ask whether to proceed anyway or set it up first. To set it up: the user shares examples of their own writing and I derive style notes and save them to `_AI/VOICE.md`.

## Step 0: Identify the piece

The user says **compose** and names the output. Check whether `brief.md` and `guide.md` already exist in the piece-folder. If both exist, skip to Step 4. If neither exists, start at Step 1.

## Step 1: Grill to establish the brief

Follow [[grill-me]] to establish:

- **What** — working title and format
- **For** — audience and context
- **Angle** — point of view, argument, or tone
- **Draw from** — which wiki pages, knowledge bases, or vault sources
- **Must haves** — key points that must appear
- **Must nots** — things to avoid

One question at a time. Resolve each before moving on.

## Step 2: Write and approve the brief

Write `brief.md` from the grilling. Show it to the user. The user dictates any corrections. Update until approved.

Once approved, append a log entry:

```bash
bash _AI/core/scripts/log-write.sh "COMPOSE BRIEF APPROVED: [piece title] — [one line summary]"
```

## Step 3: Build and approve the guide

Write `guide.md` — a section-by-section scaffold. For each section: heading, key points to hit, vault sources (wikilinks), and any assets needed.

Show the structure to the user. The user approves or adjusts sections before any prose is drafted. Do not begin Step 4 until the guide is approved.

## Step 4: Drafting loop (repeat per section)

For each section in the guide, in order:

1. Read `_AI/VOICE.md`, the relevant wiki/KB material, and the guide section
2. Draft the section internally, then show it **one paragraph at a time** in the chat
3. For each paragraph, the user dictates one of:
   - **"Good"** — move to the next paragraph
   - **"Change X"** — adjust and show the revised paragraph; repeat until approved
   - **"It should say..."** — the user dictates the passage; clean up their dictation and show the result for approval
4. Once all paragraphs in the section are approved, run the **takeaway check** (see below), then write the full section to `output.md`, mark it done in `guide.md` with ✓, and move to the next section

## Takeaway check

After all descriptive paragraphs in a section are approved, ask: *does this section give the reader something they didn't have before — a pattern named, a risk flagged, an insight they couldn't have arrived at themselves?*

- If yes and it's already in the approved paragraphs: proceed.
- If yes but it's missing: use [[grill-me]] to surface it — a few targeted questions to draw out the designer's or author's insight — then draft a synthesis paragraph from the answers and put it through the normal approval loop before writing to `output.md`.
- If no takeaway is needed (e.g. a purely contextual or scene-setting section): proceed without one.

This step applies most strongly to **design documents**. For blog posts, articles, or personal writing, use judgement — only prompt if the section feels like reporting rather than thinking.

## Step 5: Completion

When all sections are approved, confirm with the user that the piece is complete. Append a log entry:

```bash
bash _AI/core/scripts/log-write.sh "COMPOSE: [piece title] — [brief summary]"
```

## File structure

```
[piece-folder]/
  brief.md    ← I write from grilling; the user approves
  guide.md    ← I write; sections marked ✓ as approved
  output.md   ← I write approved prose; grows section by section
  assets/     ← images, maps, diagrams
```

**Location:**
- Project deliverables: inside the project folder, e.g. `projects/my-project/design-doc/`
- General writing: in a `writing/` root folder if it exists

## Continuity across sessions

State lives in the files. When the user returns to a piece in a new session and says **compose**: read `brief.md` (what the piece is), `guide.md` (which sections remain), and `output.md` (what is already approved). Continue from the first unmarked section. No recap needed.

## Style rules

- Always read `_AI/VOICE.md` before drafting any section
- Write in the user's voice — not formal, not academic, not AI-sounding
- Short sentences. Confident. No waffle.
- If uncertain about tone for a particular passage, offer two short alternatives and ask the user to choose
