---
name: Cumulative distribution (ECDF)
slug: ecdf
aliases: [empirical cumulative distribution function, cumulative curve, cumulative frequency plot, Lorenz curve, percentile plot]
family: distribution
also: [correlation, deviation]
question: What fraction of values is below x, and how do several distributions compare across their whole range?
shapes: ["q", "q,n"]
goals: [distribution, cumulative, fraction below, percentile, share under, compare distributions, latency, inequality, ecdf]
max_series: 6
max_categories: 0
evidence: medium
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: native
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://seaborn.pydata.org/generated/seaborn.ecdfplot.html, https://plotly.com/python/ecdf-plots/, https://vega.github.io/vega-lite/examples/area_cumulative_freq.html, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.ecdf.html, https://www.data-to-viz.com/]
---

# Cumulative distribution (ECDF)

## When to use

- Questions phrased as "what share is under x" or "what is the 95th percentile": read them straight off the curve.
- Comparing up to about six distributions precisely: curves on a shared 0 to 1 axis never occlude and every quantile is comparable, unlike overlaid histograms.
- Latency and performance data (p50, p95, p99), income and inequality (the Lorenz curve is the ECDF of cumulative share), reliability (time to failure).
- Any n: no bins, no bandwidth, no smoothing choices; the curve is the data.
- Excels at: distribution comparison without a single analyst choice that could change the picture.

## When not to use

- General audiences without a caption: the cumulative axis is unfamiliar and readers look for a peak that is not there.
- The message is shape (modes, skew): a bump in a histogram becomes a subtle change of slope in an ECDF; show a `histogram` or `density` alongside.
- More than about six curves: they cross and tangle; facet or grey-plus-highlight.
- When counts per group matter: the y axis is a share, so group sizes vanish; put n in the legend.

## Substitutes

- Shape of one variable: `histogram`, `density`.
- Summary across many groups: `boxplot`.
- Few groups, shape and summary: `violin`, `raincloud`.
- Percentiles as a single number per group: `dot-plot` of the chosen percentile with `error-bars`.

## Evidence

- The curve is position on a common scale on both axes (Cleveland and McGill 1984), and vertical distance between curves at any x is a direct aligned comparison, so quantile lookups are accurate. Widely recommended in engineering and analytics practice (seaborn, Plotly and matplotlib all added dedicated functions between 2020 and 2023): `medium`, since no perception study tests ECDF reading against histograms for lay readers.
- Franconeri et al. 2021: readers extract shape fast but a cumulative curve's "shape" is not the distribution's shape, which is the main comprehension risk for non-experts.

## Accessibility

- Label the y axis "share of values at or below x" (or "cumulative %"); mark the 0.5 and 0.95 gridlines when the question is about medians or tails.
- Direct-label each curve at its right end; distinct hue plus line style for more than three.
- Text alternative: "Cumulative distribution of <measure> for <groups>; half of <A> is below X versus Y for <B>; the 95th percentile is Z for <A>."
- Stroke 2 px; 3:1 contrast; a step (not interpolated) line is the honest rendering for small n.

## Build

### mermaid

Not drawable in Mermaid (no continuous x axis with a step line). Render with the vega-lite or matplotlib target and link the image.

### vega-lite

No ECDF mark; a window transform over sorted values builds it:

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "values.csv"},
 "transform": [{"sort": [{"field": "value"}], "window": [{"op": "count", "as": "n"}], "frame": [null, 0], "groupby": ["group"]},
               {"joinaggregate": [{"op": "count", "as": "total"}], "groupby": ["group"]},
               {"calculate": "datum.n / datum.total", "as": "share"}],
 "mark": {"type": "line", "interpolate": "step-after"},
 "encoding": {"x": {"field": "value", "type": "quantitative"}, "y": {"field": "share", "type": "quantitative", "axis": {"format": "%"}},
              "color": {"field": "group", "type": "nominal"}}}
```

Hand-written; the three transforms are the "real work" that makes this `approx`.

### plotly

`px.ecdf(df, x="value", color="group")` (plotly.py 5.x and later); `ecdfnorm="percent"` for a percent axis, `marginal="histogram"` to add the shape above. Hand-written; `cw.py build` does not emit it.

### chartjs

Sort values in code, compute `i / n` for each, then a `line` type with `stepped: "after"`, `pointRadius: 0`, `scales.x.type = "linear"` and `scales.y.max = 1`. Hand-written.

### matplotlib

`ax.ecdf(values, label=name)` (matplotlib 3.8+) per group, or `seaborn.ecdfplot(data=df, x="value", hue="group", ax=ax)`; `ax.axhline(0.95, ls=":")` marks a percentile of interest. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: `line` with `step: "end"` over sorted cumulative values. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
