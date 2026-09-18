# Chart-type taxonomy and selection evidence (research notes, 2026-09-17)

Scope: data-visualization chart types (not knowledge graphs), cross-referenced against the FT Visual Vocabulary, the Data Visualisation Catalogue, From Data to Viz, Abela's Chart Chooser, Vega-Lite / Observable Plot / ECharts / Plotly galleries, Mermaid, and Datawrapper / Flourish menus. Items marked **[unverified]** were not confirmed against a primary source in this session (fetch failed or reliant on prior knowledge). Items marked **[memory]** come from working knowledge and should be spot-checked before publication.

---

## 0. Sources consulted (primary, fetched this session)

| Source | URL | Notes |
|---|---|---|
| FT Visual Vocabulary (chart-doctor repo) | https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary | 9 families, ~70 types, each with a one-line rule; fetched in full |
| Data Visualisation Catalogue | https://datavizcatalogue.com/ | 60+ methods, function-based index |
| From Data to Viz | https://www.data-to-viz.com/ | decision tree by data type (numeric / categoric / num+cat / maps / network / time series) |
| Vega-Lite example gallery | https://vega.github.io/vega-lite/examples/ | section headings fetched |
| Plotly Python gallery | https://plotly.com/python/ | categories fetched |
| ECharts series types | https://echarts.apache.org/en/llms.txt | 23 2D series types + 3D + GL |
| Observable Plot API | https://observablehq.com/plot/api (429 on fetch; marks confirmed via search summary and https://observablehq.com/@observablehq/plot-marks-cheatsheet) | |
| Mermaid diagram list | https://mermaid.js.org/intro/ | includes newer chart types (xychart, sankey, radar, treemap, quadrant) |
| Datawrapper: "A friendly guide to choosing a chart type" (Muth, 2025-06-16) | https://www.datawrapper.de/blog/chart-types-guide | six-goal decision procedure |
| Datawrapper: stacked column charts (Muth, Feb 2025) | https://www.datawrapper.de/blog/stacked-column-charts | |
| Datawrapper: dual-axis charts | https://www.datawrapper.de/blog/dual-axis-charts | |
| Datawrapper chart menu | https://www.datawrapper.de/charts | "23 interactive chart types" plus maps and tables |
| Flourish templates | https://flourish.studio/visualisations/ and https://flourish.studio/learn/chart-types/ | template names not enumerated by fetch **[partially unverified]** |
| Kosara, pie-chart series | https://eagereyes.org/pie-charts | Skau & Kosara EuroVis 2016 |
| Franconeri et al. 2021 | https://journals.sagepub.com/doi/10.1177/15291006211051956 (403 on fetch; abstract via PubMed https://pubmed.ncbi.nlm.nih.gov/34907835/) | |
| Cleveland & McGill 1984 ranking | summarized at https://homepage.divms.uiowa.edu/~luke/classes/STAT4580/percep.html | |
| Heer & Bostock 2010 | https://www.semanticscholar.org/paper/55d3281f6b34c50df975b7261044689bf73ec610 | |
| Bateman et al. 2010 "Useful Junk?" | https://vis.csail.mit.edu/classes/6.859/readings/pdfs/Bateman-UsefulJunk.pdf ; Kosara commentary https://eagereyes.org/criticism/chart-junk-considered-useful-after-all | |
| Raincloud plots (Allen et al. 2019) | https://discovery.ucl.ac.uk/id/eprint/10178652/ | |
| Okabe & Ito palette | https://jfly.uni-koeln.de/color/ (hex values live in the linked PDF, not the page) | |
| Draco / Draco 2 | https://idl.cs.washington.edu/files/2019-Draco-InfoVis.pdf ; https://idl.cs.washington.edu/files/2023-Draco2-VIS.pdf | |
| Data Formulator | https://github.com/microsoft/data-formulator | v0.7 stable 2026-05-28, v0.8 beta 2026-08-15 |
| LIDA | https://github.com/microsoft/lida | |
| nvBench 2.0 | https://arxiv.org/abs/2503.12880 ; https://github.com/HKUSTDial/nvBench-2.0 (NeurIPS 2025) | |
| Chart2Code hierarchical benchmark (ACL 2026) | https://arxiv.org/abs/2510.17932 | |
| LLM x Vis paper list | https://github.com/zengxingchen/LLM-Visualization-Paper-List | |
| Chartability | referenced via https://www.a11y-collective.com/blog/accessible-charts/ ; canonical https://chartability.fizz.studio/ **[unverified this session]** | |

Abela's original 2006 blog post redirected to a domain-parking page (extremepresentation.typepad.com is dead); the diagram content is confirmed via secondary copies (e.g. https://www.studocu.com/latam/document/universidad-autonoma-de-santo-domingo/didactica-general/choosing-a-good-chart-09-1/38072430). The 2009 PDF is still widely mirrored.

---

## 1. Cross-referenced taxonomy

### 1.1 How the reference taxonomies differ

- **FT Visual Vocabulary** (Smith et al., 2016 onward): organized by *the relationship you want to show* — Deviation, Correlation, Ranking, Distribution, Change over time, Magnitude, Part-to-whole, Spatial, Flow. Same chart can appear in several families (slope appears in Ranking and Change over time; waterfall in Part-to-whole and Flow; lollipop in Ranking and Magnitude). This is the most useful spine for a knowledge base because it maps to the *question*.
- **Abela Chart Chooser** (2006/2009): four branches — Comparison, Distribution, Composition, Relationship — then sub-questions (among items vs over time; how many variables; static vs changing over time). Simpler and older; it is the ancestor of most "chart chooser" posters. Criticized (informally, by e.g. Kosara and Muth **[memory]**) for treating "composition" too generously (recommends pies, stacked 100% areas) and for having no Spatial/Flow branches.
- **From Data to Viz** (Holtz & Healy): organized by *data shape* (Numeric / Categoric / Num & Cat / Maps / Network / Time series) and by how many variables. Its "caveats" pages are the best single collection of misuse notes (spaghetti plots, dual axis, radar, pie, truncated axis, etc.).
- **Data Visualisation Catalogue** (Ribecca): flat alphabetical list of ~60 methods, each tagged by function (comparisons, proportions, relationships, hierarchy, concepts, location, part-to-whole, distribution, how things work, processes, movement/flow, patterns, range, data over time, analysis, reference tools). Includes several diagram/"concept" types (brainstorm, flow chart, illustration diagram, Venn) that the FT excludes.
- **Library galleries** are organized by *mark/series type*: Vega-Lite (bar; histogram/density/dot; scatter & strip; line; area & streamgraph; table-based/heatmap; circular; error bars/bands; box plots; layered incl. candlestick, dual-axis, bullet; faceting/small multiples; repeat/concat incl. SPLOM; maps; interactive). Observable Plot exposes marks (area, arrow, bar, cell, dot, geo, image, line, link, raster, rect, rule, text, tick, tree, vector, contour, density) plus transforms (bin, group, stack, hexbin, dodge, window, normalize, map, tree) so that "chart types" are compositions. ECharts exposes 23 2D series types: line, bar, pie, scatter, effectScatter, radar, tree, treemap, sunburst, boxplot, candlestick, heatmap, map, parallel, lines, graph, sankey, funnel, gauge, pictorialBar, themeRiver, custom, and **chord** (new in ECharts 6, 2025), plus 3D (bar3D, line3D, scatter3D, surface, map3D, polygons3D) and GL variants. Plotly groups by Basic / Statistical / Scientific / Financial / Maps / 3D / Bioinformatics / ML.
- **Mermaid** (text-to-diagram): mostly software diagrams, but the chart set is now: pie, xychart (bar+line), quadrant chart, gantt, timeline, sankey, radar, treemap, venn, plus mindmap, kanban, packet, architecture, block, and newer Wardley / Cynefin / Ishikawa / event-modeling diagrams (marked new in the docs as of Sept 2026). No scatter, heatmap, or histogram.
- **Datawrapper** (23 chart types as of 2026, plus maps and tables): line, multiple lines (small multiples), area, stacked area?, column, stacked column, grouped column, small-multiple columns, bar, stacked bar, split bar, grouped bar, arrow plot, range plot, dot plot, scatter, bubble, pie, donut, multiple pies/donuts, election donut, treemap, waffle? **[menu items marked "?" unverified]**, choropleth, symbol, locator maps, and tables. Muth's 2025 guide lists these by goal: developments over time; shares/proportions; absolute numbers; correlations; flows (alluvial/Sankey — Datawrapper now has these **[unverified]**); geographic.
- **Flourish** (Canva): template gallery includes line/bar/pie, bar chart race, scatter, Sankey/alluvial, chord, hierarchy (treemap/sunburst/circle packing), network graph, parliament, projection map, marker map, table, survey (beeswarm/dot), sports bracket, quiz, story carousels **[template names from search summaries and prior knowledge; not enumerated from the gallery]**.

