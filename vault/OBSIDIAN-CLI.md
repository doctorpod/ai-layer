# Obsidian CLI

A curated reference for the `obsidian` command-line tool, useful for vault operations that are cheaper or more correct via Obsidian's live index than via Grep/Read/mv.

**Before using any command below:**

- **macOS-only, and not on `$PATH`.** The binary lives at `/Applications/Obsidian.app/Contents/MacOS/obsidian` — this is a property of Obsidian.app's bundle layout, not a per-machine path, so it's not a portability shortcut to fix.
- **Requires the GUI app running with the vault open.** This CLI reads Obsidian's live in-app index. It does not work headlessly (CI, git hooks, scripts run outside an interactive session with the app open).
- **Always pass `vault=<name>` explicitly.** Never rely on the default "active vault" — that's whichever Obsidian window currently has OS focus, which may not be the vault you're working in. Omitting it on a mutating command (`move`, `rename`, `property:set`, `append`) risks silently changing the wrong vault.
- **Always pass `format=json` on `search` and `search:context`.** These two commands return empty output in the default `format=text` (a confirmed CLI quirk) — including `total`. Every other command below works correctly in its default format.

## Finding things

```bash
# Full-text search — format=json is required, not optional (see above)
/Applications/Obsidian.app/Contents/MacOS/obsidian search query="<text>" format=json vault=<name>

# Search with surrounding context lines
/Applications/Obsidian.app/Contents/MacOS/obsidian search:context query="<text>" format=json vault=<name>

# What links to a given file
/Applications/Obsidian.app/Contents/MacOS/obsidian backlinks path=<file> vault=<name>

# What a given file links out to
/Applications/Obsidian.app/Contents/MacOS/obsidian links path=<file> vault=<name>

# Files with no incoming links
/Applications/Obsidian.app/Contents/MacOS/obsidian orphans vault=<name>

# Wikilinks that don't resolve to any file
/Applications/Obsidian.app/Contents/MacOS/obsidian unresolved vault=<name>

# Files with no outgoing links
/Applications/Obsidian.app/Contents/MacOS/obsidian deadends vault=<name>

# Heading outline of a file, without reading the whole thing
/Applications/Obsidian.app/Contents/MacOS/obsidian outline path=<file> vault=<name>

# Resolve a file by name (like a wikilink) — errors cleanly if no match
/Applications/Obsidian.app/Contents/MacOS/obsidian file file=<name> vault=<name>

# List files (optionally filtered)
/Applications/Obsidian.app/Contents/MacOS/obsidian files vault=<name>
```

## Frontmatter & metadata

```bash
/Applications/Obsidian.app/Contents/MacOS/obsidian properties path=<file> vault=<name>
/Applications/Obsidian.app/Contents/MacOS/obsidian property:read path=<file> property=<key> vault=<name>
/Applications/Obsidian.app/Contents/MacOS/obsidian property:set path=<file> property=<key> value=<value> vault=<name>
/Applications/Obsidian.app/Contents/MacOS/obsidian tags vault=<name>
/Applications/Obsidian.app/Contents/MacOS/obsidian tasks vault=<name>
```

## Reading & editing files

```bash
/Applications/Obsidian.app/Contents/MacOS/obsidian read path=<file> vault=<name>
/Applications/Obsidian.app/Contents/MacOS/obsidian append path=<file> content=<text> vault=<name>
/Applications/Obsidian.app/Contents/MacOS/obsidian prepend path=<file> content=<text> vault=<name>

# Move or rename — updates all [[wikilinks]] to the file vault-wide automatically.
# Raw `mv` or an Edit-based rename does NOT do this — links will silently break.
/Applications/Obsidian.app/Contents/MacOS/obsidian move file=<name> to=<path> vault=<name>
/Applications/Obsidian.app/Contents/MacOS/obsidian rename file=<name> to=<newname> vault=<name>
```

## Out of scope

This reference deliberately excludes `dev:*`, `plugin:*`, `theme:*`, `quickadd:*`, and `bookmark`/`snippets`/`hotkey`/`tab`/`workspace` management — these configure Obsidian itself rather than support note workflows.

Full reference: `obsidian help` or `obsidian help <command>`.
