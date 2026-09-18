---
name: 2D density plot
slug: density-2d
aliases: [contour plot, kernel density contour, 2D KDE, density contour, bivariate density]
family: correlation
also: [distribution]
question: Where do two continuous variables concentrate together, and how many modes does the joint distribution have?
shapes: ["q,q"]
goals: [correlation, distribution, density, contour, concentration, overplotting, many points, clusters, modes, joint distribution]
max_series: 3
max_categories: 0
evidence: medium
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: native
  chartjs: none
  matplotlib: native
  terminal: none
added: 2026-09-18
last_verified: 2026-09-18
sources: [https://plotly.com/python/2d-histogram-contour/, https://seaborn.pydata.org/generated/seaborn.kdeplot.html, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.contour.html, https://www.data-to-viz.com/graph/density2d.html, https://vega.github.io/vega-lite/docs/density.html]
---

# 2D density plot

## When to use

- Thousands of points where a scatter turns into a solid blob: the contours show where the mass is and whether there are several clusters.
- The question is about the joint distribution (modes, ridges, correlation shape) rather than individual points.
- Comparing two or three groups' joint distributions with overlaid contour outlines, which a scatter with colour cannot do at that density.
- Excels at: revealing multimodality and the shape of the relationship without overplotting.

## When not to use

- Few points (under a few hundred): the smoothing invents structure; use `scatter`.
- The reader needs individual values or outliers: contours hide both; use `scatter` or `hexbin`.
- Discrete or bounded data (counts, percentages near 0 or 100): kernel smoothing bleeds past the bounds; use `hexbin` or a `heatmap` of counts.
- Audiences unfamiliar with contour reading: filled contours read as a map and the levels are easy to misinterpret; a `hexbin` with a count legend is more literal.
- Bandwidth choice changes the picture; never present one bandwidth as the truth without checking another.

## Substitutes

- Many points, literal counts: `hexbin`.
- Fewer points: `scatter` with transparency.
- One variable at a time: `density` or `histogram`.
- Grid of category pairs: `heatmap`.
- Several variable pairs: `splom`.

## Evidence

- Position encodings of the two axes are read accurately (Cleveland and McGill 1984); the density itself is read as contour spacing or colour, which is a weaker channel, so the rating is `medium`.
- Franconeri et al. 2021: viewers extract shape and clusters fast from a filled region, so the plot answers "where and how many clusters" well and "how much" poorly.
- Bandwidth sensitivity is the recognised pitfall in every practitioner guide (From Data to Viz, seaborn docs).

## Accessibility

- Filled contours need a sequential single-hue ramp with a labelled legend; outlines alone need at least 3:1 contrast and distinct line styles per group.
- Text alternative: "2D density plot of X against Y; the mass concentrates around (a, b) with a second cluster near (c, d)."
- Offer the underlying summary (counts per bin or group medians) as a table.

## Build

### vega-lite

Approximate: Vega-Lite has a 1D `density` transform only; a 2D density is drawn as a binned `rect` heatmap (`"bin": {"maxbins": 40}` on both x and y, `"aggregate": "count"` on colour), which is a smoothed-looking hexbin rather than a kernel contour. True contours need full Vega's `contour` transform, which vl-convert also renders. Hand-written.

### plotly

`{"type": "histogram2dcontour", "x": [...], "y": [...], "colorscale": "Blues", "contours": {"coloring": "fill"}}`; overlay `{"type": "scatter", "mode": "markers", "marker": {"opacity": 0.3}}` when points should stay visible. Native; hand-written.

### matplotlib

seaborn: `sns.kdeplot(data=df, x="x", y="y", fill=True, levels=8, hue="group")` or matplotlib `ax.contourf(X, Y, Z)` after `scipy.stats.gaussian_kde`. Native; hand-written.

## Notes

- 2026-09-18: written from the 2026-09-17 taxonomy research.
