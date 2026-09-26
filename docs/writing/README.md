---
tags: [ai-layer-docs]
sources:
  - vault/workflows/sync-guide.md
  - vault/workflows/interview.md
  - vault/workflows/elicit.md
  - vault/workflows/beats.md
  - vault/workflows/polish.md
  - vault/workflows/scribe.md
  - vault/workflows/sanity.md
  - vault/workflows/gap-check.md
  - vault/workflows/diploma-ready.md
  - shared/snippets/piece-folder.md
checked: 2026-09-26
---

# Writing workflows

How a piece of writing moves from a brief to a finished draft, and which tool helps at each stage.

- Every piece lives in a [[piece folder]]: a [[piece brief]], a [[guide folder]] of material, the [[output draft]] you write, and `assets/`.
- Nine workflows help along the way. None of them writes your prose.
- For a lookup of every page, see the [[writing/INDEX|Index]].

## The running example

Every example in these pages uses one invented piece, so you can follow the same notes from page to page.

- **The piece:** a permaculture design report for the Hollin Lane community orchard, at `projects/hollin-lane/design-doc/`.
- **The client:** Maggie Thorne, for the Hollin Lane Residents' Group.
- **Two parts** (a [[multi-part piece]]):
  - `parts/client/`: the client document, following GOBRADIMET. Outline: `01 Goals`, `02 Observation`, `06 Design`. Its material comes from the `hollin-lane` knowledge base.
  - `parts/reflection/`: the Diploma reflection. Outline: `01 Choosing a framework`, `02 What I'd do differently`. Its material comes from you.
- **Sources** in the knowledge base's `curated/`: `debrief-2026-03-14-site-walk`, `Maggie Thorne interview 1 - transcript`.
- **Gathered notes** in `parts/client/guide/`:
  - `Fruit for the school kitchen, not a showpiece` (01 Goals)
  - `Wet corner by the north gate floods every winter` (02 Observation)
  - `South bed shaded by the neighbour's hedge until noon` (02 Observation)
  - `Heavy clay under the wet corner` (02 Observation)
  - `Swale above the wet corner` (06 Design)
- **Interview threads** in `parts/reflection/guide/`: `01 choosing the framework` (closed), `02 the wet corner surprise` (open), and thread 3, "working with volunteers" (dropped, so it has no note).
- **Assets:** `base-map.png`, `swale-section.png`.

## The lifecycle

### 1. Brief

You write `brief.md` for each part: what it is, who it's for, where the material comes from and, for a framework like GOBRADIMET, the [[brief outline]]. No workflow owns this step. Ask in chat if you want help.

### 2. Gather

Fill each part's `guide/` with a [[gatherer]]:

- For `parts/client/`, [[sync-guide workflow|sync-guide]] triages the curated site-walk debrief and interview transcript, keeps what matters to the brief, and files quotes as notes such as `Wet corner by the north gate floods every winter`. Run it again whenever new material lands.
- For `parts/reflection/`, [[interview workflow|interview]] builds a timeline from your logs, then asks you about one thread at a time and saves your answers verbatim. When you misremember when you first saw the wet corner, it points you to the January log without changing what you said.

Browse the result in the [[guide view]]. Mark notes `rejected` if you've no real basis for them.

### 3. Shape

Before writing a section:

- If the words won't start, [[elicit workflow|elicit]] gives you a burst of angles from the section's notes, in chat.
- If you don't know the order, [[beats workflow|beats]] writes a [[beats block]] under `## 02 Observation`: set up the dry site, complicate it with the north gate, pivot to water as a resource.

### 4. Draft

You write `output.md`, typing or dictating. Mark notes `used` as you draw on them. Along the way:

- [[polish workflow|polish]] cleans up dictated text inside a [[polish marker]], fixing spelling and punctuation and never your meaning.
- [[scribe workflow|scribe]] answers an instruction you leave in a [[scribe marker]], right beside the prose: "does this justify the swale?"

### 5. Check

- [[sanity workflow|sanity]] flags where the draft contradicts itself: the north gate is "dry in summer" on one line and has "standing water most of the year" on another.
- [[gap-check workflow|gap-check]] reports that the wet corner is covered only thinly, that the swale is missing, and that `swale-section.png` is never used. It records a [[coverage verdict]] on each note.
- [[diploma-ready workflow|diploma-ready]] walks the Diploma [[assessment rubric]] and returns Nearly Ready.

Then back to drafting, and round again.

## A toolbox, not a pipeline

The stages above are a typical order, not a fixed one. The tools never call each other. They're linked only by the files in the piece folder, so you choose what to run next: sync-guide again halfway through the draft, beats on one section while another is finished, gap-check whenever you like. The reasoning behind this is in [[PATTERNS]] (Gatherer; Log inputs, derive the rest; Toolbox, not pipeline).

## Which tool when

- **[[sync-guide workflow|sync-guide]] or [[interview workflow|interview]]?** Is the material in your knowledge bases, or in your head? Either way, the notes come out the same shape.
- **[[elicit workflow|elicit]] or [[beats workflow|beats]]?** elicit gives you sparks for a first sentence, in chat. beats gives you the section's order, written into the draft.
- **[[elicit workflow|elicit]] or [[interview workflow|interview]]?** elicit is one brainstorm from notes you already have. interview runs over several sessions and produces the notes.
- **[[polish workflow|polish]] or [[scribe workflow|scribe]]?** polish does one fixed job, cleaning your text, and strips its markers. scribe does whatever you ask and keeps its marker. Both work on any file, not just a piece.
- **[[polish workflow|polish]] or [[sanity workflow|sanity]]?** polish fixes how the text is written and never comments on content. sanity comments on content and never touches the text.
- **[[gap-check workflow|gap-check]] or [[diploma-ready workflow|diploma-ready]]?** gap-check asks whether the draft covers the guide, and records coverage. diploma-ready asks whether it would pass a tutor, gives a verdict, and writes nothing.

## More

- [[writing/INDEX|Index]]: every workflow and concept page, one line each.
- Each workflow page ends with the path of the workflow file it describes, under `_AI/local/workflows/`.
