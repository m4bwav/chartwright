# Research: chartwright

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the evergreen plugin's `protocol/PROTOCOL.md`. Full research notes: `../../ai-docs/research/`.

Topic: chart type selection evidence and the chart menus, syntax and versions of Mermaid, Vega-Lite, Plotly, Chart.js and matplotlib; how agents choose and build charts. Tier `fast`. Last refresh 2026-09-17; next due 2026-10-01.

## Current understanding

- Chart selection: the message picks the family (FT Visual Vocabulary's nine, plus hierarchy, relationship, single-value, table); within a family, prefer position and length encodings over angle, area and colour (Cleveland and McGill 1984; Heer and Bostock 2010). Pies are fine up to about 5 slices for part-to-whole "majority" questions (Skau and Kosara 2016). Layout decides which comparison is easy; annotate the intended one (Franconeri et al. 2021). Settled.
- Caps: about 5 lines, 3 grouped series, 4 stacked segments, 8 categorical hues; beyond, small multiples or a table. Practitioner consensus (Datawrapper, FT, dataviz skill). Settled.
- Targets (2026-09-17): Mermaid 12.0.0 (2026-09-10) adds treemap, venn, use case, agentflow and ELK default; hosts lag (GitHub 11.16.1, Obsidian 11.13, GitLab 11), so the portable floor is 11.13 and `xychart-beta`. Vega-Lite 6.4.3 with vl-convert 1.9.0.post1 (2.0.0rc7 in preview) is the best headless image path. plotly.js 4.1.1 / plotly.py 7.1.0 (2026-08/09 majors; mapbox traces removed; kaleido 1.x needs Chrome). Chart.js 4.5.1, no release since 2025-10. ECharts 6.1.0 (2026-05) is the strongest candidate for a sixth target (chord, beeswarm native, SSR). matplotlib 3.11.2. Moving.
- Agent practice: generated Vega-Lite specs fail far less than generated code (VegaChat 2026, arXiv 2601.15385: 0% vs 30.6% visualization errors); antvis/mcp-server-chart (4.4k stars, 26 tools) and antvis/chart-visualization-skills are the most used agent chart tools but render remotely and cost 5 to 8k tokens of schema per session; Anthropic's bundled `dataviz` skill covers palette and marks, not type selection. A CLI plus skill is the token-efficient shape. Contested only in that MCP servers keep growing.
- Token savings: read a compact index, pass data by file reference (a thousand inline rows costs 6 to 10k tokens), template plus parameters over code generation, validate specs mechanically before any retry. Settled.

## Open questions

- Which Mermaid version GitHub and Obsidian run after 2026-10 (decides when named xychart series and treemap can be emitted by default).
- Whether Chart.js 5 ships or the project stays flat (affects whether chartjs stays a first-class target).
- vl-convert 2.0 stable date (its `serve` mode could replace per-call rendering).

## Search plan

Subject:

- `mermaid release notes <month year>`, `mermaid.js.org/syntax/xyChart.html` (named series, legends), `site:github.com/orgs/community/discussions mermaid version`
- `vega-lite release`, `vl-convert release`, `plotly.js release notes`, `chart.js release`, `apache echarts release`, `matplotlib release`
- `"which chart" guide site:datawrapper.de <year>`, `"visual vocabulary" update`, `data visualization perception study <year>`

Tooling:

- `path:SKILL.md chart OR visualization` on GitHub code search sorted by recently updated; `npx skills find chart`; skills.sh weekly installs for "chart", "dataviz", "visualization"
- `https://registry.modelcontextprotocol.io/v0/servers?search=chart`; `antvis/mcp-server-chart` releases; `quickchart` releases
- `anthropics/claude-plugins-official` and `anthropics/skills` for chart or dataviz changes

Practice:

- `"claude code" OR codex OR cursor "chart" "vega-lite" OR mermaid workflow <year>`; hn.algolia.com `llm chart generation`
- `site:arxiv.org LLM chart generation OR visualization recommendation <year>` (Data Formulator, LIDA, VegaChat, Draco follow-ups)

Testing:

- `site:arxiv.org chart generation benchmark <year>` (nvBench 2.0, VisEval, ChartMimic, Chart2Code), `vega-lite schema validation`, `mermaid.parse` validation
- `path:SKILL.md chart evals` on GitHub

Best sources: mermaid.js.org and the mermaid GitHub releases; vega.github.io and vega/vl-convert releases; plotly changelogs; chartjs.org; echarts.apache.org; matplotlib release notes; datawrapper.de/blog; eagereyes.org; the papers listed in `kb/rules/evidence.md`. Noisy: "best chart libraries <year>" listicles, scraped MCP directories.

## Findings log

Newest first.

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