### 1.2 Consolidated list by FT family

Below, each type is given a canonical name, aliases, and where it appears (FT = FT Visual Vocabulary, DVC = Data Viz Catalogue, D2V = From Data to Viz, VL = Vega-Lite gallery, OP = Observable Plot, EC = ECharts, PL = Plotly, MM = Mermaid, DW = Datawrapper, FL = Flourish). Detailed per-type cards follow in section 2.

**Deviation** — diverging bar; diverging stacked bar (Likert); spine chart; surplus/deficit filled line (difference chart); waterfall (also part-to-whole/flow); bullet chart (target deviation).

**Correlation** — scatterplot; bubble chart; connected scatterplot; XY heatmap / matrix; line + column (dual axis); scatterplot matrix (SPLOM); hexbin; 2D density / contour; correlogram; parallel coordinates (also magnitude); quadrant chart (MM).

**Ranking** — ordered bar/column; ordered proportional symbol; dot strip plot; slope chart; lollipop; bump chart (rank over time); bar chart race (animated ranking, FL).

**Distribution** — histogram; density plot; box plot; violin; ridgeline (joyplot); raincloud; beeswarm; strip / jitter / dot strip; dot plot (Wilkinson); barcode plot; population pyramid; cumulative curve / ECDF; QQ plot; 2D histogram / hexbin; stem-and-leaf (DVC); error bars; range/band.

**Change over time** — line; multi-line and spaghetti; column; area; stacked area; streamgraph; step chart; slope; connected scatter; candlestick / OHLC; fan chart; range/band chart; calendar heatmap; horizon chart; sparkline; timeline / Priestley timeline; Gantt; circle timeline; seismogram; bump chart; arrow plot (DW); cycle plot **[memory]**; spiral plot (DVC).

**Magnitude** — bar/column; paired (grouped) bar; proportional stacked bar; proportional symbol / proportional area; isotype / pictogram; lollipop; radar / spider; parallel coordinates; radial bar / radial column / Nightingale rose (DVC); gauge (EC/PL); KPI / stat tile; table as visualization.

**Part-to-whole** — stacked column/bar; 100% stacked bar; pie; donut; treemap; sunburst; icicle; circle packing; Voronoi; arc / parliament; gridplot / waffle; dot matrix; Venn; waterfall; marimekko / mosaic; bar-of-pie **[Excel-specific]**; funnel.

**Spatial** — choropleth; proportional symbol (bubble) map; dot density map; flow map; contour / isopleth map; equalised cartogram (tile grid / hex map); scaled cartogram; heat map (gridded); hexbin map; connection map; locator map; 3D surface / terrain (PL/EC).

**Flow** — Sankey; alluvial / parallel sets; chord; arc diagram; network (node-link); waterfall; hierarchical edge bundling; flow map; tree / dendrogram (hierarchy); adjacency matrix.

**Outside the FT families but present in tool menus** — Gantt (project scheduling), quadrant chart, mind map / concept map, tree diagram / org chart, flow chart, word cloud, tally chart, timetable, Kagi / point-and-figure (specialist finance), ternary plot, 3D scatter/surface, volcano / Manhattan (bioinformatics), ROC/PR curves.

### 1.3 New or rising types (2023–2026 signal)

Based on presence across recent library releases and editorial tools (signal, not a rigorous measurement):

