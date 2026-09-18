---
name: 100% stacked bar chart
slug: stacked-bar-100
aliases: [percent stacked bar, normalized stacked bar, proportional stacked bar, 100% stacked column]
family: part-to-whole
also: [deviation, change-over-time]
question: What share of each whole does every part take, compared across categories?
shapes: ["n,q*n", "o,q*n", "time,q*n"]
goals: [share, percentage, proportion, composition, part to whole, mix, relative, per cent, normalized, compare shares, split]
max_series: 4
max_categories: 12
evidence: medium
popularity: core
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: approx
  matplotlib: approx
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/stacked-column-charts, https://vega.github.io/vega-lite/docs/stack.html, https://plotly.com/javascript/reference/layout/#layout-barnorm]
---

# 100% stacked bar chart

## When to use

- Several wholes of different sizes and the question is the mix inside each: market share by country, vote split by district, survey answers by group.
- The reader compares the same part across bars: place it on the baseline (or against the top edge) so its share reads as position on a common scale.
- Composition over time when totals are irrelevant or shown elsewhere: share of energy sources per year.
- The selection rules' default for "X is N% of the whole" when there is more than one whole.
- Excels at: a row of bars whose first and last segments can be compared accurately at a glance; the majority line (50%) is a natural reference.

## When not to use

- Totals matter: normalising hides that one bar is ten times another; use `stacked-bar` or add a separate bar of totals.
- Middle segments are the message: their bases float and readers cannot compare them; reorder so the key segment sits on an edge, or use `small-multiples`.
- More than four segments or many tiny segments: fold into "Other".
- One whole only: a single 100% bar is fine, but a `pie` or `waffle` may answer a majority question faster.
- Categories with widely different base sizes where the size should influence the read: `marimekko`.

## Substitutes

- Totals plus mix: `stacked-bar`; two-dimensional shares with meaningful widths: `marimekko`.
- Ordered survey scales centred on neutral: `diverging-stacked-bar`.
- One whole, few parts: `pie`, `donut`, `waffle`.
- Shares over many periods: `stacked-area` normalised.
- Exact shares per cell: a `table` with inline bars or a `heatmap`.

## Evidence

- The edge segments are position on a common scale and are read accurately; inner segments are non-aligned lengths and are not (Cleveland and McGill 1984; Heer and Bostock 2010). `medium`: the same evidence as the stacked bar, with the added benefit that both edges are aligned.
- Datawrapper's 2025 stacked-column guidance: put the compared series on the baseline, keep to about four segments, and split bars when readers need every segment.
- Franconeri et al. 2021: the layout decides which comparison is easy; a 100% stack makes "share of the first segment across groups" easy and everything else slow.

## Accessibility

- Label shares directly (percent with no decimals) inside segments wide enough; the rest in a legend that follows stack order.
- One hue ramp for ordered segments, at most four distinct colour-blind-safe hues for unordered ones; hatching for print.
- Text alternative: "100% stacked bar chart of <parts> share by <category>; <part> ranges from <min> in <A> to <max> in <B>." Offer the table with counts and shares.
- State the base counts (n per bar) in a caption so small groups are not read as strong evidence.

## Build

### mermaid

Mermaid `xychart` has no stacking or normalisation. Render with vega-lite to an image and link it.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "shares.csv"},
 "mark": "bar",
 "encoding": {"y": {"field": "country", "type": "nominal"},
              "x": {"field": "count", "type": "quantitative", "stack": "normalize", "axis": {"format": "%"}},
              "color": {"field": "source", "type": "nominal"}, "order": {"field": "source"}}}
```

Hand-written from the `stacked-bar` builder output: `cw.py build --chart stacked-bar --target vega-lite --data shares.csv --x country --y count --series source`, then set `"stack": "normalize"` on the quantitative channel and `"axis": {"format": "%"}`.

### plotly

One bar trace per segment, `layout.barmode = "stack"` and `layout.barnorm = "percent"`; Plotly normalises each bar itself. Hand-written from `cw.py build --chart stacked-bar --target plotly ...` plus the `barnorm` line.

### chartjs

Chart.js has no normalisation option: divide each value by its bar total before building, then use the stacked-bar config with `scales.y.max = 100` and a `%` tick callback. `approx` because the arithmetic lives outside the chart.

### matplotlib

Hand-written: compute `shares = values / values.sum(axis=0)`, then `ax.bar(cats, share_i, bottom=cumulative)` per segment with `ax.yaxis.set_major_formatter(PercentFormatter(1.0))`. `approx` for the same reason as Chart.js. Render with `cw.py render --target matplotlib`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
