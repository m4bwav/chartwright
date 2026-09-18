---
name: Bullet chart
slug: bullet
aliases: [bullet graph, target bar, progress bar with target, Few bullet, KPI bar]
family: deviation
also: [single-value, magnitude]
question: How does the actual value compare to its target and to qualitative bands (poor, satisfactory, good)?
shapes: ["n,q,q", "q,q", "n,q,q,q+"]
goals: [deviation, target, actual vs target, progress, goal, against plan, kpi, thresholds, bands, on track, quota, attainment, meter]
max_series: 1
max_categories: 12
evidence: medium
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: approx
  chartjs: approx
  matplotlib: native
  terminal: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://vega.github.io/vega-lite/examples/layer_bar_bullet.html, https://plotly.com/javascript/bullet-charts/, https://datavizcatalogue.com/methods/bullet_graph.html]
---

# Bullet chart

## When to use

- One measure against a target: sales against quota, latency against SLA, spend against budget; the bar is the actual, a tick is the target, and shaded bands behind mark poor, satisfactory and good ranges.
- A dashboard with several KPIs stacked as thin rows (up to about 12), each read the same way, in the space one gauge would take.
- Replacing a `gauge`: same question, a fraction of the space, and length instead of angle.
- The bands carry business meaning (thresholds set in advance), not arbitrary thirds.
- Excels at: three facts per row (actual, target, band) read in one glance, all as length and position on a common scale (Few 2006).

## When not to use

- No target or thresholds exist: a plain `bar` or `stat-tile`.
- The reader needs the trend to the target over time: a `line` with the target as a reference line.
- Several actuals per row (this year and last year): `dumbbell` or `grouped-bar`.
- Bands that are not ordered or not on the same scale as the measure.
- General audiences meeting the form for the first time without a legend: the tick and bands need a one-line key.

## Substitutes

- No target: `stat-tile` or `bar`.
- Progress over time: `line` with a target rule.
- Many measures against targets in a table layout: `table` with an inline bar column and a target marker.
- A dashboard cliché the client insists on: `gauge` (declining; this file is the recommended replacement).

## Evidence

- Actual (bar length from zero) and target (position) are the two most accurate encodings (Cleveland and McGill 1984), and the bands turn a threshold judgement into a position comparison. `medium`: Few's design rationale (Information Dashboard Design, 2006) and consistent adoption in dashboard guidance, without a dedicated perception study.
- Franconeri et al. 2021: aligned rows with the same scale and a repeated target mark make cross-row comparison fast; different scales per row (the usual case) make it slow, so label every row's value and target.
- The 2026-09-17 taxonomy research lists it as the substitute for gauges, which guides discourage.

## Accessibility

- Bands in three steps of one grey (light to dark, never colours), the actual bar in a saturated colour at 3:1 against all three bands, the target tick 3 px in black.
- Actual and target printed as text at the row end ("42 of 50").
- A one-line key: "bar = actual, line = target, shading = poor / ok / good".
- Text alternative: "Bullet chart: <measure> at <actual> against a target of <target>, in the <band> range." Offer the table with actual, target and band columns.
- Rows at least 24 px tall so the tick and the bar are distinct.

## Build

### mermaid

`image`: Mermaid has no layered bars or reference marks. Render the vega-lite recipe and link the image; the in-place fallback is a Mermaid `bar` with the target in the title.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "kpis.csv"},
 "encoding": {"y": {"field": "kpi", "type": "nominal", "axis": {"title": null}}},
 "layer": [{"mark": {"type": "bar", "color": "#eee", "size": 24}, "encoding": {"x": {"field": "band3", "type": "quantitative", "scale": {"nice": false}, "axis": {"title": null}}}},
           {"mark": {"type": "bar", "color": "#ddd", "size": 24}, "encoding": {"x": {"field": "band2", "type": "quantitative"}}},
           {"mark": {"type": "bar", "color": "#ccc", "size": 24}, "encoding": {"x": {"field": "band1", "type": "quantitative"}}},
           {"mark": {"type": "bar", "color": "#0072B2", "size": 10}, "encoding": {"x": {"field": "actual", "type": "quantitative"}}},
           {"mark": {"type": "tick", "color": "black", "thickness": 3, "size": 24}, "encoding": {"x": {"field": "target", "type": "quantitative"}}}]}
```

Wide data with `kpi, actual, target, band1, band2, band3`; use `"resolve": {"scale": {"x": "independent"}}` with a `facet` by row when rows need their own scales. Hand-written; render with `cw.py render --target vega-lite --in chart.vl.json --out chart.svg`.

### plotly

`approx`: `{"type": "indicator", "mode": "number+gauge", "gauge": {"shape": "bullet", "axis": {"range": [0, 60]}, "threshold": {"value": 50, "line": {"color": "black", "width": 3}}, "steps": [{"range": [0, 20], "color": "#ccc"}, {"range": [20, 40], "color": "#ddd"}, {"range": [40, 60], "color": "#eee"}], "bar": {"color": "#0072B2"}}, "value": 42}`; one indicator per row in a `grid` layout. Real bullet look, but each row is a separate indicator with its own domain, so alignment across rows is manual. Hand-written.

### chartjs

`approx`: three stacked-free floating `bar` datasets `[[0, band1], [band1, band2], [band2, band3]]` in greys with `barPercentage: 1`, a narrow `bar` dataset for the actual (`barPercentage: 0.4`), and a `scatter` or line dataset with a `"line"` point style rotated 90 degrees for the target, all on `indexAxis: "y"`. Hand-written mixed chart.

### matplotlib

`ax.barh(y, band3, color="#eee", height=0.8); ax.barh(y, band2, color="#ddd", height=0.8); ax.barh(y, band1, color="#ccc", height=0.8); ax.barh(y, actual, color="#0072B2", height=0.3); ax.vlines(target, y - 0.4, y + 0.4, color="black", linewidth=3)` per row, `ax.set_yticks(range(n), kpis)`. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. The designated substitute for `gauge`.
