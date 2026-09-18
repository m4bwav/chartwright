---
name: Waffle chart
slug: waffle
aliases: [gridplot, square pie, unit chart, dot matrix chart, 10x10 grid]
family: part-to-whole
also: [magnitude]
question: What share of the whole, in whole percent, does each part take?
shapes: ["n,q"]
goals: [share, percent, proportion, part to whole, out of 100, one in ten, general audience, units, count of, grid]
max_series: 0
max_categories: 4
evidence: low
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: approx
  matplotlib: approx
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com, https://datavizcatalogue.com, https://github.com/gyli/PyWaffle]
---

# Waffle chart

## When to use

- One whole with shares that round cleanly to whole percent: "62 of every 100 households", "3 in 10 adults".
- A general or young audience: counting squares is a skill everyone has; the grid reads as "out of 100" without an axis.
- Small multiples of waffles across categories (FT gridplot): the same 10x10 grid per region lets the eye compare filled areas roughly and counts precisely.
- A part smaller than 5% that a pie slice would hide: one or two coloured squares still show.
- Excels at: a memorable, countable share for reports, posters and slides; honest about rounding because the units are visible.

## When not to use

- More than three or four parts: the grid becomes a mosaic and counting fails.
- Fractional shares that matter (12.4% vs 12.6%): the grid rounds to units; use a `bar` or a `table`.
- Many wholes to compare precisely: filled-square area comparison across grids is rough; use `stacked-bar-100`.
- Values that are not a share of one whole, or that exceed 100 units without a stated unit size.
- Fancy icon fills (pictograms) when icons are not all the same size: the counts stop being comparable; see `pictogram`.

## Substitutes

- Precise shares or many parts: `bar` or `stacked-bar-100`.
- Sum-of-slices majority questions: `pie` or `donut`.
- Counts with a meaningful icon per unit: `pictogram`.
- Hierarchical shares: `treemap`.
- A single share with a target: `bullet`.

## Evidence

- No dedicated perception study; the case rests on convention and on counting being exact where area estimation is not (Cleveland and McGill 1984 rank area low; unit counting sidesteps estimation for small numbers). `low`.
- Practitioner guidance (FT gridplot, Datawrapper, From Data to Viz, Data Visualisation Catalogue) recommends it for whole-percent shares to lay audiences, with few parts.
- Bateman et al. 2010 support memorable, embellished forms when accuracy is not lost; a waffle is a mild embellishment of a stacked bar.

## Accessibility

- Give each part a label with its count ("62 squares = 62%") near its block of squares; do not rely on the legend alone.
- Fill order that reads like text (row by row from the top left) or bottom-up like a bar; state which in the caption.
- Colour-blind-safe hues with a lightness difference; a gap between squares of at least 1 px so the grid is countable.
- Text alternative: "Waffle chart, 100 squares: <A> <n> squares (<n>%), <B> <n> squares..."; the table is the same list.

## Build

### mermaid

Mermaid has no grid or unit chart. Render with vega-lite or matplotlib to an image and link it.

### vega-lite

Hand-written: expand the shares to 100 rows with `sequence` and `calculate`, then `"mark": {"type": "square", "size": 300}` on `x = datum.i % 10` and `y = floor(datum.i / 10)` (ordinal, axes hidden), `color` by the part each index falls into.

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json",
 "data": {"sequence": {"start": 0, "stop": 100, "as": "i"}},
 "transform": [{"calculate": "datum.i < 62 ? 'Mobile' : datum.i < 96 ? 'Desktop' : 'Tablet'", "as": "part"},
               {"calculate": "datum.i % 10", "as": "col"}, {"calculate": "floor(datum.i / 10)", "as": "row"}],
 "mark": {"type": "square", "size": 300},
 "encoding": {"x": {"field": "col", "type": "ordinal", "axis": null}, "y": {"field": "row", "type": "ordinal", "axis": null, "sort": "descending"},
              "color": {"field": "part", "type": "nominal"}}}
```

`approx` because the thresholds are computed in the spec, not by a waffle mark.

### plotly

Hand-written: a 10x10 `heatmap` trace with `z` holding the part index per cell, `xgap`/`ygap` of 3, a discrete `colorscale`, hidden axes and `showscale: false`; or `scatter` with square markers. `approx`.

### chartjs

Hand-written: `chartjs-chart-matrix` plugin with 100 cells (`x`, `y`, `v`) and `backgroundColor` per part, or a `scatter` with `pointStyle: "rect"`. `approx`, community plugin.

### matplotlib

Hand-written: `pip install pywaffle` then `plt.figure(FigureClass=Waffle, rows=10, columns=10, values={"Mobile": 62, "Desktop": 34, "Tablet": 4}, legend={"loc": "lower left", "bbox_to_anchor": (0, 1)})`; without the add-on, `ax.imshow` of a 10x10 integer grid with a `ListedColormap`. Render with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