- **Rising / now mainstream**: beeswarm (native in Observable Plot's dodge transform, Flourish "survey", Datawrapper "dot plot"?), raincloud (Allen et al. 2019, now in R `ggrain`, Python `ptitprince`, JASP), ridgeline (`ggridges`, Plotly, seaborn recipes), bump chart (`ggbump`, FT sports), dumbbell / range plot (DW "range plot", `ggalt`), lollipop, waffle, hexbin (OP transform, D2V), marimekko (DW 2024 **[unverified]**), calendar heatmap (EC calendar coordinate, GitHub contribution graph made it universal), horizon chart (niche but stable), small multiples (first-class in DW 2023–2024 "multiple lines"/"small multiple columns" — https://www.datawrapper.de/blog/small-multiple-line-charts), chord (ECharts 6 added `series-chord`), Sankey/alluvial (Mermaid, DW, FL, EC, PL all support), sunburst/icicle (EC, PL, VL via Vega), Voronoi (OP `voronoi` mark, D3), arrow plot (DW).
- **Stable / evergreen**: bar, line, scatter, histogram, box, heatmap, pie/donut, treemap, choropleth, stacked bar/area.
- **Declining or discouraged**: 3D bar/pie (no serious tool promotes), radar for comparison across many entities (FT allows it "if variables organised sensibly"; D2V lists caveats), dual-axis line (Datawrapper offers it but warns; https://www.datawrapper.de/blog/dual-axis-charts), word cloud (DVC lists; most guides discourage), stacked area with many series (spaghetti/streamgraph problems), gauge (dashboard cliché), exploded pie, bar-of-pie.
- **Rising in AI/dashboard context**: KPI/stat tiles with sparklines, table-as-visualization (heat-coloured tables, inline bars; Datawrapper tables, Flourish tables, Observable "table" inputs), and text-first "big number" displays.

---

## 2. Chart cards

Format: **Name** (aliases) — FT family — question — data shape — use — avoid/misuse — evidence — accessibility — substitute — support/velocity.

Perceptual shorthand used below: "C&M rank" refers to Cleveland & McGill (1984), *Graphical Perception*, JASA 79(387): position on common scale > position on non-aligned scales > length/direction/angle > area > volume/curvature > shading/colour saturation. Heer & Bostock (2010, CHI) replicated this ranking on Mechanical Turk and added rectangular area (treemap) and circular area (bubble), both worse than length. Franconeri et al. (2021, *Psychological Science in the Public Interest* 22(3)) synthesize: viewers extract global statistics fast, shapes fast, but pairwise comparisons slow; visual comparisons across separated regions are error-prone; annotation and direct labelling reduce cognitive load; colour and axis manipulation are the main sources of misleading charts.

### 2.1 Magnitude and ranking

**Bar chart** (column chart when vertical; horizontal bar) — Magnitude / Ranking — "how big is each category; which is largest?" — 1 categorical + 1 quantitative; optionally a second categorical for grouped/stacked. — Use: comparing amounts across categories; horizontal bars when labels are long; sort by value unless categories have intrinsic order. — Avoid: truncated baseline (bars must start at zero — FT: "Must always start at 0"), too many categories (>~15 becomes a table), using bars for continuous time with irregular intervals. — Evidence: length + position on common scale; top of C&M ranking. — Accessibility: works well with direct value labels; keep sort order consistent; provide data table. — Substitute: lollipop (when many bars create ink density), dot plot (when baseline zero is not meaningful), table. — Support: universal; stable.

**Grouped bar** (clustered, paired column, multi-set bar) — Magnitude — "how do 2–3 series compare within each category?" — 1 categorical x 1 small categorical x quantitative. — Use: 2 series (FT: "tricky with more than 2"). — Avoid: >3 series (use small multiples or dot plot); comparing across groups is hard because bars are not adjacent. — Substitute: dot plot / dumbbell, small multiples, slope. — Support: universal.

**Stacked bar / stacked column** — Part-to-whole / Magnitude — "what is the total and how does it split?" — 1 categorical x categorical parts x quantitative. — Use: emphasis on total with one important part placed at the baseline (Muth 2025). — Avoid: comparing non-baseline segments across bars (different baselines); >~10 columns; irregular time intervals (use line/area). — Evidence: only the bottom segment is on a common scale; others are length-only comparisons (C&M second tier). Datawrapper Feb 2025: "hard for readers to compare columns that don't start at the same baseline… consider split bars or small multiples." — Substitute: small multiples of simple bars, split bars, line chart for shares over time. — Support: universal.

**100% stacked bar** (proportional stacked bar, normalized) — Part-to-whole — "what share does each part have, across categories?" — same as stacked bar, normalized. — Use: comparing shares of first and last segment across rows; Likert/diverging stacked bars for survey data (FT: "perfect for survey results which involve sentiment", centre at neutral). — Avoid: reading middle segments; hiding totals (add n). — Substitute: multiple pies/donuts, waffle grid, slope for two time points.

**Diverging bar** — Deviation — "which are above/below the reference (zero, target, average)?" — 1 categorical + signed quantitative. — Use: positive/negative values, change vs baseline. — Avoid: colour-only sign encoding without labels (colour-vision users). — Support: universal.

**Lollipop** — Ranking / Magnitude — same as bar with less ink. — Use: many categories, values close in magnitude where the dot's position does the work. FT notes it "does not HAVE to start at zero" because the reader reads the dot position, not the stem length. — Avoid: when precise length comparison matters. — Support: ggplot2 (`geom_segment`+`geom_point`), Plot, D2V, Datawrapper (via dot plot). Rising.

**Dot plot (Cleveland dot plot)** — Magnitude / Ranking / Distribution — "what is each category's value, and its range?" — 1 categorical + 1–3 quantitative. — Use: comparing 2–3 values per category (min/max, before/after) with position on a common scale; baseline need not be zero. — Evidence: Cleveland (1984, *The Elements of Graphing Data*) proposed it as the perceptually superior alternative to bars. — Substitute: dumbbell/range plot when showing two endpoints. — Support: DW "dot plot" and "range plot", Plot dot mark, ggplot2. Rising.

**Dumbbell / range plot** (connected dot plot, barbell, gap chart) — Deviation / Change — "how did each category move between two states; what is the gap?" — 1 categorical + 2 quantitative (same unit). — Use: before/after, gender gap, min/max. — Avoid: >2 points per row (use slope or line). — Substitute: slope chart, arrow plot (DW). — Support: DW, `ggalt`, Plotly via shapes, Plot link mark. Rising.

**Slope chart (slopegraph)** — Ranking / Change over time — "how did values or ranks change between two (or three) points?" — categorical x 2–3 ordered time points x quantitative. — Use: showing rank changes; Storytelling with Data recommends it for two-period comparisons with direct labels (https://www.storytellingwithdata.com/blog/2020/2/19/what-is-a-slopegraph — page 404'd this session; claim from prior knowledge **[unverified URL]**). — Avoid: many crossing lines with similar values (label clutter). — Substitute: dumbbell, bump chart (more periods). — Support: VL example, D3, DW (as line chart), Flourish line. Stable.

**Bump chart** (rank chart) — Ranking / Change over time — "how did ranks change over many periods?" — entity x time x rank. — Use: ordinal ranks only (equal spacing hides magnitude). — Avoid: when magnitude differences matter — use line chart of values. — Substitute: line chart, ribbon/bump-area (Flourish "line chart race"). — Support: `ggbump`, Flourish, Plot via line + rank transform. Rising (sports, charts, elections).

**Bar chart race** — Ranking over time (animated) — engagement piece; poor for precise reading; evidence of memorability but not accuracy **[memory]**. Support: Flourish (its signature template), Plotly animation. Peaked ~2019–2021, still common.

**Proportional symbol / proportional area chart** (bubble comparison, circle comparison) — Magnitude — "roughly how big is each?" — 1 categorical + 1 quantitative. — Use: very large range of values, precision not needed (FT). — Avoid: fine comparisons (circular area is near the bottom of C&M; Heer & Bostock confirmed area is poorer than length). Always scale by area, never radius. — Substitute: bar (log-scale if range is extreme). Stable.

**Pictogram / isotype** (unit chart) — Magnitude / Part-to-whole — "how many units?" — count data. — Use: whole numbers, general audiences; FT: "do not slice off an arm". — Evidence: Haroz, Kosara & Franconeri 2015 ("ISOTYPE Visualization: Working Memory, Performance, and Engagement with Pictographs", CHI) found pictographs did not hurt accuracy and helped memory when icons carry meaning **[memory]**. — Support: DW, Flourish, D3. Stable.

**Radar / spider chart** — Magnitude — "what is the profile of one entity across 5–10 variables?" — 1 entity (or few) x N quantitative on comparable scales. — Use: profile comparison of few entities; FT: "make sure variables are organised sensibly". — Avoid: many entities (overlap), variables on different units, reading the enclosed area (area is meaningless and depends on axis ordering). D2V caveat page. — Substitute: parallel coordinates, small-multiple bars, heatmap. — Support: EC, PL, Mermaid (new), Chart.js; not in DW. Stable but discouraged.

**Parallel coordinates** — Magnitude / Correlation — "how do many entities compare across many dimensions; which correlate?" — N entities x M quantitative. — Use: exploratory, high-dimensional, with brushing. — Avoid: static presentation for general audiences; axis order changes what you see. — Substitute: SPLOM, heatmap, PCA scatter. — Support: EC, PL, D3, VL (via fold + line). Stable (analytics only).

**Gauge / meter** — Magnitude vs target — single value in a range. — Avoid: wastes space; angle encoding. — Substitute: bullet chart, KPI tile with progress bar. — Support: EC, PL, dashboards. Declining in design guidance, persistent in BI.

**Bullet chart** (Few 2006) — Deviation / Magnitude — "how does actual compare to target and qualitative bands?" — 1 quantitative + target + 2–3 band thresholds. — Use: dashboards, replacing gauges. — Support: VL example, Plotly indicator, D3. Stable niche.

**KPI / stat tile / big number** — Magnitude — "what is the current value and its change?" — single value + delta + optional sparkline. — Use: dashboards; Datawrapper's "simple text" recommendation when only one number matters. — Avoid: red/green deltas alone; tiles without time context. — Substitute: sparkline + value; table. — Support: every BI tool; Plotly `indicator`. Rising.

**Sparkline** (Tufte 2006) — Change over time — "what is the recent shape of the trend?" — time x quantitative, inline. — Use: tables, tiles, many series. — Avoid: axes/labels (the point is word-sized); reading exact values. — Support: DW tables, Plot, D3, Excel. Stable.

**Table as visualization** (heat table, table with inline bars, ranked table) — Magnitude / Ranking — "look up exact values and scan for patterns." — Use: when precise values matter or many measures; add colour scale/bars; Muth: "dot plots or tables for extensive datasets". — Accessibility: the most screen-reader-friendly format; always provide as a fallback. — Support: DW tables, Flourish table, Observable, Vega-Lite (text/rect marks). Rising.

### 2.2 Change over time

**Line chart** — Change over time — "how does a value change; what is the trend?" — ordered time x quantitative; 1–~5 series (Datawrapper/FT guidance **[memory: exact limits vary]**). — Use: continuous, regularly sampled series; multi-line with direct labels on the right; markers if irregular (FT). — Avoid: spaghetti (>5–7 undifferentiated lines — use small multiples or grey background + highlight), y-axis needn't start at zero but say so; line for categorical x-axes. — Evidence: position on common scale; slope perception is biased by aspect ratio (Cleveland's banking to 45°; Heer & Agrawala 2006 "Multi-Scale Banking" **[memory]**). — Accessibility: label lines directly (not by colour legend); use line style variation; Franconeri et al. stress direct labelling. — Substitute: slope chart (2 points), small multiples, area (single series with zero baseline). — Support: universal.

**Small multiples** (trellis, facet, panel chart, lattice) — meta-type — "how does the same pattern vary across categories?" — any chart x categorical facet. — Use: >4 series, comparing shape not exact values; share axes; Datawrapper made these first-class ("multiple lines", "small multiple columns"). — Avoid: differing axes across panels without warning; tiny panels below ~100 px. — Evidence: Tufte; Franconeri et al. on limits of simultaneous comparison; small multiples convert slow cross-region comparisons into parallel shape recognition. — Support: VL facet, Plot facet, ggplot2 facets, DW, Plotly subplots. Rising.

**Area chart** — Change over time / Magnitude — "how does a total change?" — time x quantitative (1 series). — Use: single series where volume matters; baseline must be zero. — Avoid: multiple overlapping areas (occlusion); non-zero baseline. — Substitute: line. Stable.

**Stacked area** — Change / Part-to-whole — "how does the total change and how do parts contribute?" — time x parts x quantitative. — Use: total + ≤4 parts, bottom series is the one readers must read accurately (FT: "seeing change in components can be very difficult"). — Avoid: reading middle streams; many series. — Substitute: small-multiple lines, 100% stacked area for share, line chart of shares. Stable.

**Streamgraph** (ThemeRiver) — Change / Part-to-whole — "how do many components' volumes ebb and flow?" — time x many parts. — Use: aesthetic overview of many categories (Byron & Wattenberg 2008 *Stacked Graphs — Geometry & Aesthetics*). — Avoid: any precise reading; no baseline. — Substitute: stacked area, small multiples, ridgeline. — Support: EC themeRiver, VL, Plot (stack offset "wiggle"), D3. Stable niche.

**Step chart** — Change — "when did a discrete level change?" — time x piecewise-constant quantitative (prices, interest rates, inventory). — Use: values that hold until changed. — Avoid: interpolating between samples. — Support: VL, Plot (`curve: "step"`), EC, PL, DW **[DW unverified]**. Stable.

**Range / band chart** (error band, ribbon, min–max band, fan chart) — Change / uncertainty — "what is the envelope or confidence interval?" — time x low/high (+ centre). — Use: forecasts (fan chart, FT "uncertainty grows the further forward"), daily temperature ranges, confidence intervals. — Evidence: bands are read better than error bars for continuous series; users misread CI bands as containing all data (Padilla, Hullman work on uncertainty **[memory]**). — Support: VL error band, Plot area/rule, PL, DW range area **[unverified]**. Rising with uncertainty communication.

**Candlestick / OHLC** — Change (stock) — "what were open/high/low/close per period?" — time x 4 quantitative (+ volume). — Use: financial data for practitioners. — Avoid: general audiences (use line of close). — Support: VL, EC, PL, Highcharts; Kagi and point-and-figure are specialist variants (DVC). Stable niche.

**Connected scatterplot** — Correlation / Change — "how did two variables co-evolve?" — time x 2 quantitative. — Use: clear directional progression, annotate start/end and arrows. — Evidence: Haroz, Kosara & Franconeri 2016 (*The Connected Scatterplot for Presenting Paired Time Series*, TVCG) found they are engaging but error-prone without annotation **[memory]**. — Substitute: two stacked lines sharing x. Niche.

**Calendar heatmap** — Change (temporal pattern) — "which days/weeks are high?" — daily date x quantitative. — Use: daily patterns across years (GitHub contributions). FT: precision sacrificed. — Substitute: line, cycle plot. — Support: EC calendar, Plot cell mark, D3, Plotly via heatmap. Rising.

**Horizon chart** (Heer, Kong & Agrawala 2009 *Sizing the Horizon*) — Change — "many series in little vertical space." — time x N series. — Use: dozens of series in dashboards. — Avoid: general audiences (layered bands need training). — Support: D3, Plot examples, Vega. Stable niche.

**Timeline / Priestley timeline / Gantt** — Change — "when did things start and how long did they last?" — entity x start/end dates (+ dependencies for Gantt). — Use: events with duration; Gantt for schedules. — Avoid: Gantt for >~30 tasks without grouping. — Support: Mermaid gantt/timeline, PL, VL (bar with x/x2), DVC. Stable.

**Cycle plot** **[memory]** — Change — "trend within each season, seasons side by side" (Cleveland). — Niche.

**Spiral plot** (DVC) — Change — periodic data on a spiral. Niche; engaging but hard to read.

**Arrow plot** (DW) — Change — start→end arrow per category; a dumbbell with direction. Rising in newsrooms.

### 2.3 Distribution

**Histogram** — Distribution — "what is the shape of the data?" — 1 quantitative (binned) → count. — Use: the default; FT: keep gaps small. — Avoid: bin width games; comparing many groups (use ridgeline/box); using for categorical data (that is a bar chart). — Substitute: density, dot plot for small n, ECDF for comparisons. Universal.

**Density plot** (KDE) — Distribution — "smooth shape?" — 1 quantitative. — Use: continuous data with large n; overlay ≤3 groups. — Avoid: small n (smoothing invents shape); bandwidth choice hides multimodality. — Substitute: histogram, ECDF. Universal in stats libs; not in DW/Flourish menus.

**Box plot** (box-and-whisker, Tukey 1970s) — Distribution — "how do medians and spreads compare across groups?" — categorical x quantitative. — Use: many groups, robust summaries. — Avoid: hiding bimodality (the box plot's classic failure); small n; audiences who don't know the convention. — Evidence: FT; Matejka & Fitzmaurice 2017 "Same Stats, Different Graphs" shows same box plot for very different data **[memory]**. — Substitute: violin, raincloud, strip + median. Universal.

**Violin** — Distribution — "full shape per group?" — categorical x quantitative. — Use: complex/bimodal distributions (FT). — Avoid: small n; mirrored density is redundant (half-violin is enough). — Substitute: raincloud, ridgeline. Support: VL (via density), PL, EC (custom), ggplot2, seaborn. Stable.

**Ridgeline (joyplot)** — Distribution / Change — "how does a distribution shift across many ordered groups (months, years)?" — ordered categorical x quantitative. — Use: 6–30 groups, ordered. — Avoid: unordered groups; overlaps hiding peaks. — Support: `ggridges`, D2V, Plotly, Plot (area + facet). Rising since 2017; stable now.

**Raincloud** (Allen et al. 2019, *Wellcome Open Research*, https://discovery.ucl.ac.uk/id/eprint/10178652/) — Distribution — "shape + summary + raw points at once." — categorical x quantitative, moderate n. — Use: scientific reporting; transparency about raw data. — Avoid: large n (dots saturate), narrow layouts. — Support: R `ggrain`, Python `ptitprince`, JASP, MATLAB; no BI tool. Rising in science.

**Beeswarm** (Eklund 2016 `beeswarm`; Plot `dodge`) — Distribution — "where does every individual sit?" — categorical x quantitative, n up to a few hundred. — Use: showing every unit (countries, players, survey respondents), highlighting one. — Avoid: large n (use jitter/violin), needing exact values. — Substitute: strip/jitter, histogram, dot plot. — Support: Plot dodge transform, D3 force, Flourish "survey" template, ggbeeswarm. Rising.

**Strip plot / jitter / dot strip / barcode** — Distribution / Ranking — "all values per category, space-efficient." — Use: small n; FT: "problem when too many dots have the same value" (add jitter or beeswarm). Support: VL strip, Plot tick/dot, seaborn. Stable.

**Wilkinson dot plot** (stacked dots) — Distribution — histogram made of countable dots; great for teaching and small n. Support: VL, ggplot2 `geom_dotplot`. Stable niche.

**Population pyramid** — Distribution / Deviation — age x sex counts; mirrored bars. Standard demographic chart. Support: DW, VL example, DVC. Stable.

**Cumulative curve / ECDF** — Distribution — "what fraction is below x? how do groups compare across the whole range?" — 1 quantitative (+ group). — Use: comparing several distributions precisely; inequality (Lorenz curve is the special case). — Avoid: general audiences without explanation. — Support: seaborn `ecdfplot`, Plotly `ecdf`, VL (window transform). Rising in analytics.

**QQ plot** — Distribution — "does the sample follow a theoretical or another distribution?" — quantiles vs quantiles. Statistical diagnostic only. Support: statsmodels, R, Plotly examples. Stable niche.

**Error bars** — Distribution / uncertainty — mean ± CI/SD per category. — Avoid: "bar + error bar" (dynamite plot) hides distribution; ambiguity about what the bar denotes (SD vs SE vs CI) — always state it. — Evidence: Correll & Gleicher 2014 "Error Bars Considered Harmful" (TVCG) found bar+error bars cause "within-the-bar bias"; gradient/violin plots did better **[memory]**. — Substitute: dot + interval, violin, raincloud. Universal.

**2D histogram / hexbin / 2D density / contour** — Correlation / Distribution — "where is the mass in a scatter of many points?" — 2 quantitative, large n. — Use: >~5k points where overplotting hides structure; hexbin avoids the grid alignment artifacts of square bins. — Substitute: scatter with alpha, sampled scatter. — Support: Plot hexbin/density/contour, VL (bin x/y + rect), PL 2D histogram/contour, DW "2D histogram" (per Muth 2025 guide), ggplot2 `geom_hex`. Rising.

**Stem-and-leaf** (DVC) — teaching/legacy. Declining.

### 2.4 Correlation

**Scatterplot** — Correlation — "is there a relationship between x and y; are there clusters/outliers?" — 2 quantitative (+ colour categorical, + size). — Use: default for two continuous variables; add trend line and annotate outliers. — Avoid: overplotting (use alpha/hexbin), implying causation, dual axis instead of scatter for two series' relationship. — Evidence: both axes are position on common scale (best C&M encoding); Franconeri et al.: correlation perception is biased (people underestimate r; Rensink & Baldridge 2010 **[memory]**). — Accessibility: colour categories need shapes too; describe clusters in alt text. Universal.

**Bubble chart** — Correlation — scatter + size (3rd quantitative) — Use: size for a rough third variable; scale by area. — Avoid: reading size precisely (area encoding); many bubbles overlapping. — Substitute: small multiples of scatter, colour instead of size. Universal.

**Scatterplot matrix (SPLOM)** — Correlation — all pairwise relations among 3–8 variables. Support: VL repeat, PL `scatter_matrix`, seaborn pairplot. Analytics only.

**Correlogram / correlation heatmap** — Correlation — matrix of correlation coefficients with diverging colour. Support: seaborn, D2V, Plot cell. Stable.

**XY heatmap / matrix** — Correlation / Magnitude — "pattern across two categorical dimensions?" — categorical x categorical x quantitative. — Use: patterns, not fine values (FT); order rows/columns meaningfully (seriation/clustering). — Avoid: rainbow colour scales; more than one quantitative meaning; expecting precise reading (colour is the bottom of C&M). — Accessibility: add numbers in cells; use perceptually uniform (viridis) or diverging with a neutral midpoint. — Substitute: small-multiple bars, dot matrix with size. Universal.

**Line + column (dual axis)** — Correlation / Change — "how do an amount and a rate move together?" (FT). — Avoid: two lines on two y-axes (arbitrary scale alignment invents correlations; Datawrapper: "usually not the best choice for general audiences… easily misread", https://www.datawrapper.de/blog/dual-axis-charts). — Substitute: two stacked panels with shared x, indexed lines (rebased to 100), connected scatter. Declining in editorial use, persistent in BI.

**Quadrant chart** (Mermaid, BCG matrix) — Correlation — 2 quantitative with threshold lines, used as a management framework. Niche.

### 2.5 Part-to-whole

**Pie chart** — Part-to-whole — "how big is a share of the whole; do a few slices together make a majority?" — 1 categorical (≤5–6 parts) x proportions summing to 100%. — Use: few parts, big differences, whole matters; Kosara: pies beat bars for "combine neighbouring slices and compare to the whole". — Avoid: >6 slices, comparing similar slices, comparing across multiple pies, 3D/exploded, pies over time. — Evidence: Skau & Kosara, "Arcs, Angles, or Areas: Individual Data Encodings in Pie and Donut Charts", EuroVis 2016 (https://media.eagereyes.org/papers/2016/Skau-EuroVis-2016.pdf — PDF fetched but could not be text-extracted; summary from https://eagereyes.org/pie-charts): readers do **not** primarily use angle; arc length/area do the work, so donuts are as accurate as pies and angle-only variants are worst. Cleveland & McGill (1984) found pie (angle) worse than bar (position) for proportion judgments. — Accessibility: label slices directly with percentages; avoid legend-by-colour. — Substitute: bar chart of shares, waffle, single stacked bar. Universal; editorial use stable but restricted.

**Donut** — Part-to-whole — same as pie; the hole is a place for the headline number (FT). Kosara: performs comparably to pie. Universal; rising in dashboards.

**Waffle / gridplot / dot matrix** (unit chart, 10x10 grid) — Part-to-whole — "what share, in whole percent?" — proportions on whole numbers. — Use: percentages for general audiences, small multiples of waffles across categories (FT gridplot). — Avoid: non-integer or many categories. — Support: DW, Flourish, D2V, `waffle` R pkg. Rising.

**Treemap** (Shneiderman 1991) — Part-to-whole / hierarchy — "how does a whole break into nested parts by size?" — hierarchy x size (+ colour). — Use: hundreds of leaves, hierarchical, size skewed. — Avoid: small differences (rectangular area is poor: Heer & Bostock), many tiny segments (FT), treemaps for non-hierarchical single-level data (use bars). — Substitute: bar, sunburst (if depth matters), icicle. — Support: EC, PL, D3, Vega, DW, Flourish, Mermaid (new). Stable.

**Sunburst** (radial icicle) — Part-to-whole / hierarchy — same data as treemap; emphasizes depth and path. — Avoid: reading angles at outer rings; deep hierarchies. — Substitute: icicle (rectangular, more readable, labels fit), treemap. Support: EC, PL, D3. Stable.

**Icicle / partition** — hierarchy with rectangular layers; labels fit better than sunburst; used for flame graphs (profiling). Support: PL icicle, D3, Vega. Niche but useful.

**Circle packing** — hierarchy by nesting circles; pretty, wastes space; area encoding poor. Support: D3, D2V, Flourish. Niche.

**Marimekko / mosaic** — Part-to-whole (2 dimensions) — "share by two categorical variables where widths also mean something?" — 2 categorical x quantitative (widths = totals, heights = shares). — Use: market share x segment size. — Avoid: general audiences without annotation; >~5x5 cells. — Substitute: stacked bars with a separate width chart, heat table. Support: VL (mosaic example), DW (per Muth 2025 guide), Flourish **[unverified]**, ggmosaic. Rising slowly.

**Arc / parliament / hemicycle** — Part-to-whole — seats by party. Standard for election coverage. Support: DW "election donut", Flourish parliament, D3. Stable.

**Voronoi** — Part-to-whole / Spatial — turn points into areas of nearest influence; FT lists it. Use: territory maps, hover targets. Support: D3, Plot voronoi mark. Niche.

**Venn / Euler** — schematic only (FT: "generally only used for schematic representation"). Areas rarely proportional. Substitute: UpSet plot. Support: Mermaid (new), DVC.

**UpSet plot** (Lex et al. 2014, TVCG) — Part-to-whole / set intersections — "which combinations of sets are most common?" — sets x elements. — Use: >3 sets, where Venn fails. — Support: R `UpSetR`, Python `upsetplot`, Vega examples. Rising in bio/data science; absent from BI tools.

**Waterfall** (bridge chart) — Part-to-whole / Flow / Deviation — "how do sequential increments and decrements get from start to end total?" — ordered steps x signed quantitative. — Use: finance (P&L bridges), budgets; colour +/−. — Avoid: many small steps; unclear subtotal bars. — Support: PL, DW, EC (via stacked bar trick), Excel. Stable.

**Funnel** — Part-to-whole / Flow — "how much drops out at each sequential stage?" — ordered stages x count. — Avoid: width encoding when stages are not strictly nested; funnels are really bar charts. — Substitute: ordered bar with conversion labels. Support: PL, EC, Mermaid? (no). Stable in marketing BI.

**Bar-of-pie / pie-of-pie** — Excel-only artifact; avoid. Substitute: nested bars or treemap. Declining.

### 2.6 Spatial

**Choropleth** — Spatial — "how does a rate vary by region?" — regions x rate/ratio. — Use: rates only (FT: "should always be rates rather than totals"); classed or continuous with a perceptually uniform or diverging scheme. — Avoid: totals (large sparse areas dominate — the "land doesn't vote" problem); rainbow scales; too many classes (>7). — Evidence: colour is the weakest C&M encoding; Brewer's ColorBrewer guidance for class counts **[memory]**. — Substitute: cartogram, tile grid map, symbol map for counts. — Support: DW, Flourish, VL, PL, EC, D3. Universal.

**Proportional symbol / bubble map** — Spatial — counts/totals located on a map. Avoid: overlap; area misread. Universal.

**Dot density map** — Spatial — one dot per n units; shows distribution. Annotate patterns (FT). Support: D3, QGIS, Plot. Stable.

**Hexbin map / gridded heat map** — Spatial — aggregated counts in hex or square cells, not snapped to admin boundaries (FT "heat map"). Support: Plot hexbin, D2V, deck.gl. Rising.

**Cartogram (scaled / contiguous / Dorling)** — Spatial — regions resized by value. Use: votes, population. Avoid: audiences unfamiliar with geography distortion. Support: D3-cartogram, Flourish **[unverified]**. Stable niche.

**Tile grid map / hex map (equalised cartogram)** — Spatial — every region as an equal tile; FT: "good for representing voting regions". Use: US states, UK constituencies, EU countries. Support: DW (symbol map with tiles? **[unverified]**), D3, Flourish, `geofacet` R. Rising in newsrooms.

**Flow map / connection map** — Spatial / Flow — movement between places with lines (width = volume). Avoid: hairball; use bundling or aggregation. Support: D3, deck.gl, EC lines, Flourish. Stable.

**Contour / isopleth map** — Spatial — areas of equal value (elevation, temperature, pressure). Support: Plot contour, PL, D3. Stable.

**Locator map** — Spatial — just where something is; DW's third map type. Universal.

### 2.7 Flow, network, hierarchy

**Sankey** (river plot) — Flow — "how do quantities flow from sources to sinks, and where do they go?" — source x target x weight, often multi-stage. — Use: energy budgets, user journeys, migration; keep ≤~20 nodes per stage. — Avoid: cycles, many thin flows, reading node totals when nodes are not conserving. — Substitute: alluvial (categorical stages), chord (two-way), stacked bars. — Support: EC, PL, D3-sankey, Mermaid, DW, Flourish, Vega. Rising; now universal.

**Alluvial / parallel sets** — Flow — categorical variables across stages (e.g., class → survival). Difference from Sankey: nodes are categories of ordered variables, flows are cohorts. Support: DW (per 2025 guide), Flourish, `ggalluvial`, D3. Rising.

**Chord diagram** — Flow — "two-way flows among a small set of entities and net winners" (FT). — Avoid: >~10 entities; general audiences. — Substitute: heatmap/matrix, Sankey. Support: D3, EC 6 (new), Flourish, Plotly (none native). Stable niche.

**Arc diagram** — Flow / Network — nodes on a line, links as arcs; good for ordered sequences (e.g., text repetition), poor for dense graphs. Support: D3, D2V, DVC. Niche.

**Network / node-link diagram** — Flow — "who is connected to whom; what is the structure?" — nodes x edges (+ weights). — Use: <~200 nodes with force layout, communities highlighted. — Avoid: hairballs; reading precise values; force layouts imply meaningless positions. — Substitute: adjacency matrix (dense graphs; Ghoniem, Fekete & Castagliola 2004 found matrices outperform node-link for larger/denser graphs except path-following **[memory]**), arc diagram, hierarchical edge bundling. — Support: EC graph, D3-force, Flourish network, Vega, Plotly (via traces). Stable.

**Adjacency matrix** — Flow / Correlation — same data as network, as a grid. Support: D3, Plot cell, D2V. Niche.

**Tree / dendrogram** — hierarchy — "what is the hierarchy / clustering?" — parent-child (+ height for dendrograms). — Use: org charts, taxonomies, hierarchical clustering. — Avoid: >~100 leaves without collapsing. — Substitute: treemap/icicle for size; indented tree/table. — Support: EC tree, Plot tree mark, D3 cluster/tree, Mermaid mindmap/flowchart, Plotly `create_dendrogram`. Stable.

**Hierarchical edge bundling** — Flow — hierarchy + cross-links (Holten 2006). Support: D3. Niche.

### 2.8 Diagram-style types in chart menus (brief)

Flow chart, mind map, Gantt (see above), quadrant, org chart, timeline, kanban, C4/architecture (Mermaid), Wardley, Cynefin, Ishikawa (Mermaid 2026 additions): these are diagrams, not data charts. Include in a chart knowledge base only as "schematic / process" family with the note that they encode structure, not quantities.

---

## 3. Evidence-based selection rules

### 3.1 Perceptual accuracy of encodings

- **Cleveland & McGill 1984** (JASA; https://www.jstor.org/stable/2288400 **[URL from memory]**) ranked elementary perceptual tasks: (1) position along a common scale, (2) position along non-aligned scales, (3) length, direction, angle, (4) area, (5) volume, curvature, (6) shading, colour saturation. Practical form: **position > length > angle/slope > area > volume > colour**. Consequences: dot plots and bars beat pies; bars beat treemaps and bubbles; heatmaps are for pattern, not value.
- **Heer & Bostock 2010** (CHI, *Crowdsourcing Graphical Perception*; https://www.semanticscholar.org/paper/55d3281f6b34c50df975b7261044689bf73ec610) replicated the ranking on Mechanical Turk, adding rectangular area (treemap-style) and circular area (bubbles), both worse than length; also found log error grows with chart height/gridline density effects. Established crowdsourced perception studies as valid.
- **Skau & Kosara 2016** (EuroVis; summary at https://eagereyes.org/pie-charts): pie readers use arc length/area, not angle; donuts are fine; "angle-only" and pie variants that distort arc (exploded, 3D) are worst. Kosara's practical rule: pies are fine for ≤5 slices, a single part-to-whole, and questions like "is A+B a majority".
- **Franconeri, Padilla, Shah, Zacks & Hullman 2021** (*Psychological Science in the Public Interest* 22(3), https://journals.sagepub.com/doi/10.1177/15291006211051956; PubMed https://pubmed.ncbi.nlm.nih.gov/34907835/): three perceptual "tools" (global statistics extraction — fast; shape extraction — fast; sentence-like comparisons of subsets — slow, one at a time). Guidance: design so the intended comparison is the easiest one (adjacent, aligned, same colour); annotate and label directly; beware axis truncation, aspect ratio, colour scales, 3D; the same data in different layouts yields different "sentences" in the viewer's head; uncertainty is best shown with distributions/quantile dot plots rather than error bars.
- **Bateman et al. 2010** (CHI, *Useful Junk?*; https://vis.csail.mit.edu/classes/6.859/readings/pdfs/Bateman-UsefulJunk.pdf): Holmes-style embellished charts were recalled better after delays, with no loss in immediate comprehension accuracy. Kosara's commentary: https://eagereyes.org/criticism/chart-junk-considered-useful-after-all. So Tufte's data-ink ratio is a design heuristic, not a law; the safer synthesis (data.europa.eu guide, https://data.europa.eu/apps/data-visualisation-guide/chart-junk-and-data-ink-minimalistic-vs-rich-design): remove *non-data ink that competes with data*, keep embellishment that carries meaning or memorability.

### 3.2 Rules of thumb drawn from those sources and the tool guides

1. **Start from the message, not the data** (Muth 2025, https://www.datawrapper.de/blog/chart-types-guide): write the headline sentence; the sentence's verb (grew, is larger than, makes up, correlates with, is distributed, flows to, is located) picks the FT family.
2. **Prefer position-on-common-scale**: bars/dots/lines/scatter first; reach for area (treemap, bubble) only when hierarchy or extreme range demands; reach for colour (heatmap, choropleth) only for pattern or geography.
3. **Pies**: OK for ≤5 parts, one whole, large differences, and "sum of slices" questions; label directly; otherwise bar. Donut ≈ pie (Kosara 2016).
4. **Stacked bars**: put the series readers must compare on the baseline; ≤4 segments; use small multiples or split bars for cross-column comparison (Datawrapper Feb 2025, https://www.datawrapper.de/blog/stacked-column-charts).
5. **Dual axes**: avoid for general audiences (Datawrapper); instead two panels sharing x, indexing both to 100, or a connected scatter. If forced: colour-code axes, label values, never let gridlines suggest a false crossing.
6. **Log scales**: use for multiplicative/exponential data (growth rates, epidemics, incomes spanning orders of magnitude); label with real values at each decade; warn readers explicitly; never use log for stacked or area charts (area under a log axis is meaningless) **[memory: standard guidance, e.g. Datawrapper "log scales" post, URL not verified]**.
7. **Series limits**: multi-line ≤~5 differentiated series (or grey-plus-highlight); grouped bars ≤3 series; stacked ≤4 parts; pie ≤5–6; categorical colours ≤7–8 (Tableau 10 and Okabe-Ito top out at 8–10 for a reason); above these, use small multiples, a table, or interaction.
8. **Small multiples vs overlays**: overlay when the comparison is between lines at the *same x* and lines are few; small multiples when comparing *shapes* across many categories or when lines cross a lot. Share axes; order panels meaningfully; Franconeri et al.: side-by-side comparison of shapes is fast, comparing values across separated panels is slow — so add a reference line (overall mean) in every panel.
9. **Colour**: sequential (one hue, luminance ramp: viridis, cividis, ColorBrewer Blues) for ordered magnitude; diverging (two hues around a neutral midpoint: RdBu, BrBG) only when the midpoint is meaningful (zero, average, target); categorical (distinct hues, equal luminance-ish) for ≤8 unordered classes. Colourblind-safe defaults: **Okabe & Ito 2002/2008** palette (https://jfly.uni-koeln.de/color/): black #000000, orange #E69F00, sky blue #56B4E9, bluish green #009E73, yellow #F0E442, blue #0072B2, vermilion #D55E00, reddish purple #CC79A7 **[hex values from memory; page fetched but hex list is in the linked PDF]**; **viridis/magma/plasma/cividis** (perceptually uniform, CVD-safe; Smith & van der Walt 2015 **[memory]**); **Tableau 10** (2016 revision, tuned for discriminability, not fully CVD-safe **[memory]**); ColorBrewer (Brewer/Harrower) with the "colorblind safe" filter. Never rely on colour alone (WCAG 1.4.1): add labels, shapes, patterns, or direct annotation.
10. **Annotation and direct labelling**: label lines at their ends, put values on bars when few, annotate the "so what" on the chart (Storytelling with Data; Franconeri et al.). Legends force slow lookups.
11. **Axes**: bars start at zero; lines and dots need not, but say so; keep aspect ratio so typical slopes are near 45° (Cleveland banking); avoid broken axes.
12. **Uncertainty**: prefer bands, quantile dot plots, or hypothetical-outcome plots to bare error bars (Correll & Gleicher 2014; Kay et al. 2016; Hullman et al. 2015 **[memory]**).
13. **Tables are charts too**: when readers need exact numbers or many measures per row, a sorted, colour-coded table beats a chart (Datawrapper, Few).
14. **Accessibility** (Chartability heuristics, https://chartability.fizz.studio/ **[unverified]**; WCAG 1.1.1, 1.4.1, 1.4.3, 1.4.11): text alternative in the "chart type + what it shows + key finding" pattern; a data table alternative; 3:1 contrast for graphical objects; no colour-only encoding; keyboard-navigable interactives; consider sonification for time series (Highcharts Sonification, Apple Audio Graphs **[memory]**). Bars, lines, and tables are the most screen-reader-friendly; pies, treemaps, networks the least. Practical guides: https://www.washington.edu/accesstech/dataviz/ , https://www.a11y-collective.com/blog/accessible-charts/ .

### 3.3 Decision procedures practitioners actually use

- **FT Visual Vocabulary poster**: pick the relationship (9 families) → pick from 4–12 types in that column, each with a one-line caveat. Used by newsroom graphics desks, Tableau ("Visual Vocabulary" workbook), Power BI ports.
- **Abela Chart Chooser**: "What would you like to show?" → comparison / distribution / composition / relationship → number of variables / over time or among items → chart. Simple, common in corporate training, dated.
- **From Data to Viz**: start from data shape (one numeric, two numeric, one cat + one num, …) → chart candidates → caveat pages. Best for analysts who know their data but not their message.
- **Datawrapper Muth 2025**: six goals (time, shares, absolute numbers, correlation, flow, geography) with "basic types first, fancy types for engagement when the message survives".
- **Storytelling with Data (Knaflic)**: the "graph choosing" set is deliberately small — simple text, table, heat table, scatter, line, slope, bar (vertical/horizontal, stacked, waterfall), square area; everything else is treated as exceptional **[memory]**.
- **Flourish "Start with data"** (https://flourish.studio/learn/chart-types/): pattern-matches uploaded columns to candidate templates — a lightweight form of automatic recommendation.
- **Vega-Lite / Draco / Voyager**: formal specification-based recommendation (see section 4).

---

## 4. How AI agents and LLMs currently choose and build charts (2024–2026)

### 4.1 Approaches

1. **Constraint/knowledge-base recommenders (pre-LLM, still used as guardrails)**. *CompassQL/Voyager* (Wongsuphasawat et al. 2016–2017, UW IDL; https://dl.acm.org/doi/10.1145/2939502.2939506) enumerate Vega-Lite specs from a partial query and rank by effectiveness (Mackinlay's APT criteria: expressiveness, then effectiveness via the C&M ranking). *Draco* (Moritz et al., InfoVis 2019, https://idl.cs.washington.edu/files/2019-Draco-InfoVis.pdf) encodes design rules as Answer Set Programming hard/soft constraints with learned weights; *Draco 2* (Yang et al., VIS 2023, https://idl.cs.washington.edu/files/2023-Draco2-VIS.pdf) is a Python platform with `complete_spec`, explicitly proposed as the "completion" stage after an LLM emits a partial spec. *DracoGPT* (VIS 2024) probes what design preferences LLMs have encoded and finds they diverge from perception studies (per the paper list at https://github.com/zengxingchen/LLM-Visualization-Paper-List). "Too Many Cooks" (https://arxiv.org/pdf/2308.14241) shows Draco's recommendations depend heavily on which perception studies feed its weights.

2. **LLM-as-code-writer pipelines**. *LIDA* (Dibia, ACL 2023 demo; https://github.com/microsoft/lida): summarizer → goal explorer (persona-conditioned) → visgenerator (code in matplotlib/seaborn/altair/plotly) → infographer; reports <3.5% execution-error rate; chart type is chosen implicitly by the LLM given the data summary and goal (no explicit perceptual ranking). *ChartGPT* (Tian et al., TVCG 2024 **[memory]**) decomposes NL → chart into steps (select columns, transform, mark, encodings) and fine-tunes a model to output Vega-Lite-like specs. *VizGPT* (open source, 2023) is a chat wrapper producing Vega-Lite. *nl4dv* (Narechania et al., VIS 2020) is the earlier rule-based NL toolkit that returns Vega-Lite plus an "attribute/task" analysis; task inference (correlation, distribution, trend, filter) drives type choice.

3. **Interactive AI analysts with explicit chart engines**. *Data Formulator* (Microsoft Research; https://github.com/microsoft/data-formulator; v0.7 stable 2026-05-28, v0.8 beta 2026-08-15): the user binds "concepts" (existing or LLM-derived columns) to visual channels; the LLM writes data-transformation code, while the chart is rendered from a declarative spec — since 2026 through "Flint", an in-house compact chart language with a style-refinement agent and "30+ chart types" including maps. The design principle: LLM for *data transformation*, deterministic grammar for *encoding*. Observable, Deepnote, Hex, Julius, and ChatGPT Advanced Data Analysis follow the code-writer pattern (matplotlib/plotly) **[memory]**.

4. **Multi-agent / self-correcting generation**. *nvAgent* (2025), *VisPath* (2025), *METAL* (ACL 2025), *PlotCraft* (2025, https://arxiv.org/pdf/2511.00010) add planner/coder/critic loops that render, inspect the image with a VLM, and fix. *C2* (NAACL 2025) is auto-feedback for chart generation. *AVA* (EuroVis 2024) uses visual perception of the rendered chart as feedback.

### 4.2 Benchmarks and what they measure

- **nvBench** (2021) and **nvBench 2.0** (NeurIPS 2025; https://arxiv.org/abs/2503.12880; https://github.com/HKUSTDial/nvBench-2.0): NL → Vega-Lite; 2.0 has 7,878 ambiguous queries mapping to 24,076 valid charts over 780 tables, scored by F1@k over the set of valid interpretations; Step-NL2VIS reaches F1@3 = 81.5%.
- **VisEval** (Chen et al., VIS 2024): NL → code; checks validity, legality (correct chart type/data/order), readability (VLM-judged).
- **Text2Vis** (EMNLP 2025), **ChartMimic** (2024/ICLR 2025), **Plot2Code** (2025), **ChartEdit**, **RealChart2Code** (2026): chart image → code reproduction; ChartMimic reports GPT-4o at 82% and is considered saturated; **Chart2Code hierarchical benchmark** (ACL 2026; https://arxiv.org/abs/2510.17932) has 2,186 tasks across 22 chart types in three levels (replication, editing, long-table-to-chart) and finds GPT-5.2 only ~33 on editing.
- **ChartQA / ChartQAPro / CharXiv / ChartAnno** (2024–2026): chart *reading* rather than choosing; relevant because agents use VLM reading as the critic in self-correction loops.
- **VisJudge-Bench** (2025, https://arxiv.org/pdf/2510.22373): aesthetics/quality judgments of visualizations by VLMs.
- **MatPlotAgent**, **PlotCraft**: complex/interactive plotting tasks.

### 4.3 Criteria these systems use (synthesis)

- Data-type matching (nominal/ordinal/quantitative/temporal → mark and channel), inherited from APT/CompassQL and encoded in Draco's constraints; LLM systems mostly learn this implicitly.
- Task/intent inference (trend, comparison, distribution, correlation, part-to-whole, flow) from the NL query — nl4dv, ChartGPT, nvBench 2.0's stepwise reasoning, Data Formulator's concept binding.
- Effectiveness ranking (position > length > … ) explicit in Draco/CompassQL; **absent or inconsistent** in pure-LLM pipelines (DracoGPT finding). This is the main documented gap in 2025–2026: LLMs over-produce pies, dual axes, and 3D when asked loosely, and benchmark scoring rarely penalizes a *valid but perceptually poor* choice.
- Execution success and visual faithfulness (VisEval, ChartMimic) dominate benchmark design; readability is judged by VLMs, which have their own perception biases (see "Evaluating Graphical Perception Capabilities of Vision Transformers", https://arxiv.org/pdf/2602.18178, and VisDoT https://arxiv.org/pdf/2603.11631).
- Practical recommendation for an agent: let the LLM classify intent + data shape, then apply an explicit rule table (FT family → allowed types → perceptual ranking → series/category limits → colour policy → accessibility fallback) before writing code; use Draco 2 or a simple rule checker as a linter on the produced spec.

---

## 5. Gaps and things to verify before publication

- Datawrapper's exact 23-type menu and whether marimekko/alluvial/waffle ship (menu page fetch returned only the summary; verify at https://www.datawrapper.de/charts and https://www.datawrapper.de/academy).
- Flourish's full template list (gallery page did not enumerate templates on fetch; verify at https://app.flourish.studio/templates **[URL from memory]**).
- Storytelling with Data slopegraph URL (404).
- Okabe-Ito hex values (from memory; PDF on the jfly page has the canonical values).
- Exact series-count limits: no single primary source; numbers above are the common newsroom heuristics.
- Skau & Kosara 2016 details were taken from Kosara's blog summary, not the PDF text.
- Mermaid's list is as of the intro page on 2026-09-17; several chart types are labelled new/beta and may change.
- ECharts `series-chord` confirmed in llms.txt; release version (6.0) from memory.
