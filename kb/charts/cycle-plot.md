---
name: Cycle plot
slug: cycle-plot
aliases: [seasonal subseries plot, month plot, subseries plot, cycle-subseries plot, seasonal cycle chart]
family: change-over-time
also: [deviation]
question: Is there a seasonal pattern, and is each season's level rising or falling across the years (or weeks)?
shapes: ["time,q", "o,o,q"]
goals: [seasonality, seasonal, cycle, month of year, day of week, quarter, subseries, within-season trend, change-over-time, monthly pattern, weekly pattern, seasonal component]
max_series: 1
max_categories: 12
evidence: medium
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
  pptx: approx
  quickchart: none
  xlsx: approx
  gdocs: image
  docx: image
  gsheets: approx
  observable-plot: approx
  d2: none
  plantuml: none
added: 2026-09-18
last_verified: 2026-09-18
sources: [https://www.perceptualedge.com/articles/guests/intro_to_cycle_plots.pdf, https://en.wikipedia.org/wiki/Seasonal_subseries_plot, https://otexts.com/fpp3/subseries.html, https://www.statsmodels.org/dev/generated/statsmodels.graphics.tsaplots.month_plot.html, https://stat.ethz.ch/R-manual/R-devel/library/stats/html/monthplot.html, https://rdrr.io/cran/feasts/man/gg_subseries.html, https://www.vizwiz.com/2022/08/cycle-plot.html]
---

# Cycle plot

## When to use

- One measure sampled at a regular seasonal period (months of the year, days of the week, quarters, hours of the day) over several cycles (years, weeks, days).
- The question is two-fold: which seasons are high or low (the level of each mini series and its mean line) and whether a given season is trending up or down across cycles (the slope inside each mini series). A cycle plot answers both in one picture; a one-line-per-year chart answers only the first, an end-to-end line only the trend.
- Three to about fifteen cycles per season: enough points to read a slope, few enough to fit in a narrow panel.
- Exploratory seasonal diagnostics before modelling or seasonal adjustment (Hyndman and Athanasopoulos, FPP3 section 2.5; Cleveland 1993).
- Excels at: exposing a change in seasonality, such as "September attendance has fallen every year while July held", which is invisible in a multi-line chart (Robbins 2008).

## When not to use

- The period is unknown or irregular: the plot requires the season to be fixed in advance; run an autocorrelation check first.
- A strong trend or long oscillation dominates the series: every panel slopes the same way and the seasonal message is lost; detrend or decompose (STL) and plot the seasonal component, as Cleveland, Dunn and Terpenning did.
- Fewer than three cycles: a within-season slope from two points is noise; use a `grouped-bar` or `slope` chart.
- More than about 15 seasons (days of the month, weeks of the year): the panels turn into a ragged wall; use a `heatmap` (season on x, cycle on y) or `calendar-heatmap`.
- The reader needs exact dates or the order of events across seasons: the x axis is discontinuous, so a `line` chart of the raw series must sit beside it.
- Comparing several measures at once: one cycle plot per measure, or a `small-multiples` grid of them; do not overlay.

## Substitutes

- Only the seasonal shape matters, not the change across cycles: a `line` chart with one line per year (seasonal plot) or a `radar` when the audience expects a clock face.
- Only the long-run trend matters: a plain `line` or `step` chart of the raw series.
- Many seasons or many cycles: `heatmap` with season on x and cycle on y; daily data over years: `calendar-heatmap`.
- Two cycles only: `slope` or `dumbbell` by season.
- Each cycle in its own panel: `small-multiples` of lines (this is the other facet direction: panel per cycle rather than per season).
- Distribution within each season rather than its path: `boxplot` or `violin` per season.

## Evidence

- No perception study tests the cycle plot itself; the rating is `medium`, resting on Cleveland (1993, 1994) and Robbins (2005, 2008), who show on the same data that the within-season trend appears in a cycle plot and not in a seasonal line chart or an end-to-end line.
- Its encodings are the strongest ones: position on a common y scale for the values (Cleveland and McGill 1984; Heer and Bostock 2010), slope for the within-season trend, and a rule for the mean, which the eye compares across panels as aligned positions.
- Cox (2006, Stata Journal) documents the Stata implementation and its variants (bars instead of lines, medians instead of means).
- Hyndman and Athanasopoulos (FPP3, 3rd ed., section 2.5) use it as one of two standard seasonal graphics, next to the seasonal plot, and note it reveals changes in seasonality the seasonal plot misses.
- Origin: Cleveland, Dunn and Terpenning (1978), SABL seasonal analysis package, Bell Laboratories; unverified beyond secondary citations (Robbins 2008, Wikipedia).

## Accessibility

- Needs no colour: one hue for the lines, a darker or thicker rule for the means (Robbins 2008 notes it prints in black and white). If a season is highlighted, use weight or a label, not colour alone.
- Label every panel with the season name under it; label the mean line once in the first panel ("mean") so the rule is not read as a target.
- Start the y axis where the data need it but show the axis; the point of the chart is comparing the mean lines, so a truncated axis exaggerates the seasonal spread, say so in a caption.
- Text alternative: "Cycle plot of <measure> by <season> over <first cycle> to <last cycle>; <season A> has the highest average and is rising, <season B> is falling." Offer the season-by-cycle table on request.
- Keep the panels equally wide and the gaps narrow (about one point width) so the discontinuity reads as structure, not as missing data.

## Build

Data shape: long rows of `season, cycle, value` (for example `month, year, sales`). From a dated series derive `season = month(date)` and `cycle = year(date)` first. No `cw.py build` recipe exists yet; every target below is hand-written.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "sales.csv"},
 "facet": {"column": {"field": "month", "type": "ordinal", "sort": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], "header": {"title": null}}},
 "spacing": 4,
 "spec": {"width": 40, "height": 200,
  "layer": [
   {"mark": {"type": "line", "point": true}, "encoding": {"x": {"field": "year", "type": "ordinal", "axis": null}, "y": {"field": "sales", "type": "quantitative"}}},
   {"mark": {"type": "rule", "color": "#555", "strokeWidth": 2}, "encoding": {"y": {"aggregate": "mean", "field": "sales", "type": "quantitative"}}}]}}
