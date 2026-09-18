---
name: Adjacency matrix
slug: adjacency-matrix
aliases: [matrix diagram, network matrix, transition matrix, origin-destination matrix, co-occurrence matrix, confusion matrix]
family: relationship
also: [flow, correlation]
question: Which pairs are connected and how strongly, for every pair at once?
shapes: ["n,n,q", "n,n", "flow"]
goals: [relationship, matrix, pairwise, between every pair, transitions, origin destination, co-occurrence, confusion, dense network, who with whom, grid]
max_series: 0
max_categories: 60
evidence: medium
popularity: common
status: stable
support:
  mermaid: none
  vega-lite: native
  plotly: native
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
  docx: image
  gsheets: image
  observable-plot: native
  d2: none
  plantuml: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/heatmap.html, https://vega.github.io/vega-lite/docs/rect.html, https://plotly.com/javascript/heatmaps/, https://github.com/kurkle/chartjs-chart-matrix, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.imshow.html, https://doi.org/10.1057/palgrave.ivs.9500092]
---

# Adjacency matrix

## When to use

- The same data as a `network` (nodes and weighted links) laid out as a grid: rows are sources, columns are targets, a cell is the link and its colour or number is the weight.
- Dense graphs, or graphs with more than about 50 nodes, where a node-link picture is a hairball; the matrix stays readable at any density.
- Exact values matter: transition counts, origin-destination volumes, confusion matrices, co-occurrence counts; print the numbers in the cells.
- Finding missing links, cliques and blocks: with rows and columns sorted by cluster, communities appear as dark squares on the diagonal.
- Excels at: completeness and lookup; every pair has a place, and a reader can find A to B in two moves (Ghoniem, Fekete and Castagliola 2004).

## When not to use

- Path following (A to B to C): readers must hop between cells; a `network` diagram wins for small sparse graphs.
- Unsorted rows and columns: the pattern is invisible; order by cluster, degree, or a natural order (time, geography) and say which.
- Very sparse large graphs: mostly empty cells; an edge list table or a `network` with a filter is more compact.
- Comparing values by colour only: use printed numbers or a `bar` of the row totals beside it.
- Directed data drawn symmetric, or symmetric data drawn twice, without saying so; state whether rows send and columns receive.

## Substitutes

- Small sparse graph, structure and paths: `network`.
- Ordered nodes, few links: `arc-diagram`.
- Small weighted symmetric set for a poster: `chord`.
- Cohort transitions across ordered stages: `alluvial`; directional conserved flows: `sankey`.
- General two-category grids not about links: `heatmap`; correlation between variables: `correlogram`.

## Evidence

- Ghoniem, Fekete and Castagliola 2004 (Information Visualization 4(2)): for graphs above about 20 nodes or of medium density, matrices outperformed node-link diagrams on most tasks (finding nodes, links, common neighbours) except path finding. One controlled study, replicated in later work on matrix reordering, hence `medium`.
- Cell colour is the weakest encoding (Cleveland and McGill 1984), so print values where cells are large enough; a matrix is a `table` first and a picture second.
- Row and column ordering (seriation) is the design decision that decides whether structure appears; Franconeri et al. 2021 on making the intended comparison adjacent.

## Accessibility

- Values printed in cells when there are at most about 20 by 20; otherwise a colour bar with real values and a downloadable table.
- One-hue sequential ramp (viridis, Blues) or diverging with a neutral midpoint only when zero or a baseline is meaningful; no rainbow.
- Row and column labels at both edges for large matrices; clear direction statement ("rows send, columns receive").
- Text alternative: "Adjacency matrix of <n> <entities>; strongest link <A> to <B> (<value>); <k> blocks along the diagonal; <finding>." The matrix itself is the data alternative; provide it as CSV.

## Build

Not supported by `cw.py build` under this slug; the same data drawn as a `heatmap` is supported (`cw.py build --chart heatmap --target vega-lite --data links.csv --x target --y source --series weight`; check the heatmap file for the exact flags). Input is either `source,target,weight` rows (long form, missing pairs are empty cells) or a square matrix.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "links.csv"},
 "layer": [{"mark": "rect", "encoding": {"color": {"field": "weight", "type": "quantitative", "scale": {"scheme": "blues"}}}},
           {"mark": {"type": "text", "fontSize": 9}, "encoding": {"text": {"field": "weight"}, "color": {"condition": {"test": "datum.weight > 50", "value": "white"}, "value": "black"}}}],
 "encoding": {"x": {"field": "target", "type": "nominal", "sort": {"field": "order"}}, "y": {"field": "source", "type": "nominal", "sort": {"field": "order"}}}}
```

Sort both axes by a precomputed `order` column (cluster or degree). Render with `cw.py render --target vega-lite --in matrix.vl.json --out matrix.png`.

### plotly

`{"type": "heatmap", "z": [[...]], "x": names, "y": names, "colorscale": "Blues", "texttemplate": "%{z}", "xgap": 1, "ygap": 1}` with `layout.yaxis.autorange = "reversed"` so the first row is at the top. Python: `px.imshow(matrix, x=names, y=names, text_auto=True, color_continuous_scale="Blues")`.

### chartjs

`chartjs-chart-matrix` plugin: `type: "matrix"`, data `{x: target, y: source, v: weight}`, `backgroundColor` as a function of `v`, `width`/`height` callbacks from the chart area divided by n. Numbers need `chartjs-plugin-datalabels`. Canvas, so add `aria-label` and a fallback table.

### matplotlib

`im = ax.imshow(M, cmap="Blues"); ax.set_xticks(range(n), names, rotation=90); ax.set_yticks(range(n), names); fig.colorbar(im, ax=ax, label="weight")` and, for small n, `for i, j in np.ndindex(M.shape): ax.text(j, i, M[i, j], ha="center", va="center", fontsize=7)`. `seaborn.heatmap(M, annot=True, fmt="d", cmap="Blues", xticklabels=names, yticklabels=names)` does the same in one call; `seaborn.clustermap` reorders rows and columns by clustering. Render with `cw.py render --target matplotlib --in matrix.py --out matrix.png`.

### echarts

Hand-written: `heatmap` on category axes. See `kb/targets/echarts.md`.

### observable-plot

`cw.py build --chart adjacency-matrix --target observable-plot --data file.csv --x <x> --y <y> [--series <s>]` emits the `Plot.plot({...})` snippet; add `--html --out page.html` for a page (d3 and Plot 0.6 from jsdelivr).

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. The relationship-specific advice here (ordering, direction statement, path-following weakness) is what separates this file from `heatmap`; the drawing recipes are the same.
