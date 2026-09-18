---
name: Strip plot
slug: strip
aliases: [dot strip plot, jitter plot, barcode plot, rug plot, one-dimensional scatter]
family: distribution
also: [ranking, magnitude]
question: What are all the values in each category, in the least space?
shapes: ["n,q", "o,q", "q"]
goals: [distribution, all values, per category, compact, jitter, small n, raw data, dots, strip]
max_series: 0
max_categories: 30
evidence: medium
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: approx
  matplotlib: native
  terminal: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://vega.github.io/vega-lite/examples/tick_strip.html, https://plotly.com/python/strip-charts/, https://seaborn.pydata.org/generated/seaborn.stripplot.html]
---

# Strip plot

## When to use

- Small to moderate n per category (up to about 100) and the reader should see every value.
- Many categories (up to about 30) stacked as rows: a strip per row is the most space-efficient distribution display there is.
- A quick honest look at spread and outliers before choosing a summary chart.
- As the "rug" under a `histogram` or `density` to show where the real values lie.
- Excels at: compactness; thirty categories fit in the height a box plot needs for ten.

## When not to use

- Many values share the same reading: the ticks stack and hide each other (FT's caveat). Add jitter or transparency, or switch to `beeswarm`.
- Large n (thousands): the strip becomes a solid bar; use `histogram`, `violin` or `boxplot`.
- Readers need the median or quartiles: overlay a median mark, or use `boxplot`.
- The message is shape (bimodality) with large n: `density`.

## Substitutes

- Overlap-free small n: `beeswarm`.
- Summary per category: `boxplot`; shape per category: `violin`.
- One value per category: `dot-plot`, `lollipop`.
- Shape plus summary plus points: `raincloud`.
- One numeric variable, larger n: `histogram`.

## Evidence

- Each value is position on a common scale, the best-read encoding (Cleveland and McGill 1984; Heer and Bostock 2010); the only loss is occlusion when values coincide, which jitter mitigates. FT and From Data to Viz treat it as the honest small-n default: `medium` rather than `high` because occlusion is unmeasured.
- Jitter adds random displacement in the category direction only; the measure axis stays exact.

## Accessibility

- Ticks (thin vertical bars) at 60 percent opacity read better than dots when values pile up; dots at 4 px or more when n is small.
- Category labels on the left; a median marker in a second colour with a legend entry.
- Text alternative: "Strip plot of <measure> by <category>; <category A> spans A to B with one outlier at C; <category B> is tightly clustered near D."
- Seed the jitter so the chart is reproducible; say "positions jittered" in the caption.

## Build

### mermaid

Not drawable in Mermaid. Render with the vega-lite or matplotlib target and link the image.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "values.csv"},
 "mark": {"type": "tick", "opacity": 0.6},
 "encoding": {"x": {"field": "value", "type": "quantitative"}, "y": {"field": "category", "type": "nominal"}}}
```

`cw.py build --chart strip --target vega-lite --data values.csv --x value --y category [--html]`. For jitter switch to `"mark": "point"` and add `"transform": [{"calculate": "random()", "as": "jitter"}]` with `"yOffset": {"field": "jitter", "type": "quantitative"}`.

### plotly

`px.strip(df, x="value", y="category")` (a `box` trace with `boxpoints: "all"`, `pointpos: 0`, `jitter: 0.5` and the box hidden; `fillcolor: "rgba(0,0,0,0)"`, `line.color` transparent). Hand-written; `cw.py build` does not emit it.

### chartjs

A `scatter` type with the category mapped to an integer y plus a small random offset computed in code, `pointRadius: 3`, and `scales.y.ticks.callback` mapping integers back to names. Hand-written.

### matplotlib

`seaborn.stripplot(data=df, x="value", y="category", jitter=0.25, alpha=0.6, ax=ax)`; plain matplotlib: `ax.plot(values, [i] * len(values), "|", markersize=12, alpha=0.6)` per row for ticks. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