```

`approx`: composed from a column facet, a line layer and an aggregate rule; the y scale is shared by default (`resolve` untouched). Use `"sort"` to rotate the season order. Reorder the months in the sort array when the peak straddles December.

### plotly

`approx`: `fig = make_subplots(rows=1, cols=12, shared_yaxes=True, horizontal_spacing=0.01, subplot_titles=months)`; per season `fig.add_trace(go.Scatter(x=years, y=values, mode="lines+markers", showlegend=False), row=1, col=i)` then `fig.add_hline(y=values.mean(), row=1, col=i, line_color="#555")`; hide the x tick labels with `fig.update_xaxes(showticklabels=False)`.

### chartjs

`approx`: Chart.js has no facets, so draw one small `line` chart per season in a flex row with a shared fixed `scales.y.min/max`, and add the mean as a second dataset of constant values (`borderDash: [4, 4]`, `pointRadius: 0`). Or reshape to one chart whose labels are `season-cycle` pairs with `null` gaps between seasons (`spanGaps: false`) and a per-season mean dataset.

### matplotlib

`native` through statsmodels: `from statsmodels.graphics.tsaplots import month_plot; month_plot(series)` for a monthly `DatetimeIndex` or `PeriodIndex` series (`quarter_plot` for quarterly). Without statsmodels: `fig, axes = plt.subplots(1, n, sharey=True, gridspec_kw={"wspace": 0.05})`; per season `ax.plot(years, values, marker="o")`, `ax.axhline(values.mean(), color="#555")`, `ax.set_xticks([])`, `ax.set_title(name, fontsize=9)`. Then `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

`approx`: one `grid` per season laid out left to right with `xAxis` (`type: "category"`, `axisLabel: {show: false}`) and `yAxis` per grid, `yAxis.min/max` fixed to the same values so the panels share a scale, one `line` series per grid with `markLine: {data: [{type: "average"}]}` for the mean, and the season name as the grid's `title`. See `kb/targets/echarts.md`.

### pptx

`approx`: a native line chart on a reshaped table: one category per `season-cycle` pair with an empty category between seasons so the line breaks, one series for the values and one for the per-season mean (repeated per point). python-pptx `XL_CHART_TYPE.LINE_MARKERS`; blank cells break the line when `chart.plots[0]` has `show_blanks_as = "gap"` (XML `dispBlanksAs`). Editable but the season labels sit under the first point of each panel.

### quickchart

`none`: a Chart.js URL has no facets and the gapped single-chart workaround exceeds the practical URL length for twelve seasons times several years; render the matplotlib PNG instead.

### xlsx

`approx`: same reshaped table as pptx (season, cycle, value, mean, with a blank separator row between seasons) and an openpyxl `LineChart` with `display_blanks = "gap"`; add the mean column as a second series.

### gsheets

`approx`: `addChart` with `basicChart.chartType: "LINE"` over the same gapped table (blank rows break the line); the mean is a second series column. `interpolateNulls` must stay false.

### observable-plot

```js
Plot.plot({fx: {label: null, padding: 0.1}, x: {axis: null}, marks: [
  Plot.lineY(data, {x: "year", y: "sales", fx: "month", stroke: "steelblue"}),
  Plot.dot(data, {x: "year", y: "sales", fx: "month"}),
  Plot.ruleY(data, Plot.groupZ({y: "mean"}, {y: "sales", fx: "month", stroke: "#555"}))]})
```

`approx`: the `fx` facet with a grouped `ruleY` is the idiomatic composition; give `fx.domain` the season order to rotate it.

### mermaid, gdocs, docx

`image`: render the matplotlib (or Vega-Lite) version to PNG or SVG and place the picture; Mermaid `xychart` has no facets or reference lines.

## Notes

- 2026-09-18: written from R-20260918-1 (Robbins 2008, FPP3 2.5, statsmodels and R docs); no library among the sixteen targets has a native cycle plot, so every recipe composes facets plus a mean rule.
