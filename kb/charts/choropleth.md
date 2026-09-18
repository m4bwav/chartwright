---
name: Choropleth map
slug: choropleth
aliases: [filled map, shaded map, thematic map, region map, heat map by region]
family: spatial
also: [magnitude, deviation]
question: How does a rate or ratio vary across regions?
shapes: ["geo,q", "geo,o"]
goals: [spatial, map, by region, by state, by country, by county, rate, share, density, per capita, geography, where]
max_series: 1
max_categories: 7
evidence: medium
popularity: core
status: stable
support:
  mermaid: none
  vega-lite: native
  plotly: native
  chartjs: none
  matplotlib: native
  terminal: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/chart-types-guide, https://vega.github.io/vega-lite/docs/geoshape.html, https://plotly.com/javascript/choropleth-maps/, https://geopandas.org/en/stable/docs/user_guide/mapping.html, https://colorbrewer2.org]
---

# Choropleth map

## When to use

- One rate, ratio or index per administrative region (unemployment rate by county, vote share by constituency, cases per 100k by country) where the reader already knows the geography.
- The message is a spatial pattern: a north-south divide, a cluster, a border effect. The map exists to show where, not how much.
- Regions of roughly comparable size, or a message that survives large empty regions dominating the picture.
- Diverging measures (swing, change versus average) with a meaningful midpoint: a two-hue scheme around neutral.
- Excels at: locating a pattern the reader can tie to places they know; nothing else does that as directly (FT Visual Vocabulary).

## When not to use

- Totals or counts (population, sales, votes cast): large sparse regions win by area, the "land does not vote" problem (FT: "should always be rates rather than totals"). Use `bubble-map` for counts.
- The reader must compare exact values between regions: colour is the weakest encoding (Cleveland and McGill 1984); use a sorted `bar` or a `table`, or pair the map with one.
- Regions of wildly different size where small ones carry the story (cities, small states): they vanish; use `tile-grid-map` or `hex-map`.
- More than about 7 classes, or a continuous rainbow scale: readers cannot order the colours. Use 4 to 7 classes of one hue, or a perceptually uniform ramp.
- Data at a different resolution from the boundaries (points, or regions that changed over time): aggregate honestly or use a `dot-density-map`.
- Several measures or several time points: one map per measure as `small-multiples`, never one map with mixed encodings.

## Substitutes

- Counts and totals: `bubble-map` (proportional symbol).
- Equal weight per region, elections, small regions matter: `tile-grid-map` or `hex-map`.
- Values scaled to region size so area means something: `cartogram`.
- Individual events or population spread: `dot-density-map`.
- Exact comparison of regions: `bar` sorted by value, `dot-plot`, or a `table` with a colour column.
- Ranking of regions over time: `bump`; change between two dates: `slope`.

## Evidence

- Colour lightness is the least accurate elementary encoding (Cleveland and McGill 1984; Heer and Bostock 2010), so a choropleth is for pattern, not value; label the extremes and give a table for lookups. Rated `medium`: strong practitioner consensus (FT, Datawrapper, Brewer) but no perception study showing choropleths beat alternatives at a defined task.
- Class count and scheme: Brewer's ColorBrewer guidance (sequential one hue, 3 to 7 classes, diverging around a real midpoint) is the standard; class breaks (quantile, equal interval, Jenks) change the picture, so state which one was used.
- Rates over totals: FT Visual Vocabulary and Datawrapper both make this the first rule for choropleths; area-weighted perception exaggerates large regions.
- Franconeri et al. 2021: colour scales are one of the main sources of misleading charts; a legend with real values at each break, and annotation of the finding, reduce misreading.

## Accessibility

- Sequential scheme of one hue (viridis, cividis, ColorBrewer Blues) or a colour-blind-safe diverging scheme (RdBu, BrBG with a neutral midpoint); never rainbow, never red-green.
- Colour is the only encoding, so add labels for the regions that matter (top, bottom, the one the text discusses) and a legend with the actual values at each break.
- Text alternative: "Choropleth map of <measure> by <region type>; highest in <A> at <value>, lowest in <B>; <pattern>." Offer the sorted table.
- Region borders in a thin neutral stroke so adjacent similar regions stay distinguishable; 3:1 contrast between adjacent classes where possible.

## Build

Not supported by `cw.py build`; every recipe is hand-written. All targets need a boundary file (TopoJSON or GeoJSON keyed by region id); the data joins to it by that key. Keep the geometry simplified (mapshaper, about 1 MB or less) for the web.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json",
 "data": {"url": "counties.topojson", "format": {"type": "topojson", "feature": "counties"}},
 "transform": [{"lookup": "id", "from": {"data": {"url": "rates.csv"}, "key": "id", "fields": ["rate"]}}],
 "projection": {"type": "albersUsa"},
 "mark": {"type": "geoshape", "stroke": "white", "strokeWidth": 0.3},
 "encoding": {"color": {"field": "rate", "type": "quantitative", "scale": {"scheme": "blues"}, "bin": {"maxbins": 6}}}}
```

`lookup` joins the CSV to the geometry; `bin` gives classes (drop it for a continuous ramp); `"type": "quantile"` in the scale gives quantile classes. Projections: `albersUsa`, `mercator`, `equalEarth`. Render with `cw.py render --target vega-lite --in map.vl.json --out map.png`.

### plotly

`{"type": "choropleth", "locations": ["CA", "TX"], "locationmode": "USA-states", "z": [5.1, 4.2], "colorscale": "Blues"}` with `layout.geo.scope = "usa"`; built-in geometries for countries (ISO-3) and US states, `geojson` plus `featureidkey` for anything else. Python: `px.choropleth(df, locations="iso3", color="rate", color_continuous_scale="Blues")`. Write HTML with `include_plotlyjs="cdn"`; static PNG needs Chrome.

### matplotlib

`gdf = geopandas.read_file("counties.geojson").merge(df, on="id"); gdf.plot(column="rate", cmap="Blues", scheme="quantiles", k=5, legend=True, edgecolor="white", linewidth=0.3, ax=ax); ax.set_axis_off()`. `scheme` needs `mapclassify`. Save with `fig.savefig("map.png", dpi=200)`. Run through `cw.py render --target matplotlib --in map.py --out map.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. `chartjs` is `none` because the chartjs target file lists no map support; `mermaid` has no map type at all.
