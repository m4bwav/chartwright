---
name: chartwright
description: "Pick and build the right chart or graph for any request, in the place it will be read: a named chart ('a line graph with time as x and price as y', 'bar chart of sales by region', 'pie of the budget'), the right chart for a question ('how should I show the drop-off between signup steps', 'what chart for survey answers'), or charts chosen from context to illustrate a document, report, README, slide, dashboard or artifact ('add some relevant graphs to this report', 'visualize this CSV', 'put a chart in the README'). Renders to Markdown (Mermaid), web pages (Vega-Lite, Plotly, Chart.js) and static PNG/SVG for Word, Google Docs, Slack or slides, choosing from an evidence-based knowledge base of about 80 chart types with when-to-use, when-not, substitutes and caveats. Use whenever the user says chart, graph, plot, visualize, visualization, sparkline, histogram, heatmap, sankey, treemap, dashboard, 'show this as a', 'make a figure', 'diagram of the numbers', or asks which chart type to use; also for 'refresh chartwright' and 'is chartwright stale'. Growing the knowledge base (new chart type, new render target, a note on a chart, researching a novel chart request) is the sibling chartwright-curate skill; palette and mark styling detail is the bundled dataviz skill, which this skill calls when present. Not for network or knowledge graphs of a codebase (graphify) and not for diagrams with no data (flowcharts, sequence diagrams)."
---

# chartwright

Outcome: the requested chart exists in the target medium, was chosen by the knowledge base's rules rather than habit, renders without error, and the source (spec or script) is saved beside it so it can be regenerated without the data passing through the model again.

Plugin root: two levels above this file. `CW` below means `python "<plugin root>/scripts/cw.py"` (`python3` on macOS and Linux; `scripts/cw.ps1` and `scripts/cw.sh` are launchers). Knowledge base: `<plugin root>/kb/`.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `verify_at_use` is true, re-check the listed `volatile_claims` before relying on them. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then run the refresh (`evergreen-refresh`) in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task. Never block the task on a refresh unless the task depends on the stale claim.

## Step 1: classify the request

Three shapes, each with its own path:

| Shape | Signal | Path |
|---|---|---|
| Named chart | the user names a type and the fields ("line graph, time on x, price on y") | Step 2 confirms the type is not a misuse (one `CW show <slug> --section not`), then Step 3 |
| Question | the user describes data or a message and asks what chart, or asks for "a chart of" without a type | Step 2 picks |
| Document | "add charts to", "illustrate", "visualize this report", a file or artifact is open and the ask is to enrich it | Step 2a finds the claims first, then Step 2 per claim |

Find the data: a CSV, a table in the document, numbers in the prose, or an artifact's data. If numbers must be extracted from prose, write them to a small CSV first (`<name>.csv` beside the output) so the build reads a file. If there is no data at all, say so and offer a schematic chart with placeholder values, labelled as such.

### Step 2a: charts for a document

Read the document. List the claims that carry numbers or comparisons (grew, more than, share of, correlated, spread, flows to, where). For each claim a reader would want to verify or feel, plan one chart: the claim as the title, the data it needs, and where it goes (next to the claim). Two to five per section; never one per paragraph, never decoration. Show the plan in one short list before building when there are more than three charts. Rules: `kb/rules/selection.md` §7.

## Step 2: pick the chart type

1. Read `kb/INDEX.md` once per session (about 80 rows). Do not read the whole `kb/charts/` folder.
2. Profile the data without reading it: `CW data file.csv` gives column kinds and a shape guess.
3. Ask the chooser: `CW pick --question "<the user's words>" --shape <shape> [--series N] [--categories N] [--target <target>] --json`. It scores every chart on family, goal words, data shape, series and category caps and target support, and returns the top three with reasons and warnings.
4. Read only what is needed: `CW show <slug> --section when not substitutes` for the top pick (and the runner-up when scores are close). If the "When not to use" list matches the situation, take the substitute it names.
5. Apply the judgment rules in `kb/rules/selection.md` (message first, position over area over colour, series caps, no dual axes, no 3D, small multiples over spaghetti). When the user named a chart that the rules call a misuse, build what they asked for and say in one line what the knowledge base recommends instead, unless the misuse would mislead (a truncated bar axis, a pie of 15 slices), in which case say so before building.
6. No match, or the request names a chart type the index lacks (`CW pick` says "no match" or the name is unknown): hand over to `chartwright-curate` to research it and add it, then continue here.

