---
name: Sunburst chart
slug: sunburst
aliases: [radial treemap, ring chart, multilevel pie, radial icicle, nested donut]
family: hierarchy
also: [part-to-whole]
question: How does a whole split into nested levels, and what path leads to each leaf?
shapes: ["hier,q", "n,n,q"]
goals: [hierarchy, nested, levels, path, drill down, breakdown, multilevel, share, rings, categories and subcategories, sunburst]
max_series: 0
max_categories: 20
evidence: low
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: native
  chartjs: none
  matplotlib: approx
  terminal: none
  echarts: native
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://plotly.com/javascript/sunburst-charts/, https://vega.github.io/vega/examples/sunburst/, https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://eagereyes.org/pie-charts]
---

# Sunburst chart

## When to use

- A hierarchy of two to four levels where the depth and the path from root to leaf are the story: file system, taxonomy, sequence of steps taken by users.
- Interactive drill-down: clicking a ring segment re-roots the chart; this is the sunburst's real strength in a web page.
- Shares at the first level must read like a pie or donut (the inner ring) while the outer rings show how each part subdivides.
- Excels at: showing depth and containment in a compact circle; the inner ring gives the top-level shares, the outer rings the detail.

## When not to use

- Reading or comparing sizes at outer rings: arc lengths at different radii are not comparable, and thin outer arcs are unreadable. Use `icicle` or `treemap`.
- Deep hierarchies (five or more levels) or many leaves: the outer rings become hairlines.
- Labels matter: text along arcs is hard to fit and read; the rectangular `icicle` keeps labels horizontal.
- Flat data: it is a `pie` with extra rings; use a `pie`, `donut` or `bar`.
- Static print for a general audience: without hover the outer rings are noise; consider a `treemap`.

## Substitutes

- Same data with readable labels: `icicle`; size dominance at scale: `treemap`.
- Structure without sizes: `tree`; clustering with merge heights: `dendrogram`.
- One level: `pie` or `donut`; several wholes: `stacked-bar-100`.
- Paths through stages with counts: `sankey`.

## Evidence

- Angle and arc are weaker encodings than position and length (Cleveland and McGill 1984), and arc length depends on radius, so outer rings are read worse than a pie (an extension of Skau and Kosara 2016's finding that readers use arc length). `low`: no study shows the sunburst outperforming its rectangular cousins; guidance (FT, From Data to Viz) accepts it for depth and interactivity only.
- Franconeri et al. 2021: comparisons across separated regions are error-prone; segments of the same parent are adjacent but siblings across parents are not.
- Popularity `common`: native in Plotly, ECharts, D3 and Vega; absent from Chart.js and Mermaid.

## Accessibility

- Label the inner ring segments directly; outer labels only where the arc is wide enough, with the rest in a tooltip and a table.
- Colour by top-level parent with lighter shades for children (one hue per branch, at most 8 branches); the hierarchy then survives greyscale roughly by lightness.
- Text alternative: "Sunburst chart of <measure>; top level: <A> <p>%, <B> <p>%; within <A>, <child> is largest at <p>%." Provide the indented table with values.
- Interactive versions need keyboard access to drill down or a static table fallback.

## Build

### mermaid

No Mermaid sunburst. Render with plotly (interactive) or matplotlib (static) and link the image; a `mindmap` shows the structure without sizes when a text host is mandatory.

### vega-lite

Vega-Lite has no radial partition; full Vega has (`stratify` then `partition` with `"type": "partition", "size": [{"signal": "2 * PI"}, {"signal": "width / 2"}], "as": ["a0", "r0", "a1", "r1"]` and an `arc` mark), rendered by vl-convert as well. Hand-written from the Vega sunburst example. `approx`.

### plotly

`{"type": "sunburst", "labels": ["All", "A", "A1", "A2", "B"], "parents": ["", "All", "A", "A", "All"], "values": [0, 60, 40, 20, 40], "branchvalues": "remainder", "maxdepth": 3}`; click to drill down comes free. Hand-written, then `cw.py render --target plotly --in fig.json --out chart.html`.

### chartjs

Not available: no core type and no maintained plugin. Use plotly or a matplotlib image.

### matplotlib

Hand-written: nested `ax.pie` calls with `radius` and `wedgeprops=dict(width=0.3, edgecolor="white")`, inner ring for parents and outer ring for children in the same order, so the outer wedges align with their parents; or `ax.bar` on a polar axis with computed `left`/`width` per level. Render with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: series type `sunburst` with nested `children`. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
