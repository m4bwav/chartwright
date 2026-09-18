---
name: Ridgeline plot
slug: ridgeline
aliases: [joyplot, joy plot, ridge plot, stacked density plot]
family: distribution
also: [change-over-time]
question: How does the shape of a distribution shift across many ordered groups, such as months, years or dose levels?
shapes: ["o,q", "time,q", "n,q"]
goals: [distribution, shift, over time, many groups, ordered groups, shape, seasonality, ridgeline, joyplot]
max_series: 0
max_categories: 30
evidence: low
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: none
  matplotlib: approx
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
sources: [https://www.data-to-viz.com/graph/ridgeline.html, https://vega.github.io/vega-lite/examples/area_density_stacked.html, https://plotly.com/python/violin/, https://github.com/leotac/joypy, https://wilkelab.org/ggridges/]
---

# Ridgeline plot

## When to use

- Six to thirty groups with a natural order (months, years, age bands, dose levels) and the question is how the shape drifts along that order.
- Each group has enough values (50 upwards) for a stable density.
- The distributions overlap on the value axis; the vertical offset separates them where overlaid densities would tangle.
- Seasonal patterns (temperature by month) or a shift over years (income by cohort).
- Excels at: a wall of distributions read as one landscape; the eye follows the peak from ridge to ridge.

## When not to use

- Unordered groups: the stacking order is arbitrary and the "drift" it shows is fiction; use `boxplot` or `violin`.
- Few groups (under five): overlaid `density` curves or `violin` compare more directly.
- When values must be read precisely: the overlap hides the lower parts of each ridge and there is no shared baseline.
- Small n per group; the smoothing invents peaks.
- Narrow layouts: ridgelines need height (about 25 px per group) to avoid overlap that hides peaks.
- Comparing counts: ridges are usually normalised, so a busy month and a quiet one look alike; say so or scale by count.

## Substitutes

- Few groups: `density` overlaid, or `violin`.
- Summary statistics over ordered groups: `boxplot` per period, or a `line` of the median with a `range-band`.
- Many groups where exact comparison matters: `small-multiples` of histograms with shared axes, or `ecdf`.
- Time on x and distribution as colour: `heatmap` (period by value bin).

## Evidence

- No perception study of ridgelines; the form is a 2017 convention (`ggridges`) adopted because stacked densities save space: `low`.
- What it inherits: shape extraction is fast (Franconeri et al. 2021) so the peak drift is read at a glance; values across ridges are on non-aligned scales, which Cleveland and McGill 1984 rank below aligned position, so exact comparison is poor.
- From Data to Viz caveat: works only when the groups are ordered and the overlap is moderate.

## Accessibility

- Label each ridge on the left; no legend.
- A single hue with slight opacity is clearest; if colour encodes the group value (a viridis ramp along the order) it is redundant with position and safe.
- Text alternative: "Ridgeline plot of <measure> by <ordered group>; the peak moves from X in <first> to Y in <last>; <group> is the widest."
- Keep each ridge's outline at 3:1 contrast; overlap no more than about half a ridge height.

## Build

### mermaid

Not drawable in Mermaid. Render with the matplotlib or vega-lite target and link the image.

### vega-lite

Density transform plus row faceting with negative spacing so the ridges overlap:

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "values.csv"},
 "transform": [{"density": "value", "groupby": ["month"]}],
 "mark": {"type": "area", "line": true, "opacity": 0.7},
 "encoding": {"x": {"field": "value", "type": "quantitative"}, "y": {"field": "density", "type": "quantitative", "axis": null},
              "row": {"field": "month", "type": "ordinal", "header": {"labelAngle": 0, "labelAlign": "left"}}},
 "config": {"facet": {"spacing": -12}, "view": {"stroke": null}}}
```

Hand-written; `cw.py build` does not emit it. Set `"height": 30` on the inner view and `"bounds": "flush"` so the ridges overlap cleanly. Real composition work, hence `approx`.

### plotly

One `violin` trace per group with `side: "positive"`, `orientation: "h"`, `width: 3`, `points: false`, and `layout.yaxis` categories in order; the horizontal half violins overlap like ridges. Or one `scatter` line with `fill: "tozeroy"` per group on stacked subplots. Hand-written.

### matplotlib

`joypy.joyplot(df, by="month", column="value", overlap=0.6)` (pip `joypy`), or plain matplotlib: one density per group via `scipy.stats.gaussian_kde`, drawn with `ax.fill_between(grid, i * step, i * step + density, alpha=0.7)` and group labels on the left. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`. Composition rather than a primitive, hence `approx`.

### echarts

Hand-written: several `grid` entries with `line` plus `areaStyle` offset per row. See `kb/targets/echarts.md`.

### observable-plot

`Plot.areaY` with `fy: "group"` facets and a small negative `marginBottom`; density computed beforehand.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
