---
title: The generated kb index links every entry
kind: decision
status: active
date: 2026-09-18
verified: 2026-09-18
tags: [index, obsidian, links]
---

# The generated kb index links every entry

## Context
The generated `kb/INDEX.md` listed chart and target slugs as plain text so an agent could read a compact table and call `cw.py show <slug>`. Read in Obsidian (the user's vault since 2026-09-18) the 99 knowledge-base pages had no inbound links.

## Decision
`cw.py index` writes every slug as a relative markdown link to its file, links the targets and the rules, and links the schema and README from the header. The README links the other entry points (skills, examples, ai-docs, changelog).

## Reasons
People read the knowledge base in Obsidian and on GitHub as well as agents; a link per row costs about 20 characters and the index stays 1/26 the size of the charts folder (the compactness test still passes with room). Nothing parses the table back; `cw.py` reads `index.json`. This is the Evergreen Protocol 1.8 §9 rule applied to a generated file.

## Rejected
- A separate human-facing index beside the compact one: two files to keep in step, and the compact one is the one agents would still quote.
- Wikilinks in the index: do not render on GitHub, and the repo's duplicate companion names (CHANGELOG.md in three folders) make them ambiguous.

Related: [the obsidian-notes decision on link form](https://github.com/m4bwav/obsidian-notes/blob/master/ai-docs/decisions/2026-09-18-relative-markdown-links-and-an-index-per-folder-wikilinks-on.md), [the research notes behind the knowledge base](../research/INDEX.md).
