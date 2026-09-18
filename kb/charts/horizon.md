---
name: Horizon chart
slug: horizon
aliases: [horizon graph, layered band chart, folded area chart, two-tone pseudo colouring]
family: change-over-time
also: [deviation]
question: How do dozens of series change over time when each can only have a few pixels of height?
shapes: ["time,q*n", "time,n,q"]
goals: [horizon, many series, dense, dashboard, compact, dozens of time series, monitoring, above and below baseline, space-saving]
max_series: 50
max_categories: 0
evidence: medium
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: image
  matplotlib: native
  terminal: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://idl.cs.washington.edu/papers/horizon/, https://vega.github.io/vega-lite/examples/area_horizon.html, https://observablehq.com/@d3/horizon-chart]
---

# Horizon chart

## When to use

- Dozens of series (servers, sensors, stocks, regions) that must be compared over the same time axis in a page or a dashboard where each gets 20 to 40 px of height.
- Deviations above and below a baseline (zero, the mean, a target) where sign matters: positive bands in one hue, negative mirrored in another.
- Readers who see the chart regularly (operations, monitoring, trading) and can learn the folding convention.
- Excels at: preserving the resolution of a full-height area chart in a fraction of the space (Heer, Kong and Agrawala 2009).

## When not to use

- General or one-time audiences: the folded bands need explanation, and the darker-means-higher rule is not intuitive.
- Fewer than about 8 series: `small-multiples` of `line` or `area` at full height are simpler.
- Reading a value at a date: the value is band count times band height plus the position within the band, which is slow; add tooltips or a table.
- A markdown or Chart.js host: no primitive draws the fold; render an image.

## Substitutes

- Few series: `small-multiples` of `line`.
- Pattern over many series without sign: `heatmap` with time on x and series on y.
- Many components as one aesthetic picture: `streamgraph`.
- Deviation of one series: `area` split at the baseline with two colours.
- Tiny inline trend per row of a table: `sparkline`.

## Evidence

- Heer, Kong and Agrawala 2009 ("Sizing the Horizon", CHI) measured estimation accuracy and speed against line charts at several heights and found that 2-band mirrored horizon charts keep accuracy at heights where lines fail, with an optimal chart height of about 24 px for 2 bands. One well-designed study, later confirmed in practice by D3 and Vega examples: `medium`.
- Each band is position on a common scale within its band; the band count is a colour lightness step, which is the weak part of the encoding (Cleveland and McGill 1984).
- Keep to 2 or 3 bands; more bands trade legibility for a little more height saving.

## Accessibility

- Two hues for sign (blue up, orange down, or another colour-blind-safe pair) and 2 to 3 lightness steps per hue with at least 20 percent lightness between steps.
- Explain the folding in a one-line caption and show a legend of the band scale.
- Text alternative: "Horizon chart of N series from <start> to <end>; <series> rose furthest above the baseline in <period>, <series> fell furthest in <period>." Provide the table, since values are hard to read.
- Each row labelled at the left; rows at least 20 px tall; hover tooltips in interactive targets.

## Build

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "series.csv"},
 "height": 30, "width": 400,
 "transform": [{"calculate": "datum.value - 60", "as": "band2"}],
 "encoding": {"x": {"field": "date", "type": "temporal"}},
 "layer": [
  {"mark": {"type": "area", "clip": true, "opacity": 0.5}, "encoding": {"y": {"field": "value", "type": "quantitative", "scale": {"domain": [0, 60]}}}},
  {"mark": {"type": "area", "clip": true, "opacity": 0.5}, "encoding": {"y": {"field": "band2", "type": "quantitative", "scale": {"domain": [0, 60]}}}}]}
```

Hand-written from the gallery example (`area_horizon`): one clipped, translucent area layer per band, so the fold is composed by hand and the band count is fixed in the spec; wrap in `"facet": {"row": ...}` for many series. `approx` for that reason.

### plotly

`approx`: for each band and each series add a `{"type": "scatter", "fill": "tozeroy", "mode": "lines", "y": clip(value - k * band, 0, band)}` trace in its own subplot row (`make_subplots(rows=n, shared_xaxes=True)`), with `yaxis.range = [0, band]`. Hand-written.

### matplotlib

For each series `ax = axes[i]` then for `k in range(bands)`: `ax.fill_between(dates, 0, numpy.clip(values - k * band, 0, band), color=colour, alpha=0.35)`; `ax.set_ylim(0, band)`, `ax.set_yticks([])`, negative values mirrored with `-values` in the second hue. Hand-written, then `cw.py render --target matplotlib --in chart.py --out chart.png`.

Markdown and Chart.js hosts: render the matplotlib or vega-lite version and link the image.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
