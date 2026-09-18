---
name: Dot density map
slug: dot-density-map
aliases: [dot map, dot distribution map, one dot per n map, point density map]
family: spatial
also: [distribution]
question: How is a population or set of events spread across space?
shapes: ["geo,q", "geo,q,n", "q,q", "q,q,n"]
goals: [spatial, map, density, spread, distribution, where people live, events, incidents, points, settlement, concentration]
max_series: 4
max_categories: 0
evidence: low
popularity: common
status: stable
support:
  mermaid: none
  vega-lite: approx
  plotly: approx
  chartjs: none
  matplotlib: approx
  terminal: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://datavizcatalogue.com/methods/dot_distribution_map.html, https://vega.github.io/vega-lite/docs/geoshape.html, https://plotly.com/javascript/scatter-plots-on-maps/, https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.sample_points.html]
---

# Dot density map

## When to use

- The spread of a population or of events across space is the message: where people live, where incidents happened, where a species was recorded.
- Two forms: one dot per event with real coordinates (crime reports, tree records) or one dot per n units placed randomly inside each region (one dot = 1,000 people), the classic census form.
- Up to about 4 categories as colours (ethnic groups, parties, species) when the interleaving of categories is the point; more than that becomes noise.
- Very large n where individual symbols would overlap into a texture anyway: texture is what a dot density map is for.
- Excels at: showing concentration and emptiness at once; the eye reads density as a global statistic quickly (Franconeri et al. 2021).

## When not to use

- Reading a value for a region: dots cannot be counted; use `choropleth` for rates or `bubble-map` for totals.
- Regions of very different size with random placement: dots spread evenly inside a large sparse county invent settlement where none exists; use land-use masks or a finer unit.
- Small n (dozens of points): it is a `scatter` on a map; plot the points plainly with labels.
- Categories that must be compared quantitatively: colour interleaving shows mixing, not amounts; use `stacked-bar-100` per region.
- Zoomed-out views where dots merge into solid fill: the map becomes a bad `choropleth`; reduce dot size or dot value.

## Substitutes

- Rates by region: `choropleth`.
- Totals by place: `bubble-map`.
- Dense points aggregated honestly: `hex-map` (hexbin counts) or a gridded `heatmap`.
- Continuous density surface: `density-2d` (kernel density contour) over the map.
- Category mix per region as numbers: `stacked-bar-100` or a `table`.

## Evidence

- Rated `low`: convention and cartographic tradition (Data Visualisation Catalogue; FT Visual Vocabulary lists it with the note to annotate the patterns), not a perception study. Density perception is fast but quantitatively unreliable, so the chart works only for the qualitative "where" question.
- Random placement inside regions is a known source of misreading (dots in uninhabited areas); cartography texts advise masking with land use or using the finest region available.
- Franconeri et al. 2021: global statistics (density, clustering) are extracted fast; annotate the clusters the text talks about so readers see the intended ones.

## Accessibility

- Dot size 1 to 2 px at the final resolution with slight opacity so overlap darkens; state the dot value ("one dot = 100 people") in the legend.
- Category colours from a colour-blind-safe set (Okabe-Ito), maximum 4, each named in the legend; test that the dominant pair is distinguishable when interleaved.
- Text alternative: "Dot density map of <what>; each dot is <n>; densest around <A> and <B>, sparse in <C>." Offer a table of totals by region as the data alternative.
- Base map in light grey with thin borders so the dots carry all the contrast.

## Build

Not supported by `cw.py build`. Every target is `approx` because the dots must be generated first: either the data already has coordinates (plot them as points) or a script samples n random points per region polygon before drawing. `geopandas.GeoSeries.sample_points` does the sampling; save the generated CSV and reuse it in any target.

### vega-lite

Two layers: a `geoshape` base map and a `circle` layer with `longitude` and `latitude` encodings from the sampled CSV, `"size": {"value": 4}`, `"opacity": 0.5`, `color` on the category field. Same skeleton as `bubble-map` with fixed size instead of a size field. Render with `cw.py render --target vega-lite --in map.vl.json --out map.png`.

### plotly

`{"type": "scattergeo", "lon": [...], "lat": [...], "mode": "markers", "marker": {"size": 2, "opacity": 0.5, "color": [...]}}` from the sampled points; for tens of thousands of dots use `scattermap` with a tiled base (plotly.js 4 renamed the mapbox traces to `*map`). Python: `px.scatter_geo(df, lat="lat", lon="lon", color="group", opacity=0.5)`.

### matplotlib

`pts = gdf.sample_points(size=(gdf.population // 1000).astype(int)).explode(index_parts=False); base = gdf.plot(color="#f2f2f2", edgecolor="white", ax=ax); pts.plot(ax=ax, markersize=1, alpha=0.5, color="#0072B2"); ax.set_axis_off()`. Save with dpi 200 or more so the dots stay separate. Render with `cw.py render --target matplotlib --in map.py --out map.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. The generated dot CSV is an artefact to keep beside the chart so the random placement is reproducible (set a seed).
