# Charting libraries and tools across render targets — research report

Date: 2026-09-17. Sources: npm registry API, api.npmjs.org, PyPI JSON API, pypistats.org, api.github.com, official docs/release pages, GitHub issues/discussions. Figures marked "(measured)" were pulled live today; "(unverified)" means a search snippet I could not confirm against a primary page. Weekly downloads are npm last-week or pypistats last-week.

Note on tool behaviour: the WebFetch summariser mislabelled several GitHub release dates as 2024/2023; all dates below were cross-checked against the registry APIs, which agree with 2026.

---

## A. MARKDOWN targets

### A1. Mermaid

| Item | Value |
|---|---|
| Current version | **12.0.0**, published 2026-09-10 (npm, measured) |
| Previous line | 11.17.2 (2026-08-25); 11.16.x = the line most hosts run |
| GitHub stars | 90,298 (measured) |
| npm weekly downloads | 15.15 M (measured) |
| License | MIT |
| Velocity | Rising strongly (new diagram type every 1–2 months in 2026; 11.16 → 12.0 in ~4 months) |
| Repo | https://github.com/mermaid-js/mermaid |
| CLI | `@mermaid-js/mermaid-cli` 11.17.0 (2026-09-02, still on Mermaid 11; 533k weekly) — renders to SVG/PNG/PDF via Puppeteer |

