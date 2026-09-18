# Decision: knowledge base as markdown with frontmatter, one stdlib CLI, two skills

Date: 2026-09-17. Status: accepted.

## Context

The plugin must answer three request shapes (named chart, chart for a question, charts for a document), render in several places, hold a growable knowledge base with per-type notes, stay current, and save tokens without losing fidelity.

## Decision

1. Knowledge base = `kb/charts/<slug>.md` with YAML-style frontmatter (family, shapes, goals, caps, evidence, popularity, per-target support) and fixed body sections. Markdown so humans and any agent can edit it; frontmatter so a script can index and score it. `kb/INDEX.md` is generated and is what the agent reads (about 1/20 of the folder's tokens).
2. One CLI, `scripts/cw.py`, standard library only, with `.ps1` and `.sh` launchers. It indexes, validates, picks (deterministic scoring on family, goal words, shape, caps, target support), profiles CSVs, builds specs for five targets from a CSV by file reference, renders headlessly where a renderer exists, and scaffolds new entries. Token saving comes from: reading the index not the folder, `show --section` for partial reads, data by file reference, and the chooser replacing free reasoning.
3. Two skills: `chartwright` (use) and `chartwright-curate` (grow). A third "document" skill was folded into `chartwright` Step 2a because the difference is in planning, not in the toolchain.
4. Targets in 0.1: mermaid, vega-lite, plotly, chartjs, matplotlib. Vega-Lite is the default web and image path (most reliable for generated specs; vl-convert needs no browser). Office and ECharts targets are documented as candidates in `kb/rules/choosing-a-target.md`.
5. Styling delegates to the bundled Claude `dataviz` skill when present (validated palette, mark specs, anti-patterns) rather than duplicating it; the knowledge base holds the type-selection knowledge that dataviz lacks.
6. Evergreen: `chartwright` tier fast (libraries and Mermaid hosts churn), `chartwright-curate` tier moderate.

## Alternatives rejected

- An MCP server (like antvis/mcp-server-chart): 5 to 8k tokens of tool schemas per session and a remote render dependency. A CLI plus skill loads only on trigger.
- JSON or SQLite knowledge base: harder for humans to annotate; markdown with a validator gives the same machine-readability.
- Generating D3 or matplotlib code by the model for every chart: 5 to 10 times the tokens and a much higher error rate than declarative specs (VegaChat 2026, arXiv 2401.11255).
