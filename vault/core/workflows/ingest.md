The user has added one or more new sources to `inbox/` and has asked you to ingest:

## Step 0: Classify the source

Before anything else, identify the source type from the content (speaker labels, Q&A format, URL presence, authorial voice):

- **First-person**: interview transcript, field notes, site visit notes, personal recording, meeting notes where the user was present
- **External**: YouTube transcript, blog post, article, book extract, podcast transcript, web content

If genuinely unclear, ask the user.

## Step 1: Discuss key takeaways (all sources)

Discuss key takeaways with the user before writing anything.

## Step 1b: Uncertainty round

**First-person sources** — go through uncertain claims **one at a time**: misheard proper nouns, ambiguous numbers, unclear context due to transcription quality.

**External sources** — go through context gaps **one at a time**: anything the source leaves unclear that the user might already know (who a person is, whether a recommendation has since been acted on, whether a status has changed). Do not ask about document-internal ambiguities the user couldn't know — those go straight to `[!caution]` callouts or `QUESTIONS.md`.

In both cases: present one item, wait for the answer, resolve it, then move to the next. If a claim cannot be resolved, flag it with a `[!caution]` callout when writing (see citation rules).

## Steps 2–8 (all sources)

1. Create a summary page in `wiki/` named after the source
2. Create or update concept pages in `wiki/` for each major idea or entity
3. Add short wiki-links `[[page-name]]` to connect related pages
4. If you see what looks like a person's name, just make it a wikilink, don't create a note for it in the wiki
5. Update `INDEX.md` with new pages and one-line descriptions
6. Append a log with a brief summary (max 12 words) by running `bash _AI/core/scripts/log-write.sh "INGEST: <brief summary>"`
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
4. Check dimensions: `sips -g pixelHeight pixelWidth <file>`
5. If either dimension >1200px or file >500KB: `sips -Z 1200 <file>`
6. Embed in wiki page after the `---` divider: `![[assets/<filename>]]`
7. If no suitable image found within 2–3 searches, or concept is woolly: skip — do not force a poor or irrelevant image

## Writing style

Follow the guidelines in [[_AI/core/STYLE.md]].

## Page format

Every wiki page should follow this structure:

```markdown
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

## Step 9: Glossary and SPATIAL pass

Once wiki pages are written and files moved to `curated/`, do a closing pass:

**Glossary**: scan the wiki pages just written for any term, named feature, or concept that isn't yet in `GLOSSARY.md`. Propose additions one at a time — don't bulk-add. If `GLOSSARY.md` doesn't exist but candidates have emerged, offer to create it.

**SPATIAL**: if `SPATIAL.md` exists in this KB and the source contained location claims, check whether any named features need adding or correcting. If `SPATIAL.md` doesn't exist but the source described a physical site with named features, offer to create it. Format: see [[_AI/core/AI.md]].
