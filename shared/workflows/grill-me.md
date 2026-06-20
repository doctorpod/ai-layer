---
name: grill-me
description: Capture design decisions into a durable ADR-style record while interviewing you about your plan.
---
# Workflow: Grill Me

Relentlessly interview me about every aspect of this plan, one question at a time, to reach shared understanding and capture durable decisions.

## Interview style

- Ask one question at a time.
- For each question, give your recommended answer.
- If a question can be answered by exploring the project files, explore them instead of asking.

## Lazy capture

Do not create any files until a qualifying decision emerges — keep the session lightweight.

### What qualifies for capture

A decision qualifies if it is:
- Hard to reverse
- Surprising without context, or
- A genuine trade-off between named alternatives

Minor calls and settled choices do not qualify — they flow into the eventual PRP instead.

### On the first qualifying decision

1. Ask the user for a **kebab-case slug** for this work (e.g. `add-invoice-total`). In a code project this slug becomes the ticket name that `create-prp` will use.
2. Create the topic folder:
   - Code project → `_AI/PRPs/<slug>/`
   - Vault → `_AI/chats/<slug>/`
3. Announce that capture has started.
4. Append the decision to `DECISIONS.md` in the topic folder (creating the file if new):

```
## <decision title>
**Decision:** <what was decided>
**Why:** <the reason>
**Alternatives:** <what was considered and rejected>
```

Continue appending each subsequent qualifying decision in the same format.

### On the first canonical term

When a term emerges that needs a precise, shared definition:

**If in an Obsidian vault**: skip the file-selection step entirely. Ask: *"This looks like a glossary-worthy term — shall I create a concept note for it?"* If yes, create the note using the concept note template in the topic folder (`_AI/chats/<slug>/`):

```markdown
---
categories: ["[[Glossary]]"]
---
*One-sentence definition.*

Further context or detail here (optional).
```

The note's filename is the canonical term name: lowercase with spaces for normal terms (e.g. `prompt engineering.md`), UPPERCASE for acronyms (e.g. `RAG.md`). The `aliases` field is only needed for genuine alternate names or synonyms — not for display formatting, since the filename is already human-readable.

**If in a code project**:

1. Search the project for existing `GLOSSARY.md` files.
2. Ask the user which to use:
   - An existing `GLOSSARY.md` (show the paths found)
   - A new one created in the topic folder
   - None
3. Record the choice as a pointer at the **top** of `DECISIONS.md` (before any `##` entries):
   - `Glossary: ../../GLOSSARY.md` (relative path to the chosen file), or
   - `Glossary: ./GLOSSARY.md` (new file in topic folder), or
   - `Glossary: none`
4. Police terms live from that point: flag conflicts with the chosen glossary, propose canonical terms, keep entries terms-only (no implementation detail). Create `GLOSSARY.md` lazily — only when a real term is ready to record.

### Parking unresolved items

If a question cannot be resolved in the session, add it to `QUESTIONS.md` in the topic folder and move on:

```
- [ ] <the question — include why it's blocked and what's needed to resolve it>
```

### If nothing qualifies

If the session ends with no durable decision, write nothing. The interview's value was the shared understanding.

## After the session

Capture is self-justifying — the decision record has value as permanent history, independent of what follows. Do **not** imply that a PRP must come next.

Only if you are in a **code project** and the user signals an intent to build, mention:

> `create-prp` can optionally synthesize a PRP from these captured files when you're ready to implement.
