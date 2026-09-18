---
name: Range band chart
slug: range-band
aliases: [band chart, ribbon chart, fan chart, error band, confidence band, min-max area, uncertainty band]
family: change-over-time
also: [distribution, deviation]
question: What envelope, range or uncertainty surrounds a value as it changes over time?
shapes: ["time,q,q", "time,q,q,q", "time,q+"]
goals: [range, band, uncertainty, confidence interval, forecast, fan chart, min and max, envelope, prediction interval, spread over time, high and low]
max_series: 3
max_categories: 0
evidence: medium
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: native
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: approx
  quickchart: none
  xlsx: approx
  gdocs: image
  docx: image
  gsheets: image
  observable-plot: native
  d2: none
  plantuml: approx
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://vega.github.io/vega-lite/docs/errorband.html, https://journals.sagepub.com/doi/10.1177/15291006211051956, https://ieeexplore.ieee.org/document/6876013]
---

# Range band chart

## When to use

- A central estimate with an interval over time: forecast with prediction intervals (a fan chart widens into the future), a mean with a confidence band, a model with its credible interval.
- A daily or periodic range without a centre: temperature high and low, bid and ask, min and max across many runs.
- Nested intervals (50, 80, 95 percent) as bands of decreasing opacity, which is what a fan chart is.
- Up to about 3 series with bands; beyond that the bands overlap into mud.
- Excels at: keeping uncertainty attached to the line so that a forecast is never read as a fact.

## When not to use

- Bands so wide that they cover the whole chart: the message is "we do not know"; say that in words or show the distribution differently.
- Several series with overlapping bands: the intersections cannot be read; use `small-multiples`.
- The band represents something other than a range (a category, a target zone): label it as such or use a shaded reference region instead.
- Readers assume the band contains all possible outcomes: caption what the interval is (95 percent, min and max, one standard deviation).
- A markdown host: Mermaid has no area or band mark; render an image.

## Substitutes

- Uncertainty at discrete points rather than along time: `error-bars`, or quantile dot plots when the audience can learn them.
- The full distribution per period: `boxplot` per period, `violin`, or `ridgeline`.
- Open, high, low and close of a price: `candlestick`.
- Only the central line: `line`.
- Many scenarios instead of an interval: spaghetti of thin `line`s (hypothetical outcome style).

## Evidence

- Correll and Gleicher 2014 ("Error Bars Considered Harmful") found gradient and violin-style representations read better than bare error bars; Franconeri et al. 2021 recommend distributions and bands over bars for uncertainty. Continuous bands are better read than error bars, but readers still tend to treat a band as a hard container of all outcomes (Padilla and Hullman's uncertainty work). One line of studies with a known caveat: `medium`.
- The centre line remains position on a common scale (Cleveland and McGill 1984); the band edges are read less precisely, which is acceptable since they represent uncertainty.
- The Financial Times Visual Vocabulary: a fan chart shows "uncertainty grows the further forward".

## Accessibility

- Band opacity about 20 to 30 percent of the line colour, with a faint edge line so the extent is visible in greyscale; nested bands step opacity.
- Say what the band is in the caption or a label inside the band ("80 percent interval"); never rely on the legend alone.
- Text alternative: "Line with a range band of <measure> from <start> to <end>; the central estimate rises from A to B; the 80 percent interval at <end> spans C to D."
- The central line at 2 px with 3:1 contrast; the band must never reduce the line's contrast below that.

## Build

### vega-lite

`cw.py build --chart range-band --target vega-lite --data forecast.csv --x date --y low --y2 high [--series mean]` composes the band (area from `--y` to `--y2`) and an optional centre line.

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "forecast.csv"},
 "encoding": {"x": {"field": "date", "type": "temporal"}},
 "layer": [
  {"mark": {"type": "area", "opacity": 0.25}, "encoding": {"y": {"field": "lo", "type": "quantitative"}, "y2": {"field": "hi"}}},
  {"mark": "line", "encoding": {"y": {"field": "mid", "type": "quantitative"}}}]}
```

Hand-written (no builder). When the band must be computed from raw samples use `"mark": {"type": "errorband", "extent": "ci"}` on the raw field instead of precomputed `lo` and `hi`. Stack more area layers for a fan.

### plotly

Three traces in order: `{"x": dates, "y": hi, "mode": "lines", "line": {"width": 0}}`, `{"x": dates, "y": lo, "mode": "lines", "line": {"width": 0}, "fill": "tonexty", "fillcolor": "rgba(0,114,178,0.25)"}`, then the centre `{"x": dates, "y": mid, "mode": "lines"}`. Hand-written.

### chartjs

`type: "line"` with datasets `hi` (`fill: "+1"`, `pointRadius: 0`, `borderWidth: 0`), `lo` (no fill), then `mid`; the `fill: "+1"` fills between adjacent datasets. Hand-written.

### matplotlib

`ax.fill_between(dates, lo, hi, alpha=0.25, linewidth=0)` then `ax.plot(dates, mid, linewidth=2)`; repeat `fill_between` with narrower intervals for a fan. Hand-written, then `cw.py render --target matplotlib --in chart.py --out chart.png`.

Markdown hosts: render the vega-lite spec to SVG and link it.

### echarts

Hand-written: two stacked `line` series with `areaStyle` on the upper and transparent lower. See `kb/targets/echarts.md`.

### pptx

Approximate: AREA_STACKED with a transparent lower series.

### xlsx

Approximate: AreaChart stacked with a transparent lower series.

### plantuml

two `area` series (upper and lower) in `@startchart`; the lower one painted background colour. Approximate.

### observable-plot

`Plot.areaY(data, {x, y1: "low", y2: "high", fillOpacity: 0.3})` under `Plot.lineY`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
