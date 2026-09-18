---
name: Sparkline
slug: sparkline
aliases: [inline chart, word-sized graphic, mini line, trend line in a table, micro chart]
family: change-over-time
also: [single-value, table]
question: What is the recent shape of a trend, at a glance, next to the number it belongs to?
shapes: ["time,q", "o,q"]
goals: [sparkline, inline, tiny, in a table, next to a number, KPI, recent trend, at a glance, last 30 days, compact, terminal]
max_series: 1
max_categories: 0
evidence: low
popularity: common
status: stable
support:
  mermaid: none
  vega-lite: native
  plotly: native
  chartjs: native
  matplotlib: native
  terminal: native
  echarts: approx
  pptx: approx
  quickchart: approx
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0001OR, https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://vega.github.io/vega-lite/docs/axis.html, https://www.datawrapper.de/blog/chart-types-guide]
---

# Sparkline

## When to use

- A trend that belongs beside a number: a KPI tile, a table row, a sentence ("revenue ▁▂▃▅▇ up 12 percent").
- Many series that each need only a shape, one per row, aligned so the eye compares them down the column.
- Chat replies and terminals where an image is impossible: a Unicode block sparkline costs about one token per point.
- The last N periods of something that has a current value; the sparkline gives the context, the number gives the value.
- Excels at: shape without ceremony; no axes, no legend, no title, the height of the surrounding text (Tufte 2006).

## When not to use

- Reading values or comparing two points: no axis means no numbers; add the first and last value as text or use a `line`.
- More than one series in one sparkline: overlapping micro lines are unreadable; one per row.
- Series where the zero baseline matters (counts that should be read as amounts): a sparkline auto-scales to its own range and exaggerates small changes; say so or use a mini `column`.
- Rows in a table with different scales but readers expect comparability: either share the scale (and lose detail) or label each row's range.
- Standalone: a sparkline with nothing next to it is a bad line chart.

## Substitutes

- A single chart with axes: `line`.
- Discrete counts inline: a mini `column` (win-loss bars are the classic variant).
- Value plus delta plus trend in a tile: `stat-tile`, which contains a sparkline.
- Many series with values: `table` with inline bars or heat colouring.
- Many series in a compact stack with sign: `horizon`.

## Evidence

- Tufte 2006 ("Beautiful Evidence") defines sparklines and argues for them on data density; there is no perception study of accuracy, and by design they trade accuracy for context. Rating `low`: use them for shape, never for values.
- Shape extraction is a fast global process (Franconeri et al. 2021), which is exactly what a sparkline asks for.
- Datawrapper tables and most BI tools ship them as a table column type, which is the practitioner consensus on where they belong.

## Accessibility

- Always pair with the number it decorates, and with first and last values in text when the change matters.
- Mark the last point (a dot) and, optionally, the min and max in a second colour with 3:1 contrast.
- Text alternative: "Sparkline of <measure> over the last N <periods>, rising from A to B." In a table, the alternative is the row's own cells.
- Height at least the line height of the surrounding text (about 16 to 20 px); stroke 1.5 px; no antialiasing tricks that thin it further.

## Build

Terminal and chat, any host: map each value to one of `▁▂▃▄▅▆▇█` by its position between the series min and max, one character per point: `"".join("▁▂▃▄▅▆▇█"[int(7 * (v - lo) / (hi - lo or 1))] for v in values)`. Mermaid is `none`: an xychart cannot be drawn inline or without axes, and a markdown host gets the Unicode string or an SVG image.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "last30.csv"},
 "width": 120, "height": 24, "view": {"stroke": null}, "config": {"axis": null},
 "mark": {"type": "line", "strokeWidth": 1.5},
 "encoding": {"x": {"field": "date", "type": "temporal"}, "y": {"field": "value", "type": "quantitative", "scale": {"zero": false}}}}
```

Hand-written (no builder); `cw.py render --target vega-lite --in spark.vl.json --out spark.svg` gives an inline-sized SVG. Add a `point` layer filtered to the last row for the end dot.

### plotly

`{"type": "scatter", "mode": "lines", "x": [...], "y": [...], "line": {"width": 1.5}}` with `layout = {"width": 120, "height": 30, "margin": {"l": 0, "r": 0, "t": 0, "b": 0}, "xaxis": {"visible": false}, "yaxis": {"visible": false}, "showlegend": false}` and `config.staticPlot = true`. Hand-written.

### chartjs

`type: "line"` with `options: {scales: {x: {display: false}, y: {display: false}}, plugins: {legend: {display: false}, tooltip: {enabled: false}}, elements: {point: {radius: 0}}, responsive: false}` on a 120 by 30 canvas. Hand-written; QuickChart also has a `sparkline` chart type for image URLs.

### matplotlib

`fig, ax = plt.subplots(figsize=(1.2, 0.3), dpi=200); ax.plot(values, linewidth=1.2); ax.plot(len(values) - 1, values[-1], "o", markersize=3); ax.axis("off"); fig.savefig("spark.png", bbox_inches="tight", pad_inches=0)`. Hand-written, then `cw.py render --target matplotlib --in chart.py --out spark.png`.

### terminal

`cw.py build --chart sparkline --target terminal --data file.csv --x date --y value` prints the block sparkline with endpoints and range.

### echarts

Hand-written: `line` with axes hidden (`show: false`) and `grid` zeroed. See `kb/targets/echarts.md`.

### pptx

Approximate: a tiny LINE chart with axes deleted (`chart.value_axis.visible = False`).

### quickchart

Approximate: QuickChart `sparkline` type; write the Chart.js config by hand and URL-encode it (see `kb/targets/quickchart.md`).

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
