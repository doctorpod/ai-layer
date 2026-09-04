---
name: ingest
description: Ingest new sources from the vault-root inbox/ by classifying, routing to a KB, and processing them.
---

The user has added one or more new sources to the single `inbox/` at the vault root and has asked you to ingest:

## Step 0: Classify the source

Before anything else, identify the source type from the content (speaker labels, Q&A format, URL presence, authorial voice):

- **First-person**: interview transcript, field notes, site visit notes, personal recording, meeting notes where the user was present
- **External**: YouTube transcript, blog post, article, book extract, podcast transcript, web content
- **Web-stub**: frontmatter `tags` includes `web-stub` — a pointer file, not pasted source content. Fetch the `url` property live (WebFetch) before proceeding; treat the fetched page as the source content from here on, same as any other external source.

If genuinely unclear, ask the user.

## Step 0a: Route each source to a knowledge base

The `inbox/` is a single folder at the vault root — sources land there with no KB assigned. Before ingesting, work out where each one belongs:

- Identify the KB whose thematic scope covers the source's strongest claim. Skim candidate `INDEX.md` files if the fit isn't obvious.
- If several sources are waiting, list them and propose an anchor KB for each, then confirm with the user before processing any.
- If the user named a KB when invoking the workflow, treat that as the anchor for the source(s) they mean — still sanity-check the fit.
- A `web-stub` may carry a `kb:` frontmatter hint from whoever created it. Treat it as a suggestion, not a decision.
- If a source's strongest claim fits no existing KB, say so — don't force it. It may need a new KB (needs the user's go-ahead) or may not belong in the wiki system at all.

This step only fixes where the *source page* is anchored and which `curated/` the file ends up in. Concept pages the source generates can still land in other KBs — see Cross-KB sources below.

## Step 0b: Advertisement check (external sources only)

Before discussing takeaways, scan for signs the source is promotional content:

- Stats or claims sourced exclusively from the vendor/author being promoted
- A product, service, course, or event linked or plugged mid-article
- Urgency framing ("limited window", "act now") tied to a commercial offer
- No independent third-party sources cited
- Publisher is the vendor, or the article reads as sponsored/native advertising

If two or more signals are present: **stop and flag it to the user** before going any further. Name the signals you found and ask whether to continue or bin the source. Do not proceed to Step 1 until the user confirms.

## Step 1: Discuss key takeaways (all sources)

Discuss key takeaways with the user before writing anything.

## Step 1b: Uncertainty round

**First-person sources** — go through uncertain claims **one at a time**: misheard proper nouns, ambiguous numbers, unclear context due to transcription quality.

**External sources** — go through context gaps **one at a time**: anything the source leaves unclear that the user might already know (who a person is, whether a recommendation has since been acted on, whether a status has changed). For document-internal ambiguities the user couldn't know, check whether the gap is externally verifiable (a definition, a public record, a fact about a third party or place) before parking it — do a web search and present what you find for the user to confirm or correct. Only if that fails, or the gap depends on something only the user or a private party would know, does it go straight to `[!caution]` callouts or, per `_AI/shared/snippets/questions.md`, a new Question.

In both cases: present one item, wait for the answer (or search result), resolve it, then move to the next. If a claim cannot be resolved, flag it with a `[!caution]` callout when writing (see citation rules).

## Cross-KB sources

A single source may have its strongest claim in one KB but generate concept pages that belong in another. When this happens:

- Anchor the source page in the KB chosen in Step 0a
- Create concept pages in whichever KB owns that concept
- Update `INDEX.md` in every KB touched
- Use full-path wikilinks (`[[lib/atlas/other-kb/wiki/page-name|display name]]`) only when there is a filename clash across KBs; otherwise use the short form

## Steps 2–8 (all sources)

Follow `_AI/shared/snippets/wiki-write-steps.md`, substituting `source` for `[NOUN]` and `INGEST` for `[WORKFLOW]`.

A single source may touch 10-15 wiki pages. That is normal.

## Step 2a: Page sizing and existing-home check

Wiki pages drift toward being source-shaped — one page per idea the source happens to raise, structured the way the source structured it. Source-shaped pages are too specific to be linked to by later sources and other pages. Two checks and a format rule keep pages generic and re-linkable. Apply them every time Step 2 of `wiki-write-steps.md` would create or update a concept page.

### Check for an existing home before creating a page

Before creating any new wiki page, search the target KB's `wiki/` for a page whose core claim already covers the new material (use the `obsidian` CLI, or grep the one-line descriptions in `INDEX.md`).

- **Found one**: don't create a new page. Add a footnoted paragraph to the existing page using the multi-source citation rules below. This is now the common case, not the exception — most ingest passes should be *enriching* existing pages, not spawning new ones. Pages generalise as they accrete sources.
- **Nothing fits**: create a new page.

Because existing pages will now routinely gain a second, third, fourth source, the "retrofit `[^1]` to the page's existing sentences" step in the citation rules fires on almost every pass. Do not skip it.

**Merge bar**: only fold new material into an existing page when it supports the *same claim*, not merely the same topic. "Also about hedges" is not enough. If the new material makes a genuinely different claim, it needs its own page even if the subject overlaps — that guards against premature generalisation.

### State the page's point in one sentence

Before creating a page, complete this sentence about it:

> This page says that ______.

- It must be a **claim** — something that could be true or false.
- **Can't complete it?** You have a topic or a summary, not a concept. Don't create the page — the material belongs as a section or paragraph on a page that does make a claim.
- **Does the completed sentence name a source, a date, or a specific project?** The page is tied too tightly to where it came from. Rewrite the sentence as a general claim, create the page under that general title, and demote the specific detail into the body as an instance (see Page format → `## Evidence`).

Example: about to create `Bob Newington's tree advice` — "This page says that Bob Newington advised removing the leylandii." Names a person and an event. Generalise: "This page says that fast-growing conifers crowd out native planting and are usually worth removing." Title it `Conifers and native planting`; Bob's advice becomes one footnoted bullet in the Evidence section.

### The per-source summary page is a pointer, not an article

`wiki-write-steps.md` Step 1 calls for a summary page named after the source (or, in a debrief, the subject). Under this scheme that page carries **no prose of its own**. It is a short pointer:

```markdown
# <Source or subject name>

**Summary**: What this source is and what it fed into.
**Sources**: [[the-curated-source-file]]
**Last updated**: YYYY-MM-DD

---

This source contributed to:

- [[concept-page-a]] — one line on what it added
- [[concept-page-b]] — one line on what it added
```

All substantive content lives on the concept pages it links to. Don't restate their claims here.

This applies to **every KB — project KBs as well as the atlas**. A project's source pages are pointers too, not narrative write-ups. Existing full-prose source pages are not converted retroactively by an ordinary ingest or debrief; that's a job for `/normalise`, so a KB part-way through the transition will hold both styles for a while.

## Step 2b: Image search (per new wiki page)

For each wiki page created in Step 2, assess whether the concept is **concrete** or **woolly**:

- **Concrete** — has a specific, recognisable visual (a named diagram, a specific building, a map, a tool, a species): search Wikimedia Commons for a freely-licensed image
- **Woolly** — abstract process, historical arc, social phenomenon, philosophical concept: skip entirely

If searching:
1. Search Wikimedia Commons first (stable, freely-licensed)
2. Images must only be of type JPG or PNG
3. If a suitable image found within 2–3 searches: download to `<kb>/assets/<page-name>.<ext>`
4. Run `python3 _AI/local/scripts/normalize-image.py <kb>/assets/<page-name>.<ext>` — checks dimensions/filesize and resizes in place if either exceeds the limit
5. Embed in wiki page after the `---` divider: `![[assets/<filename>]]`
6. If no suitable image found within 2–3 searches, or concept is woolly: skip — do not force a poor or irrelevant image

## Writing style

Follow the guidelines in `_AI/local/STYLE.md`.

### Write concept pages as generic articles, not source summaries

Each wiki page should read as a standalone article about the concept itself — not as a record of what the source says about it. Use the source for evidence and examples, but frame the body around the concept. The `Sources` frontmatter field is the link back to the specific source; the page body should be useful to someone who has never seen that source.

Wrong: *"In this talk, Tolle explains that the ego loves its problems…"*
Right: *"The ego maintains itself through problems. It says it wants resolution, but unconscious thinking continuously recreates the conditions that produce suffering…"*

Keep the writing alive — these pages should hold attention the way a good article does, not read like a textbook. Concrete images over neutral summaries. This keeps pages open to future sources and worth reading on their own terms.

Step 2a and the `## Evidence` section in Page format make this structural rather than advisory: the generic claim and the source-specific detail live in separate parts of the page. "Generic" does not mean "short" — one idea per page, but that idea is unpacked in full, lively prose. The dryness risk is real only if pages shrink to stubs; they should not.

## Page format

Every concept page has a two-part shape: the durable idea first, written source-free; then an `## Evidence` section where specific sources are tracked. Full structure:

```markdown
---
tags: ["ai-generated"]
---

# Page Title

**Summary**: One to two sentences describing this page.
**Sources**: List of [[wiki-linked]] raw source files this page draws from
**Last updated**: Date of most recent update.

---

The durable idea, explained in clear, lively prose with short paragraphs and
concrete images. Written with no reference to any source — this is the part that
stays true regardless of which sources come and go. One idea per page (Step 2a),
unpacked in full, with enough substance to be worth landing on cold.

Link to related concepts using [[wiki-links]] throughout the text.

## Evidence

Where specific sources support, illustrate, or complicate the idea above. One
bullet per instance, each traced to its source:

- Bob Newington advised removing the north-boundary leylandii on his 2026 visit.[^1]
- The Kearsney Abbey planting notes describe the same crowding-out under a mature yew.[^2]

## Related

- [[related-concept-1]]
- [[related-concept-2]]

[^1]: [[debrief-2026-06-12-bob-newington-visit]]
[^2]: [[kearsney-abbey-planting-notes]]
```

The two-part shape is a diagnostic. If the `## Evidence` section is all there is — no
durable idea above it — the page is source-shaped and needs generalising (Step 2a).
If the idea above has nothing under `## Evidence`, it is unsupported.

The header `**Sources**:` field only works while a page has a single source — see Citation
rules for what changes once a second source touches it. On a single-source page the
`## Evidence` bullets need no footnotes (the header covers them); footnotes kick in when
the second source arrives. The two-part shape itself applies from the first source.

## Citation rules

Every factual claim must be traceable to the source that supports it.

### Single-source pages

While a page draws on only one source, the header `**Sources**:` field (see Page format) already names it unambiguously. No per-sentence citation markers needed.

### Multi-source pages: switch to footnotes

The moment a second source touches an existing page — a later ingest pass, or a debrief — per-page attribution stops being enough, because a reader can no longer tell which sentence came from which source. Switch to per-claim footnotes:

- **Retrofit first**: before adding anything new, go back over the page's existing sentences and add `[^1]` to each, tracing them to the source currently named in the `**Sources**:` field. Skipping this step leaves those sentences silently uncited the moment the header is dropped — the header was their only citation.
- Mark the new claim(s) inline too: `...claim sentence.[^2]`
- Define each footnote once, at the bottom of the page: `[^1]: [[source-page]]` (or the filename/URL for a source with no wiki page of its own)
- Reuse the same `[^n]` everywhere that source is cited again — don't mint a new footnote per repetition
- Drop the header `**Sources**:` field only once every sentence on the page carries its own footnote. The footnote list is now the sources list — keeping both risks the two drifting apart.

### Never blend two sources into one sentence

When a later pass adds a new source's claim to an existing page, don't fold it into an existing sentence written from a different source, even if merging would read more smoothly. Keep them as separate, separately-footnoted sentences. A merged sentence can't be traced back to either source individually — this is the main way wiki pages end up conflating claims.

### Flag issues with callouts

Flag any of the following issues using a markdown callout immediately after the affected claim:

  ```
  > [!caution] Brief synopsis of the issue
  > Further detail — e.g. which sources conflict, why uncertain, where in source to check
  ```

  Use this callout for:
  - **Source conflict**: two sources disagree on a claim
  - **No source**: a claim has no source backing it
  - **Uncertain source quality**: poor audio, OCR errors, unclear phrasing — for external sources include a location hint (timestamp, section heading)

### Try a web search before flagging a claim as unverifiable

Before writing a `[!caution]` callout for a **no source** claim, judge whether it's the kind a web search could plausibly settle — a factual or statistical claim, not a personal anecdote or someone's stated opinion. If so, offer the user a web search to try to verify or source it before writing the callout. Always surface what the search found (or didn't) to the user before it lands in the KB — a web search is assistant-initiated, so unlike every other source in this vault, nobody has vetted the page yet.

Then branch on what the search turns up:

- **Nothing found**: still write the `[!caution]` callout, but say a search was tried and didn't turn one up — a checked-and-still-unverified claim is a stronger signal than one nobody looked into.
- **One fact, used once**: cite it with a footnote instead of the caution note — `[^n]: [Title](URL), accessed YYYY-MM-DD`. No new file. This makes the page multi-source even though only one claim moved — apply the retrofit rule above (Citation rules) before dropping the `**Sources**:` header.
- **Multiple facts, or a source worth reusing**: don't absorb the facts into wiki content now. Write a stub file into the vault-root `inbox/` (filename: the page's title, matching how clippings are already named in `curated/`) and leave it queued for a proper `/ingest` pass:

  ```markdown
  ---
  tags: ["ai-generated", "web-stub"]
  url: https://...
  last_accessed: YYYY-MM-DD
  context: "[[debrief-or-session-note]]"
  kb: target-kb-folder-name   # optional hint for the ingest pass; omit if unsure
  flagged_for:
    - topic one
    - topic two
  ---
  Optional free text — only for conditional caveats (source currency, quality). Often empty.
  ```

  Note the claim itself as pending against the stub, not as an established fact, until the later ingest pass writes it up properly.

### Assistant-generated inferences: surmise

The above covers claims already present in source material with no source backing them. A different case is a sentence the assistant generates itself to bridge a gap in the explanation — not paraphrasing or condensing any source. Follow `_AI/shared/snippets/surmise.md` for that case.

## Step 9: Glossary and SPATIAL pass

Once wiki pages are written and files moved to `curated/`, do a closing pass:

**Concept notes**: scan the wiki pages just written for any term, named feature, or concept that could stand as a glossary entry. For each candidate:
- Search the vault by filename for an existing note matching the canonical term name (if the `obsidian` CLI is available, `obsidian file file="<term>" vault=<name>` resolves by name like a wikilink and errors cleanly if no match exists — faster than a filename search)
- If a match exists and already has `categories: ["[[Glossary]]"]` in its frontmatter: skip
- If a match exists without the category: propose adding `categories: ["[[Glossary]]"]` to its frontmatter
- If no match: propose creating a new concept note (confirm with user before creating; one at a time)

Note: any wiki page created during ingest can itself become a glossary entry — just add the category to its frontmatter.

Concept note template:
```markdown
---
categories:
  - "[[Glossary]]"
tags:
  - ai-generated
---
*One-sentence definition.*

Further context or detail here (optional).
```

The note's filename is the canonical term name: lowercase with spaces for normal terms (e.g. `prompt engineering.md`), UPPERCASE for acronyms (e.g. `RAG.md`). The `aliases` field is only needed for genuine alternate names or synonyms — not for display formatting, since the filename is already human-readable. The italic first line is the definition; everything after the blank line is free-form.

**SPATIAL**: if `SPATIAL.md` exists in this KB and the source contained location claims, check whether any named features need adding or correcting. If `SPATIAL.md` doesn't exist but the source described a physical site with named features, offer to create it. Format: see `_AI/local/AI.md`.

## Step 9a: Page-sizing review

For each wiki page **created or touched in this pass**, check whether it is still the right size:

- **List what links to it** — `obsidian` CLI backlinks, or grep the KB for `[[page-name]]`.
- **Inbound links point for clearly different reasons** → the page is too broad. Propose splitting it into one page per claim people are actually linking to, and say which inbound links move where.
- **One inbound link, and it comes from the page's own source** → the page is source-shaped and orphaned. Propose merging it up into a broader parent page and redirecting the link.
- **Propose only.** Don't restructure unprompted — same rule as concept notes in Step 9. One proposal at a time; wait for the user.

A full sweep of an existing KB's back-catalogue is out of scope here — that's the `/normalise` workflow. This step only covers pages this pass has already disturbed.

## Step 9b: Cross-workflow check

Follow `_AI/shared/snippets/cross-workflow-check.md`, substituting `in this source` for `[CONTEXT]`.

## Step 10: Learnings

Follow `_AI/shared/snippets/learnings.md`, substituting `INGEST` for `[WORKFLOW]`.
