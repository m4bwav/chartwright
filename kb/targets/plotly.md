---
name: Web, interactive (Plotly)
slug: plotly
kind: web
renders_in: [any web page via plotly.js, Jupyter and Dash via plotly.py, static PNG via kaleido 1.x (needs Chrome)]
version_checked: "plotly.js 4.1.1 (2026-09-14), plotly.py 7.1.0 (2026-09-15), kaleido 1.4.0"
last_verified: 2026-09-17
renderer: none
tested:
  - Windows 2026-09-18: JSON built and page written; page not opened in a browser
sources: [https://plotly.com/javascript/, https://github.com/plotly/plotly.py/blob/main/CHANGELOG.md, https://github.com/plotly/Kaleido/releases]
---

# Web, interactive (Plotly)

Pick Plotly when the page needs hover, zoom, 3D, financial or statistical traces that Vega-Lite lacks (candlestick, violin, sunburst, treemap, sankey, funnel, indicator/gauge, parallel coordinates, choropleth with built-in geo). Larger bundle (about 3.5 MB) and no browser-free static export, so it is the second choice for documents.

## What it can draw

| chart | support | note |
|---|---|---|
| line, multi-line, step, area, stacked-area, bar, column, grouped-bar, stacked-bar, diverging-bar, scatter, bubble, histogram, boxplot, violin, heatmap, pie, donut, sunburst, treemap, icicle, sankey, funnel, waterfall, candlestick, ohlc, indicator (gauge, stat tile), parallel-coordinates, radar (scatterpolar), choropleth, bubble-map, density-2d, contour, splom, 3d-scatter, 3d-surface | native | trace `type` names: scatter, bar, pie, histogram, box, violin, heatmap, sunburst, treemap, icicle, sankey, funnel, waterfall, candlestick, ohlc, indicator, parcoords, scatterpolar, choropleth, scattergeo, histogram2dcontour, contour, splom, scatter3d, surface, densitymap |
| lollipop, dumbbell, slope, bullet, calendar-heatmap, beeswarm, ridgeline, bump | approx | composed from scatter/bar traces or plotly.express helpers |
| chord, network, dendrogram | approx | figure_factory dendrogram; network as scatter lines |

## Syntax essentials

```json
{"data": [{"type": "scatter", "mode": "lines+markers", "name": "2026", "x": ["2026-01", "2026-02"], "y": [100, 104]}],
 "layout": {"title": {"text": "Price over time"}, "xaxis": {"title": {"text": "date"}}, "yaxis": {"title": {"text": "price"}}, "template": "plotly_white"}}
```

- A figure is `{data: [traces], layout: {...}}`; `Plotly.newPlot(div, data, layout, {responsive: true, displaylogo: false})`.
- Grouped vs stacked bars: `layout.barmode = "group" | "stack" | "relative"`.
- Areas: `fill: "tozeroy"` or `stackgroup: "one"`.
- Dark mode: `template: "plotly_dark"`; colour order via `layout.colorway`.
- plotly.js 4.0 (2026-08) removed the `*mapbox` traces (use `*map`), removed Chart Studio config, and switched colour parsing to culori (rgb fractions are no longer percentages). plotly.py 7.0 dropped Kaleido below 1.0 and Orca.
- Python: `import plotly.express as px; px.line(df, x="date", y="price", color="series").write_html("x.html", include_plotlyjs="cdn")`.

## Limits

- Static PNG needs Chrome or Chromium on the machine (`kaleido 1.x`, `kaleido_get_chrome`); corporate proxies often block the download. Prefer the vega-lite target for images.
- Full bundle is heavy for a docs page; use the partial bundles (`plotly-basic`, `plotly-cartesian`) when only basic traces are used.
- No markdown host renders it; embed as an HTML file or iframe.

## Render

- Page: `cw.py build ... --target plotly --html --out chart.html` (loads plotly.js 4.1.1 from cdn.plot.ly).
- From a saved figure JSON: `cw.py render --target plotly --in fig.json --out chart.html`.
- Image: `python -c "import plotly.io as pio, json; pio.write_image(json.load(open('fig.json')), 'chart.png', scale=2)"` after `pip install plotly kaleido` and a Chrome install.

## Notes

- 2026-09-17: created from the 2026-09-17 library research.
