---
name: Scatter plot
slug: scatter
aliases: [scatterplot, XY plot, scatter chart, scattergram, dot cloud]
family: correlation
also: [distribution, deviation]
question: Is there a relationship between two numeric variables, and where are the clusters and outliers?
shapes: ["q,q", "q,q,n", "q,q,text"]
goals: [correlation, relationship, versus, against, x vs y, association, clusters, outliers, trend line, regression, two variables, scatter]
max_series: 4
max_categories: 0
evidence: high
popularity: core
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: native
  matplotlib: native
  terminal: none
  echarts: native
  pptx: native
  quickchart: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/chart-types-guide, https://journals.sagepub.com/doi/10.1177/15291006211051956, https://vega.github.io/vega-lite/docs/point.html, https://plotly.com/python/line-and-scatter/, https://www.chartjs.org/docs/latest/charts/scatter.html, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html]
---

# Scatter plot

## When to use

- Two numeric measures per unit and the question is whether they move together, in which direction, how tightly, and with what exceptions.
- Finding clusters, gaps and outliers that a correlation coefficient hides.
- Up to about four groups distinguished by colour and shape, or one group highlighted against grey.
- Any n from tens to a few thousand; above that, thin with transparency or switch to `hexbin`.
- Excels at: the default for "X relates to Y"; both axes are position on a common scale, so each point's two values are read accurately, and the cloud's shape is grasped at once.

## When not to use

- Implying causation: a scatter shows association; the title must not say "X drives Y" unless the design supports it.
- Overplotting: thousands of points at the same spot become a blob; use alpha, smaller markers, sampling, `hexbin` or `density-2d`.
- Two time series against time: that is a `line` (or a `connected-scatter` if the pair's path matters), not a scatter of one against the other, unless the relationship is the question.
- Categorical x: that is a `strip` or `dot-plot`.
- Dual y axes as a substitute for a scatter: two lines on two scales invent crossings; plot the pair as a scatter or index both.
- Adding a trend line to data with clusters or curvature: fit the right model (loess) or none; a straight line through a curve misleads.

## Substitutes

- Third numeric variable: `bubble` (size) or colour ramp.
- Change over time of the pair: `connected-scatter`.
- Many variable pairs: `splom`; correlation coefficients only: `correlogram`.
- Large n: `hexbin`, `density-2d`.
- Two categorical dimensions and a value: `heatmap`.
- Positioning items against two thresholds: `quadrant`.

## Evidence

- Both encodings are position along a common scale, the top of Cleveland and McGill 1984, replicated by Heer and Bostock 2010: `high`.
- Correlation strength is systematically underestimated by viewers, and the perceived r depends on the aspect ratio and point density (Rensink and Baldridge 2010; reviewed in Franconeri et al. 2021), so print r or the fitted slope on the chart rather than trusting the impression.
- Franconeri et al. 2021: clusters and outliers are extracted fast as global features; comparing two specific points is slow, so label the points that matter.
- Square aspect ratio and equal axis treatment keep the cloud's shape honest; the axes need not start at zero, and the caption should say so.

## Accessibility

- Groups by colour and marker shape (circle, square, triangle), never colour alone; legend plus direct labels on notable points.
- Markers 5 px or larger with a thin darker outline; alpha 0.5 to 0.7 when points overlap.
- Text alternative: "Scatter plot of <y> against <x> for <n> <units>; a positive relationship (r = 0.6), with <unit> an outlier at high x and low y."
- Axis titles with units; gridlines light; a trend line, if drawn, in a colour distinct from all groups with its equation or r in the caption.

## Build

### mermaid

Not drawable in Mermaid (`xychart` has no point series). Render with the vega-lite target and link the image.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "points.csv"},
 "mark": {"type": "point", "filled": true, "opacity": 0.7},
 "encoding": {"x": {"field": "income", "type": "quantitative", "scale": {"zero": false}},
              "y": {"field": "life_expectancy", "type": "quantitative", "scale": {"zero": false}},
              "color": {"field": "region", "type": "nominal"}, "shape": {"field": "region", "type": "nominal"},
              "tooltip": [{"field": "country"}, {"field": "income"}, {"field": "life_expectancy"}]}}
```

`cw.py build --chart scatter --target vega-lite --data points.csv --x income --y life_expectancy [--series region] [--html]`. A trend line is a second layer with `"transform": [{"regression": "life_expectancy", "on": "income"}]` and `"mark": "line"` (`loess` for a curve); labels are a `text` layer filtered to the points of interest.

### plotly

`{"type": "scatter", "mode": "markers", "x": [...], "y": [...], "text": names, "marker": {"size": 8, "opacity": 0.7}}` per group; `px.scatter(df, x=..., y=..., color=..., symbol=..., trendline="ols", hover_name="country")` in Python. `cw.py build --chart scatter --target plotly --data points.csv --x income --y life_expectancy --html`.

### chartjs

`{"type": "scatter", "data": {"datasets": [{"label": "Europe", "data": [{"x": 1, "y": 2}, ...], "pointStyle": "circle"}]}}` with `scales.x.type = "linear"`; vary `pointStyle` per dataset for shape. `cw.py build --chart scatter --target chartjs --data points.csv --x income --y life_expectancy --html`.

### matplotlib

`ax.scatter(x, y, s=30, alpha=0.7, label=name, marker="o")` per group with distinct markers, `ax.legend()`, `ax.annotate(name, (xi, yi))` for outliers; `numpy.polyfit` or `seaborn.regplot` for a trend line. `cw.py build --chart scatter --target matplotlib --data points.csv --x income --y life_expectancy --out chart.py --png chart.png` then `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

`cw.py build --chart scatter --target echarts --data file.csv --x <x> --y <y> [--series <s>] --html` writes the option and page.

### pptx

`cw.py build --chart scatter --target pptx --data file.csv --x <x> --y <y> [--series <s>] --out chart.py --png chart.pptx` then `cw.py render --target pptx --in chart.py --out chart.pptx` (editable native chart).

### quickchart

`cw.py build --chart scatter --target quickchart --data file.csv --x <x> --y <y> [--series <s>]` prints a markdown image line whose URL renders the chart (data is public in the URL).

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
