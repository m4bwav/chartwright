---
name: Calendar heatmap
slug: calendar-heatmap
aliases: [calendar chart, contribution graph, GitHub graph, day grid, activity calendar, year calendar heatmap]
family: change-over-time
also: [distribution, magnitude]
question: Which days, weeks or months were high or low across a year or more?
shapes: ["time,q"]
goals: [calendar, daily, by day, contributions, activity, streak, weekday pattern, seasonal, day of week, year at a glance, heatmap over time]
max_series: 1
max_categories: 0
evidence: low
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: approx
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: native
  pptx: image
  quickchart: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://vega.github.io/vega-lite/docs/timeunit.html, https://echarts.apache.org/en/option.html#calendar, https://plotly.com/python/heatmaps/]
---

# Calendar heatmap

## When to use

- One daily measure over months or years (commits, steps, sales, incidents, temperature) where the reader scans for patterns by weekday, week and season.
- Streaks, gaps and outliers: a run of dark cells or an empty stretch is visible at once.
- Weekly rhythms (quiet weekends, busy Mondays) that a line hides in noise.
- A dashboard tile where 365 values must fit in a small space.
- Excels at: pattern recognition across the calendar structure; the eye reads rows (weekdays) and columns (weeks) simultaneously.

## When not to use

- Reading values: colour is the least accurate encoding (Cleveland and McGill 1984); pair with a table or tooltips.
- The trend across the year is the message: a `line` or weekly `column` shows it better.
- Data coarser than daily (monthly totals): use `column` or a plain month by year `heatmap`.
- Several measures or several entities: one calendar each in `small-multiples`, never overlaid.
- A rainbow palette: use one hue light to dark, or a diverging scale with a meaningful midpoint.

## Substitutes

- Trend over the year: `line`.
- Weekly or monthly totals: `column`.
- Weekday by hour patterns: `heatmap` (7 by 24 grid).
- Seasonal comparison across years: `small-multiples` of lines, one per year, or a cycle plot.
- Daily distribution: `histogram` of daily values.

## Evidence

- Colour saturation and lightness sit at the bottom of the Cleveland and McGill 1984 ranking, so a calendar heatmap shows pattern, not value; the layout's strength (aligned weekday rows) is grounded in convention and the ubiquity of the GitHub contribution graph rather than a perception study. Rating `low`.
- The Financial Times Visual Vocabulary lists it under change over time with "precision is sacrificed".
- Sequential palettes must be perceptually uniform (viridis family, ColorBrewer single hue) so equal steps in value look like equal steps in colour.

## Accessibility

- One-hue sequential ramp with 4 to 6 steps, colour-blind safe; give the legend the value range of each step.
- Cells at least 10 px with a 1 px gap; label months along the top and weekdays down the side.
- Text alternative: "Calendar heatmap of daily <measure> for <year>; busiest day <date> at <value>, N days with no activity, weekends consistently lower." Provide the daily table or a weekly summary.
- Interactive targets: tooltip with the date and value on every cell.

## Build

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "daily.csv"},
 "mark": "rect",
 "encoding": {"x": {"field": "date", "timeUnit": "week", "type": "ordinal", "axis": {"labelExpr": "monthAbbrevFormat(month(datum.value))", "labelOverlap": true}},
              "y": {"field": "date", "timeUnit": "day", "type": "ordinal", "sort": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
              "color": {"field": "count", "type": "quantitative", "scale": {"scheme": "greens"}}}}
```

Hand-written (no builder). For several years add `"row": {"field": "date", "timeUnit": "year"}`. `timeUnit` does the calendar arithmetic, so the data stays one row per day.

`cw.py build --chart calendar-heatmap --target vega-lite --data daily.csv --x date --y value` uses `timeUnit` week on x and day on y with a green sequential scale.

### plotly

`approx`: compute week-of-year and weekday columns in Python, pivot to a 7 by 53 matrix, then `{"type": "heatmap", "z": matrix, "x": weeks, "y": weekdays, "xgap": 2, "ygap": 2, "colorscale": "Greens"}`. Month labels need manual `xaxis.tickvals`. Hand-written.

### chartjs

`approx`: needs the `chartjs-chart-matrix` plugin (`type: "matrix"`, one data point per day with `x: week, y: weekday, v: count` and a `backgroundColor` callback). Hand-written.

### matplotlib

Reshape the daily series to a 7 by 53 array (`numpy.full((7, 53), numpy.nan)` filled by `[weekday, week]`), then `ax.imshow(grid, cmap="Greens", aspect="equal")` with month ticks from the first week of each month; or `pip install calplot` and `calplot.calplot(series)`. Hand-written, then `cw.py render --target matplotlib --in chart.py --out chart.png`.

Markdown hosts: render the vega-lite spec to SVG and link it.

### echarts

Hand-written: series type `calendar` + `heatmap` with `coordinateSystem: "calendar"`. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
