---
name: Q-Q plot
slug: qq
aliases: [quantile-quantile plot, QQ plot, normal probability plot, probability plot]
family: distribution
also: [correlation]
question: Does a sample follow a theoretical distribution (usually normal), or the same distribution as another sample?
shapes: ["q", "q,q"]
goals: [distribution, normality, residuals, diagnostic, quantiles, theoretical, fit, heavy tails, qq plot]
max_series: 3
max_categories: 0
evidence: low
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://www.statsmodels.org/stable/generated/statsmodels.graphics.gofplots.qqplot.html, https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html, https://vega.github.io/vega-lite/docs/quantile.html, https://plotly.com/python/v3/normality-test/, https://datavizcatalogue.com/]
---

# Q-Q plot

## When to use

- Checking whether model residuals are normal before trusting a t-test, a confidence interval or a linear model.
- Comparing two samples' distributions quantile by quantile (a two-sample Q-Q plot) when the question is "same shape?".
- Spotting heavy tails, skew and outliers: they show as curvature or points leaving the reference line at the ends.
- Statistical appendices, model diagnostics, analytical notebooks.
- Excels at: a sharp visual test of distributional fit where a histogram is too coarse to judge the tails.

## When not to use

- Any general audience: the axes are quantiles of quantiles and nothing else reads naturally; use a `histogram` with the fitted curve overlaid.
- Small n (under about 20): the extreme quantiles wobble on their own and the plot over-alarms.
- When the question is "what does the distribution look like", not "does it match": `histogram`, `density`, `ecdf`.
- More than three samples on one plot; facet instead.

## Substitutes

- Shape for a non-statistical reader: `histogram` with a fitted normal curve, `density`.
- Comparing several distributions precisely: `ecdf`.
- Quick summary of many groups: `boxplot`.
- Checking a relationship rather than a distribution: `scatter` of residuals against fitted values.

## Evidence

- The plot is a scatter (position on two aligned scales), so deviations from the 45 degree line are seen accurately; there is no perception study of Q-Q plots as a communication device, and their use is a statistical convention: `low`. The rating would rise with a study of how reliably analysts detect non-normality from them versus tests.
- Practitioner guidance (statsmodels, R `qqnorm`) is unanimous that the plot outperforms a normality test for judging what kind of departure exists.

## Accessibility

- Draw the reference line (45 degrees, or the fitted line through the quartiles) in a contrasting colour and say which in the caption.
- Equal axis scaling so the line is really at 45 degrees; label both axes ("theoretical quantiles", "sample quantiles").
- Text alternative: "Normal Q-Q plot of <variable>, n = <n>; points follow the line in the centre and bend upward at the right, indicating a heavy right tail."
- Markers at least 4 px, hollow, so overlapping quantiles stay visible.

## Build

### mermaid

Not drawable in Mermaid (no scatter). Render with the matplotlib target and link the image.

### vega-lite

The `quantile` transform computes sample quantiles; a second `calculate` maps probabilities to theoretical quantiles (Vega-Lite has no inverse normal function, so approximate or precompute):

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "values.csv"},
 "transform": [{"quantile": "value", "step": 0.01, "as": ["p", "v"]},
               {"calculate": "quantileNormal(datum.p)", "as": "theoretical"}],
 "layer": [{"mark": "point", "encoding": {"x": {"field": "theoretical", "type": "quantitative"}, "y": {"field": "v", "type": "quantitative"}}},
           {"mark": "rule", "encoding": {"x": {"datum": -3}, "y": {"datum": -3}, "x2": {"datum": 3}, "y2": {"datum": 3}}}]}
```

`quantileNormal` is a Vega expression function available since Vega 5. Hand-written; the reference line values must be set from the data, hence `approx`.

### plotly

Compute quantiles in Python (`scipy.stats.probplot(values, dist="norm")` returns theoretical and ordered sample quantiles plus the fitted line), then `{"type": "scatter", "mode": "markers"}` for the points and a second `scatter` with `mode: "lines"` for the line. Hand-written.

### chartjs

Same precomputation, then a `scatter` dataset for the points and a `line` dataset with two points for the reference line, `scales.x.type = "linear"`. Hand-written.

### matplotlib

`statsmodels.api.qqplot(values, line="45", ax=ax)` (pip `statsmodels`), or `scipy.stats.probplot(values, dist="norm", plot=ax)` which draws points and the fitted line; two-sample: sort both, interpolate to equal length, `ax.scatter(qa, qb)`. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: `scatter` on value axes plus a `markLine` diagonal. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