## Step 3: pick the target

`kb/rules/choosing-a-target.md`. In short: markdown file or GitHub/Obsidian/Notion → `mermaid` when the type is in Mermaid's native list, else an SVG/PNG rendered from `vega-lite` and linked; web page or artifact → `vega-lite` (Plotly for candlestick, sankey, sunburst, treemap, 3D; Chart.js when the page already uses it); Word, Google Docs, slides, Slack, email → PNG at 2x from `vega-lite`, `matplotlib` for types outside it; terminal or plain chat → the `terminal` target (block sparkline or block bars) or a small table. If the destination is not obvious from the request or the open file, ask in one line.

## Step 4: build

1. Builder first: `CW build --chart <slug> --target <target> --data file.csv --x <col> --y <col> [--series <col>] [--title "<the claim>"] --out <file> [--html]`. The builder covers the common types per target (list in `ai-docs/notes/kb-authoring-brief.md`); the data goes from the file into the spec without passing through the model.
2. Outside the builder: `CW show <slug> --section build --target <target>` gives the recipe; write the spec or script by hand from it, keeping the data by URL or file reference where the target allows (`--flag dataByUrl` for Vega-Lite).
3. Styling: if the bundled `dataviz` skill is available, run its procedure for colour, marks, hover and accessibility on the spec (its palette validator decides categorical colours; its anti-patterns list is the final check). Without it, use the Okabe-Ito palette and the accessibility notes in the chart file.
4. Title with the finding, label directly, keep the axis honest (bars from zero), and write the text alternative (type, what it shows, key finding) as a caption or alt text.

## Step 5: prove it, then place it

- Render or parse: `CW render --target vega-lite --in spec.vl.json --out chart.png` (or `.svg`); `CW render --target matplotlib --in chart.py --out chart.png`; Mermaid: `CW render --target mermaid ...` when `mmdc` or `npx` exists, otherwise at least check the block against the syntax essentials in `kb/targets/mermaid.md` and the host version floor. A build that fails to render is not done.
- Look at the image (Read the PNG or SVG) for label collisions, empty plots, wrong axis types; fix and re-render.
- Place it: the fenced block or image link at the claim's position in the document; the HTML file or artifact for web; the PNG path for documents. Save the spec or script next to the image.
- Report: one to three lines: chart type and why (the rule that picked it), the target, the file or block written, and the evidence it renders (file size or the render command's output). Mention a rejected alternative only when the user asked for it.

## Step 6: learn from the request

When the request needed research, a new chart type, a new target, or a correction from the user, run `chartwright-curate` after delivering so the next request is cheaper: it adds the chart or note to the knowledge base and logs the change. A user preference about charts in general ("always horizontal bars", "never pies") goes to `LEARNINGS.md` now.

## Output shape

```
Line chart (change-over-time; position on a common scale beats bars for 60 points) → Mermaid xychart in README.md under "Pricing".
Source: docs/charts/price.csv; block validated against Mermaid 11.13 syntax.
```

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` now (format in `../../protocol` via the evergreen plugin; check existing entries first: add, update, retire, or nothing). If a learning proves a claim above wrong, fix it here, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`. A learning about one chart type goes into that chart's `## Notes` (`CW note <slug> "<text>"`) as well.

## Maintenance

This skill is evergreen (topic: chart type selection evidence and the chart menus, syntax and versions of Mermaid, Vega-Lite, Plotly, Chart.js and matplotlib; how agents choose and build charts; tier `fast`, currently every 14 days, next due 2026-10-01). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md) (every change, with reasons), [LEARNINGS.md](LEARNINGS.md) (lessons), [TESTS.md](TESTS.md) and `evals/evals.json` (the cases that prove it and the runs). Protocol: the evergreen plugin's `protocol/PROTOCOL.md` (../../protocol/PROTOCOL.md when this plugin is vendored beside it). Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`; audit with `evergreen-audit`.
