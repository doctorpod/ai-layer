1. Create a summary page in `wiki/` named after the [NOUN] — keep it a short pointer that links to the concept pages it fed, with no prose of its own (see the ingest workflow's *Page sizing and existing-home check* section)
2. Create or update concept pages in `wiki/`. Before creating any page, check for an existing home for the material and state the page's point in one sentence — both are gating checks in the ingest workflow's *Page sizing and existing-home check* section. Prefer updating an existing page to creating a new one
3. Add short wiki-links `[[page-name]]` to connect related pages
4. If you see what looks like a person's name, just make it a wikilink — don't create a note for it in the wiki
5. Update `INDEX.md` with new pages and one-line descriptions
6. Append a log with a brief summary (max 12 words) by running `bash _AI/local/scripts/log-write.sh "[WORKFLOW]: <brief summary>"`
7. Move the processed file(s) from the vault-root `inbox/` to the anchor KB's `curated/`
