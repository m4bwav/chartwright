# Choosing a render target

Pick the smallest target the destination renders natively, then the cheapest to produce. Cost is in tokens (spec size) and setup (installs the reader's machine may lack). Target files in `kb/targets/` carry the details and the current versions.

| Destination | First choice | Fallback | Why |
|---|---|---|---|
| README, GitHub or GitLab issue/PR, Obsidian note, Notion, Azure DevOps wiki, Docusaurus or MkDocs page | `mermaid` if the type is line, bar, pie, sankey, radar, quadrant, timeline, gantt | SVG via `vega-lite` render, linked as an image, spec saved beside it | Mermaid renders in place with no build step; everything else is a picture |
| Web page, dashboard, HTML report, Claude artifact | `vega-lite` (vega-embed) | `plotly` for candlestick, sankey, sunburst, treemap, 3D, gauges; `chartjs` when the page already uses it | Vega-Lite is the most reliable for generated specs and the smallest |
| Word, Google Docs, PowerPoint, Google Slides, Slack, email, LaTeX, PDF | PNG at 2x via `vega-lite` render | `matplotlib` script for types outside Vega-Lite; native python-pptx or openpyxl charts when the file must stay editable | These hosts show images only; SVG is rejected or degraded |
| Terminal, chat reply with no image support | Unicode sparkline `▁▂▃▅▇` or a small markdown table | plotext for a real terminal plot | About one token per point |
| Jupyter, data notebook | Altair (same Vega-Lite spec) | matplotlib, plotly | Notebook renders both interactively |
| Spreadsheet | openpyxl (Excel) or Sheets API `EmbeddedChart` | image | Native charts stay editable |

## Decision steps

1. Where will the reader see it? Ask if not obvious from the request or the file being edited (a `.md` in a repo means markdown; a `.html` or artifact means web; a `.docx`/`.pptx`/Google Doc means image or native).
2. Is the chart type in that target's "What it can draw" table as `native`? If `approx`, decide whether the approximation loses the point (a grouped bar as overlapping Mermaid bars does). If `image` or `none`, move down the fallback column.
3. Does the reader's host run a new enough version? Mermaid hosts lag (GitHub 11.16, Obsidian 11.13): stay on the 11.13 floor unless the host is known.
4. Keep the source: save the spec or script next to the rendered image (`chart.vl.json` beside `chart.png`) so the chart can be regenerated and so the data never has to pass through the model again.
5. Data by reference: build with `cw.py build --data file.csv` rather than pasting rows into the spec; use `--flag dataByUrl` for Vega-Lite specs that will live next to their CSV.

## Token cost ladder (approximate, data by reference)

sparkline (1 token per point) < Mermaid xychart (30 + data) < Vega-Lite spec (120 to 200) < Chart.js / Plotly / ECharts config (150 to 250) < Observable Plot (100 to 160) < matplotlib script (200 to 400) < D3 (800 to 1500). Inline data costs 6 to 10 tokens per row per column; a thousand rows inline is the single biggest waste.

## Adding a target

`python scripts/cw.py new-target <slug> --name "<Name>" --kind markdown|web|image|office|terminal`, fill the stub, then add a `<slug>:` line to every chart's `support:` map (`cw.py validate` lists the gaps) and a `### <slug>` recipe under `## Build` for each chart marked native or approx. Candidates already researched for a later version: `echarts` (v6.1, chord and beeswarm native, SSR to SVG), `pptx` (python-pptx native charts), `xlsx` (openpyxl), `gsheets` (EmbeddedChart), `plantuml` (`@startchart` since 1.2026.0), `terminal` (plotext, termgraph), `quickchart` (Chart.js config as a URL).
