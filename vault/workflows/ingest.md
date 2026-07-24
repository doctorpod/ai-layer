---
name: ingest
description: Ingest new sources from inbox/ by classifying and processing them.
---

The user has added one or more new sources to `inbox/` and has asked you to ingest:

## Step 0: Classify the source

Before anything else, identify the source type from the content (speaker labels, Q&A format, URL presence, authorial voice):

- **First-person**: interview transcript, field notes, site visit notes, personal recording, meeting notes where the user was present
- **External**: YouTube transcript, blog post, article, book extract, podcast transcript, web content
- **Web-stub**: frontmatter `tags` includes `web-stub` — a pointer file, not pasted source content. Fetch the `url` property live (WebFetch) before proceeding; treat the fetched page as the source content from here on, same as any other external source.

If genuinely unclear, ask the user.

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

**External sources** — go through context gaps **one at a time**: anything the source leaves unclear that the user might already know (who a person is, whether a recommendation has since been acted on, whether a status has changed). Do not ask about document-internal ambiguities the user couldn't know — those go straight to `[!caution]` callouts or `QUESTIONS.md`.

In both cases: present one item, wait for the answer, resolve it, then move to the next. If a claim cannot be resolved, flag it with a `[!caution]` callout when writing (see citation rules).

## Cross-KB sources

A single source may have its strongest claim in one KB but generate concept pages that belong in another. When this happens:

- Anchor the source page in the KB with the strongest thematic claim
- Create concept pages in whichever KB owns that concept
- Update `INDEX.md` in every KB touched
- Use full-path wikilinks (`[[lib/atlas/other-kb/wiki/page-name|display name]]`) only when there is a filename clash across KBs; otherwise use the short form

## Steps 2–8 (all sources)

1. Create a summary page in `wiki/` named after the source
2. Create or update concept pages in `wiki/` for each major idea or entity
3. Add short wiki-links `[[page-name]]` to connect related pages
4. If you see what looks like a person's name, just make it a wikilink, don't create a note for it in the wiki
5. Update `INDEX.md` with new pages and one-line descriptions
6. Append a log with a brief summary (max 12 words) by running `bash _AI/local/scripts/log-write.sh "INGEST: <brief summary>"`
7. Move the file from `inbox/` to `curated/`

A single source may touch 10-15 wiki pages. That is normal.

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

## Page format

Every wiki page should follow this structure:

```markdown
---
tags: ["ai-generated"]
---

# Page Title

**Summary**: One to two sentences describing this page.
**Sources**: List of [[wiki-linked]] raw source files this page draws from
**Last updated**: Date of most recent update.

---

Main content goes here. Use clear headings and short paragraphs.

Link to related concepts using [[wiki-links]] throughout the text.

## Related

- [[related-concept-1]]
- [[related-concept-2]]
```

## Citation rules

- Every factual claim should reference its source file
- Use the format (source: filename.pdf) after the claim
- Flag any of the following issues using a markdown callout immediately after the affected claim:

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
- **One fact, used once**: cite it inline instead of the caution note — `(source: [Title](URL), accessed YYYY-MM-DD)`. No new file.
- **Multiple facts, or a source worth reusing**: don't absorb the facts into wiki content now. Write a stub file into the relevant KB's `inbox/` (filename: the page's title, matching how clippings are already named in `curated/`) and leave it queued for a proper `/ingest` pass:

  ```markdown
  ---
  tags: ["ai-generated", "web-stub"]
  url: https://...
  last_accessed: YYYY-MM-DD
  context: "[[debrief-or-session-note]]"
  flagged_for:
    - topic one
    - topic two
  ---
  Optional free text — only for conditional caveats (source currency, quality). Often empty.
  ```

  Note the claim itself as pending against the stub, not as an established fact, until the later ingest pass writes it up properly.

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

## Step 10: Learnings

Follow `_AI/shared/snippets/learnings.md`, substituting `INGEST` for `[WORKFLOW]`.
