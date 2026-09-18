---
name: Web, canvas (Chart.js)
slug: chartjs
kind: web
renders_in: [any web page, React/Vue wrappers, QuickChart URL images, chartjs-node-canvas headless PNG]
version_checked: "Chart.js 4.5.1 (2025-10-13; no release for 11 months), chartjs-node-canvas 5.0.0, QuickChart Chart.js 4 via version=4"
last_verified: 2026-09-17
renderer: none
sources: [https://www.chartjs.org/docs/latest/, https://www.chartjs.org/docs/latest/general/accessibility.html, https://quickchart.io/documentation/]
---

# Web, canvas (Chart.js)

Pick Chart.js when the host page already uses it, when a tiny bundle (about 70 kB) matters, or when a chart-as-URL image (QuickChart) is the easiest way into a chat or email. It draws the basic types well and nothing else; its canvas output is not accessible without extra work.

## What it can draw

| chart | support | note |
|---|---|---|
| line, multi-line, step, area, bar, column, grouped-bar, stacked-bar, diverging-bar, scatter, bubble, pie, donut, radar, polar-area | native | `type`: line, bar, scatter, bubble, pie, doughnut, radar, polarArea; `indexAxis: "y"` for horizontal bars; `fill` for area; `stepped` for step |
| histogram, boxplot, violin, heatmap (matrix), treemap, sankey, funnel, candlestick, error-bars, gauge, word cloud | approx | community plugins (chartjs-chart-matrix, -treemap, -sankey, -financial, -boxplot, -error-bars, -funnel, chartjs-gauge); quality and maintenance vary |
| dumbbell, lollipop, slope, bullet, waterfall | approx | floating bars (`[low, high]` data) or mixed line/bar datasets |
| choropleth, network, sunburst, parallel-coordinates, ridgeline | none | use vega-lite or plotly |

## Syntax essentials

```json
{"type": "line",
 "data": {"labels": ["Jan", "Feb", "Mar"], "datasets": [{"label": "2026", "data": [100, 104, 101]}]},
 "options": {"responsive": true, "plugins": {"title": {"display": true, "text": "Price over time"}}}}
```

- `new Chart(canvas, config)`. Datasets share `labels`; time axes need the date adapter (`chartjs-adapter-date-fns`) and `scales.x.type = "time"`.
- Stacking: `options.scales.x.stacked = true` and `y.stacked = true`. Horizontal: `options.indexAxis = "y"`.
- Colours are not assigned automatically before 4.x's `plugins.colors`; pass `borderColor`/`backgroundColor` per dataset for a controlled palette.
- QuickChart: `https://quickchart.io/chart?version=4&c=<url-encoded config>` returns PNG (`&format=svg|webp|pdf`), which is 80 to 200 tokens for a chart in a chat message; self-host with Docker (AGPL-3.0).

## Limits

- Canvas: screen readers see nothing unless the `<canvas>` carries `role="img"` and `aria-label`, plus a fallback table inside it. No SVG export.
- Fewer statistical types; plugins needed for anything beyond the eight core types.
- Project velocity is flat (no release since 2025-10); fine for stable use, not the place to expect new chart types.

## Render

- Page: `cw.py build ... --target chartjs --html --out chart.html` (jsdelivr `chart.js@4`).
- Headless PNG: `npm i chartjs-node-canvas chart.js` then `new ChartJSNodeCanvas({width, height}).renderToBuffer(config)`.
- Image URL: QuickChart as above.

## Notes

- 2026-09-17: created from the 2026-09-17 library research.
