# Research: chartwright-curate

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: the evergreen plugin's `protocol/PROTOCOL.md`. Full research notes: `../../ai-docs/research/`.

Topic: sources for chart taxonomy, perception evidence, and library chart menus used to grow the chart knowledge base. Tier `moderate`. Last refresh 2026-10-17; next due in `evergreen.json`.

## Current understanding

- The reference taxonomies disagree in granularity, not substance: the FT Visual Vocabulary (about 70 types in 9 families) is the best spine; the Data Visualisation Catalogue has the widest name list; From Data to Viz keys on data shape; tool galleries (Vega-Lite, Plotly, ECharts, Observable Plot, Mermaid) show what is buildable and what is rising. A new chart type earns a file when it appears in two or more of these or in a library release note of the last three years. Type boundaries are purpose-made scope choices, not one correct answer (Han, McNutt and Isaacs 2026, VIS preprint arXiv 2608.02512): when a request is near an existing type, decide alias or new file by whether the defining features differ, and say which features may vary. The FT chart-doctor repository (last commit 2024-03), the Data Visualisation Catalogue and From Data to Viz were unchanged on 2026-10-17; practitioner movement now shows first in tool menus (Datawrapper added dual-axis and waterfall in 2026-07).
- Evidence sources are stable and few: Cleveland and McGill 1984, Heer and Bostock 2010, Skau and Kosara 2016, Franconeri et al. 2021, Bateman et al. 2010, plus eagereyes.org and datawrapper.de for practitioner synthesis. New perception studies cluster around IEEE VIS (programme page ieeevis.org/year/YYYY/program/papers, papers public from about August); VIS 2026 brings a task-dependent revision of the channel ranking (Lee et al. 2026, arXiv 2608.04435) and an argument against further channel-ranking studies (Reda et al. 2026, arXiv 2608.07834). These refine, not overturn, Cleveland and McGill 1984. Practitioner stances can reverse: Datawrapper's 2018 dual-axis warning was withdrawn by its author in 2026 (Muth 2026-07-23), so cite a dated post, not "Datawrapper guidance".
- Velocity signals that work: library release notes (ECharts 6 added chord and beeswarm; Mermaid 11.6 radar, 11.8 treemap, 11.13 venn, 11.14 wardley, 12.0 use case and agentflow, 12.1 and 12.2 no chart types; Observable Plot's dodge and voronoi; Datawrapper dual-axis and waterfall 2026-07), Datawrapper and Flourish menu changes, npm and PyPI download trends. Signals that mislead: all-time GitHub stars, listicles.
- The knowledge base schema (`kb/SCHEMA.md`) is validated by `cw.py --strict validate`; the authoring standard is `ai-docs/notes/kb-authoring-brief.md`.

## Open questions

- Whether `dual-axis` earns its own chart file (offered natively by Chart.js, ECharts, Plotly, Excel combo charts and, since 2026-07, Datawrapper; the guidance was softened in place on 2026-10-17, R-20261017-2). Needs a support line and recipe for all 16 targets.
- Whether Datawrapper's arrow maps (2024) are an alias of `flow-map` or a type of their own.
- The VIS 2026 paper "Defaulting to Bar Charts: Chart-Type Bias and Scalar-Comparison Collapse in Autonomous Visualization Agents" had no preprint on 2026-10-17; read it after VIS (2026-11-09 to 11-13) and decide whether the chartwright skill needs a "not a bar" eval case (R-20261017-4).
- Resolved 2026-10-17: ECharts and pptx are both built targets (16 targets in `kb/targets/`). Datawrapper has no native marimekko: its 2024 recap lists only small-multiple lines and arrow maps as new types, and the current chart-types page has none.

## Search plan

Subject:

- `site:datawrapper.de/blog chart <year>`, `site:eagereyes.org <year>`, `flourish new template <year>`, `datawrapper new chart type <year>`
- `"visual vocabulary" chart types update` (or the commits page https://github.com/Financial-Times/chart-doctor/commits/main), `datavizcatalogue new`, `"from data to viz" update`
- Read the blog index pages directly, since search engines miss new posts: https://www.datawrapper.de/blog (blog.datawrapper.de redirects there) and https://flourish.studio/blog/
- IEEE VIS programme: https://ieeevis.org/year/<year>/program/papers (about 275k characters, read with offsets; search engines did not find VIS titles, this page did)
- OpenAlex with relevance sort plus a `from_publication_date` filter, or `title.search` (`sort=publication_date:desc` returned only noise on 2026-10-17, and one 429); Semantic Scholar for citations of Franconeri 2021
- Vendor forums (announcements first, then known issues since `last_checked`): Vega-Lite GitHub Discussions https://github.com/vega/vega-lite/discussions; Observable Plot https://github.com/observablehq/plot/discussions; ECharts https://github.com/apache/echarts/discussions; Mermaid https://github.com/mermaid-js/mermaid/discussions and the release list (`gh release list -R mermaid-js/mermaid`; read the release bodies for "new diagram" lines); Datawrapper has no public forum, use its blog and Academy (https://www.datawrapper.de/academy); Flourish help center https://helpcenter.flourish.studio (refuses fetch with 403) and its blog

Tooling:

- `path:SKILL.md chart OR visualization` on GitHub code search sorted by recently updated; `npx skills find chart`; skills.sh weekly installs for "chart" and "dataviz"
- `https://registry.modelcontextprotocol.io/v0/servers?search=visualization` (search=chart is mostly charter boats and astrology); `antvis/mcp-server-chart` releases; Flourish Connector (an MCP connector that picks a template for the agent)
- skills.sh does not render through a fetch; use `npx skills find chart`. Tessl registry reviews (tessl.io/registry) are a usable quality signal for skills
- Library release pages: mermaid, vega-lite, vl-convert, plotly.js, chart.js, echarts, observable plot, matplotlib, seaborn, plotnine, altair

Practice:

- `"chart chooser" OR "chart recommendation" LLM <year> site:arxiv.org`; `Draco visualization constraints <year>`; `Data Formulator release`
- `site:github.com "visualization" "knowledge base" agent skill <year>`

Testing:

- `site:arxiv.org chart generation benchmark <year>` (nvBench 2.0, VisEval, ChartMimic, Chart2Code); `vega-lite spec validation`; `mermaid.parse`

Best sources: the FT chart-doctor repo, datavizcatalogue.com, data-to-viz.com, datawrapper.de/blog, eagereyes.org, the library release notes and galleries. Noisy: "best chart types" listicles, chart-type infographics without sources.

## Findings log

Newest first.

### R-20261017-5 · 2026-10-17 · Quiet tracks and baselines
- Summary: tooling: nothing new that does curation; the MCP registry's chart servers all generate charts (ApexCharts MCP 0.10.3, regiabi chart-mcp 0.6.47) and none chooses a type from evidence; Flourish's AI Assistant and Connector (2026-07-23) lets an agent pick a Flourish template, which makes Flourish's template list agent-facing. Practice: Data Formulator 0.8b1 (2026-08-15) and Draco 2 unchanged; the chart-choosing skills found are thin purpose-to-type maps without cited sources. Subject: FT chart-doctor, Data Visualisation Catalogue, From Data to Viz and eagereyes quiet; Datawrapper added keyboard navigation and reader font scaling (2026-10-14), an accessibility feature, no new type; Flourish posted a beeswarm guide (2026-09-14). Datawrapper marimekko: not native (open question resolved).
- Track: subject, tooling, practice
- Sources: https://registry.modelcontextprotocol.io/v0/servers?search=chart, https://helpcenter.flourish.studio/hc/en-us/articles/16487012057999-Flourish-Connector-an-intro, https://flourish.studio/blog/, https://github.com/microsoft/data-formulator/releases, https://github.com/cmudig/draco2, https://github.com/Financial-Times/chart-doctor/commits/main, https://www.datawrapper.de/blog
- Magnitude: 0.2 (largest: Flourish Connector, note)
- Applied: none (RESEARCH only)

### R-20261017-4 · 2026-10-17 · VIS 2026 names chart-type bias in visualization agents
- Summary: the VIS 2026 programme lists "Defaulting to Bar Charts: Chart-Type Bias and Scalar-Comparison Collapse in Autonomous Visualization Agents" (no preprint yet), ChartFI (arXiv 2605.23694, 896 chart-description pairs scored for faithfulness), MV-Bench, SciVisAgentBench and "Visualization Autocomplete". No new chart-recommendation benchmark with a 2609 or 2610 arXiv id. The bar-bias paper describes the failure chartwright's chooser exists to prevent; its eval case belongs to the chartwright skill, not this one.
- Track: testing, practice
- Sources: https://ieeevis.org/year/2026/program/papers, https://arxiv.org/abs/2605.23694
- Magnitude: 0.3
- Applied: none; open question carried (read after VIS 2026-11-09)

### R-20261017-3 · 2026-10-17 · VIS 2026 perception and taxonomy papers
- Summary: "Revisiting Channel Effectiveness" (Lee, Park, Chang and Seo; arXiv 2608.04435): seven channels on four tasks, the ranking shifts by task, position wins mainly through its fixed anchor, area is poor for accuracy but best for pop-out. "Marks, Channels, and Dead Ends" (Reda et al.; arXiv 2608.07834) argues for modelling charts as images. "On Defining Chart Types Boundaries" (Han, McNutt and Isaacs; arXiv 2608.02512) treats a type definition as a purpose-made scope choice, separating defining from variable features. Others in the programme: average estimates in line graphs biased toward high-variability regions, title framing and pattern identification in line charts, practice with uncertainty visualization, a ten-year colour discrimination replication.
- Track: subject (evidence)
- Sources: https://arxiv.org/abs/2608.04435, https://arxiv.org/abs/2608.07834, https://arxiv.org/abs/2608.02512, https://ieeevis.org/year/2026/program/papers
- Magnitude: 0.35 (refines the evidence set and the new-type rule; overturns nothing)
- Applied: C-20261017-3

### R-20261017-2 · 2026-10-17 · Datawrapper reverses its dual-axis stance and ships the type
- Summary: Lisa Charlotte Muth, who wrote Datawrapper's 2018 warning, published "Why I changed my mind on dual-axis charts" (2026-07-23, read 2026-10-17): dual axes suit readers "navigating a space" (when one moved, what did the other do), keep absolute levels that indexing loses, and are "sometimes fine"; the endorsement is narrow. Datawrapper added dual-axis and waterfall chart types (Business plan) the same month, with colour-keyed axes. The URL https://www.datawrapper.de/blog/dual-axis-charts that `connected-scatter.md` cited as the warning is now the launch post. The knowledge base said "never a dual axis" (grouped-bar), "index both to 100" (line, selection rule) and cited a "dual-axis warning" (evidence). Dual-axis is native in Chart.js, ECharts, Plotly, Excel combo charts and now Datawrapper, so it clears the two-source bar for its own file (open question).
- Track: subject
- Sources: https://www.datawrapper.de/blog/why-i-changed-my-mind-on-dual-axis-charts, https://www.datawrapper.de/blog/dual-axis-charts, https://www.datawrapper.de/blog/waterfall-charts
- Magnitude: 0.5 (a recommendation changed)
- Applied: C-20261017-2

### R-20261017-1 · 2026-10-17 · Mermaid treemap, venn and wardley predate 12.0
- Summary: the release bodies show treemap added in 11.8.0 ("new diagram type nested treemap"), `venn-beta` in 11.13.0 (the syntax page says v11.12.3+) and wardley in 11.14.0; 12.0.0 (2026-09-10) added only UML use case and agentflow, 12.1.0 (2026-10-02) and 12.2.0 (2026-10-13) no chart types. The knowledge base said treemap and venn needed 12.0 and would not render on GitHub (11.16.1) or Obsidian (11.13), so the chooser routed them to images needlessly. Both are at or above the floor; not yet tested on either host. The 2026-09-17 research note conflated 12.0's theme changes for venn with its arrival.
- Track: subject
- Sources: https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4011.8.0, https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4011.13.0, https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0, https://mermaid.js.org/syntax/venn.html (all read 2026-10-17 through gh)
- Magnitude: 0.5 (a recommendation changed: treemap and venn can stay in Markdown on current hosts)
- Applied: C-20261017-1

### R-20260918-1 · 2026-09-18 · Cycle plot (seasonal subseries plot): subject, evidence, support, build
- Question: what is a cycle plot, when does it beat a multi-line seasonal chart, and which targets draw it?
- Subject: introduced by Cleveland, Dunn and Terpenning (1978, SABL package, Bell Labs) to study the seasonal component of a decomposed series; popularised by Robbins (2008, Perceptual Edge guest article) and Cox (2006, Stata Journal). Aliases: seasonal subseries plot, month plot, subseries plot, cycle-subseries plot. Encoding: one mini time series per season (Jan..Dec, Mon..Sun, Q1..Q4) laid side by side on a shared y axis, each with a horizontal mean line; x within a panel is the cycle (year, week). Shows the seasonal level (mean lines) and the within-season trend at once, which neither an end-to-end line nor a one-line-per-year chart does. Needs a known period; rotate the season order so the months of interest sit in the middle; less useful when trend or oscillation dominates (decompose first). Works without colour.
- Evidence: no dedicated perception study found; the claim rests on Cleveland (1993, 1994) and Robbins (2005, 2008) plus position-on-common-scale results (Cleveland and McGill 1984). Rated medium. Hyndman and Athanasopoulos (FPP3 2.5) use it as a standard seasonal diagnostic.
- Popularity and velocity: native in R (stats::monthplot, forecast::ggsubseriesplot, feasts::gg_subseries), Python statsmodels (month_plot, quarter_plot), Stata (cycleplot). Not in the menus of Vega-Lite, Plotly, ECharts, Chart.js, Observable Plot, Datawrapper, Flourish, Mermaid or python-pptx (checked 2026-09-18); Tableau and Power BI need calculated fields or a marketplace visual (Nova Silva). Composable from faceted lines in any grammar. Niche, stable; no release-note movement in the last three years.
- Build: facet or column-per-season with a line mark plus a rule at the mean (Vega-Lite facet + layer; Plotly make_subplots shared_yaxes; ECharts one grid per season; Observable Plot fx facet with lineY and ruleY; matplotlib statsmodels.month_plot or one subplot per season; Chart.js one small chart per season; pptx/xlsx: line chart on a reshaped table with blank separator rows).
- Sources: https://www.perceptualedge.com/articles/guests/intro_to_cycle_plots.pdf, https://en.wikipedia.org/wiki/Seasonal_subseries_plot, https://otexts.com/fpp3/subseries.html, https://www.statsmodels.org/dev/generated/statsmodels.graphics.tsaplots.month_plot.html, https://stat.ethz.ch/R-manual/R-devel/library/stats/html/monthplot.html, https://rdrr.io/cran/feasts/man/gg_subseries.html, https://policyviz.com/2021/02/09/the-cycle-plot/, https://www.vizwiz.com/2022/08/cycle-plot.html, https://visuals.novasilva.com/power-bi-visual-cycle-plot/ (NIST handbook page 1.3.3.28 redirected on 2026-09-18, not read)
- Track: subject, evidence, popularity, build
- Magnitude: additive (new entry, no existing claim changed)
- Applied: C-20260918-4

### R-20260917-1 · 2026-09-17 · Initial research (all four tracks)
- Summary: The two research passes recorded in `../../ai-docs/research/` (chart taxonomy and evidence; libraries and render targets) established the sources above, the rising and declining type lists (section 1.3 of the taxonomy report), the evidence set, and the agent-tooling landscape (antvis MCP and skills, Anthropic dataviz, QuickChart, Vega-Lite MCPs, Kroki; benchmarks nvBench 2.0, VisEval, ChartMimic, Chart2Code). The knowledge base was authored from them with a per-family fan-out and validated by `cw.py --strict validate`.
- Track: subject, tooling, practice, testing
- Sources: https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://datavizcatalogue.com, https://www.data-to-viz.com, https://www.datawrapper.de/blog/chart-types-guide, https://eagereyes.org/pie-charts, https://github.com/antvis/mcp-server-chart, https://github.com/microsoft/data-formulator
- Magnitude: n/a (initial)
- Applied: C-20260917-1
