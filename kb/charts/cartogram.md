---
name: Cartogram
slug: cartogram
aliases: [scaled cartogram, contiguous cartogram, Dorling cartogram, area cartogram, population cartogram, distorted map]
family: spatial
also: [magnitude, part-to-whole]
question: How big is each region when area stands for a value instead of land?
shapes: ["geo,q", "geo,q,n"]
goals: [spatial, map, population, votes, weighted by, distorted, scaled, electoral, seats, land does not vote, proportional area]
max_series: 1
max_categories: 7
evidence: low
popularity: niche
status: stable
support:
  mermaid: none
  vega-lite: approx
  plotly: approx
  chartjs: none
  matplotlib: approx
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/cartogram.html, https://datavizcatalogue.com/methods/cartogram.html, https://github.com/mthh/cartogram_geopandas, https://vega.github.io/vega-lite/docs/geoshape.html]
---

# Cartogram

## When to use

- A second value (population, votes, GDP, seats) must correct the land-area bias of a `choropleth`: election maps where dense cities matter more than empty counties.
- Three forms. Contiguous (regions stretched, still touching): keeps neighbours, distorts shape. Non-contiguous (regions shrunk in place): keeps shape, loses adjacency. Dorling (a circle per region, packed): cleanest, loses both, easiest to read as data.
- The audience knows the base geography well enough to recognise the distortion, and the distortion itself is the message ("this is what the electorate looks like").
- A colour on top (winner, category, rate) when area is the weight and colour is the outcome: area times colour is the honest picture of a vote.
- Excels at: making area mean something; a Dorling cartogram is a `bubble-map` with overlaps resolved.

## When not to use

- Audiences unfamiliar with the geography or with cartograms: the distorted shapes look like errors; use a `tile-grid-map` or `hex-map`, which give equal weight without the shock.
- Reading values: area is read badly (Heer and Bostock 2010); pair with a sorted `bar` for numbers.
- The weighting value is nearly uniform: the cartogram equals the map; use a `choropleth`.
- Frequent republication with changing data: contiguous cartograms are computed, slow and unstable between runs; a fixed hex layout is reproducible.
- Print at small size: distorted regions lose labels; use a Dorling form with codes inside circles.

## Substitutes

- Equal weight per region, no computation: `tile-grid-map` or `hex-map`.
- Totals without distortion: `bubble-map`.
- Rates with true shapes: `choropleth`.
- Values as numbers: `bar` sorted, or `dot-plot`.
- Share of a whole by region: `treemap` or `waffle` with region labels.

## Evidence

- Rated `low`: the argument is logical (area should encode the value being discussed; FT and Data to Viz) rather than empirical, and Data to Viz lists reader confusion as the main caveat. Area perception is the weak point (Cleveland and McGill 1984; Heer and Bostock 2010).
- Dorling 1996 introduced the circle cartogram for British elections; newsrooms (Guardian, FT, NYT 2016 onward) use Dorling and hex forms more than contiguous ones because they read faster.
- Franconeri et al. 2021: a familiar shape recognised at a glance is a global feature; distorting it costs recognition, so a locator inset of the true map beside the cartogram helps.

## Accessibility

- Inset of the undistorted map so readers can orient; label the largest and the most distorted regions.
- Dorling form: region codes inside circles, colour-blind-safe categorical fill, 1 px darker outline.
- Text alternative: "Cartogram of <regions> sized by <value>, coloured by <category>; <A> dominates at <value>; <pattern>." Offer the table with both value and category.
- Legend for area (three reference sizes) and for colour; no colour-only encoding.

## Build

Not supported by `cw.py build`. Every target is `approx` because the geometry must be computed first: contiguous with `cartogram_geopandas` (Python) or `cartogram` (R), Dorling with a circle-packing pass (`d3.forceCollide` or a simple iterative push in Python), non-contiguous by scaling each polygon about its centroid (`shapely.affinity.scale`). Save the result as GeoJSON and draw it as a `choropleth` in any target.

### vega-lite

Contiguous or non-contiguous: the choropleth recipe pointed at the computed GeoJSON (`"format": {"type": "json", "property": "features"}`), `geoshape` mark, colour from the data. Dorling: a `circle` layer with `x`, `y` from the computed centres (planar, `"axis": null`) and `size` from the value, plus a `text` layer for codes. Render with `cw.py render --target vega-lite --in carto.vl.json --out carto.png`.

### plotly

Contiguous: `choropleth` with `geojson` set to the computed features and `featureidkey`, `layout.geo.fitbounds = "locations"`, `visible: false` for the base. Dorling: `scatter` with `marker.size` (area mode) at computed centres, `text` labels, axes hidden and `scaleanchor` set so circles stay round.

### matplotlib

`from cartogram_geopandas import make_cartogram; cg = make_cartogram(gdf, "population", iterations=5); cg.plot(column="winner", categorical=True, legend=True, edgecolor="white", ax=ax); ax.set_axis_off()`. Dorling: `ax.scatter(x, y, s=area, c=colors)` with computed non-overlapping centres and `ax.set_aspect("equal")`. Render with `cw.py render --target matplotlib --in carto.py --out carto.png`.

### echarts

Hand-written: series type `map` with pre-distorted GeoJSON. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. When a request says "cartogram" but the audience is general, propose `hex-map` first and keep the cartogram for a second view.
