---
name: Web, interactive (Apache ECharts)
slug: echarts
kind: web
renders_in: [any web page, dashboards, Vue/React wrappers, server-side SVG via Node SSR]
version_checked: "ECharts 6.1.0 (2026-05-19); 6.0.0 2025-07-30"
last_verified: 2026-09-18
renderer: none
sources: [https://echarts.apache.org/en/option.html, https://echarts.apache.org/handbook/en/how-to/cross-platform/server/, https://github.com/apache/echarts/releases]
---

# Web, interactive (Apache ECharts)

Pick ECharts for dashboards and pages that need large data, built-in dark mode and runtime theme switching, or the types it draws natively that Vega-Lite lacks (sankey, chord, beeswarm, funnel, gauge, treemap, sunburst, graph, calendar, candlestick). One declarative option object, Apache-2.0, rising velocity (6.0 in 2025, 6.1 in 2026).

## What it can draw

| chart | support | note |
|---|---|---|
| line, multi-line, step, area, stacked-area, bar, column, grouped-bar, stacked-bar, stacked-bar-100, scatter, bubble, pie, donut, radar, funnel, sankey, alluvial, heatmap | native | covered by `cw.py build --target echarts` |
| calendar-heatmap, candlestick, boxplot, treemap, sunburst, gauge, network, chord, beeswarm, parallel-coordinates, tree, radial-bar, waterfall, bullet, choropleth, bubble-map, lollipop, dumbbell, diverging-bar, histogram, violin | native or approx | series types calendar, candlestick, boxplot, treemap, sunburst, gauge, graph, chord (6.0), scatter with jitter (6.0 beeswarm), parallel, tree, bar on polar, stacked bar with a transparent base (waterfall), custom series (violin); histogram via the ecStat transform. Hand-written from the option docs |
| word-cloud | approx | echarts-wordcloud extension |

## Syntax essentials

```json
{"title": {"text": "Price over time"}, "tooltip": {"trigger": "axis"},
 "xAxis": {"type": "category", "data": ["Jan", "Feb", "Mar"]}, "yAxis": {"type": "value"},
 "series": [{"type": "line", "name": "2026", "data": [100, 104, 101]}]}
```

- `echarts.init(el).setOption(option)`; `echarts.init(el, 'dark')` for the dark theme; `chart.resize()` on window resize.
- Stacking: `stack: "total"` on each series; areas: `areaStyle: {}`; steps: `step: "end"`; horizontal bars: swap `xAxis` and `yAxis` types.
- Time axes: `xAxis.type = "time"` with `[timestamp, value]` pairs in `data`.
- Colour: `color: [...]` at the top level (Okabe-Ito list works); `visualMap` for sequential scales on heatmaps and maps.
- Accessibility: `aria: {enabled: true, decal: {show: true}}` adds a generated description and pattern fills.
- Large data: `large: true` and `sampling: "lttb"` on line series; `dataset` with `source` rows keeps data out of the series objects.

## Limits

- No browser-free image export without Node: server-side rendering needs `echarts.init(null, null, {renderer: "svg", ssr: true, width, height}).renderToSVGString()` under Node, or node-canvas for PNG. For documents use the vega-lite target.
- No markdown host renders it; embed as an HTML file or iframe.
- The option surface is huge; keep to the shapes above unless the chart file gives a recipe.

## Render

- Page: `cw.py build ... --target echarts --html --out chart.html` (jsdelivr `echarts@6`).
- From a saved option: `cw.py render --target echarts --in option.json --out chart.html`.
- SVG on a machine with Node: a ten-line script using the SSR call above; not wired into `cw.py render`.

## Notes

- 2026-09-18: added as a target from the 2026-09-17 library research (ECharts 6.1: chord, beeswarm jitter, matrix coordinate system, auto dark mode).
