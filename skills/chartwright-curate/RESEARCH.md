# Research: chartwright-curate

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the evergreen plugin's `protocol/PROTOCOL.md`. Full research notes: `../../ai-docs/research/`.

Topic: sources for chart taxonomy, perception evidence, and library chart menus used to grow the chart knowledge base. Tier `moderate`. Last refresh 2026-09-17; next due 2026-10-17.

## Current understanding

- The reference taxonomies disagree in granularity, not substance: the FT Visual Vocabulary (about 70 types in 9 families) is the best spine; the Data Visualisation Catalogue has the widest name list; From Data to Viz keys on data shape; tool galleries (Vega-Lite, Plotly, ECharts, Observable Plot, Mermaid) show what is buildable and what is rising. A new chart type earns a file when it appears in two or more of these or in a library release note of the last three years.
- Evidence sources are stable and few: Cleveland and McGill 1984, Heer and Bostock 2010, Skau and Kosara 2016, Franconeri et al. 2021, Bateman et al. 2010, plus eagereyes.org and datawrapper.de for practitioner synthesis. New perception studies appear a few times a year; OpenAlex and Semantic Scholar searches catch them.
- Velocity signals that work: library release notes (ECharts 6 added chord and beeswarm; Mermaid 11.6 radar, 12.0 treemap and venn; Observable Plot's dodge and voronoi), Datawrapper and Flourish menu changes, npm and PyPI download trends. Signals that mislead: all-time GitHub stars, listicles.
- The knowledge base schema (`kb/SCHEMA.md`) is validated by `cw.py --strict validate`; the authoring standard is `ai-docs/notes/kb-authoring-brief.md`.

## Open questions

- Whether to add ECharts as a sixth target first, or Office (python-pptx) native charts; both were researched 2026-09-17 and neither is built.
- Whether Datawrapper added marimekko natively in 2024 (unverified in the taxonomy research).

## Search plan

Subject:

- `site:datawrapper.de/blog chart <year>`, `site:eagereyes.org <year>`, `flourish new template <year>`, `datawrapper new chart type <year>`
- `"visual vocabulary" chart types update`, `datavizcatalogue new`, `"from data to viz" update`
- OpenAlex `works?search=chart perception study&sort=publication_date:desc`; Semantic Scholar for citations of Franconeri 2021

Tooling:

- `path:SKILL.md chart OR visualization` on GitHub code search sorted by recently updated; `npx skills find chart`; skills.sh weekly installs for "chart" and "dataviz"
- `https://registry.modelcontextprotocol.io/v0/servers?search=chart`; `antvis/mcp-server-chart` releases
- Library release pages: mermaid, vega-lite, vl-convert, plotly.js, chart.js, echarts, observable plot, matplotlib, seaborn, plotnine, altair

Practice:

- `"chart chooser" OR "chart recommendation" LLM <year> site:arxiv.org`; `Draco visualization constraints <year>`; `Data Formulator release`
- `site:github.com "visualization" "knowledge base" agent skill <year>`

Testing:

- `site:arxiv.org chart generation benchmark <year>` (nvBench 2.0, VisEval, ChartMimic, Chart2Code); `vega-lite spec validation`; `mermaid.parse`

Best sources: the FT chart-doctor repo, datavizcatalogue.com, data-to-viz.com, datawrapper.de/blog, eagereyes.org, the library release notes and galleries. Noisy: "best chart types" listicles, chart-type infographics without sources.

## Findings log

Newest first.

### R-20260917-1 · 2026-09-17 · Initial research (all four tracks)
- Summary: The two research passes recorded in `../../ai-docs/research/` (chart taxonomy and evidence; libraries and render targets) established the sources above, the rising and declining type lists (section 1.3 of the taxonomy report), the evidence set, and the agent-tooling landscape (antvis MCP and skills, Anthropic dataviz, QuickChart, Vega-Lite MCPs, Kroki; benchmarks nvBench 2.0, VisEval, ChartMimic, Chart2Code). The knowledge base was authored from them with a per-family fan-out and validated by `cw.py --strict validate`.
- Track: subject, tooling, practice, testing
- Sources: https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://datavizcatalogue.com, https://www.data-to-viz.com, https://www.datawrapper.de/blog/chart-types-guide, https://eagereyes.org/pie-charts, https://github.com/antvis/mcp-server-chart, https://github.com/microsoft/data-formulator
- Magnitude: n/a (initial)
- Applied: C-20260917-1
