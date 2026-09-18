---
name: chartwright
description: "Pick and build the right chart or graph for any request, in the place it will be read: a named chart ('a line graph with time as x and price as y', 'bar chart of sales by region', 'pie of the budget'), the right chart for a question ('how should I show the drop-off between signup steps', 'what chart for survey answers'), or charts chosen from context to illustrate a document, report, README, slide, dashboard or artifact ('add some relevant graphs to this report', 'visualize this CSV', 'put a chart in the README'). Renders to Markdown (Mermaid), web pages (Vega-Lite, ECharts, Plotly, Chart.js), static PNG/SVG for Word, Google Docs, Slack or slides, editable PowerPoint charts, chart-as-URL images, and terminal sparklines, choosing from an evidence-based knowledge base of about 80 chart types with when-to-use, when-not, substitutes and caveats. Use whenever the user says chart, graph, plot, visualize, visualization, sparkline, histogram, heatmap, sankey, treemap, dashboard, 'show this as a', 'make a figure', 'diagram of the numbers', or asks which chart type to use; also for 'refresh chartwright' and 'is chartwright stale'. Growing the knowledge base (new chart type, new render target, a note on a chart, researching a novel chart request) is the sibling chartwright-curate skill; palette and mark styling detail is the bundled dataviz skill, which this skill calls when present. Not for network or knowledge graphs of a codebase (graphify) and not for diagrams with no data (flowcharts, sequence diagrams)."
---

# chartwright

Outcome: the requested chart exists in the target medium, chosen by the knowledge base's rules, renders without error, and its source (spec or script) is saved beside it.

Plugin root: two levels above this file. `CW` = `python "<plugin root>/scripts/cw.py"` (`python3` on macOS/Linux; launchers `scripts/cw.ps1`, `scripts/cw.sh`). Knowledge base: `<plugin root>/kb/`. Read a reference file only when its step is reached.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `verify_at_use` is true, re-check the listed `volatile_claims` before relying on them. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then run the refresh (`evergreen-refresh`) in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task. Never block the task on a refresh unless the task depends on the stale claim.

## Step 1: classify

- Named chart (type and fields given): confirm it is not a misuse with `CW show <slug> --section not`, then Step 3.
- Question (data or message described, no type): Step 2.
- Document ("add charts to", "illustrate", a file or artifact open): read [references/document-charts.md](references/document-charts.md), plan one chart per claim worth showing, then Step 2 per chart.

Data: a CSV, a table, numbers in prose (write them to a small CSV beside the output first), or an artifact's data. No data at all: say so and offer a labelled schematic.

## Step 2: pick

1. Read `kb/INDEX.md` once per session. Never read the whole `kb/charts/` folder.
2. `CW data file.csv` for column kinds and a shape guess.
3. `CW pick --question "<user's words>" --shape <shape> [--series N] [--categories N] [--target <t>] --json`: top three with reasons and warnings.
4. `CW show <slug> --section when not substitutes` for the top pick (and the runner-up when close). A matching "when not" means take the substitute.
5. Judgment rules: `kb/rules/selection.md` (message first, position over area over colour, series caps, no dual axes, no 3D). A user-named misuse is built as asked with a one-line note, unless it would mislead (truncated bar axis, 15-slice pie): say so first.
6. No match or unknown type: hand over to `chartwright-curate`, then continue.

## Step 3 to 5: target, build, verify

Before building, check the target's `tested:` status against the user's platform; if untested there, say so and ask before continuing (rule in `references/build-and-verify.md`, section "Untested targets and platforms").

Read [references/build-and-verify.md](references/build-and-verify.md) (target table, builder coverage per target, column roles for composed charts, styling via the `dataviz` skill, render commands, placement). In short: `CW build --chart <slug> --target <t> --data file.csv --x <col> --y <col> [--series <col>] [--title "<claim>"] --out <file>`, then `CW render ...`, look at the output, place it, save the source beside it. A build that fails to render is not done.

## Step 6: report and learn

Report in one to three lines: chart type and the rule that picked it, target, file or block written, render evidence. If the request needed research, a new type or target, or a correction, run `chartwright-curate` after delivering. A general chart preference ("never pies") goes to `LEARNINGS.md` now.

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` now (check existing entries first: add, update, retire, or nothing). If a learning proves a claim above wrong, fix it here, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`. A learning about one chart type also goes into that chart's `## Notes` (`CW note <slug> "<text>"`).

## Maintenance

This skill is evergreen (topic: chart type selection evidence and the chart menus, syntax and versions of Mermaid, Vega-Lite, ECharts, Plotly, Chart.js, matplotlib and python-pptx; how agents choose and build charts; tier `fast`, currently every 14 days, next due 2026-10-01). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`; references in `references/`. Protocol: the installed evergreen plugin (`protocol: "plugin"` in evergreen.json). Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`; audit with `evergreen-audit`.
