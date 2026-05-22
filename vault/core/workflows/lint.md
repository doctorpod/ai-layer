When the user asks you to **lint** or **audit** a knowledge base:

## Step 1: Run the structural check

```
python3 _AI/core/scripts/lint-kb.py <kb-path>
```

Read the output. This catches format issues, orphan pages, broken cross-KB links, and pending `[!caution]` markers without reading all wiki files.

## Step 1b: Asset orphan check

If an `assets/` folder exists in the KB, check for files not linked from any wiki page:

```bash
for f in <kb-path>/assets/*; do
  name=$(basename "$f")
  grep -rl "assets/$name" <kb-path>/wiki/ > /dev/null 2>&1 || echo "Orphaned asset: $name"
done
```

Report any orphans. Offer to delete them.

## Step 2: Content checks (targeted)

For checks the script cannot do, read only the specific files needed:

- **Contradictions**: read pages most likely to overlap on a shared topic
- **Person names not wikilinked**: read pages most likely to mention people by name in prose
- **Outdated claims**: focus on pages with dates or time-sensitive content
- **Glossary coverage**: if `GLOSSARY.md` exists, scan wiki pages for bolded terms, named features, and proper nouns for places or objects — flag any that appear in the wiki but are absent from the glossary
- **SPATIAL consistency**: if `SPATIAL.md` exists, spot-check that location descriptions in wiki pages don't contradict SPATIAL entries (e.g. a wiki page says "northeast corner" but SPATIAL says "southwest")

## Step 3: Report and resolve sequentially

Report all findings as a numbered list with suggested fixes. Then work through them one at a time:

- Fix issues that don't need user input immediately and move on
- For issues that need clarification, ask **one question**, wait for the answer, resolve it, then ask the next

## Step 4: Log
Once all findings have been dealt with, append a log with a brief summary (max 12 words) by running `bash _AI/core/scripts/log-write.sh "LINT: <brief summary>"`
