---
name: Heatmap
slug: heatmap
aliases: [heat map, matrix chart, colour matrix, XY heatmap, heat table, grid chart]
family: correlation
also: [magnitude, change-over-time, table]
question: What is the pattern of a value across two categorical dimensions?
shapes: ["n,n,q", "o,o,q", "time,n,q", "n,o,q"]
goals: [pattern, matrix, two dimensions, by hour and day, by month and year, grid, intensity, cross-tab, where is it high, heatmap]
max_series: 0
max_categories: 50
evidence: medium
popularity: core
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: approx
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://vega.github.io/vega-lite/docs/rect.html, https://plotly.com/python/heatmaps/, https://github.com/kurkle/chartjs-chart-matrix, https://seaborn.pydata.org/generated/seaborn.heatmap.html, https://jfly.uni-koeln.de/color/]
---

# Heatmap

## When to use

- A value indexed by two categorical or ordinal dimensions (hour by weekday, product by region, month by year) and the question is where it is high or low, not what it is exactly.
- Many series over time (20 to 50 rows) where lines would tangle: time on x, series on y, value as colour.
- Spotting structure: blocks, stripes, diagonals, after ordering rows and columns meaningfully (by total, by cluster, by natural order).
- Dense tables that readers scan rather than look up.
- Excels at: pattern over a large grid at a glance; nothing else shows 2,000 values on one screen.

## When not to use

- Precise values: colour is the bottom of the Cleveland and McGill ranking; add numbers in the cells or use a `table` when values must be read.
- Rainbow colour scales: they create false boundaries; use one hue light to dark (sequential) or two hues with a neutral midpoint that means something (diverging).
- Unordered rows and columns: an unsorted heatmap looks random; seriate or cluster first.
- Two different quantities on one colour scale, or a scale that mixes counts with rates.
- Few cells (under about 12): a `grouped-bar` or `dot-plot` shows the values better.
- Missing values coloured as if they were zero: draw them grey or empty and say so.

## Substitutes

- Values must be read: `table` with heat colouring or inline bars.
- Few categories: `grouped-bar`, `small-multiples`.
- Time by series with a shared scale: `small-multiples` of lines; daily values over years: `calendar-heatmap`.
- Two numeric variables: `hexbin`, `density-2d`.
- Correlation coefficients: `correlogram`.
- Value as size rather than colour: a dot matrix (`bubble` on categorical axes).

## Evidence

- Colour saturation and lightness are the least accurately read encodings (Cleveland and McGill 1984), so the heatmap's strength is pattern, not value; FT caveat says exactly this. Practitioner consensus (FT, Datawrapper, seaborn's defaults) backs sequential or diverging perceptually uniform scales (Smith and van der Walt 2015, viridis): `medium`.
- Franconeri et al. 2021: colour scales are among the main sources of misleading charts; a perceptually uniform ramp with a labelled legend is the mitigation.

## Accessibility

- Perceptually uniform, colour-blind-safe ramp (viridis, cividis, ColorBrewer Blues; RdBu for diverging with the midpoint labelled).
- Numbers in cells when the grid is under about 400 cells; otherwise a colour legend with ticks and units.
- Cell borders or a 1 px gap so adjacent cells separate for low-vision readers; 3:1 contrast between the lightest cell and the background.
- Text alternative: "Heatmap of <value> by <rows> and <columns>; highest in <row> on <column> (X), lowest in <row> on <column>; values rise toward the bottom right."
- Provide the table on request; a heatmap is not readable by screen readers without it.

## Build

### mermaid

Not drawable in Mermaid. Render with the vega-lite target and link the image; a markdown table with the values is the text fallback.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "grid.csv"},
 "mark": "rect",
 "encoding": {"x": {"field": "hour", "type": "ordinal"}, "y": {"field": "weekday", "type": "ordinal"},
              "color": {"field": "visits", "type": "quantitative", "scale": {"scheme": "viridis"}}}}
```

`cw.py build --chart heatmap --target vega-lite --data grid.csv --x hour --y weekday --color visits [--html]`. Numbers in cells: a second `text` layer on the same encoding; diverging: `"scale": {"scheme": "redblue", "domainMid": 0}`; `"sort": "-color"` on an axis orders by value.

### plotly

`{"type": "heatmap", "z": [[...], [...]], "x": columns, "y": rows, "colorscale": "Viridis", "texttemplate": "%{z}"}`; `px.imshow(pivot, text_auto=True, color_continuous_scale="Viridis")` in Python. `cw.py build --chart heatmap --target plotly --data grid.csv --x hour --y weekday --color visits --html`.

### chartjs

Community plugin `chartjs-chart-matrix`: `{"type": "matrix", "data": {"datasets": [{"data": [{"x": "Mon", "y": "9", "v": 12}], "backgroundColor": ctx => colour(ctx.raw.v), "width": ..., "height": ...}]}}` with category scales on both axes. Hand-written; the colour ramp is your function.

### matplotlib

`seaborn.heatmap(pivot, cmap="viridis", annot=True, fmt=".0f", linewidths=0.5, ax=ax)`; plain matplotlib: `im = ax.imshow(matrix, cmap="viridis"); fig.colorbar(im)`, then `ax.set_xticks(range(n), labels=cols)`. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
