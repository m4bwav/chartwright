---
name: Box plot
slug: boxplot
aliases: [box-and-whisker plot, box and whisker, Tukey box plot, boxplot]
family: distribution
also: [ranking, deviation]
question: How do the median and spread of a numeric variable compare across groups?
shapes: ["n,q", "o,q", "q"]
goals: [distribution, compare groups, median, spread, quartiles, outliers, variability, range, across categories, box plot]
max_series: 0
max_categories: 20
evidence: medium
popularity: core
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: native
  pptx: image
  quickchart: approx
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/caveat/boxplot.html, https://vega.github.io/vega-lite/docs/boxplot.html, https://plotly.com/python/box-plots/, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html, https://www.autodesk.com/research/publications/same-stats-different-graphs]
---

# Box plot

## When to use

- Many groups (5 to 20) and the question is robust summaries: median, interquartile range, whiskers, outliers.
- Audiences who know the convention (analysts, scientists, engineering readers).
- Skewed data with outliers, where the mean plus standard deviation misleads.
- Ordered groups (months, dose levels) laid out left to right so the median's drift reads as a line would.
- Excels at: compact, honest comparison of central value and spread across many groups on one axis.

## When not to use

- Hiding bimodality: two clusters produce the same box as one wide hump (Matejka and Fitzmaurice 2017); check with a `histogram` or `violin` first.
- Small n per group (under about 10): five summary statistics from eight values overstate precision; show the points (`strip`, `beeswarm`).
- General audiences: FT flags the convention as unfamiliar; explain "the box holds the middle half" in a caption or use a dot with a range.
- When the whisker rule is unstated: 1.5 IQR, min-max and 5th-95th percentile all exist; say which.
- Comparing totals or counts: a box plot says nothing about how many values each group has; add n under each label.

## Substitutes

- Shape matters (bimodal, skewed): `violin`; shape plus raw values plus summary: `raincloud`.
- Small n: `strip` or `beeswarm` with a median mark.
- Many ordered groups where the shift in shape is the story: `ridgeline`.
- Precise comparison of whole distributions: `ecdf`.
- Mean with a confidence interval: `error-bars` (dot and interval, not bar and whisker).
- One group only: `histogram`.

## Evidence

- Median and quartile positions are position on a common scale, read accurately (Cleveland and McGill 1984). But the plot is a summary: Matejka and Fitzmaurice 2017 ("Same Stats, Different Graphs") show identical box plots for wildly different distributions, so the reading is only as good as the assumption of unimodality: `medium`.
- Franconeri et al. 2021 and Kay et al. 2016 argue distributions and quantile dot plots communicate spread better than summary glyphs for non-expert readers.
- FT Visual Vocabulary caveat: summarises multiple distributions but hides shape; confusing for readers who do not know the parts.

## Accessibility

- Order groups by median (or by their natural order) so the eye can scan; horizontal boxes with labels on the left when names are long.
- Draw the median as a thick line (2 px or more) in a contrasting colour; show outliers as hollow markers.
- State in the caption what the whiskers span and what the box is; put n beside each group label.
- Text alternative: "Box plot of <measure> by <group>; medians range from A (<group>) to B (<group>); <group> has the widest spread and several high outliers."
- Colour is decorative here; groups are identified by their axis label, so one fill colour is fine and safest.

## Build

### mermaid

Mermaid has no box plot. Render with the vega-lite or matplotlib target and link the image; if the chart must live in markdown text, a table of median and quartiles per group is the honest fallback.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "values.csv"},
 "mark": {"type": "boxplot", "extent": 1.5},
 "encoding": {"x": {"field": "group", "type": "nominal"}, "y": {"field": "value", "type": "quantitative"}}}
```

`cw.py build --chart boxplot --target vega-lite --data values.csv --x group --y value [--html]`. `"extent": "min-max"` for full whiskers; swap x and y for horizontal boxes; `"sort": "-y"` on x orders by median only with a pre-aggregated sort field, so pre-sort the data when order matters.

### plotly

`{"type": "box", "x": groups, "y": values, "boxpoints": "outliers"}` or one trace per group; `boxmean: true` adds the mean, `boxpoints: "all"` with `jitter: 0.3` shows every value. `cw.py build --chart boxplot --target plotly --data values.csv --x group --y value --html`.

### chartjs

Community plugin `@sgratzl/chartjs-chart-boxplot`: register it, then `{"type": "boxplot", "data": {"labels": groups, "datasets": [{"data": [[...values of group 1], [...]]}]}}`; the plugin computes the statistics. Hand-written; plugin maintenance is community-only.

### matplotlib

`ax.boxplot([g1, g2, g3], tick_labels=names, whis=1.5, showfliers=True)` (matplotlib 3.9+ spells it `tick_labels`); or `seaborn.boxplot(data=df, x="group", y="value", ax=ax)`. `cw.py build --chart boxplot --target matplotlib --data values.csv --x group --y value --out chart.py --png chart.png` then `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: series type `boxplot` (pre-compute the five numbers or use the ecStat `boxplot` transform). See `kb/targets/echarts.md`.

### quickchart

Approximate: QuickChart `boxplot` plugin type; write the Chart.js config by hand and URL-encode it (see `kb/targets/quickchart.md`).

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
