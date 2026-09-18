---
name: Icicle chart
slug: icicle
aliases: [partition chart, partition layout, flame graph, rectangular sunburst, adjacency diagram]
family: hierarchy
also: [part-to-whole]
question: How does a hierarchy partition by size at every level, with labels readable at each depth?
shapes: ["hier,q", "n,n,q"]
goals: [hierarchy, partition, levels, nested, flame graph, profiling, call stack, breakdown, depth, path, icicle]
max_series: 0
max_categories: 40
evidence: low
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: native
  chartjs: none
  matplotlib: approx
  terminal: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://plotly.com/javascript/icicle-charts/, https://vega.github.io/vega/examples/, https://www.brendangregg.com/flamegraphs.html, https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary]
---

# Icicle chart

## When to use

- A hierarchy with sizes where labels must be readable at every level: rectangles stack top-down (icicle) or bottom-up (flame graph) with horizontal text.
- Profiling data: the flame graph is an icicle of call stacks by CPU time and the standard tool for "where does the time go" (Gregg).
- Depth is the story (three to six levels) and the sunburst's outer rings would be too thin.
- Widths of siblings must be compared: all rectangles at one level share a baseline, so width is length on an aligned scale, better than arc.
- Excels at: deep hierarchies with many small leaves, with zoom-on-click in interactive versions.

## When not to use

- Two levels with few parts: a `stacked-bar` or `treemap` is simpler.
- Sizes are not additive (rates, averages): the partition assumes children sum to the parent.
- Very wide hierarchies (hundreds of siblings) in a static image: leaves become one pixel wide; aggregate or provide interaction.
- Audiences that have never seen one need a sentence of explanation; a `treemap` is more familiar for shares.

## Substitutes

- Shares that dominate, fewer levels: `treemap`; radial, drill-down aesthetic: `sunburst`.
- Structure only: `tree`; clustering: `dendrogram`.
- A sequence of nested stages with counts: `funnel` or `sankey`.
- Two levels: `stacked-bar` per parent.

## Evidence

- Widths at the same level are lengths on a shared baseline, an encoding read better than the areas of a treemap or the arcs of a sunburst (Cleveland and McGill 1984), but no study measures the icicle directly. `low`: convention in profiling and in the D3 and Vega communities, endorsed as the readable alternative to sunbursts by practitioners.
- Franconeri et al. 2021: horizontal labels and aligned baselines reduce the cost of comparison; the icicle has both.
- Popularity `niche`: native in Plotly, D3 and Vega; everyday only in performance engineering (flame graphs).

## Accessibility

- Label every rectangle wide enough for text; truncate with an ellipsis and give the full name in a tooltip and a table.
- Colour by top-level branch with lighter children, or a single hue with lightness by depth; a flame graph's random warm hues carry no data, so a legend must say so.
- Text alternative: "Icicle chart of <measure> across <N> levels: <root> splits into <A> (<p>%) and <B> (<p>%); the deepest heavy path is <path>." Provide the indented table.
- Borders with 3:1 contrast so sibling rectangles are separable.

## Build

### mermaid

No Mermaid partition chart. Render with plotly or matplotlib and link the image; a `mindmap` gives the structure alone.

### vega-lite

Full Vega only: `stratify` then `partition` in rectangular mode (`"type": "partition", "size": [{"signal": "width"}, {"signal": "height"}], "as": ["x0", "y0", "x1", "y1"]`) and a `rect` mark, rendered by vl-convert. Hand-written. `approx`.

### plotly

`{"type": "icicle", "labels": ["All", "A", "A1", "A2", "B"], "parents": ["", "All", "A", "A", "All"], "values": [0, 60, 40, 20, 40], "branchvalues": "remainder", "tiling": {"orientation": "v"}}`; `orientation: "h"` lays it left to right, `flip: "y"` makes a flame graph. Hand-written, then `cw.py render --target plotly --in fig.json --out chart.html`.

### chartjs

Not available: no core type and no maintained plugin. Use plotly or a matplotlib image.

### matplotlib

Hand-written: compute the partition (depth-first, each node's `x0` = running offset within its parent, width = value / root total), then `ax.barh(y=depth, width=w, left=x0, height=1, edgecolor="white")` per node and `ax.text` labels where `w` exceeds the text width; `ax.invert_yaxis()` for an icicle, leave it for a flame graph. Render with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
