---
name: Parallel coordinates
slug: parallel-coordinates
aliases: [parallel coordinates plot, parcoords, parallel axes plot, PCP]
family: magnitude
also: [correlation, distribution]
question: How do many entities compare across many quantitative dimensions, and which dimensions move together?
shapes: ["n,q+", "q+"]
goals: [magnitude, correlation, many dimensions, multivariate, high-dimensional, compare across variables, profiles, explore, brushing, parallel coordinates, trade-offs]
max_series: 0
max_categories: 12
evidence: medium
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: native
  chartjs: none
  matplotlib: native
  terminal: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/parallel.html, https://plotly.com/javascript/parallel-coordinates-plot/, https://vega.github.io/vega-lite/examples/parallel_coordinate.html, https://pandas.pydata.org/docs/reference/api/pandas.plotting.parallel_coordinates.html]
---

# Parallel coordinates

## When to use

- Tens to thousands of entities (cars, candidates, configurations) measured on 4 to 12 quantitative dimensions, and the question is exploratory: which dimensions trade off, which entities are outliers, what does the top cluster look like.
- Interactive settings where the reader can brush an axis range and reorder axes (Plotly's `parcoords` does both); the chart is an analysis tool more than a presentation graphic.
- Each dimension has its own scale, which a `radar` cannot handle: every axis is normalised independently and labelled with its own ticks.
- Highlighting a few entities against a grey background of all the others.
- Excels at: revealing correlation between adjacent axes (parallel lines mean positive correlation, crossing lines mean negative) and spotting outliers across many variables.

## When not to use

- A static chart for a general audience: the tangle of lines has no obvious reading; pick the finding and draw it as a `scatter` or `bar`.
- Few entities and few dimensions (under 5 each): a `dot-plot` or a `table` says it plainly.
- Correlation between non-adjacent axes: it is invisible; axis order decides what the reader sees, so reorder or use a `splom` or `correlogram`.
- Categorical dimensions: use `alluvial` (parallel sets), which is the categorical counterpart.
- Precise values: lines cross the axes at positions that are hard to read; provide a table.

## Substitutes

- Pairwise correlations: `splom` or `correlogram`.
- Categorical dimensions: `alluvial`.
- Few entities, profile shape: `radar` (only with comparable scales) or `small-multiples` of `bar`.
- Entities by dimension as a grid: `heatmap` with rows sorted by one column.
- Reduce dimensions and plot: `scatter` of two principal components.

## Evidence

- Each axis is position on a common scale (Cleveland and McGill 1984), and the adjacent-axis correlation reading is well documented in the information visualisation literature (Inselberg's original formulation); `medium` because usability for non-experts is poor and depends on interaction, and no perception study places it against alternatives for presentation tasks.
- Franconeri et al. 2021: many crossing lines defeat the fast shape reading; highlighting a subset restores it, so always grey the background and colour the few.
- From Data to Viz and the FT note the axis-order dependency; a reasonable default orders axes so that the most correlated ones are adjacent.

## Accessibility

- At most one highlighted colour class plus grey; a sequential colour by one dimension is acceptable if a colour bar is shown.
- Axis titles and tick labels on every axis; state the normalisation ("each axis scaled to its own range").
- Lines 1 px at 30 percent opacity for the background set, 2 px opaque for highlights.
- Text alternative: "Parallel coordinates plot of <n> <entities> across <dimensions>; <finding, e.g. entities high on A are low on B>." Always offer the table; this chart is unreadable to screen readers.
- Interactive versions need keyboard access to the brush or a filtered table as a fallback.

## Build

### mermaid

`image`: no Mermaid equivalent. Render with plotly (static via kaleido) or matplotlib and link the image; for a document, prefer drawing the specific finding as a bar or scatter in Mermaid.

### vega-lite

`approx`: fold the wide data to long, normalise per dimension with a `window` or `joinaggregate` transform, then draw `line` marks with `detail` set to the entity id, `x` ordinal by dimension name and `y` the normalised value; axis ticks per dimension need extra `text` layers (the Vega-Lite gallery's parallel coordinates example does exactly this). Hand-written and long; interaction (brushing) is not available in static output.

### plotly

```json
{"data": [{"type": "parcoords",
           "line": {"color": [...], "colorscale": "Viridis"},
           "dimensions": [{"label": "MPG", "values": [...]}, {"label": "HP", "values": [...]}, {"label": "Weight", "values": [...]}]}]}
```

Native trace with brushing and axis drag built in; `line.color` by one dimension or a category code. Hand-written; open with `cw.py render --target plotly --in fig.json --out chart.html`.

### matplotlib

`pandas.plotting.parallel_coordinates(df, "class", colormap="viridis", alpha=0.4)` on a data frame normalised per column (`(df - df.min()) / (df.max() - df.min())`), or one `ax.plot(range(n_dims), row)` per entity. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. Chart.js has no plugin for it (`none`).
