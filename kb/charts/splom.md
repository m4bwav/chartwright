---
name: Scatterplot matrix
slug: splom
aliases: [SPLOM, pairs plot, pair plot, scatter matrix, pairwise scatter]
family: correlation
also: [distribution]
question: Which pairs of several numeric variables are related, and what does each variable's distribution look like?
shapes: ["q+", "q+,n"]
goals: [correlation, pairwise, several variables, which variables relate, exploratory, multivariate, pairs, splom]
max_series: 3
max_categories: 0
evidence: medium
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: image
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://vega.github.io/vega-lite/examples/interactive_splom.html, https://plotly.com/python/splom/, https://seaborn.pydata.org/generated/seaborn.pairplot.html, https://www.data-to-viz.com/graph/correlogram.html]
---

# Scatterplot matrix

## When to use

- Three to about eight numeric variables and the question is "which of these relate to which", before choosing the one pair worth a `scatter`.
- Exploratory analysis, model building, data quality checks: outliers and non-linear pairs show up that a coefficient hides.
- Up to three groups by colour when a group structure might explain the relationships.
- Analytical audiences who will scan a grid; not a headline chart.
- Excels at: one screen that surveys every pairwise relationship, with each variable's distribution on the diagonal.

## When not to use

- More than about eight variables: 64 tiny panels with unreadable axes; use a `correlogram` to find the interesting pairs first.
- General audiences or a single message: pick the pair and draw a `scatter`.
- Large n: every panel overplots; sample or use hexbin panels.
- Mixed variable types: categorical columns belong in `strip` or `boxplot` panels, not scatter panels.
- The upper and lower triangles repeat: fill one with coefficients or densities, or show only one triangle.

## Substitutes

- Many variables, quick survey: `correlogram`.
- One pair with a story: `scatter` or `bubble`.
- Comparing many variables per unit rather than pairs: `parallel-coordinates`.
- Distributions only: `small-multiples` of `histogram`.

## Evidence

- Each panel is a `scatter` (position on common scales, Cleveland and McGill 1984), but panels are small and axis labels sparse, and comparing across panels is slow (Franconeri et al. 2021). Standard tool in statistical practice (seaborn, plotly, Vega-Lite each ship it): `medium`.
- Correlation underestimation (Rensink and Baldridge 2010) applies in each panel; annotate r per panel when the coefficient matters.

## Accessibility

- Variable names on the diagonal in large type; shared scales per row and column; ticks only on the outer edges.
- Groups by colour and marker shape with one legend; small markers (3 to 4 px) with alpha 0.5.
- Text alternative: "Scatterplot matrix of <k> variables for <n> <units>; the strongest relationship is <A> with <B> (r = 0.8); <C> is unrelated to the others."
- A `correlogram` or a table of coefficients as the companion for screen readers.

## Build

### mermaid

Not drawable in Mermaid. Render with the vega-lite or matplotlib target and link the image.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "cars.csv"},
 "repeat": {"row": ["mpg", "hp", "weight"], "column": ["weight", "hp", "mpg"]},
 "spec": {"width": 140, "height": 140, "mark": {"type": "point", "size": 12, "opacity": 0.6},
          "encoding": {"x": {"field": {"repeat": "column"}, "type": "quantitative", "scale": {"zero": false}},
                       "y": {"field": {"repeat": "row"}, "type": "quantitative", "scale": {"zero": false}},
                       "color": {"field": "origin", "type": "nominal"}}}}
```

Hand-written; `cw.py build` does not emit it. `repeat` is the documented way, hence `native`. Render with `cw.py render --target vega-lite --in chart.vl.json --out chart.png`.

### plotly

`{"type": "splom", "dimensions": [{"label": "mpg", "values": [...]}, {"label": "hp", "values": [...]}], "marker": {"color": groups, "size": 4, "opacity": 0.6}, "diagonal": {"visible": false}, "showupperhalf": false}`; `px.scatter_matrix(df, dimensions=[...], color="origin")` in Python. Hand-written.

### chartjs

No faceting; a grid of separate scatter canvases is possible but tedious and axis sharing is manual. Render an image with the vega-lite or matplotlib target.

### matplotlib

`seaborn.pairplot(df[cols + ["origin"]], hue="origin", corner=True, plot_kws={"s": 12, "alpha": 0.6})` (`corner=True` drops the duplicate triangle; `diag_kind="hist"` or `"kde"`). Plain pandas: `pandas.plotting.scatter_matrix(df[cols], alpha=0.6, diagonal="hist")`. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: several `grid` entries with `scatter` series per pair. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
