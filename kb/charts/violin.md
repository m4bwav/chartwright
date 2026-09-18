---
name: Violin plot
slug: violin
aliases: [violin chart, half violin, mirrored density]
family: distribution
also: [deviation]
question: What is the full shape of a numeric variable in each group, not just its median and spread?
shapes: ["n,q", "o,q"]
goals: [distribution, shape, compare groups, bimodal, density per group, spread, skew, violin]
max_series: 0
max_categories: 12
evidence: medium
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: native
  chartjs: approx
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/violin.html, https://vega.github.io/vega-lite/examples/layer_violin_density.html, https://plotly.com/python/violin/, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.violinplot.html]
---

# Violin plot

## When to use

- Comparing groups whose distributions are not simple humps: bimodal, heavily skewed, or with gaps that a box would hide.
- Moderate n per group (50 upwards) so the density estimate is stable.
- Up to about 12 groups side by side; beyond that the violins get too thin to read.
- Paired with an inner box or median dot so readers still get the summary statistics.
- Excels at: showing that two groups with the same median have different shapes (FT: "more complex distributions").

## When not to use

- Small n: the smooth outline invents shape from a handful of points; use `strip` or `beeswarm`.
- Bounded variables: the density spills past zero or 100; clip (`cut=0` in seaborn) or use a histogram.
- The mirrored outline is redundant: the left half repeats the right. A half violin frees the other side for the raw points (`raincloud`).
- Audiences unfamiliar with density: the width has no unit; explain "wider means more values here".
- When counts per group matter: violins are usually scaled to equal area or width; state the scaling or scale by count.

## Substitutes

- Summary only, many groups: `boxplot`.
- Shape plus raw points plus summary: `raincloud`.
- Many ordered groups: `ridgeline`.
- Small n: `strip`, `beeswarm`.
- Precise cross-group comparison of whole distributions: `ecdf`.
- One group: `density` or `histogram`.

## Evidence

- Correll and Gleicher 2014 found violins (and gradient plots) read more accurately than bar-plus-error-bar for uncertainty, and Franconeri et al. 2021 recommend showing distributions over summaries. The density estimate itself carries the bandwidth caveat of `density`: `medium`.
- FT caveat: more complex than a box plot; use when the shape is the story.
- No study compares full and half violins; the redundancy argument is practitioner reasoning (Allen et al. 2019), not measured.

## Accessibility

- Add an inner box or a median line and quartile ticks; the outline alone gives no anchor for screen readers or for precise reading.
- Label groups on the axis; one fill colour is enough since groups are identified by position, or a distinct colour per group with a legend when the same groups recur across charts.
- Text alternative: "Violin plot of <measure> by <group>; <group A> is bimodal with peaks near X and Y, <group B> is concentrated near Z."
- Outline stroke 1.5 px or more at 3:1 contrast; fill at 40 to 60 percent opacity.

## Build

### mermaid

Not drawable in Mermaid. Render with the matplotlib or vega-lite target and link the image.

### vega-lite

No violin mark. Compose a density transform with an area mark whose width is the density, one column per group, mirrored by drawing the density on both sides via `x` and `x2` or by stacking with `"stack": "center"`:

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "values.csv"},
 "transform": [{"density": "value", "groupby": ["group"]}],
 "mark": {"type": "area", "orient": "horizontal"},
 "encoding": {"y": {"field": "value", "type": "quantitative"},
              "x": {"field": "density", "type": "quantitative", "stack": "center", "axis": null},
              "column": {"field": "group", "spacing": 0}, "color": {"field": "group", "legend": null}}}
```

Hand-written; the inner box is a second layer with `boxplot`. Real work, hence `approx`.

### plotly

`{"type": "violin", "x": groups, "y": values, "box": {"visible": true}, "meanline": {"visible": true}, "points": "outliers"}`; `side: "positive"` gives a half violin, `scalemode: "count"` scales width by n. Hand-written; `cw.py build` does not emit it.

### chartjs

Community plugin `@sgratzl/chartjs-chart-boxplot` also registers a `violin` type: `{"type": "violin", "data": {"labels": groups, "datasets": [{"data": [[...], [...]]}]}}`. Hand-written; plugin quality is community-maintained.

### matplotlib

`ax.violinplot([g1, g2], showmedians=True)`, or `seaborn.violinplot(data=df, x="group", y="value", inner="box", cut=0, ax=ax)` (`inner="quart"` for quartile lines, `split=True` with `hue` for two-sided comparisons). Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
