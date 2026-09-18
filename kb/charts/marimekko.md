---
name: Marimekko chart
slug: marimekko
aliases: [mosaic plot, mekko chart, variable-width stacked bar, spine plot]
family: part-to-whole
also: [magnitude, correlation]
question: How do shares split by two categorical variables, when the widths also mean the size of each group?
shapes: ["n,n,q"]
goals: [share, segment, market share, mix, two dimensions, size and share, cross tab, contingency, part to whole, weighted]
max_series: 5
max_categories: 5
evidence: low
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: image
  matplotlib: approx
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://vega.github.io/vega-lite/examples/rect_mosaic_labelled.html, https://www.datawrapper.de/blog/chart-types-guide, https://datavizcatalogue.com]
---

# Marimekko chart

## When to use

- Two categorical variables and a quantity: column width is the total of the first (segment size), column height splits show the share of the second (product mix within the segment). Market size by region and share by supplier is the classic case.
- The reader must see both "this segment is big" and "within it, X dominates" in one picture; the area of each cell is the absolute value.
- A contingency table (mosaic plot) where independence would show as aligned splits across columns: departures from alignment are the finding.
- At most about five by five cells with labels that fit.
- Excels at: replacing a pair of charts (a bar of totals and a 100% stacked bar of shares) with one, when the audience is analytical.

## When not to use

- A general audience without annotation: readers misread widths as a third variable or as time (FT caveat).
- More than about five columns or five segments: cells become slivers and labels collide.
- Precise comparison of shares across columns: segment bases float and widths differ, so both length and area judgments are needed; use `stacked-bar-100` plus a separate `bar` of totals.
- Small totals: narrow columns hide the very segments that might matter; consider a `table`.

## Substitutes

- Totals and shares readable separately: `stacked-bar` (totals) or `stacked-bar-100` with a bar of totals beside it.
- Cross-tab pattern without sizes: `heatmap` of shares or counts.
- Nested whole by size only: `treemap`.
- Exact numbers: `table` with inline bars.

## Evidence

- No dedicated perception study; area and non-aligned length are the weakest encodings in the Cleveland and McGill 1984 ranking, and a Marimekko uses both. `low`.
- FT Visual Vocabulary lists it as a two-variable part-to-whole with the caveat that it is hard for general audiences; Datawrapper's 2025 guide and Vega-Lite's mosaic example show the form is spreading in editorial and analytical tools (`rising`).
- Franconeri et al. 2021: annotate the specific comparison; a Marimekko without cell labels asks readers to estimate two dimensions at once.

## Accessibility

- Label each cell with its value or share when it is wide enough, and every column with its total width meaning ("$4.2bn").
- One hue ramp per segment order or at most five colour-blind-safe hues; thin white borders so cells are separable.
- Text alternative: "Marimekko chart of <quantity> by <column variable> (width) and <segment variable> (height); <A> is the largest column at <total>, dominated by <segment> at <share>." Provide the cross-tab as a table.
- Axis of cumulative percent on both edges so widths can be read.

## Build

### mermaid

No Mermaid diagram draws variable-width stacked columns. Render with vega-lite to an image and link it.

### vega-lite

Hand-written from the gallery's mosaic example: two `stack` transforms (one across columns on the total, one within each column on the share) and a `rect` mark with `x`/`x2`/`y`/`y2` on the computed offsets.

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "market.csv"},
 "transform": [{"aggregate": [{"op": "sum", "field": "value", "as": "v"}], "groupby": ["region", "supplier"]},
               {"stack": "v", "groupby": ["region"], "as": ["y0", "y1"], "offset": "normalize", "sort": [{"field": "supplier"}]},
               {"window": [{"op": "sum", "field": "v", "as": "total"}], "frame": [null, null], "groupby": ["region"]},
               {"stack": "total", "groupby": [], "as": ["x0", "x1"], "sort": [{"field": "region"}]}],
 "mark": "rect",
 "encoding": {"x": {"field": "x0", "type": "quantitative"}, "x2": {"field": "x1"},
              "y": {"field": "y0", "type": "quantitative", "axis": {"format": "%"}}, "y2": {"field": "y1"},
              "color": {"field": "supplier", "type": "nominal"}}}
```

`approx` because the layout is arithmetic in transforms, not a mark; the second stack needs one row per region, so pre-aggregate totals when the window step misbehaves.

### plotly

Hand-written: one `bar` trace per segment with `x` set to column centres, `width` set to column totals (normalised), `offset: 0`, `layout.barmode = "stack"`, and `barnorm = "percent"` for the heights. `approx`, positions computed outside Plotly.

### chartjs

Chart.js bars cannot take a per-bar width; render the chart elsewhere (vega-lite or matplotlib) and embed the image.

### matplotlib

Hand-written: compute `lefts = cumsum(totals) - totals`, then per segment `ax.bar(lefts, shares_i, width=totals, bottom=cum_i, align="edge", edgecolor="white")`; label columns at `lefts + totals / 2`. Render with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: custom series `renderItem` (variable-width bars). See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
