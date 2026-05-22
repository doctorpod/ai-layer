# Connect

When asked to **connect** or run a **cross-wiki insights** pass:

1. Read the `INDEX.md` from each knowledge base to survey the terrain
2. Grep for existing `## Wider connections` sections to see what's already known
3. Load only the specific pages likely to yield *new* connections — aim for 6–10 pages, not the whole corpus
4. Identify new connections: relationships, overlaps, tensions, or synergies between knowledge bases that aren't already recorded
5. For each new connection, add a `## Wider connections` section (or append to an existing one) at the end of **both** pages — write one sentence per side explaining the connection from that page's perspective
6. Run `python3 _AI/core/scripts/check-connections.py` to verify all new links are reciprocal
7. Append a log with a brief summary (max 12 words) by running `bash _AI/core/scripts/log-write.sh "CONNECT: <brief summary>"`
8. Report a brief summary of what was added

## Section format

At the end of a wiki page, after `## Related pages`:

```markdown
## Wider connections

- One sentence explaining the connection from this page's perspective, with a wikilink to [[path/to/other-wiki/page|the other page]].
```

Each bullet is one connection. Use the full vault-relative path in the wikilink so it resolves unambiguously across knowledge bases. People wikilinks (e.g. `[[Jo Barker]]`) may appear within connection sentences — they are not themselves connections and the checker ignores them.

## Writing style

Follow the guidelines in [[_AI/core/STYLE.md]].

## Notes

- This workflow is incremental. Don't re-examine connections already recorded.
- Prefer specific page-to-page links over vague "these two projects are related" observations.
- Every connection must be 2-way: both pages get a sentence. Never write one side without the other.
- **Quality bar**: only write a connection if you can complete this sentence clearly and specifically: *"A reader of page A would find page B useful because..."* If the answer is vague ("they're both about design") or requires a chain of inference, skip it. Fewer sharp connections are better than many weak ones.
