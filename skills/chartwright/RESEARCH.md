# Research: chartwright

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the evergreen plugin's `protocol/PROTOCOL.md`. Full research notes: `../../ai-docs/research/`.

Topic: chart type selection evidence and the chart menus, syntax and versions of Mermaid, Vega-Lite, Plotly, Chart.js and matplotlib; how agents choose and build charts. Tier `fast`. Last refresh 2026-10-23; next due in `evergreen.json`.

## Current understanding

- Chart selection: the message picks the family (FT Visual Vocabulary's nine, plus hierarchy, relationship, single-value, table); within a family, prefer position and length encodings over angle, area and colour (Cleveland and McGill 1984; Heer and Bostock 2010). Pies are fine up to about 5 slices for part-to-whole "majority" questions (Skau and Kosara 2016). Layout decides which comparison is easy; annotate the intended one (Franconeri et al. 2021). Settled.
- Caps: about 5 lines, 3 grouped series, 4 stacked segments, 8 categorical hues; beyond, small multiples or a table. Practitioner consensus (Datawrapper, FT, dataviz skill). Settled.
- Targets (2026-09-17, rechecked 2026-10-23): Mermaid 12.2.0 (2026-10-13; 12.0.0 on 2026-09-10 added use case, agentflow and ELK default; treemap dates from 11.8, venn-beta from 11.13 and wardley from 11.14, corrected 2026-10-17 by chartwright-curate R-20261017-1; 12.1 adds ELK feedback-edge routing, packet `bitOrder`, and error diagrams that print the real parse error; 12.2 adds opt-in mindmap `colorBy: depth` and layout fixes, no chart change); mermaid-cli 12.0.0 is still the newest CLI, so the pin in cw.py is current; hosts lag (GitHub 11.16.1, Obsidian 11.13, GitLab 11.16.1), so the portable floor is 11.13 and `xychart-beta`. Obsidian 1.15.0 (Catalyst early access, 2026-10-22) drops Mermaid for its own renderer Pele, which targets Mermaid 12.1.0 syntax; once 1.15 is public GitHub becomes the floor, though Pele's xychart and named-series support is unconfirmed. Vega-Lite 6.5.0 (2026-10-08: exponential moving average transform, tooltip field filter, facet and normalized-stack fixes) with vl-convert 1.9.0.post1 (2.0.0rc7 in preview) is the best headless image path. plotly.js 4.2.0 (2026-10-29: legend `itemheight`, ternary spikelines, an XSS fix for javascript: links in MathJax text, scattergl hover freeze fix) / plotly.py 7.1.0 (2026-08/09 majors; mapbox traces removed; kaleido 1.5.0 still needs Chrome and dropped Python 3.8). Chart.js 4.6.1 (4.6.0 and 4.6.1 on 2026-10-22: pie and doughnut spacing, scale-title stroke, integer canvas sizes; no v5 in sight); cw.py loads `chart.js@4`, so it floats to 4.6. ECharts 6.1.0 (2026-05) is the strongest candidate for a sixth target (chord, beeswarm native, SSR). matplotlib 3.11.2. Moving.
- Agent practice: generated Vega-Lite specs fail far less than generated code (VegaChat 2026, arXiv 2601.15385: 0% vs 30.6% visualization errors); antvis/mcp-server-chart (4.4k stars, 26 tools) and antvis/chart-visualization-skills are the most used agent chart tools but render remotely and cost 5 to 8k tokens of schema per session; Anthropic's bundled `dataviz` skill covers palette and marks, not type selection. Microsoft's Flint (microsoft/flint-chart, MIT, 1.0.1 on 2026-10-21, which added interactions, an Image-Charts backend and PNG/SVG from the MCP server) is now a standalone library and MCP server: the agent writes a roughly 10-line semantic spec and a deterministic compiler emits Vega-Lite, ECharts, Chart.js, Plotly or native Excel charts with themes; it chooses no chart type from evidence and has no Markdown or PowerPoint target. Vendors now ship their own servers too: ApexCharts' official `apexcharts-mcp` (in the MCP registry since 2026-10-07; npm downloads in the week to 2026-10-22: antvis 2.2k, Flint 1.6k, apexcharts-mcp 0.5k after a launch spike) generates and validates ApexCharts configs only. A CLI plus skill is the token-efficient shape. Contested only in that MCP servers keep growing.
- Token savings: read a compact index, pass data by file reference (a thousand inline rows costs 6 to 10k tokens), template plus parameters over code generation, validate specs mechanically before any retry. Settled.

## Open questions

- Which Mermaid version GitHub and Obsidian run after 2026-10 (decides when named xychart series can be emitted by default; treemap and venn are already within the 11.13 floor, chartwright-curate R-20261017-1). On 2026-10-23: GitHub still has no public note of an upgrade; Obsidian 1.15.0 Catalyst (2026-10-22) replaces Mermaid with Pele (Mermaid 12.1.0 syntax), public date unknown; GitLab at 11.16.1.
- Whether Chart.js 5 ships. Partly settled 2026-10-23: 4.6.0 and 4.6.1 shipped 2026-10-22, so the project is maintained and chartjs stays a first-class target; no v5 sign.
- vl-convert 2.0 stable date (its `serve` mode could replace per-call rendering). Still 2.0.0rc7 (2026-09-14) on 2026-10-23.
- Whether Flint grows a Markdown or image-file target, or publishes measured gains over direct Vega-Lite generation (arXiv 2607.20775); either would raise it from a pointer to a candidate backend. Partly answered 2026-10-23: 1.0 adds PNG/SVG and Image-Charts URLs; still no Markdown target and no measured gains.
- Does Pele (obsidianmd/pele, npm `pele` 1.9.0, MIT, zero dependencies, sync `render(text)` to SVG) run headless in Node, and is it close enough to Mermaid to serve as a browserless parse or preview check, or as the Obsidian-faithful render once 1.15 is public?

## Search plan

Subject:

- `mermaid release notes <month year>`, `mermaid.js.org/syntax/xyChart.html` (named series, legends), `site:github.com/orgs/community/discussions mermaid version`
- `vega-lite release`, `vl-convert release`, `plotly.js release notes`, `chart.js release`, `apache echarts release`, `matplotlib release`
- `"which chart" guide site:datawrapper.de <year>`, `"visual vocabulary" update`, `data visualization perception study <year>`
- Vendor forums (announcements first, then known issues since `last_checked`): Mermaid GitHub Discussions https://github.com/mermaid-js/mermaid/discussions (gh api graphql, newest first); GitHub host changes https://github.com/orgs/community/discussions and https://github.blog/changelog/ (use its search for "mermaid"; the `/label/mermaid` page is a 404); Obsidian https://obsidian.md/changelog/ (the index, which carried the 1.15 Pele change) and https://forum.obsidian.md; Pele https://github.com/obsidianmd/pele releases and npm `pele`; Plotly https://community.plotly.com (`/latest.json?order=created`; the announcements category slug moved, so filter titles for "release"); Chart.js https://github.com/chartjs/Chart.js/discussions; Vega https://github.com/vega/vega-lite/discussions; ECharts https://github.com/apache/echarts/discussions

Tooling:

- `path:SKILL.md chart OR visualization` on GitHub code search sorted by recently updated; `npx skills find chart`; skills.sh weekly installs for "chart", "dataviz", "visualization"
- `https://registry.modelcontextprotocol.io/v0/servers?search=chart` (sort by `publishedAt`; most rows are noise such as charter-boat sites); npm weekly downloads `https://api.npmjs.org/downloads/point/last-week/<pkg>` for `@antv/mcp-server-chart`, `flint-chart-mcp`, `apexcharts-mcp`; `antvis/mcp-server-chart` releases; `microsoft/flint-chart` releases; `quickchart` releases
- `anthropics/claude-plugins-official` and `anthropics/skills` for chart or dataviz changes

Practice:

- `"claude code" OR codex OR cursor "chart" "vega-lite" OR mermaid workflow <year>`; hn.algolia.com `llm chart generation`
- `site:arxiv.org LLM chart generation OR visualization recommendation <year>` (Data Formulator, LIDA, VegaChat, Draco follow-ups)

Testing:

- arXiv listing search with a date filter (web search returns old papers), `site:arxiv.org chart generation benchmark <year>` (nvBench 2.0, VisEval, ChartMimic, Chart2Code), `vega-lite schema validation`, `mermaid.parse` validation
- `path:SKILL.md chart evals` on GitHub

Best sources: mermaid.js.org and the mermaid GitHub releases; vega.github.io and vega/vl-convert releases; plotly changelogs; chartjs.org; echarts.apache.org; matplotlib release notes; datawrapper.de/blog; eagereyes.org; the papers listed in `kb/rules/evidence.md`. Fastest version check: `npm view <pkg> time --json` and the PyPI JSON API (`https://pypi.org/pypi/<pkg>/json`) give every release date in one call each; then `gh release view` for the notes of anything new. Noisy: "best chart libraries <year>" listicles, scraped MCP directories, and web searches for "Chart.js 5" (they return Drupal module pages).

## Findings log

### R-20261030-1 · 2026-10-30 · plotly.js 4.2.0; quiet elsewhere
- Subject: plotly.js 4.2.0 (2026-10-29) adds `layout.legend.itemheight` and ternary spikelines and fixes an XSS through javascript: links in MathJax text; no chart-type change, cw.py unaffected. Mermaid: no release after 12.2.0 (develop has flowchart step numbers and ELK 0.12 pending). Chart.js 4.6.1, vl-convert and ECharts unchanged. Tooling: Flint 1.0 (2026-10-21) already logged; community chart skills found only on SEO registries. Practice and testing: nothing new.
- Track: subject. Sources: https://github.com/plotly/plotly.js/releases/tag/v4.2.0, https://registry.npmjs.org/mermaid
- magnitude 0.1 · applied: none (Current understanding edited)

Newest first.

### R-20261023-4 · 2026-10-23 · Quiet elsewhere (subject, tooling, practice, testing tracks)
- Summary: Unchanged since 2026-10-14: mermaid 12.2.0, @mermaid-js/mermaid-cli 12.0.0 (cw.py pin current), vega-lite 6.5.0, vl-convert 1.9.0.post1 with 2.0.0rc7 newest, plotly.js 4.1.2, plotly.py 7.1.0, kaleido 1.5.0, echarts 6.1.0, matplotlib 3.11.2, altair 6.3.0, python-pptx 1.0.2, apexcharts-mcp 0.10.3. `npm view @antv/mcp-server-chart version` returns 0.9.10 (modified 2026-09-21), so the 0.11.10 recorded on 2026-10-14 was wrong. Downloads in the week to 2026-10-22: antvis 2,193, flint-chart-mcp 1,610, apexcharts-mcp 470. New MCP registry "chart" entries are noise or narrow (cleanchart, regiabi chart-mcp, trade-chart). anthropics/skills: no commits since 2026-10-09. Practice: nothing new (an openai/plugins data-visualization router skill on Tessl is an unconfirmed lead). Testing: nothing new beyond RealChart2Code, Chart2Code, PlotCraft and Text2Vis.
- Track: subject, tooling, practice, testing
- Sources: https://registry.npmjs.org, https://pypi.org, https://api.npmjs.org/downloads/point/last-week/@antv/mcp-server-chart, https://registry.modelcontextprotocol.io/v0/servers?search=chart&limit=100, https://github.com/anthropics/skills/commits/main
- Magnitude: 0.1
- Applied: C-20261023-1 (RESEARCH.md only)

### R-20261023-3 · 2026-10-23 · Flint 1.0: interactions, Image-Charts backend, PNG/SVG from the MCP server (tooling track)
- Summary: Flint 1.0 (2026-10-21; flint-chart and flint-chart-mcp 1.0.1) adds linked brushing, annotations, semantic zoom and chart-table views, an Image-Charts backend (hosted image URL), and static PNG or SVG from the MCP server (resvg and napi-rs canvas); a Python port is in preview. Still no Mermaid, Markdown or PowerPoint target, no evidence-based type selection, no published benchmark. SKILL.md's "compiles to ... only" list was incomplete. Response: point (corrected the list), do not delegate.
- Track: tooling
- Sources: https://github.com/microsoft/flint-chart/releases, https://registry.npmjs.org/flint-chart-mcp/latest
- Magnitude: 0.3
- Applied: C-20261023-1

### R-20261023-2 · 2026-10-23 · Chart.js 4.6.0 and 4.6.1 (subject track)
- Summary: First releases since 2025-10 (both 2026-10-22). 4.6.0: pie, doughnut and polar-area spacing fix, scale-title stroke, filler no longer overshoots with `offset: true`, integer canvas dimensions (can shift pixels in image diffs). 4.6.1: trusted-publishing fix only. Nothing breaking, no new chart types, no v5 sign. cw.py loads `chart.js@4` from jsDelivr, so pages pick up 4.6.1.
- Track: subject
- Sources: https://github.com/chartjs/Chart.js/releases/tag/v4.6.0, https://registry.npmjs.org/chart.js
- Magnitude: 0.15
- Applied: C-20261023-1 (RESEARCH.md only)

### R-20261023-1 · 2026-10-23 · Obsidian 1.15.0 drops Mermaid for Pele (subject track; tooling note)
- Summary: Obsidian 1.15.0 Desktop (2026-10-22, Catalyst early access) says Obsidian no longer includes Mermaid; diagrams render with its own library Pele, "compatible with the latest Mermaid 12.1.0 syntax", with `.pele-*` classes and `--mermaid-*` CSS variables, and the "Show Mermaid diagrams" setting is gone. Public users stay on 11.13 until general release; once public, GitHub (11.16.1) becomes the portable floor. Pele's layout differs from Mermaid and the changelog lists no supported types, so xychart (non-beta) and named-series support are unconfirmed; default emission stays `xychart-beta` at the 11.13 floor. Pele itself (npm 1.9.0, MIT, zero dependencies, synchronous `render(text)` to SVG, claims every Mermaid 12.1.0 diagram type, no CLI or PNG) may be a browserless check; headless Node use is not stated. Response: note, revisit when 1.15 is public.
- Track: subject, tooling
- Sources: https://obsidian.md/changelog/2026-10-22-desktop-v1.15.0/, https://github.com/obsidianmd/pele, https://registry.npmjs.org/pele/latest
- Magnitude: 0.35
- Applied: C-20261023-1 (RESEARCH.md Current understanding, Open questions, Search plan)

### R-20261014-3 · 2026-10-14 · Quiet elsewhere; forum lines added to the search plan (subject, tooling, practice, testing tracks)
- Summary: Registries on 2026-10-14: plotly.py 7.1.0, chart.js 4.5.1, echarts 6.1.0, @observablehq/plot 0.6.17, matplotlib 3.11.2, altair 6.3.0, python-pptx 1.0.2, vl-convert 1.9.0.post1 stable with 2.0.0rc7 newest, flint-chart 0.5.1, @antv/mcp-server-chart 0.11.10 on npm (no GitHub release since 0.9.10), @mermaid-js/mermaid-cli 12.0.0 (the cw.py pin). anthropics/skills: only claude-api skill commits since 2026-10-03, no chart or dataviz change. Forums: Mermaid Discussions have a 2026-09-25 Q&A on layout changes between 11.12 and 12.0 (the ELK default already recorded); Plotly forum, Chart.js Discussions and Obsidian changelogs had nothing new for charts. Practice: no new agent chart workflow beyond Flint and the vendor MCP servers. Testing: no chart benchmark newer than RealChart2Code (arXiv 2603.25804) and Chart2Code (ACL 2026), both known; testing: nothing new. The search plan had no vendor-forum lines; added with URLs.
- Track: subject, tooling, practice, testing
- Sources: https://registry.npmjs.org, https://pypi.org, https://github.com/mermaid-js/mermaid/discussions, https://community.plotly.com, https://obsidian.md/changelog/2026-09-29-desktop-v1.14.3/, https://github.com/anthropics/skills/commits, https://arxiv.org/abs/2603.25804
- Magnitude: 0
- Applied: C-20261014-1 (RESEARCH.md Search plan only)

### R-20261014-2 · 2026-10-14 · ApexCharts ships an official MCP server (tooling track)
- Summary: `apexcharts-mcp` (github.com/apexcharts/apexcharts-mcp, npm since 2026-04-28, 18 versions, 0.10.3 on 2026-10-14; hosted at mcp.apexcharts.com/mcp) entered the official MCP registry on 2026-10-07. It exposes ApexCharts knowledge and generates and validates configs for charts, grid, gantt, tree, sankey, stock and maps. About 2,051 npm downloads in the week to 2026-10-12, against 3,948 for @antv/mcp-server-chart and 1,851 for flint-chart-mcp. Single-library, no evidence-based type selection, ApexCharts is not a chartwright target. Note only; revisit if ApexCharts becomes a target.
- Track: tooling
- Sources: https://registry.modelcontextprotocol.io/v0/servers?search=apexcharts, https://apexcharts.com/docs/ai/mcp/apexcharts/, https://api.npmjs.org/downloads/point/last-week/apexcharts-mcp
- Magnitude: 0.2
- Applied: C-20261014-1 (RESEARCH.md Current understanding only)

### R-20261014-1 · 2026-10-14 · Mermaid 12.2.0, Vega-Lite 6.5.0, plotly.js 4.1.2, kaleido 1.5.0 (subject track)
- Summary: Mermaid 12.2.0 (2026-10-13): opt-in mindmap `colorBy: depth`, ELK label and edge fixes, swimlane fixes; no xychart or chart-type change. Vega-Lite 6.5.0 (2026-10-08): exponential moving average transform, tooltip field filtering, fixes for facet sort with aggregates, missing facet data and explicit axis formats on normalized stacks; additive, no spec break. plotly.js 4.1.2 (2026-10-05): ResizeObserver resizing, image-export type fixes, redraw on font load; cw.py still loads 4.1.1 from the CDN, which is fine. kaleido 1.5.0 (2026-10-06): drops Python 3.8 and orjson, still needs Chrome. Host floors and every SKILL.md claim unchanged; the knowledge base's `version_checked` lines (kb/targets/plotly.md, vega-lite.md, matplotlib.md) lag by a patch or minor and can be bumped on the next chartwright-curate pass.
- Track: subject
- Sources: https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.2.0, https://github.com/vega/vega-lite/releases/tag/v6.5.0, https://github.com/plotly/plotly.js/releases/tag/v4.1.2, https://github.com/plotly/Kaleido/releases/tag/v1.5.0
- Magnitude: 0.1
- Applied: C-20261014-1 (RESEARCH.md Current understanding only)

### R-20261003-3 · 2026-10-03 · Quiet elsewhere (subject, tooling, practice, testing tracks)
- Summary: Registries checked on 2026-10-03: vega-lite 6.4.3, plotly.js 4.1.1, plotly.py 7.1.0, kaleido 1.4.0, chart.js 4.5.1, echarts 6.1.0, @observablehq/plot 0.6.17, matplotlib 3.11.2, python-pptx 1.0.2, vl-convert 1.9.0.post1 stable with 2.0.0rc7 newest; all as on 2026-09-17. antvis/mcp-server-chart: no GitHub release since 0.9.10 (2026-02-25). anthropics/skills and claude-plugins-official: no chart or dataviz changes since 2026-09-17. Practice: nothing new beyond Flint (R-20261003-2). Testing: no chart benchmark newer than those already in the 2026-09-17 report (Chart2Code, RealChart2Code, PlotCraft); testing: nothing new.
- Track: subject, tooling, practice, testing
- Sources: https://registry.npmjs.org, https://pypi.org, https://github.com/anthropics/skills/commits, https://github.com/antvis/mcp-server-chart/releases
- Magnitude: 0
- Applied: none

### R-20261003-2 · 2026-10-03 · Flint is a standalone agent chart compiler and MCP server (tooling, practice tracks)
- Summary: Microsoft Research and Renmin University's Flint, known on 2026-09-17 only as Data Formulator's internal chart language, now ships as `flint-chart` (TypeScript) and `flint-chart-mcp` (also hosted at flint.data-formulator.ai/mcp), MIT, about 4.3k stars, 0.5.1 on 2026-08-14, paper arXiv 2607.20775 (2026-07). The agent writes a compact semantic spec (70+ semantic field types, templates, named themes such as Economist or NYT); a deterministic compiler emits Vega-Lite, ECharts, Chart.js, Plotly or editable Excel. Same principle as chartwright (template plus parameters over generated code) and overlaps four of its sixteen targets; it has no evidence-based type selection, no Mermaid or other Markdown target, no PNG/SVG file path for documents and no PowerPoint. A comparable, well-used, maintained tool: point to it, do not delegate.
- Track: tooling, practice
- Sources: https://github.com/microsoft/flint-chart, https://www.microsoft.com/en-us/research/blog/flint-a-visualization-language-for-the-ai-era/, https://arxiv.org/abs/2607.20775
- Magnitude: 0.4
- Applied: C-20261003-1

### R-20261003-1 · 2026-10-03 · Mermaid 12.1.0 (subject track)
- Summary: Released 2026-10-02. ELK `orientFeedbackEdges` on by default (changes some ELK flowchart layouts), packet `bitOrder`, error diagrams now print the real parse message under "Syntax error in text" (helps verify Mermaid output when a host shows only the SVG), partial `xyChart` theme-variable overrides keep the generated defaults, gantt warns on unknown `after` ids. No chart-type or xychart syntax change; hosts still lag, so the portable floor (11.13, `xychart-beta`) is unchanged.
- Track: subject
- Sources: https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.1.0
- Magnitude: 0.1
- Applied: none (RESEARCH.md Current understanding only)

### R-20260917-2 · 2026-09-17 · Library and target landscape (tooling, testing tracks)
- Summary: Measured versions, downloads and velocity for Mermaid, Vega-Lite, Plotly, Chart.js, ECharts, Observable Plot, D3, Recharts, Highcharts, matplotlib, seaborn, plotnine, Altair, bokeh; Mermaid host versions (GitHub, GitLab, Obsidian, Azure DevOps, Docusaurus, MkDocs); Office chart APIs; agent chart tools (antvis MCP and skills, Anthropic dataviz and data-visualization skills, QuickChart, Vega-Lite MCPs, Kroki); token-efficiency techniques with evidence. Full report `../../ai-docs/research/2026-09-17-libraries-and-render-targets.md`.
- Track: tooling, testing
- Sources: https://github.com/mermaid-js/mermaid/releases, https://mermaid.js.org/syntax/xyChart.html, https://github.com/vega/vl-convert, https://github.com/plotly/plotly.py/blob/main/CHANGELOG.md, https://github.com/antvis/mcp-server-chart, https://arxiv.org/abs/2601.15385, https://arxiv.org/abs/2401.11255
- Magnitude: n/a (initial)
- Applied: C-20260917-1

### R-20260917-1 · 2026-09-17 · Chart taxonomy and selection evidence (subject, practice tracks)
- Summary: Cross-referenced the FT Visual Vocabulary, Data Visualisation Catalogue, From Data to Viz, Abela, the Vega-Lite, Plotly, ECharts and Mermaid galleries, and Datawrapper/Flourish menus into one taxonomy with rising and declining types; collected the perception evidence (Cleveland and McGill, Heer and Bostock, Skau and Kosara, Franconeri et al., Bateman et al.) and practitioner rules; surveyed how LLM systems choose charts (Draco, CompassQL, LIDA, Data Formulator, VegaChat) and the benchmarks (nvBench 2.0, VisEval, ChartMimic, Chart2Code). Full report `../../ai-docs/research/2026-09-17-chart-taxonomy-and-evidence.md`; distilled into `kb/rules/`.
- Track: subject, practice
- Sources: https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://datavizcatalogue.com, https://www.data-to-viz.com, https://www.datawrapper.de/blog/chart-types-guide, https://journals.sagepub.com/doi/10.1177/15291006211051956, https://eagereyes.org/pie-charts
- Magnitude: n/a (initial)
- Applied: C-20260917-1
