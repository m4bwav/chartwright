---
name: Error bars
slug: error-bars
aliases: [confidence interval plot, dot and interval, mean with error bars, point range, dynamite plot]
family: distribution
also: [deviation, magnitude]
question: What is the estimate for each group and how uncertain is it?
shapes: ["n,q,q,q", "n,q,q", "o,q,q,q", "time,q,q,q"]
goals: [uncertainty, confidence interval, standard error, standard deviation, mean per group, estimate, margin of error, precision, error bars]
max_series: 3
max_categories: 20
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
  echarts: approx
  pptx: approx
  quickchart: none
  xlsx: image
  gdocs: image
  docx: image
  gsheets: image
  observable-plot: native
  d2: none
  plantuml: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://vega.github.io/vega-lite/docs/errorbar.html, https://plotly.com/python/error-bars/, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.errorbar.html, https://journals.sagepub.com/doi/10.1177/15291006211051956, https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary]
---

# Error bars

## When to use

- A point estimate per group (mean, proportion, model coefficient) with a stated interval: confidence interval, standard error or standard deviation.
- Comparing estimates across up to about 20 groups, ordered by value, as a dot with a horizontal interval (a "dot and interval" or coefficient plot).
- Time series of estimates with an interval per period when a band is not possible (irregular periods, few points).
- Scientific and survey reporting where the interval type is a required disclosure.
- Excels at: a compact, honest statement of "this much, give or take this much" for many groups on one aligned scale.

## When not to use

- Bar plus error bar (the "dynamite plot"): readers judge values inside the bar as more likely than values just outside it, though both are inside the interval (Correll and Gleicher 2014); draw a dot, not a bar.
- Unstated interval type: SD, SE and 95 percent CI differ by a factor of two or more; the caption must say which. Never mix types in one chart.
- When the distribution is the message: intervals hide shape; use `violin`, `raincloud` or a quantile dot plot.
- Overlapping intervals used to judge significance: overlap of two 95 percent CIs does not mean no difference; plot the difference with its own interval.
- Many series with intervals on one axis: the caps tangle; facet.

## Substitutes

- Uncertainty over continuous x: `range-band` (fan or ribbon).
- Full distribution per group: `violin`, `boxplot`, `raincloud`.
- Two estimates compared per group: `dumbbell`.
- Estimates without uncertainty: `dot-plot`, `lollipop`.
- Quantile dot plots (Kay et al. 2016) when the audience must judge probabilities.

## Evidence

- Correll and Gleicher 2014 ("Error Bars Considered Harmful") measured the within-the-bar bias of bar plus error bar and found gradient and violin plots read more accurately; Kay et al. 2016 showed quantile dot plots beat intervals for probabilistic judgements; Franconeri et al. 2021 recommend distributions over bare intervals: `medium`, and the specific advice is "dot with interval, never bar with interval, and name the interval".
- The dot is position on a common scale (accurate); the interval's end points are also positions, so the encoding itself is fine; the failures are interpretive.

## Accessibility

- Dot at 6 px or more, interval stroke 2 px, caps optional; the dot and its interval in the same colour.
- Caption states the interval: "bars show 95 percent confidence intervals" (or SD, SE, with n).
- Order groups by estimate; horizontal layout with labels on the left for long names.
- Text alternative: "Dot and interval chart of <estimate> by <group> with 95 percent CIs; <group A> is highest at X (CI Y to Z); the intervals of <B> and <C> overlap."
- 3:1 contrast; do not encode significance by colour alone, add a marker shape or a label.

## Build

### mermaid

Not drawable in Mermaid (no error bars, no per-point ranges). Render with the vega-lite or matplotlib target and link the image; if it must be text, a table with estimate and interval columns.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "estimates.csv"},
 "layer": [
  {"mark": {"type": "errorbar", "ticks": true}, "encoding": {"y": {"field": "group", "type": "nominal", "sort": "-x"},
     "x": {"field": "lower", "type": "quantitative", "title": "estimate"}, "x2": {"field": "upper"}}},
  {"mark": {"type": "point", "filled": true, "size": 60}, "encoding": {"y": {"field": "group", "type": "nominal", "sort": "-x"},
     "x": {"field": "mean", "type": "quantitative"}}}]}
```

Hand-written; `cw.py build` does not emit it. With raw values instead of precomputed bounds, `"mark": {"type": "errorbar", "extent": "ci"}` on the raw field computes a bootstrapped 95 percent CI (`"stderr"`, `"stdev"`, `"iqr"` are the alternatives).

### plotly

`{"type": "scatter", "mode": "markers", "x": means, "y": groups, "error_x": {"type": "data", "symmetric": false, "array": upper_minus_mean, "arrayminus": mean_minus_lower}}`; `error_y` for vertical layouts. Hand-written.

### chartjs

Community plugin `chartjs-chart-error-bars` adds `barWithErrorBars`, `lineWithErrorBars` and `scatterWithErrorBars` types; data points carry `{x, y, yMin, yMax}`. Prefer `scatterWithErrorBars` (dot, not bar). Hand-written.

### matplotlib

`ax.errorbar(means, groups, xerr=[means - lower, upper - means], fmt="o", capsize=3, markersize=6)` for a horizontal dot and interval chart; `yerr` for vertical. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: custom series `renderItem` (the ECharts error-bar example). See `kb/targets/echarts.md`.

### pptx

Approximate: LINE_MARKERS plus manual error bars (python-pptx has no API); simpler as a PNG.

### observable-plot

`Plot.ruleX(data, {x1: "low", x2: "high", y})` (or `ruleY`) under a `Plot.dot` of the estimate.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