**12.0.0 highlights** (https://github.com/mermaid-js/mermaid/releases): ELK bundled and default layout for flowchart/state/class/ER/requirement; new `redux-color`/`neo` default look; new diagrams: UML **use case** and **agentflow-beta**; breaking: ES2024, Safari 17.4+, Node 22.12+. Keep old look with `layout: dagre`, `theme: default`, `look: classic`.

**Diagram types listed on mermaid.js.org at 12.0.0 (measured):** Flowchart, Swimlanes, Sequence, Class, State, ER, User Journey, Gantt, Pie, Quadrant, Requirement, Use Case, GitGraph, C4, Mindmap, Timeline, ZenUML, Sankey, XY Chart, Block, Packet, Kanban, Architecture, Radar, Event Modeling, Treemap, Venn, Ishikawa, Wardley, Cynefin, TreeView (+ railroad-beta, agentflow-beta per release notes). 11.16.0 added cynefin-beta, railroad-beta, swimlane.

Syntax and limits for the data-chart subset:

- **xychart** (line + bar only). Keyword is now `xychart` (docs still accept `xychart-beta`). Named series get a legend (`line "Revenue" [..]`, `showLegend` config); point labels since 11.16 (`line [1.5 "lbl", 2.3]`); `xychart horizontal`. x-axis categorical `x-axis [a, b, c]` or numeric range `x-axis 0 --> 10`; y-axis numeric only. **Limitations:** no scatter, no dual y-axis, multiple bar series overlap instead of grouping (issue #5292, discussion #5326), no per-point colours beyond theme vars, no log scale. https://mermaid.js.org/syntax/xyChart.html
  ```
  xychart
      title "Sales"
      x-axis [Jan, Feb, Mar]
      y-axis "USD" 0 --> 100
      bar "2025" [40, 55, 70]
      line "2026" [45, 60, 80]
  ```
- **pie**: `pie showData` + `title` + `"Label" : value` lines. No donut, no custom colours except theme.
- **quadrantChart**: points in [0,1] x [0,1], four labelled quadrants, per-point styling. No axis ticks/scales. https://mermaid.js.org/syntax/quadrantChart.html
- **sankey** (v10.3+, still marked experimental; keyword `sankey-beta`/`sankey`): CSV body `source,target,value`. Only preset node alignments. https://mermaid.js.org/syntax/sankey.html
- **radar-beta** (v11.6.0+): `axis A, B, C` + `curve name{1,2,3}`; `max`/`min` optional. https://mermaid.js.org/syntax/radar.html
- **treemap-beta** (docs say 12.0.0; existed experimentally in 11.x — unverified which minor): indented `"Section"` / `"Leaf": 12`. No negative values. https://mermaid.js.org/syntax/treemap.html
- **timeline**, **gantt** (`dateFormat`, sections, `crit`/`done`/`active`, milestones), **gitGraph**, **mindmap**, **kanban**, **packet** (bit-field diagram, `0-15: "Source Port"`), **block** (grid blocks with widths), **architecture** (icon-based service groups) — stable in 11.x.
- 2025–2026 additions: venn, ishikawa (fishbone), wardley, cynefin, treeview, event modeling, swimlane, railroad, use case, agentflow. Most are `-beta` keyworded.
- **Not in Mermaid at all:** scatter, histogram, box plot, heatmap, area, stacked/grouped bars, dual axis, funnel, bubble. For those, fall back to images or Vega-Lite.

**Where Mermaid renders and which version (matters for beta charts):**

| Host | Support | Version (2026-09) | Source |
|---|---|---|---|
| GitHub (README/issues/PR) | native ```` ```mermaid ```` | **11.16.1** (user check via `info` diagram, 2026-08-20). Lags npm by 1–2 minors; never on day-one of a major | https://github.com/orgs/community/discussions/70672 |
| GitLab | native | **Mermaid 11** since GitLab 19.0 (2026-05-21); was 10 before | https://docs.gitlab.com/releases/19/gitlab-19-0-released/ |
| Obsidian | native | **11.13.0** as of Obsidian 1.13.0 (2026-05-28); one-time consent banner added | https://obsidian.md/changelog/2026-05-28-desktop-v1.13.0/ |
| VS Code | via "Markdown Preview Mermaid Support" (bierner) extension; bundles a recent npm mermaid (exact version unverified) | – | marketplace |
| Notion | native (renders mermaid code blocks; version undocumented) | – | mermaid integrations list |
| Confluence | **not native**; Marketplace apps ("Mermaid for Confluence", Connect-based, Cloud only) | – | https://github.com/orgs/mermaid-js/discussions/3992 |
| Azure DevOps Wiki | native; standard ```` ```mermaid ```` fence accepted since Sprint 274 (2026-05) in addition to `::: mermaid`. MS docs say "9.x or higher" with limited syntax (exact version unverified) | – | https://learn.microsoft.com/en-us/azure/devops/release-notes/2026/wiki/sprint-274-update |
| Docusaurus | `@docusaurus/theme-mermaid`; PR #12454 upgrades to Mermaid 12 (merge/release state unverified) | 11 → 12 | https://github.com/facebook/docusaurus/pull/12454 |
| MkDocs Material | built-in via SuperFences, bundles Mermaid 11 ESM with ELK | 11 | https://squidfunk.github.io/mkdocs-material/reference/diagrams/ |

Practical rule: for portable markdown, stay on syntax that exists in **11.13** (Obsidian floor): xychart, pie, quadrant, sankey-beta, radar-beta, timeline, gantt, gitGraph, mindmap, kanban, packet, block, architecture are safe; treemap/venn/wardley/usecase/agentflow are not.

### A2. Other markdown-embeddable options

- **Vega-Lite in markdown**
  - Obsidian: community plugin **obsidian-vega** (Justin-J-K) renders ```` ```vega-lite ```` JSON blocks. https://github.com/Justin-J-K/obsidian-vega
  - Jupyter Book 2 / MyST: no built-in vega directive; use a MyST plugin or embed Altair output from executable cells. https://jupyterbook.org/stable/plugins/plugins/
  - GitHub/GitLab: not rendered — must go via image.
- **Chart.js via markdown-it**: `markdown-it-chart` (tylingsoft), `markdown-it-charts` (chart.js/echarts/highcharts/c3), VuePress `@vuepress/plugin-markdown-chart`, VS Code `chartjs-markdown-preview`; `datafe/markdown-chart` (ECharts renderer with markdown-it/Vue/react-markdown adapters). All site-specific; nothing renders on GitHub.
- **Kroki** (https://kroki.io, https://github.com/yuzutech/kroki, 4,335 stars, MIT, measured): one HTTP API for Mermaid, PlantUML, Vega, Vega-Lite, GraphViz, D2, Excalidraw, etc. Returns SVG/PNG. Self-hostable Docker. Integrations: Asciidoctor, Sphinx (sphinx-kroki), MkDocs, Obsidian-kroki, GitLab (Kroki setting). Useful as a "render anything to SVG URL" fallback: `https://kroki.io/vegalite/svg/<deflate+base64url spec>`.
- **PlantUML charts**: **new in 1.2026.0** — `@startchart` with bar, line, area, scatter, multiple axes, annotations; no pie. https://plantuml.com/chart-diagram
  ```
  @startchart
  h-axis [Q1, Q2, Q3, Q4]
  v-axis 0 --> 100
  bar "Revenue" [45, 62, 58, 70]
  @endchart
  ```
- **ASCII / Unicode charts** (render everywhere as a code block, zero deps):
  - **plotext** 6.1.0 (2026-09-07, MIT, 2,195 stars, 222k weekly PyPI, measured): scatter, line, bar, hist, datetime, candlestick, error bars, confusion matrix, event plots; `plt.build()` returns the string. https://github.com/piccolomo/plotext
  - **termgraph** 0.7.6 (2026-03-25, MIT, 3,297 stars): bar/horizontal/stacked/calendar heatmap from a data file; CLI. https://github.com/mkaz/termgraph
  - **asciichart** 1.5.25 (npm, 2020, MIT, 93k weekly) / `asciichartpy` (PyPI): single-function line charts. Unmaintained but stable.
  - Block-character sparklines: `▁▂▃▄▅▆▇█` (8 levels) — trivial to generate inline, ~1 token per point.
- **Images (PNG/SVG links)** — the universal fallback. GitHub renders `![](chart.svg)` and `<img src>`; SVG is sanitised (scripts, styles, class/id stripped) so keep SVGs static; use `?sanitize=true` on raw URLs. Inline `<svg>` in markdown is **not** rendered on GitHub. https://github.com/github/markup/issues/1160
- **Inline SVG** works in HTML-capable renderers (Obsidian, Docusaurus/MDX, VS Code preview); GitHub/GitLab strip it.

---

## B. WEB targets

| Library | Version (date, measured) | Stars | npm weekly | License | Velocity | Paradigm | Renderer |
|---|---|---|---|---|---|---|---|
| Vega-Lite | 6.4.3 (2026-04-24); Vega 6.4.0 (2026-08-14); vega-embed 7.2.0 (2026-09-02) | 5,492 | 895k (vega-lite), 687k (vega-embed) | BSD-3 | Steady | Declarative JSON | SVG or Canvas |
| Plotly.js / plotly.py | plotly.js **4.1.1** (2026-09-14); plotly.py **7.1.0** (2026-09-15) | 18,336 / 18,788 | 644k / PyPI 11.2M wk | MIT | Rising (majors 4.0/7.0 in Aug 2026) | Declarative JSON (traces+layout) | SVG (+WebGL for gl traces) |
| Chart.js | 4.5.1 (2025-10-13) | 67,697 | 11.4M | MIT | Flat (no release in 11 months; v5 timeline unverified) | Declarative config | Canvas |
| Apache ECharts | **6.1.0** (2026-05-19); 6.0.0 2025-07-30 | 67,347 | 4.69M | Apache-2.0 | Rising | Declarative option object | Canvas or SVG; SSR |
| Observable Plot | 0.6.17 (2025-02-14) | 5,383 | 553k | ISC | Flat (repo pushed 2026-09) | Declarative JS (marks) | SVG |
| D3 | 7.9.0 (2024-03-12) | 113,741 | 19.2M | ISC | Flat, mature | Imperative | SVG/Canvas |
| Recharts | 3.10.1 (2026-07-25) | 27,567 | **51.9M** (largest, via shadcn/ui) | MIT | Rising | Declarative React components | SVG |
| Nivo | 0.99.0 (2025-05-23) | 14,100 | 1.47M (@nivo/core) | MIT | Slow | React components | SVG/Canvas/HTML |
| Highcharts | 13.0.2 (2026-08-27) | 12,491 | 2.12M | **Proprietary** (free only for personal/non-profit/education; commercial from ~$416/dev/yr) | Steady | Declarative config | SVG |

Key notes:
- **ECharts 6** (https://echarts.apache.org/handbook/en/basics/release-note/v6-feature/): new default theme, runtime theme switch, auto dark mode, chord, beeswarm, jitter, broken axis, matrix coordinate system, reusable custom series (violin, contour, bar-range…). SSR: `echarts.init(null, null, {renderer:'svg', ssr:true, width, height})` → `renderToSVGString()`; PNG via node-canvas + `setPlatformAPI`. https://echarts.apache.org/handbook/en/how-to/cross-platform/server/
- **plotly.js 4.0** (2026-08): removed `*mapbox` traces (use `*map`), removed Chart Studio config, colour lib TinyColor→culori (rgb fractions no longer percentages), new `quiver` trace. plotly.py 7.0 dropped Kaleido <1.0, Orca, and the `engine=` arg. https://github.com/plotly/plotly.py/blob/main/CHANGELOG.md
- **Vega-Lite 6.0** (2025-03-28) was a consolidation release; 6.x adds newline tooltips, pointer cursor for interactive charts, stack order aligned to colour domain. https://github.com/vega/vega-lite/blob/main/CHANGELOG.md
- **Recharts 3** (2025-06) rewrote state, improved accessibility; 3.x releases monthly.

### Comparison

| Dimension | Vega-Lite | Plotly | Chart.js | ECharts | Observable Plot | D3 | Recharts/Nivo |
|---|---|---|---|---|---|---|---|
| Declarative? | Yes (JSON grammar) | Yes (JSON) | Yes (JSON config) | Yes (JSON option) | Yes (JS marks) | No | Yes (JSX) |
| Typical line-chart spec size (est. tokens, 3 series × 12 pts, data by reference) | ~120–200 | ~150–250 | ~150–250 | ~150–250 | ~100–160 | ~800–1500 | ~250–400 |
| Offline | Yes (bundle) | Yes (3.5 MB bundle) | Yes (small, ~70 kB) | Yes | Yes | Yes | Yes (React) |
| Accessibility | SVG; `description`/`aria` props emit `aria-label`/`role`; best of the set | SVG DOM, limited ARIA | Canvas: must add `role="img"`, `aria-label`, fallback content yourself (https://www.chartjs.org/docs/latest/general/accessibility.html) | Canvas by default; SVG renderer + `aria: {enabled:true}` auto-descriptions | SVG, `ariaLabel`/`ariaDescription` | Whatever you write | SVG; Recharts 3 added keyboard/ARIA |
| Headless static export | **vl-convert** (Rust, no browser): `vl2png/svg/pdf`; vl-convert-python 1.9.0.post1 (stable), 2.0.0rc7 (2026-09-14) | **kaleido 1.4.0** (needs system Chrome or `kaleido_get_chrome`) | `chartjs-node-canvas` 5.0.0 (node-canvas) or QuickChart | Built-in SSR to SVG; node-canvas for PNG | `Plot.plot({document})` under jsdom → SVG | jsdom or Puppeteer | react-dom/server → SVG string, or Puppeteer |
| CDN (cdnjs + jsdelivr) | jsdelivr `vega@6`, `vega-lite@6`, `vega-embed@7`; cdnjs has vega/vega-lite | both | both | both | jsdelivr `@observablehq/plot`; cdnjs yes | both | jsdelivr (needs React) |

Minimal idiomatic line chart in each:

```json
// Vega-Lite (vegaEmbed('#v', spec))
{"$schema":"https://vega.github.io/schema/vega-lite/v6.json",
 "data":{"url":"sales.csv"},
 "mark":"line",
 "encoding":{"x":{"field":"month","type":"temporal"},
             "y":{"field":"revenue","type":"quantitative"},
             "color":{"field":"region","type":"nominal"}}}
```
```js
// Plotly.js
Plotly.newPlot('p', [{x:months, y:rev, type:'scatter', mode:'lines', name:'Revenue'}], {title:{text:'Sales'}});
```
```js
// Chart.js 4
new Chart(ctx, {type:'line', data:{labels:months, datasets:[{label:'Revenue', data:rev}]}});
```
```js
// ECharts 6
echarts.init(el).setOption({xAxis:{type:'category', data:months}, yAxis:{type:'value'}, series:[{type:'line', name:'Revenue', data:rev}]});
```
```js
// Observable Plot
Plot.plot({marks:[Plot.lineY(rows, {x:'month', y:'revenue', stroke:'region'})]})
```
```js
// D3 v7 (abridged; ~25 lines for scales, axes, path)
const x=d3.scaleUtc(d3.extent(rows,d=>d.month),[40,w-10]), y=d3.scaleLinear([0,d3.max(rows,d=>d.revenue)],[h-30,10]);
svg.append('path').datum(rows).attr('fill','none').attr('stroke','steelblue').attr('d',d3.line().x(d=>x(d.month)).y(d=>y(d.revenue)));
svg.append('g').attr('transform',`translate(0,${h-30})`).call(d3.axisBottom(x)); svg.append('g').attr('transform','translate(40,0)').call(d3.axisLeft(y));
```
```jsx
// Recharts 3
<LineChart width={600} height={300} data={rows}><XAxis dataKey="month"/><YAxis/><Tooltip/><Line dataKey="revenue"/></LineChart>
```

---

## C. IMAGE / STATIC via Python

| Package | Version (date, measured) | Stars | PyPI weekly | License | Velocity |
|---|---|---|---|---|---|
| matplotlib | **3.11.2** (2026-09-11); 3.11.0 2026-06-12 (text/font overhaul) | 23,229 | 37.3M | PSF-style | Steady |
| seaborn | 0.13.2 (2024-01-25) | 14,023 | 6.26M | BSD-3 | **Flat** (no release in 2.5 yrs; `seaborn.objects` interface stable) |
| plotnine | 0.15.8 (2026-08-14) | 4,759 | 546k | MIT | Steady (ggplot2 grammar; tracks matplotlib 3.11) |
| Altair | **6.3.0** (2026-09-15) + vl-convert-python 1.9.0.post1 (2026-01-21; bundles Vega-Lite 6.4.1) / 2.0.0rc7 | 10,477 | 8.82M | BSD-3 | Rising |
| plotly.py | **7.1.0** (2026-09-15) + kaleido **1.4.0** (2026-08-31) | 18,788 | 11.2M | MIT | Rising |
| bokeh | **3.10.0** (2026-08-18) | 20,453 | 1.19M | BSD-3 | Steady |

Static export paths and pitfalls:
- **matplotlib**: `savefig('x.svg')` or `.png`, `dpi=` (150–200 for HTML docs, 300 for print; SVG ignores DPI except for rasterised elements). Headless: set `MPLBACKEND=Agg` per-process or `matplotlib.use('Agg')` before importing pyplot; don't set MPLBACKEND globally (overrides matplotlibrc). Windows: wheels are self-contained; font cache build on first run (~10 s) — warm it during install; emoji/CJK need explicit `font.family`. Theming: `plt.style.use('seaborn-v0_8-whitegrid')` or a project `.mplstyle`; `constrained_layout=True`; `ax.spines[['top','right']].set_visible(False)`. https://matplotlib.org/stable/users/explain/figure/backends.html
- **seaborn**: `sns.set_theme(style="whitegrid", context="talk")`; same export as matplotlib.
- **plotnine**: `p.save('x.png', dpi=150)` / `.svg`; `theme_minimal()`.
- **Altair + vl-convert**: `chart.save('x.png', scale_factor=2)` / `.svg` / `.pdf`; no browser required (Rust binary embedding a JS runtime); Windows wheels available; fonts: bundled Liberation fonts, `VL_CONVERT_FONT_DIR` / Google Fonts env in 2.0. Best headless story of the group. https://github.com/vega/vl-convert
- **plotly + kaleido 1.x**: `fig.write_image('x.png')`; **Chrome required** (not bundled since 1.0.0, 2025-06-19). Windows: `kaleido_get_chrome` CLI / `kaleido.get_chrome_sync()` downloads a compatible build; corporate proxies block it; plotly.py ≥ 7 removed `engine=` and Orca. Use `start_sync_server()` for batch exports (1.1+). https://github.com/plotly/Kaleido/releases
- **bokeh**: `export_png/export_svg` need Selenium + a webdriver — heaviest headless setup; prefer HTML output.
- **SVG vs PNG for docs**: SVG for GitHub/MkDocs/Docusaurus (crisp, smaller for line charts, dark-mode friendly via `currentColor`); PNG @ 2x (dpi 200 or `scale_factor=2`) for Word/Slides/Google Docs (they reject SVG), Slack, Notion image upload. Save the source spec alongside the image for regeneration.

---

## D. OFFICE / DOCS targets (brief)

- **python-docx** 1.2.0 (2025-06-16): **no native chart API** (issue #179 open since 2015). Workarounds: insert PNG (`doc.add_picture`); `docx-charts` (PyPI) edits data of charts already in a template; `python-docx-valutico` fork adds charts; or generate the chart part with python-pptx and transplant the `c:chart` XML part (community recipe). https://github.com/python-openxml/python-docx/issues/179
- **python-pptx** 1.0.2 (2024-08-07): `slide.shapes.add_chart(XL_CHART_TYPE.X, x, y, cx, cy, chart_data)`. Supported: bar/column (clustered/stacked/100%), line (+markers), pie/doughnut (+exploded), area, scatter (XY), bubble, radar; 3-D variants present in the enum but limited. Not supported: waterfall, funnel, treemap, sunburst, histogram, box ("chartex" family). https://python-pptx.readthedocs.io/en/latest/user/charts.html
- **openpyxl** 3.1.5 (2024-06-28): `BarChart, LineChart, ScatterChart, PieChart, DoughnutChart, AreaChart, BubbleChart, RadarChart, StockChart, SurfaceChart` + 3D variants; series reference cell ranges. Excel-native chartex (waterfall/funnel/treemap/sunburst/histogram/boxplot) not supported. https://openpyxl.readthedocs.io/en/stable/charts/introduction.html
- **Google Docs API**: no chart resource; embed a Sheets chart via `InlineObject` → `embeddedObject.linkedContentReference.sheetsChartReference` (spreadsheetId + chartId), or insert an image.
- **Google Sheets API** `EmbeddedChart.spec`: `basicChart` (BAR, COLUMN, LINE, AREA, STEPPED_AREA, COMBO; stacked variants) plus `pieChart`, `bubbleChart`, `candlestickChart`, `orgChart`, `histogramChart`, `waterfallChart`, `treemapChart`, `scorecardChart`. https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/charts
- **Excel/Word native (chartex)**: waterfall, funnel, treemap, sunburst, histogram, Pareto, box & whisker, map — only via Office itself or paid SDKs (Aspose etc.).

---

## E. TOOLS FOR AGENTS

| Tool | What it does | Chart types | Popularity | License | Token effect |
|---|---|---|---|---|---|
| **antvis/mcp-server-chart** (`@antv/mcp-server-chart` 0.9.10, 2026-02-25) | MCP server; each chart is a tool taking data JSON, returns an image URL (renders on Alipay `antv-studio` by default; `VIS_REQUEST_SERVER` → self-hosted GPT-Vis-SSR). stdio/SSE/streamable | 26: area, bar, boxplot, column, dual-axes, fishbone, flowchart, funnel, histogram, line, liquid, mind map, network, org chart, pie, radar, sankey, scatter, treemap, venn, violin, word cloud, spreadsheet + 3 China-only maps | 4,366 stars; 4k npm weekly | MIT | Model emits only data + a few params (~50–150 tokens); no code. Cost: 26 tool schemas in context (~5–8k tokens) unless lazily loaded; external network dependency. https://github.com/antvis/mcp-server-chart |
| **antvis/chart-visualization-skills** (`npx skills add antvis/chart-visualization-skills`) | Agent Skills (SKILL.md) version: `chart-visualization` POSTs to `https://antv-studio.alipay.com/api/gpt-vis`, returns a markdown image URL; also `antv-g2-chart`, `antv-s2`, infographic, narrative-text skills | 30+ | 494 stars (2026-09-09) | MIT | Loads only when triggered; zero code generation; remote-only rendering. https://github.com/antvis/chart-visualization-skills |
| **Anthropic `data-visualization` skill** (knowledge-work-plugins) | Guidance: chart chooser by data relationship, matplotlib/seaborn/plotly patterns, accessibility checklist; no pies >5 cats, never 3-D, dual-axis with care | 13+ patterns | 12.1k installs on skills.sh; repo 24,612 stars | Apache-2.0 | Prompt guidance only; saves reasoning, not output tokens. https://www.skills.sh/anthropics/knowledge-work-plugins/data-visualization |
| **Anthropic `dataviz` skill** (bundled in Claude Code/Cowork) | Design-system-agnostic method: form heuristic, colour formula + validator, mark specs, interaction rules, palette reference | any medium | bundled | Apache-2.0 (anthropics/skills: 176,921 stars; docx/pptx/xlsx/pdf are source-available) | Guidance; enforces visual consistency |
| **QuickChart** (https://quickchart.io, typpo/quickchart) | GET/POST `/chart?c={chart.js config}` → PNG/WebP/SVG/PDF; `version=4` for Chart.js 4; self-host Docker `ianw/quickchart`; template endpoint with query params | All Chart.js + plugins (annotations, datalabels), sparklines, QR | 2,056 stars; "300M charts/month" (site claim) | AGPL-3.0 | A chart is a URL: ~80–200 tokens and no file; template endpoint lets the model emit only values |
| **Vega-Lite MCP servers** | isaacwasserman/mcp-vegalite-server (100 stars; `save_data` + `visualize_data` → PNG); markomitranic/vegalite; stephaneberle9/mcp-server-vegalite-viewer (interactive) | anything Vega-Lite | small | MIT (per-repo, unverified) | Data stored server-side by name → spec references it; model never re-emits rows |
| **Plotly MCP** | arshlibruh/plotly-mcp-cursor (9 stars); DuckDB+Plotly bundles | plotly | tiny | – | – |
| **Kroki** | HTTP render of Mermaid/Vega-Lite/PlantUML/… to SVG | many | 4,335 stars | MIT | URL-as-chart for text DSLs |
| **vl-convert CLI** (`cargo install vl-convert` or `pip install vl-convert-python`) | `vl2png spec.json out.png`, `vl2svg`, `vl2pdf`, `vl2html`, `vl2url`; 2.0 adds `vl-convert serve` | Vega-Lite | 168 stars (lib), used by Altair (8.8M/wk) | BSD-3 | Deterministic renderer; spec can reference CSV by path/URL |
| **mermaid-cli** (`mmdc -i in.mmd -o out.svg`) | Puppeteer render | all Mermaid | 533k npm weekly | MIT | Lets markdown Mermaid double as image source |
| **chartjs-node-canvas** 5.0.0 | Node PNG render of Chart.js configs | Chart.js | 196k weekly | MIT | Same JSON as web target |
| **plotext / termgraph** | terminal/ASCII | see A2 | – | MIT | Output is text; no image round-trip |
| Claude Code plugin marketplaces | No official Anthropic chart *plugin* found in claude-plugins-official; third-party "advanced-data-visualization" skill (D3/WebGL guidance) on mcpmarket | – | – | – | – |

---

## F. TOKEN-EFFICIENCY techniques (with evidence)

1. **Prefer declarative specs over imperative code.** "Visualization Generation with Large Language Models: An Evaluation" (arXiv 2401.11255) found Vega-Lite the most reliable across models and that shorter declarative specs correlate with higher accuracy; imperative libraries (matplotlib, D3) need longer code and fail more. VegaChat (arXiv 2601.15385) reached 0% visualization-error rate on NLV/ChartLLM with Vega-Lite vs 30.6% for code-generating LIDA. Vega's own rationale: Vega-Lite exists as a compact "target language" for programs generating charts (https://vega.github.io/vega/about/vega-and-d3/). Rough sizes for one 3-series line chart with data by reference: Vega-Lite ~120–200 tokens; Chart.js/ECharts/Plotly JSON ~150–250; matplotlib ~300–450; D3 ~800–1500 (estimates from the §B snippets, not tokenizer-measured).
2. **Pass data by reference, never inline.** Vega-Lite `"data":{"url":"file.csv"}` (vl-convert resolves local paths; 2.0 allows absolute paths); Chart.js/ECharts/Plotly need a wrapper that loads the CSV; MCP servers like mcp-vegalite-server store named tables server-side. Inline 12×3 numbers ≈ 100 tokens; 1,000 rows ≈ 6–10k tokens — the single largest saving.
3. **Template + parameters.** Keep a small library of validated spec templates (line, bar, stacked bar, scatter, pie, heatmap) and have the model emit only `{template, csv, x, y, color, title}` (~40–80 tokens); a script (`chart --template line --csv sales.csv --x month --y revenue --color region --out docs/img/sales.svg`) fills it. QuickChart's `/chart/render/<templateKey>?title=…&data1=…` is the hosted form of this. Mermaid's DSL is already this shape for the markdown target.
4. **CSV → chart CLIs** so the model runs one command instead of writing code: `vl-convert vl2svg`, `termgraph data.dat`, `plotext` one-liner, `mmdc`, QuickChart URL. Prefer tools with no browser dependency (vl-convert, plotext, termgraph, ECharts SSR, matplotlib Agg) — Kaleido/Puppeteer installs are where agents burn tokens on errors.
5. **Deterministic chart chooser.** Encode the choice rules (Anthropic data-visualization skill: relationship → chart type; avoid pie >5 categories, never 3-D, dual-axis only with clear labels) in a script that inspects the CSV (column types, cardinality, time index, row count) and returns the template name. The model skips the reasoning entirely; only overrides cost tokens.
6. **Validate cheaply, fix algorithmically.** VegaChat: validate against the JSON schema first, apply deterministic fixes (date normalisation, field-name casing) before any LLM retry; cap retries. Same for Mermaid via `mermaid.parse()`/`mmdc`.
7. **Cache rendered images keyed by hash(spec+data)**; rebuild only on change (docusaurus-prerender-mermaid does this at build time). Store the spec next to the image so a later session regenerates without reading the PNG.
8. **Lazy tool schemas.** An MCP charting server with 26 tools costs ~5–8k tokens of schema per session (mcp-server-chart); a skill or CLI loads nothing until triggered. Prefer skill/CLI for occasional charts, MCP only for many charts per session.
9. **Choose the smallest target the host supports**: sparkline block chars (≈1 token/point) → Mermaid xychart (≈30 tokens + data) → Vega-Lite JSON (≈150) → PNG via template script (≈60 tokens of command) → hand-written code (hundreds+).

---

## Quick recommendations for the plugin

- Markdown target: Mermaid `xychart`/`pie`/`quadrantChart`/`sankey-beta`/`radar-beta`/`timeline`/`gantt` gated to an **11.13 syntax floor**; anything else → SVG image link generated by vl-convert (Altair/Vega-Lite) with the spec saved beside it.
- Web target: Vega-Lite (SVG, accessible, smallest spec) by default; ECharts 6 when interactivity/large data/dark-mode switching matter; Chart.js only when the host already uses it; avoid Highcharts unless licensed.
- Static Python: Altair + vl-convert-python (no Chrome) first; matplotlib/Agg for anything Vega-Lite can't; plotly+kaleido only if the user already has Chrome.
- Office: python-pptx native charts (bar/line/pie/scatter/bubble/area/doughnut/radar), openpyxl native charts, PNG for docx/Google Docs.
- Agent tooling: ship a `chart` CLI (chooser + templates + vl-convert) rather than an MCP server; optionally expose QuickChart/Kroki URL mode for zero-install hosts.

## Unverified / to confirm
- Exact Mermaid version in Notion, the VS Code extension, and Azure DevOps ("9.x or higher" per MS docs).
- Whether Docusaurus PR #12454 (Mermaid 12) is merged/released.
- Chart.js 5 timeline.
- Vega-Lite ARIA doc URL (`/docs/aria.html` 404s; ARIA config is in Vega config `aria`/`description`, https://vega.github.io/vega/docs/config/).
- Which Mermaid 11.x minor first shipped treemap-beta (docs now say 12.0.0).
- Token counts in §B/§F are estimates, not tokenizer-measured.
