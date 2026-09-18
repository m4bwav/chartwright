---
name: Density plot
slug: density
aliases: [KDE plot, kernel density plot, density curve, smoothed histogram]
family: distribution
also: [correlation]
question: What is the smooth shape of one numeric variable, and how do two or three groups' shapes compare?
shapes: ["q", "q,n"]
goals: [distribution, shape, smooth, density, kernel, spread, skew, compare shapes, overlay, bimodal]
max_series: 3
max_categories: 0
evidence: medium
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: approx
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
  docx: image
  gsheets: image
  observable-plot: approx
  d2: none
  plantuml: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://www.data-to-viz.com/graph/density.html, https://vega.github.io/vega-lite/docs/density.html, https://seaborn.pydata.org/generated/seaborn.kdeplot.html, https://plotly.com/python/distplot/, https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary]
---

# Density plot

## When to use

- One continuous variable with large n (hundreds upwards) where the histogram's bin edges distract from the shape.
- Two or three groups overlaid: a smooth outline per group is easier to compare than overlapping bars.
- The message is shape (skew, several peaks, a long tail), not counts; the y axis is density, which readers rarely need to read off.
- As one layer in a richer distribution chart (`violin`, `ridgeline`, `raincloud`).
- Excels at: a clean shape comparison for a few groups on one axis.

## When not to use

- Small n (under about 50): smoothing invents shape; a `strip` or `histogram` is honest.
- Bounded variables (ages, percentages, counts at zero): the kernel spills past the bound and shows impossible values; clip or use a histogram.
- When counts matter: the area is normalised to 1, so a group of 10 and a group of 10,000 look the same size; add n to the label or use a histogram.
- More than three groups overlaid: use `ridgeline` (ordered groups) or facet.
- Bandwidth choice can hide multimodality: try a narrower bandwidth before concluding "one peak".
- Readers who will read the y axis as a probability or a count.

## Substitutes

- Counts, small n, or bounded data: `histogram`.
- Many groups: `ridgeline`; groups plus summary statistics: `boxplot` or `violin`.
- Precise comparison of groups across the whole range: `ecdf`.
- Shape plus raw points: `raincloud`.
- Two variables: `density-2d` or `hexbin`.

## Evidence

- The curve is position along a common scale, but the quantity read is the outline's shape, not a value; shape extraction is fast (Franconeri et al. 2021). Practitioner consensus (From Data to Viz, FT) treats it as the histogram's smooth sibling with a bandwidth caveat: `medium`.
- No perception study compares density plots with histograms for shape judgements; the confidence would rise with one.
- The bandwidth and kernel are analyst choices that change the picture; state the bandwidth when it is not the library default.

## Accessibility

- Distinct hue and a different line style per group; fill at low opacity so overlaps stay visible; legend or direct label at each peak.
- Label the x axis with units; label the y axis "density" and say in the caption that the area under each curve is 1.
- Text alternative: "Density plot of <variable> for <groups>; group A peaks near X and is narrower than group B, which has a long right tail."
- 2 px minimum stroke, 3:1 contrast for each outline.

## Build

### mermaid

Not drawable in Mermaid (no continuous x axis with an area). Render with the vega-lite or matplotlib target and link the image.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "values.csv"},
 "transform": [{"density": "value", "groupby": ["group"], "bandwidth": 0.5}],
 "mark": {"type": "area", "opacity": 0.5, "line": true},
 "encoding": {"x": {"field": "value", "type": "quantitative"}, "y": {"field": "density", "type": "quantitative"},
              "color": {"field": "group", "type": "nominal"}}}
```

Hand-written; `cw.py build` does not emit it. Drop `bandwidth` for the automatic estimate; `"extent": [min, max]` clips a bounded variable; `"counts": true` scales curves by n. Render to an image with `cw.py render --target vega-lite --in chart.vl.json --out chart.png`.

### plotly

No KDE trace. Either compute the curve in Python (`scipy.stats.gaussian_kde`) and draw `{"type": "scatter", "mode": "lines", "fill": "tozeroy"}` per group, or use `plotly.figure_factory.create_distplot([a, b], ["A", "B"], show_hist=False)`. A `violin` trace with `side: "positive"` and no box is the other shortcut. Hand-written.

### chartjs

Compute the density curve in code, then `{"type": "line", "data": {"datasets": [{"data": [{"x": v, "y": d}, ...], "fill": "origin", "pointRadius": 0, "tension": 0.3}]}}` with `scales.x.type = "linear"`. Hand-written.

### matplotlib

`seaborn.kdeplot(data=df, x="value", hue="group", fill=True, alpha=0.4, ax=ax)`; `bw_adjust=0.5` narrows the bandwidth, `clip=(0, None)` respects a bound, `common_norm=False` normalises each group separately. Plain matplotlib: `scipy.stats.gaussian_kde(values)(grid)` then `ax.fill_between(grid, curve, alpha=0.4)`. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: `line` with `areaStyle` over pre-computed density points. See `kb/targets/echarts.md`.

### observable-plot

no 1D density mark: compute the KDE in JS (d3) or use `Plot.rectY(data, Plot.binX({y: "proportion"}))` as a histogram stand-in.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
