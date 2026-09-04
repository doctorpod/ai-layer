A surmise is a sentence the assistant is about to write into a wiki page that it generated itself to bridge a gap — not paraphrasing or condensing anything any source actually said. This is distinct from the no-source-claim flow above: that flow covers a claim already present in source material with nothing backing it; this covers a claim with no source at all because the assistant invented it to make the explanation coherent. For this specific case, surmise supersedes that flow — don't apply both to the same sentence.

Before treating the gap as a surmise, make the same externally-verifiable-vs-private judgment call as Step 1b above: is this the kind of thing a public web search could plausibly settle, or does it depend on internal/private knowledge no search will surface? Only try a web search when it looks externally verifiable; go straight to surmise otherwise.

If it is a surmise:

1. Using the Question convention in `_AI/shared/snippets/questions.md`, find or create the relevant Question — `pending` if newly created.
2. Write the inferential sentence as normal prose in the wiki page, immediately followed by its inline wikilink: `...claim.[[Qn - slug|Qn]]`. Not a footnote, not a `[!caution]` callout.
3. Set that Question's `status` to `surmised`.
