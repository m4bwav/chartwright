---
name: Hex map
slug: hex-map
aliases: [hexagon map, hex tile map, hexbin map, hex cartogram, hexagonal grid map]
family: spatial
also: [distribution, magnitude]
question: What is the value in each region or cell, on a hexagonal grid that keeps neighbours together?
shapes: ["geo,q", "geo,o", "q,q"]
goals: [spatial, map, hexagons, constituencies, equal area, binned, density, grid, election, aggregate points, hexbin]
max_series: 1
max_categories: 7
evidence: low
popularity: rising
status: stable
support:
  mermaid: none
  vega-lite: native
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
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/hexbinmap.html, https://vega.github.io/vega-lite/docs/geoshape.html, https://plotly.com/python/hexbin-mapbox/, https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hexbin.html, https://github.com/odileeds/hexmaps]
---

# Hex map

## When to use

- Two related forms. Hex tile map: one hexagon per region (UK constituencies, US states, French departments), an equal-area cartogram with better adjacency than square tiles. Hexbin map: points aggregated into hexagonal cells of equal area over real geography.
- Elections and per-region categories where every region must be visible and roughly where it belongs; hexagons pack with six neighbours, so the layout keeps more true adjacencies than squares.
- Many point events (taxi pickups, sightings, crimes) that need counting per area without snapping to administrative boundaries (FT "heat map" on a hex grid).
- Excels at: equal visual weight per unit with a tidier, more map-like look than a `tile-grid-map`.

## When not to use

- Readers unfamiliar with the geography or with hex cartograms: the shape distortion confuses; use `choropleth` or a `bar`.
- Continuous rates where region size matters: `choropleth`.
- Sparse point data (a few hundred points): binning hides the individual pattern; use `dot-density-map` or plain points.
- A hexbin grid whose cell size was not chosen deliberately: the picture changes with the bin width; state it and test two sizes.
- Reading exact values from hex fills: colour, the weakest encoding; label the tiles or provide a table.

## Substitutes

- Square tiles with labels and simpler code: `tile-grid-map`.
- True boundaries, rates: `choropleth`.
- Area scaled by value: `cartogram`.
- Individual events: `dot-density-map`; continuous surface: `density-2d`.
- The same binning without a map (two numeric axes): `hexbin`.

## Evidence

- Rated `low`: adoption is broad and rising (ODI Leeds hexmaps, Datawrapper, FT, Observable Plot hexbin transform) but there is no perception study of hex maps versus alternatives. The argument for hexagons is geometric (equal area, six equal neighbours, no diagonal bias of a square grid) rather than perceptual.
- The size bias of choropleths (large regions dominate) is removed by equal tiles; the cost is lost shape, which readers use for orientation.
- Colour reads pattern, not value (Cleveland and McGill 1984); Franconeri et al. 2021 on labelling directly what the reader must compare.

## Accessibility

- Label each hex tile with a short region code; for hexbin maps give the bin size in the legend ("each hexagon covers 5 km").
- One-hue sequential ramp or a colour-blind-safe categorical set; no rainbow. White 1 to 2 px gaps between tiles.
- Text alternative: "Hex map of <measure> by <region or cell>; highest in <A>; <pattern>." Offer the table by region or the top cells.
- Provide a north indicator or a familiar outline (coastline) beside a hex cartogram so readers can orient.

## Build

Not supported by `cw.py build`. For a hex tile map, use a published hex layout as GeoJSON (ODI Leeds HexJSON converts to GeoJSON; US-state hex GeoJSON files exist) and treat it as a `choropleth` with that geometry. For a hexbin map, bin the points first (matplotlib `hexbin`, or `h3` cells) and draw the resulting polygons.

### vega-lite

Hex tile map: the choropleth recipe with `"data": {"url": "hexes.geojson", "format": {"type": "json", "property": "features"}}`, `"projection": {"type": "identity", "reflectY": true}` (hex layouts are already planar), a `geoshape` mark and `color` from a `lookup` on the region key; add a `text` layer at `properties.centroid` for labels. Hexbin: pre-bin to polygons and draw the same way. `cw.py render --target vega-lite --in hex.vl.json --out hex.png`.

### plotly

Hex tile: `choropleth` with `geojson` of hexagon features and `featureidkey: "properties.code"`, `layout.geo.projection.type = "identity"` is not available for arbitrary planar data, so use `choroplethmap` (tiles) or draw hexagons as `scatter` with `marker.symbol = "hexagon2"` at tile centres, sized to touch. Hexbin: `plotly.figure_factory.create_hexbin_mapbox(df, lat="lat", lon="lon", nx_hexagon=30)` (retained in plotly.py 7 under the mapbox name for the figure factory; check the changelog). Both are compositions, hence `approx`.

### matplotlib

Hex tile: `gdf = geopandas.read_file("hexes.geojson").merge(df, on="code"); gdf.plot(column="value", cmap="Blues", edgecolor="white", ax=ax)` plus `ax.annotate` per centroid. Hexbin over a base map: `ax.hexbin(df.lon, df.lat, gridsize=40, cmap="viridis", mincnt=1)` on the same axes as `base.plot(...)`. Render with `cw.py render --target matplotlib --in hex.py --out hex.png`.

### echarts

Hand-written: custom series over a hex grid. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. The vega-lite target file lists hex-map as native because `geoshape` draws any polygon file; the hard part is obtaining the layout, not the drawing.
