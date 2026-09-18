---
name: Observable Plot (web, SVG marks)
slug: observable-plot
kind: web
renders_in: [any web page, Observable notebooks and Framework, React and Svelte apps, Node with jsdom]
version_checked: "@observablehq/plot 0.6.17 (npm latest, checked 2026-09-18); UMD build needs d3 v7 as a global"
last_verified: 2026-09-18
renderer: browser
tested: untested
sources: [https://observablehq.com/plot/, https://registry.npmjs.org/@observablehq/plot/latest, https://github.com/observablehq/plot]
---

# Observable Plot (web, SVG marks)

Pick this for a web page or notebook when the chart is a composition of simple marks (lines, bars, dots, cells, areas) over tidy data and the spec should stay short: Plot's mark-and-transform grammar is the tersest of the web targets, renders to accessible SVG, and facets and stacks with one option. Prefer Vega-Lite when the host already uses it or when a static PNG is needed (Plot has no headless renderer without jsdom), and ECharts or Plotly for pies, sankeys, radars and 3-D.

## What it can draw

| chart | support | note |
|---|---|---|
| line, multi-line, sparkline, step, connected-scatter, area, stacked-area, column, bar, grouped-bar, stacked-bar, stacked-bar-100, diverging-bar, lollipop, dot-plot, scatter, bubble, strip, beeswarm, boxplot, histogram, heatmap, correlogram, adjacency-matrix, calendar-heatmap, waffle, small-multiples, density-2d, hexbin, slope | native | marks `lineY`, `areaY`, `barX/Y`, `dot`, `tickX`, `boxY`, `rectY`+`binX`, `cell`, `waffleY`, `density`, `hexbin`, `dodgeY`, `stackY`, facets `fx`/`fy`; all built by `cw.py build --target observable-plot` |
| range-band, timeline, dumbbell, error-bars, tree, dendrogram, choropleth, dot-density-map, bubble-map, streamgraph, tile-grid-map | native | `areaY` y1/y2, `barX` x1/x2, `link`, `ruleX`, `tree`/`cluster`, `geo` with a projection, `stackY({offset: "wiggle"})`; hand-written, recipe in each chart file |
| ecdf, density, qq, population-pyramid, ridgeline, horizon, marimekko, bump, diverging-stacked-bar, bullet, gantt, hex-map, arc-diagram, pictogram, parallel-coordinates, splom, raincloud, violin, candlestick, waterfall, quadrant | approx | composed from marks with some precomputation (KDE, running totals, hand layouts) |
| pie, donut, radar, radial-bar, gauge, sankey, alluvial, chord, edge-bundling, treemap, sunburst, icicle, circle-packing, funnel, stat-tile, table, venn, word-cloud, cartogram, flow-map | none | no polar coordinates and no hierarchy or flow layouts in Plot; use ECharts, Plotly or an image target |

## Syntax essentials

```html
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script src="https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6"></script>
<div id="chart"></div>
<script>
const data = [{x: new Date("2026-01-01"), y: 100}, {x: new Date("2026-02-01"), y: 104}];
const chart = Plot.plot({
  title: "Price over time", width: 720, height: 400,
  y: {grid: true, label: "price"},
  color: {legend: true},
  marks: [Plot.ruleY([0]), Plot.lineY(data, {x: "x", y: "y", stroke: "series"})]
});
document.getElementById("chart").append(chart);
</script>
```

- Marks: `Plot.lineY`, `areaY`, `barY`/`barX` (ordinal axis), `rectY` (quantitative bins), `dot`, `cell`, `tickX`, `ruleY`, `text`, `boxY`, `waffleY`, `link`, `arrow`, `geo`, `tree`.
- Transforms wrap the options: `Plot.binX({y: "count"}, {x})`, `Plot.groupX({y: "sum"}, {x, y})`, `Plot.stackY({offset: "normalize"}, ...)`, `Plot.dodgeY(...)`, `Plot.hexbin({r: "count"}, ...)`, `Plot.normalizeY(...)`, `Plot.windowY(7, ...)`.
- Facets: `fx`/`fy` channels on any mark, or a top-level `facet: {data, x}`; colours: `color: {scheme: "blues", legend: true}`; dates must be `Date` objects (JSON gives strings).
- ESM: `import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm"` (no d3 global needed).

## Limits

- No polar marks, so no pie, donut, radar or gauge; no built-in hierarchy or flow layouts.
- Static export needs Node with jsdom (`Plot.plot({document})`) or a browser screenshot; there is no vl-convert equivalent, so for PNG deliverables build the same chart in vega-lite.
- Release cadence is slow (0.6.17 dated 2025-02); the API is stable but the library is not growing fast.

## Render

- `cw.py build --chart line --target observable-plot --data prices.csv --x date --y price --html --out chart.html` writes a page; without `--html` the output is the `const data = ...; const chart = Plot.plot({...});` snippet to paste into a page or notebook. `cw.py render --target observable-plot --in chart.js --out chart.html` wraps an existing snippet.

## Notes

- 2026-09-18: added from the 2026-09-17 library research; version and CDN fields confirmed from the npm registry on 2026-09-18. Pages built but not screenshot-verified on this machine (no headless browser step in cw.py).
