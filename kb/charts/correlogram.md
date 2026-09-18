---
name: Correlogram
slug: correlogram
aliases: [correlation matrix, correlation heatmap, corrplot, correlation plot]
family: correlation
also: [magnitude]
question: Which pairs among many variables are strongly correlated, positively or negatively?
shapes: ["n,n,q", "q+"]
goals: [correlation, correlation matrix, many variables, pairwise, feature selection, collinearity, which variables relate, matrix]
max_series: 0
max_categories: 30
evidence: medium
popularity: common
status: stable
support:
  mermaid: image
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
added: 2026-09-18
last_verified: 2026-09-18
sources: [https://www.data-to-viz.com/graph/correlogram.html, https://seaborn.pydata.org/examples/many_pairwise_correlations.html, https://plotly.com/python/heatmaps/, https://vega.github.io/vega-lite/examples/rect_heatmap.html, https://cran.r-project.org/web/packages/corrplot/vignettes/corrplot-intro.html]
---

# Correlogram

## When to use

- Ten to thirty numeric variables and the question is which pairs move together: a screening view before deeper analysis.
- Reporting a correlation matrix in a readable form: colour makes the strong pairs jump out where a table of decimals does not.
- Excels at: pattern spotting across many pairs at once, and showing blocks of related variables when rows are ordered by clustering.

## When not to use

- Fewer than about five variables: a `splom` shows the actual relationships, including non-linear ones, which a correlation coefficient hides.
- The reader needs the shape of a relationship: correlation is one number; a curved or clustered relationship reads as weak. Follow the correlogram with `scatter` plots of the interesting pairs.
- Categorical variables: Pearson correlation does not apply; use a `heatmap` of an association measure and say which.
- More than about thirty variables: cells become unreadable; cluster and show the top block, or use a table sorted by absolute correlation.
- Misuse: a rainbow or two-hue palette without a neutral midpoint at zero, which makes weak correlations look meaningful.

## Substitutes

- Few variables: `splom`.
- One pair in detail: `scatter`.
- Exact values needed: `table` with a diverging colour fill.
- Categorical pairs: `heatmap`.

## Evidence

- Colour is the weakest encoding for value (Cleveland and McGill 1984), so a correlogram is read for pattern, not magnitude; print the coefficient in the cell when values matter. Rating `medium`.
- Diverging palette with a neutral zero and ordering by hierarchical clustering are consistent practitioner guidance (From Data to Viz; corrplot vignette).
- Showing only one triangle removes the redundant half and halves the reading load.

## Accessibility

- Diverging palette (blue, white, red or the Okabe-Ito blue and vermilion) validated for colour-blind readers; the midpoint is neutral grey or white.
- Print the coefficient in each cell or at least in the strong cells; a text alternative names the strongest positive and negative pairs.
- Keep variable labels horizontal on the y axis and rotated 45 degrees at most on the x axis.

## Build

### vega-lite

Data as long rows `{var1, var2, r}`: `"mark": "rect"`, `"x": {"field": "var1", "type": "nominal"}`, `"y": {"field": "var2", "type": "nominal"}`, `"color": {"field": "r", "type": "quantitative", "scale": {"scheme": "redblue", "domain": [-1, 1]}}`, plus a `text` layer for the coefficient. `cw.py build --chart heatmap --target vega-lite --data corr.csv --x var1 --y r --series var2` gives the base; hand-add the diverging domain and the text layer.

### plotly

`{"type": "heatmap", "z": matrix, "x": names, "y": names, "zmin": -1, "zmax": 1, "colorscale": "RdBu", "text": matrix, "texttemplate": "%{text:.2f}"}`. Native; hand-written, or `px.imshow(df.corr(), text_auto=".2f", color_continuous_scale="RdBu", zmin=-1, zmax=1)`.

### chartjs

Approximate: the `chartjs-chart-matrix` plugin draws coloured cells; compute the correlations first and pass `{x, y, v}` per cell with a colour callback. Hand-written.

### matplotlib

`sns.heatmap(df.corr(), vmin=-1, vmax=1, cmap="RdBu", center=0, annot=True, fmt=".2f", mask=np.triu(np.ones_like(corr, dtype=bool)))` for the lower triangle; `sns.clustermap` to order by similarity. Native; hand-written.

### echarts

Hand-written: `heatmap` on category axes with `visualMap` from -1 to 1. See `kb/targets/echarts.md`.

## Notes

- 2026-09-18: written from the 2026-09-17 taxonomy research.
