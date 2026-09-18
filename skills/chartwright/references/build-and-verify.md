# Build and verify (chartwright Steps 3 to 5, full detail)

Read this when you are about to build. `CW` = `python "<plugin root>/scripts/cw.py"`.

## Pick the target

`kb/rules/choosing-a-target.md` has the full table. Short form:

| Destination | Target | Notes |
|---|---|---|
| Markdown file, GitHub, GitLab, Obsidian, Notion, wiki | `mermaid` when the type is native there (line, bar, pie, sankey, radar, quadrant, timeline, gantt); otherwise an SVG/PNG from `vega-lite`, linked | stay on the Mermaid 11.13 floor unless the host is known; `--flag namedSeries` on 11.16+ |
| Web page, dashboard, HTML report, artifact | `vega-lite` (default); `echarts` for sankey, chord, treemap, sunburst, gauge, large data, dark mode; `plotly` for candlestick, 3D, statistical traces; `chartjs` when the page already uses it | all get `--html` standalone pages |
| Word (.docx) | `docx` target: one-figure document from a Vega-Lite PNG at 2x with caption (python-docx); for a longer document render the PNG and place it with the snippet in `kb/targets/docx.md` or through the docx skill | Word charts cannot be written by python-docx; the picture is the chart |
| Slides, Slack, email, PDF | PNG at 2x from `vega-lite`; `matplotlib` for types outside it; `pptx` for an editable PowerPoint chart | these hosts reject or degrade SVG |
| Chat reply, terminal, commit message | `terminal` (block sparkline or bars) | one token per point |
| Excel workbook | `xlsx` (data sheet plus native chart) | editable in Excel |
| Google Sheet | `gsheets`: `values` plus an `addChart` request for the Sheets API (`batchUpdate`) | needs the Sheets API; connector-only sessions insert the chart by hand |
| Asciidoctor, Confluence or IntelliJ docs that already use PlantUML | `plantuml` (`@startchart`, 1.2026.0+) for bar, line, area, scatter | no pie; Mermaid reaches more hosts |
| Web page that wants the tersest SVG spec, Observable notebook or Framework site | `observable-plot` (`--html` for a page) | no polar marks, no headless PNG |
| A network or tree in a D2 document | `d2` (edges with labels) | D2 has no data charts at all |
| Google Doc | `gdocs`: new Doc from HTML with `quickchart` or hosted PNG images through the Drive connector; Docs API `insertInlineImage` for an existing Doc | no chart API; verify visually |
| Chat or email where an image URL works and the data is not confidential | `quickchart` | data travels in the URL |

If the destination is not obvious from the request or the open file, ask in one line.

## Build

1. Builder first. `CW build --chart <slug> --target <target> --data file.csv --x <col> --y <col> [--series <col>] [--title "<the claim>"] --out <file> [--html] [--agg sum|mean|none] [--flag ...]`. Data goes from the file into the spec; duplicate x values are summed unless `--agg` says otherwise.
2. Builder coverage (anything else is hand-written from the chart file's recipe: `CW show <slug> --section build --target <target>`):
   - mermaid: line, multi-line, step, bar, column, area, grouped-bar (lossy), pie, donut, sankey, alluvial, quadrant, radar.
   - vega-lite: line, multi-line, step, bar, column, grouped-bar, stacked-bar, stacked-bar-100, area, stacked-area, scatter, bubble, heatmap, histogram, boxplot, pie, donut, strip, dot, lollipop, dumbbell, slope, waterfall, calendar-heatmap, diverging-bar, small-multiples.
   - echarts: line, multi-line, step, area, stacked-area, bar, column, grouped-bar, stacked-bar, stacked-bar-100, scatter, bubble, pie, donut, radar, funnel, sankey, alluvial, heatmap.
   - plotly: line, multi-line, step, area, stacked-area, scatter, bubble, bar, column, grouped-bar, stacked-bar, pie, donut, histogram, boxplot, heatmap.
   - chartjs and quickchart: line, multi-line, area, step, bar, column, grouped-bar, stacked-bar, pie, donut, scatter, bubble, radar, polar-area.
   - matplotlib: line, multi-line, step, area, bar, column, grouped-bar, scatter, histogram, pie, donut, boxplot.
   - pptx: bar, column, grouped-bar, stacked-bar, stacked-bar-100, line, multi-line, area, stacked-area, pie, donut, radar, scatter, bubble.
   - terminal: line, sparkline, area, step, bar, column.
   - xlsx: bar, column, grouped-bar, stacked-bar, stacked-bar-100, line, multi-line, area, stacked-area, pie, donut, radar, scatter, bubble.
   - gdocs: no builder; use quickchart URLs or PNGs inside HTML.
   - docx: everything vega-lite builds (the script renders the PNG and writes heading, picture, caption).
   - gsheets: bar, column, grouped-bar, stacked-bar, stacked-bar-100, line, multi-line, area, stacked-area, step, scatter, pie, donut.
   - plantuml: bar, column, grouped-bar, stacked-bar, line, multi-line, sparkline, area, stacked-area, scatter.
   - observable-plot: line, multi-line, sparkline, step, connected-scatter, area, stacked-area, column, bar, grouped-bar, stacked-bar, stacked-bar-100, diverging-bar, lollipop, dot-plot, scatter, bubble, strip, beeswarm, boxplot, histogram, heatmap, correlogram, adjacency-matrix, calendar-heatmap, waffle, small-multiples, density-2d, hexbin, slope.
   - d2: network, tree, dendrogram (x=source or child, series=target or parent).
3. Column roles for composed charts: dumbbell x=category y=value series=end; slope x=period y=value series=entity; waterfall x=step y=signed change; small-multiples series=panel; sankey and alluvial x=source series=target y=weight; heatmap x=column series=row y=value; quadrant series=label.
4. Data by reference where the target allows: `--flag dataByUrl` for a Vega-Lite spec that will live next to its CSV.
5. Styling: if the bundled `dataviz` skill is available, run its procedure (palette validator, mark specs, hover, anti-patterns) on the spec. Without it, use the Okabe-Ito palette and the chart file's Accessibility section.
6. Title with the finding, label directly, bars from zero, and write the text alternative (type, what it shows, key finding) as caption or alt text.

## Verify

- Render or parse: `CW render --target vega-lite --in spec.vl.json --out chart.png|svg|pdf|html`; `CW render --target matplotlib --in chart.py --out chart.png`; `CW render --target pptx --in chart.py --out deck.pptx`; `CW render --target xlsx --in chart.py --out book.xlsx`; `CW render --target docx --in chart.py --out report.docx`; `CW render --target observable-plot --in chart.js --out page.html`; `CW render --target d2 --in graph.d2 --out graph.svg` (needs `d2`); `CW render --target plantuml --in chart.puml --out chart.svg` (needs `plantuml`, else it prints a Kroki URL); `CW render --target mermaid --in chart.md --out chart.svg` when `mmdc` or `npx` exists (otherwise check the block against `kb/targets/mermaid.md` syntax essentials); `CW render --target echarts|plotly|chartjs --in spec.json --out page.html`. A build that fails to render is not done.
- Look at the image (Read the PNG or SVG): label collisions, empty plots, wrong axis types, dates shifted by a day. Fix and re-render.
- Place it: fenced block or image link at the claim's position; HTML file or artifact for web; PNG path for documents. Save the spec or script beside the image.
- Report in one to three lines: chart type and the rule that picked it, the target, the file or block written, and the render evidence.
