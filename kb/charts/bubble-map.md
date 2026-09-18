---
name: Bubble map
slug: bubble-map
aliases: [proportional symbol map, symbol map, graduated symbol map, circle map, point size map]
family: spatial
also: [magnitude]
question: How much of something is at each place?
shapes: ["geo,q", "geo,q,n", "q,q,q"]
goals: [spatial, map, count, total, volume, size by location, cities, sites, where is the most, population, locations]
max_series: 3
max_categories: 0
evidence: medium
popularity: core
status: stable
support:
  mermaid: none
  vega-lite: native
  plotly: native
  chartjs: none
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/chart-types-guide, https://vega.github.io/vega-lite/examples/geo_circle.html, https://plotly.com/javascript/bubble-maps/, https://geopandas.org/en/stable/docs/user_guide/mapping.html]
---

# Bubble map

## When to use

- Counts and totals located in space: population of cities, cases per hospital, sales per store, earthquakes by magnitude. The bubble carries the amount, the map carries the where.
- Point locations (cities, sites) rather than regions, or regions when the measure is a total that a `choropleth` would distort.
- A few categories on top (colour per bubble) when the categories are 3 or fewer and the colour is not the main message.
- Big range of values: area scaling compresses a 1000:1 range into bubbles that still fit on the page.
- Excels at: showing where the mass is; the largest bubbles are found instantly (Franconeri et al. 2021 on fast extraction of extremes).

## When not to use

- Rates and ratios: a small region with a high rate gets a tiny bubble; use `choropleth`.
- Precise comparison between bubbles: circular area is read worse than length (Heer and Bostock 2010); pair the map with a sorted `bar` for the top n.
- Dense clusters of overlapping bubbles (every ZIP code): the overlap hides the data; aggregate to a coarser unit, use a `hex-map` or `dot-density-map`, or lower opacity.
- Bubbles scaled by radius instead of area: a value twice as large looks four times larger. Always scale area.
- Negative values: there is no negative circle; use a `choropleth` with a diverging scheme.

## Substitutes

- Rates: `choropleth`.
- Many dense points: `hex-map` (binned counts) or `dot-density-map`.
- Equal-weight regions: `tile-grid-map` with a value per tile.
- Exact values: `bar` or `lollipop` sorted by value, with the map as context.
- Movement between places: `flow-map`.
- The same measure without a map, two dimensions plus size: `bubble`.

## Evidence

- Circular area is read with systematic underestimation of large values (Cleveland and McGill 1984; Heer and Bostock 2010 measured circular area worse than length and rectangular area). Rated `medium`: the encoding is well studied and the map form is universal practice (FT, Datawrapper), but the study evidence is about the weakness, not the strength.
- Flannery compensation (perceptual scaling that inflates large symbols) is used by cartographers; most chart libraries scale area linearly, so state "area proportional to value" in the legend and show three reference circles.
- FT Visual Vocabulary: "proportional symbol" for totals, choropleth for rates; both guides warn about overlap.

## Accessibility

- Bubble outline in a darker stroke and fill at 50 to 70 percent opacity so overlaps stay visible.
- A size legend with three labelled reference circles (min, mid, max); direct labels on the largest bubbles.
- If colour encodes a category, keep it to 3 and add labels; colour-blind-safe palette (Okabe-Ito).
- Text alternative: "Bubble map of <measure> by <place>; largest in <A> (<value>), then <B>; concentrated in <region>." Offer the sorted table.

## Build

Not supported by `cw.py build`; hand-written from the recipes. A base map (TopoJSON or GeoJSON) is drawn first, then a point layer with longitude and latitude columns; area scaling is the one setting that must be checked in every library.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "projection": {"type": "albersUsa"},
 "layer": [
  {"data": {"url": "states.topojson", "format": {"type": "topojson", "feature": "states"}}, "mark": {"type": "geoshape", "fill": "#eee", "stroke": "white"}},
  {"data": {"url": "cities.csv"}, "mark": {"type": "circle", "opacity": 0.6, "stroke": "#333"},
   "encoding": {"longitude": {"field": "lon", "type": "quantitative"}, "latitude": {"field": "lat", "type": "quantitative"},
                "size": {"field": "population", "type": "quantitative", "scale": {"range": [10, 2000]}}}}]}
```

`size` on a `circle` mark maps to area, so the scaling is correct by default. Render with `cw.py render --target vega-lite --in map.vl.json --out map.png`.

### plotly

`{"type": "scattergeo", "lon": [...], "lat": [...], "marker": {"size": [...], "sizemode": "area", "sizeref": 2 * max / 40 ** 2, "opacity": 0.6}}` with `layout.geo.scope`. `sizemode: "area"` is required; the default scales diameter. Python: `px.scatter_geo(df, lat="lat", lon="lon", size="population", scope="usa")` (express handles area scaling).

### matplotlib

`base = geopandas.read_file("states.geojson").plot(color="#eee", edgecolor="white", ax=ax); ax.scatter(df.lon, df.lat, s=df.population / df.population.max() * 2000, alpha=0.6, edgecolor="#333")`. `s` is in points squared, so it is area; add three reference circles with `ax.scatter` and `ax.legend`. Render with `cw.py render --target matplotlib --in map.py --out map.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. `chartjs` and `mermaid` have no map support.
