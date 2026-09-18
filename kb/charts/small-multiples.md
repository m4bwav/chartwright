---
name: Small multiples
slug: small-multiples
aliases: [trellis chart, facet grid, panel chart, lattice plot, grid of charts, multiple lines]
family: change-over-time
also: [magnitude, distribution, correlation]
question: How does the same pattern differ across many categories, each shown in its own small panel?
shapes: ["time,n,q", "time,q*n", "n,n,q", "n,q*n"]
goals: [small multiples, facet, per region, per category, one chart each, grid, compare shapes, many series, panel, trellis, by country, breakdown]
max_series: 30
max_categories: 30
evidence: medium
popularity: rising
status: stable
support:
  mermaid: approx
  vega-lite: native
  plotly: native
  chartjs: approx
  matplotlib: native
  terminal: approx
  echarts: approx
  pptx: image
  quickchart: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://www.datawrapper.de/blog/small-multiple-line-charts, https://vega.github.io/vega-lite/docs/facet.html, https://plotly.com/python/facet-plots/, https://journals.sagepub.com/doi/10.1177/15291006211051956]
---

# Small multiples

## When to use

- More than about 5 series on one axis would tangle: one panel per series, same chart type, same axes, laid out in a grid.
- The comparison is of shapes (does every region show the same seasonal dip) rather than of values at one x.
- Series with very different levels that would flatten each other on a shared chart; each panel gets its own detail while the shared scale keeps them honest.
- Any base chart: lines over time, columns per period, scatters per group, maps per year.
- Excels at: turning slow cross-series comparison into fast parallel shape recognition; the reader scans the grid like a table.

## When not to use

- Few series (2 to 4) that must be compared at the same x: overlay them on one `line` chart.
- Panels so small that the shape disappears (below about 100 px wide): fewer panels per row, or a `heatmap`, or a `horizon` chart.
- Panels with different y scales without a warning: readers assume shared axes; if scales must differ, say so on each panel.
- Grids with no meaningful order: order panels by a value (last value, total, rank) or by geography, never alphabetically by default.
- More than about 30 panels: pick the top movers and grey the rest in one panel each, or summarise.

## Substitutes

- Few series compared at the same x: `line` (overlay).
- Many series, pattern only: `heatmap` (time on x, series on y).
- Many series, compact, with sign: `horizon`.
- Trend per row of a table: `sparkline`.
- Composition of a total: `stacked-area` (only when the total matters).

## Evidence

- Franconeri et al. 2021: side-by-side comparison of shapes is fast, while comparing values across separated regions is slow; small multiples exploit the first and should mitigate the second with a repeated reference line (overall mean) in every panel. Tufte's long-standing advocacy and Datawrapper's promotion of "multiple lines" and "small multiple columns" to first-class chart types (2023 to 2024) are the practitioner consensus. A review plus consensus: `medium`.
- Each panel keeps the base chart's encoding (position for lines and columns), so per-panel accuracy is as good as the base chart; the shared scale is what makes cross-panel reading valid.
- Datawrapper's guidance: same scale, same size, sorted panels, a highlighted panel or a grey "all others" background in each.

## Accessibility

- Shared axes with ticks on the outer panels only, but every panel titled with its category and, ideally, its last value.
- A light grey copy of all series behind each panel's highlighted series gives context without colour.
- Text alternative: "Small multiples of <measure> over time, one panel per <category> (N panels), ordered by <order>; <category> rises most, <category> falls; all share the same scale." Provide the table.
- Keep panel count and size such that lines stay at 1.5 px and text at 11 px or more; on narrow screens reflow to fewer columns.

## Build

Hand-written for every target; there is no builder. Build the base chart first with `cw.py build --chart line ...`, then wrap it as below.

### mermaid

`approx`: Mermaid has no facet. Emit one `xychart-beta` block per panel, each with the same explicit `y-axis "unit" 0 --> max` so the scales match, stacked vertically; readers scroll rather than scan a grid, and titles carry the category name. Beyond about 6 panels render an image instead.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "regions.csv"},
 "facet": {"field": "region", "type": "nominal", "columns": 4, "sort": {"field": "value", "op": "max", "order": "descending"}},
 "spec": {"width": 140, "height": 90, "mark": "line",
          "encoding": {"x": {"field": "date", "type": "temporal", "axis": {"format": "%y"}}, "y": {"field": "value", "type": "quantitative"}}}}
```

`facet` shares scales by default (`"resolve": {"scale": {"y": "independent"}}` to break that, with a warning in the caption). For a grey background of all series add a layer with `"detail"` on a copy of the data without the facet field. `"row"` and `"column"` encodings inside a single spec are the shorthand.

`cw.py build --chart small-multiples --target vega-lite --data file.csv --x date --y value --series panel` facets one line per panel, three columns, shared axes.

### plotly

Python: `px.line(df, x="date", y="value", facet_col="region", facet_col_wrap=4)`; plotly.js: `make_subplots`-style layout with one trace per `xaxisN`/`yaxisN` pair and `matches: "y"` on each y axis to share the scale. Hand-written.

### chartjs

`approx`: one `<canvas>` and one `new Chart` per panel in a CSS grid, with `options.scales.y.min` and `max` set identically by hand and `plugins.legend.display = false`; nothing links the panels. Hand-written.

### matplotlib

`fig, axes = plt.subplots(rows, cols, sharex=True, sharey=True, figsize=(cols * 2.2, rows * 1.6))`, then `for ax, (name, sub) in zip(axes.flat, groups): ax.plot(sub.date, sub.value); ax.set_title(name, fontsize=9)`; hide unused axes with `ax.set_visible(False)`. seaborn: `sns.relplot(data=df, x="date", y="value", col="region", col_wrap=4, kind="line")`. Hand-written, then `cw.py render --target matplotlib --in chart.py --out chart.png`.

### terminal

One sparkline per panel: `cw.py build --chart line --target terminal --data file.csv --x date --y value --series panel`.

### echarts

Hand-written: several `grid` entries with matching series `xAxisIndex`/`yAxisIndex`. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
