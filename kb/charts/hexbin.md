---
name: Hexbin plot
slug: hexbin
aliases: [hexagonal binning, hex density plot, 2D histogram, binned scatter, hexbin map of points]
family: correlation
also: [distribution]
question: Where is the mass in a scatter of many thousands of points, and does the relationship still hold under the pile?
shapes: ["q,q", "q,q,q"]
goals: [correlation, large data, many points, overplotting, density, where is the mass, thousands of points, binned, hexbin]
max_series: 1
max_categories: 0
evidence: medium
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: image
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hexbin.html, https://observablehq.com/plot/transforms/hexbin, https://vega.github.io/vega-lite/docs/bin.html, https://plotly.com/python/2D-Histogram/, https://www.datawrapper.de/blog/chart-types-guide]
---

# Hexbin plot

## When to use

- A `scatter` with more than about 5,000 points where alpha no longer separates dense from very dense.
- The question is the shape and density of the cloud (ridges, several modes, a curved relationship), not individual points.
- A third numeric variable to aggregate per cell (mean of z in each hexagon) instead of a count.
- Point maps with many events where a dot density map saturates (hexagons over a map).
- Excels at: turning a black blob into a readable density surface; hexagons avoid the row-and-column striping that square bins produce and pack more evenly.

## When not to use

- Small n (under a few hundred): binning hides individual points that a `scatter` would show fine.
- Readers need to identify units: bins have no names; label the outliers on a `scatter` instead.
- Several groups compared on one plot: hexbins do not overlay; facet by group, or use `density-2d` contours, which do overlay.
- When the count scale is linear but the density spans orders of magnitude: most cells look empty; use a log colour scale and say so.
- Bin size chosen to make the story: pick it from the data range (about 30 to 50 bins across) and keep it fixed across comparable charts.

## Substitutes

- Overlaying groups or a smooth surface: `density-2d`.
- Moderate n: `scatter` with alpha.
- Categorical axes: `heatmap`.
- A third variable per point, small n: `bubble`.
- One numeric variable: `histogram`.

## Evidence

- Cell colour is the least accurate encoding (Cleveland and McGill 1984), so hexbins show pattern, not counts; the honest use is the same as a `heatmap`'s. Hexagons over squares is a sampling argument (Carr et al. 1987; adopted by matplotlib, ggplot2, Observable Plot, Datawrapper's 2D histogram): `medium`.
- Franconeri et al. 2021: the surface's shape is read fast; overplotted scatters mislead about density, which is the problem hexbins solve.

## Accessibility

- Sequential perceptually uniform ramp (viridis) with a labelled colour bar; log scale announced in the legend title when used.
- Empty cells left blank (not the lowest colour) so the data's extent is visible.
- Text alternative: "Hexbin plot of <y> against <x>, n = <n>; density is highest near (X, Y) and falls along a rising diagonal; a second cluster at (X2, Y2)."
- Axis titles with units; a thin cell outline in the background colour separates cells for low-vision readers.

## Build

### mermaid

Not drawable in Mermaid. Render with the matplotlib target and link the image.

### vega-lite

No hexagon mark; a square 2D histogram is the closest form:

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "points.csv"},
 "mark": "rect",
 "encoding": {"x": {"field": "x", "bin": {"maxbins": 40}, "type": "quantitative"},
              "y": {"field": "y", "bin": {"maxbins": 40}, "type": "quantitative"},
              "color": {"aggregate": "count", "type": "quantitative", "scale": {"scheme": "viridis", "type": "symlog"}}}}
```

Hand-written; square cells, hence `approx`. True hexagons need full Vega with a hex path computed per cell.

### plotly

No hexbin trace: `{"type": "histogram2d", "x": [...], "y": [...], "nbinsx": 40, "nbinsy": 40, "colorscale": "Viridis"}` gives square bins; `px.density_heatmap(df, x=..., y=..., nbinsx=40)` in Python. Hand-written; square, hence `approx`.

### chartjs

No 2D binning and no hexagon shape; the matrix plugin could draw square bins computed in code, but this is not worth it. Render an image with the matplotlib target.

### matplotlib

`hb = ax.hexbin(x, y, gridsize=40, cmap="viridis", bins="log", mincnt=1); fig.colorbar(hb, label="count")`; `C=z, reduce_C_function=numpy.mean` aggregates a third variable per cell. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
