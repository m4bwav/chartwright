# Knowledge base authoring brief

For anyone (human or agent) writing chart files in `kb/charts/`. Written 2026-09-17 for the first fan-out; still the standard.

## Read first, in this order

1. `kb/SCHEMA.md` (frontmatter fields, families, shape grammar, required sections).
2. `kb/charts/line.md`: the exemplar; match its depth, tone and structure exactly.
3. `kb/targets/*.md` (five files): what each target can draw; a chart's `support:` map must agree with them.
4. `kb/rules/selection.md` and `kb/rules/evidence.md`: cite evidence by author-year as those files do.
5. The relevant cards in `ai-docs/research/2026-09-17-chart-taxonomy-and-evidence.md` (section 2, by family) and, for build recipes, `ai-docs/research/2026-09-17-libraries-and-render-targets.md`.

## Rules

- One file per slug, `kb/charts/<slug>.md`, frontmatter `slug` equals the file name. Every one of the five targets gets a `support:` line (`native`, `approx`, `image`, `none`) and every `native`/`approx` target gets a `### <target>` subsection under `## Build`.
- `support` honesty: `native` only when the target draws it with its own primitive; `approx` when composed from primitives with a real loss or real work; `image` when the answer is "render a picture elsewhere"; `none` when even that makes no sense (interactive-only types).
- `shapes` use the grammar in SCHEMA.md. `goals` are lower-case words or short phrases a user's request would contain (`trend`, `over time`, `share`, `rank`); include the family name as one goal. 6 to 14 goals.
- `max_series` and `max_categories`: the soft cap from the evidence, 0 when not applicable.
- `evidence`: `high` only with replicated perception studies (position/length encodings); `medium` for one study or strong practitioner consensus; `low` for convention. Say in `## Evidence` what the rating rests on.
- `popularity`: `core` (in every library and guide), `common`, `niche`, `rising` (spreading across tools 2023-2026), `declining` (guides discourage it). The research file section 1.3 has the signal.
- `## Substitutes` names other slugs in backticks; prefer slugs that exist in the plan below.
- `## Build`: the minimal idiomatic recipe per target, short. Where `scripts/cw.py build` supports the chart (list below) say the exact command; otherwise give the primitive or plugin and a one-line snippet. Do not invent library features; the targets files and the libraries research say what exists.
- Plain prose, no em dashes, no filler. Cite URLs in `sources:`. No `TODO` may remain: `python scripts/cw.py --strict validate` must pass.
- `## Notes` starts with `- 2026-09-17: written from the 2026-09-17 taxonomy research.`

## What `cw.py build` supports today (so Build sections can name the command)

- mermaid: line, multi-line, step (as line), bar, column, area (as line, no fill), grouped-bar (overlapping, lossy), pie, donut (as pie), sankey, alluvial (as sankey), quadrant, radar; `--flag namedSeries` emits `xychart` with named series (11.16+ hosts).
- vega-lite: line, multi-line, step, bar, column, grouped-bar, stacked-bar, area, stacked-area, scatter, bubble, heatmap, histogram, boxplot, pie, donut, strip, dot, lollipop; composed (2026-09-18): dumbbell, slope, waterfall, calendar-heatmap, diverging-bar, stacked-bar-100, small-multiples.
- terminal (2026-09-18): line, sparkline, area, step (block sparkline), bar, column (block bars).
- plotly: line, multi-line, step, area, stacked-area, scatter, bubble, bar, column, grouped-bar, stacked-bar, pie, donut, histogram, boxplot, heatmap.
- chartjs: line, multi-line, area, step, bar, column, grouped-bar, stacked-bar, pie, donut, scatter, bubble, radar, polar-area.
- matplotlib: line, multi-line, step, area, bar, column, grouped-bar, scatter, histogram, pie, donut, boxplot.

Everything else: hand-written from the recipe. Say so.

## Slug plan (first fan-out, 2026-09-17)

- Change over time and ranking: column, area, stacked-area, streamgraph, step, slope, bump, connected-scatter, candlestick, range-band, calendar-heatmap, horizon, sparkline, timeline, gantt, small-multiples.
- Magnitude and deviation: bar, grouped-bar, dot-plot, lollipop, dumbbell, radar, parallel-coordinates, radial-bar, pictogram, stat-tile, table, diverging-bar, diverging-stacked-bar, bullet, waterfall, gauge.
- Part to whole and hierarchy: stacked-bar, stacked-bar-100, pie, donut, waffle, marimekko, funnel, treemap, sunburst, icicle, circle-packing, venn, tree, dendrogram.
- Distribution and correlation: histogram, density, boxplot, violin, ridgeline, raincloud, beeswarm, strip, ecdf, qq, population-pyramid, error-bars, scatter, bubble, heatmap, splom, hexbin, density-2d, correlogram, quadrant.
- Spatial, flow and relationship: choropleth, bubble-map, dot-density-map, tile-grid-map, hex-map, flow-map, cartogram, sankey, alluvial, chord, arc-diagram, network, adjacency-matrix, edge-bundling, word-cloud.
- Already written: line.
