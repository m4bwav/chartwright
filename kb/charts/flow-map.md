---
name: Flow map
slug: flow-map
aliases: [connection map, origin-destination map, migration map, route map, great circle map, OD map]
family: spatial
also: [flow]
question: How much moves from which place to which place?
shapes: ["geo,geo,q", "flow", "q,q,q,q,q"]
goals: [spatial, flow, map, migration, trade, routes, origin, destination, between cities, movement, traffic, connections]
max_series: 1
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
  echarts: native
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
  docx: image
  gsheets: image
  observable-plot: none
  d2: none
  plantuml: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/connectionmap.html, https://vega.github.io/vega-lite/examples/geo_rule.html, https://plotly.com/javascript/lines-on-maps/, https://scitools.org.uk/cartopy/docs/latest/]
---

# Flow map

## When to use

- Movement between places with a quantity: migration between countries, trade between ports, commuters between districts, flights between airports.
- A small number of origins (one to a handful) with many destinations, or a few dominant pairs; the geography explains the pattern (distance, borders, coasts).
- Line width for volume, optional colour for direction or category, arrowheads or tapering when direction matters.
- Excels at: tying a flow to real distance and direction; nothing else shows "most of it goes south along the coast".

## When not to use

- Many-to-many flows among more than about 20 places: the hairball hides everything; aggregate, filter to the top flows, or use a `sankey`, `chord` or `adjacency-matrix`.
- Exact volumes: line width is read poorly; add a ranked `bar` of the top pairs.
- Flows between adjacent regions that overlap the regions themselves: lines vanish under labels; use a `choropleth` of net flow per region instead.
- Bidirectional flows drawn as one line: the reader cannot see the balance; draw two offset lines, or map net flow.
- Geography that adds nothing (flows between departments of a company): a `sankey` or `chord` is cleaner.

## Substitutes

- Many-to-many with no geography: `sankey` (directional stages) or `chord` (symmetric pairs).
- Dense pairs, exact values: `adjacency-matrix` (origin by destination heat table).
- Net effect per region: `choropleth` of net in-flow; totals per place: `bubble-map`.
- Ordered nodes on a line: `arc-diagram`.
- Grouped links with hierarchy: `edge-bundling`.

## Evidence

- Rated `low`: long cartographic tradition (Minard 1869, FT Visual Vocabulary "flow map") and consistent guidance to limit and bundle flows, but no perception study on reading line-width volumes on maps. Line width is a length-like encoding at right angles to the line; readers estimate ratios poorly when widths are small.
- Data to Viz caveat: connection maps become unreadable above a few dozen links; filter or bundle (Holten 2006 for edge bundling).
- Franconeri et al. 2021: annotate the flows the text discusses; the reader's eye goes to the longest line, not the widest.

## Accessibility

- Width scale with three reference widths in a legend; label the top 3 to 5 flows with their values on the map.
- Colour for direction only when paired with arrowheads or tapering (colour alone fails WCAG 1.4.1); colour-blind-safe pair (blue, orange).
- Lines at 60 to 80 percent opacity so crossings remain visible; base map in light grey.
- Text alternative: "Flow map of <what> between <places>; largest flow <A> to <B> (<value>); most flows go <direction/pattern>." Offer the origin-destination table.

## Build

Not supported by `cw.py build`. Every target is `approx`: the recipe is a base map layer plus a line layer from an origin-destination CSV (`origin_lon, origin_lat, dest_lon, dest_lat, value`). Great-circle curves need a geodesic interpolation step (Python `pyproj.Geod.npts` or D3 `geoInterpolate`); straight rules are acceptable for regional maps.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "projection": {"type": "equalEarth"},
 "layer": [
  {"data": {"url": "world.topojson", "format": {"type": "topojson", "feature": "countries"}}, "mark": {"type": "geoshape", "fill": "#eee", "stroke": "white"}},
  {"data": {"url": "flows.csv"}, "mark": {"type": "rule", "opacity": 0.7, "color": "#0072B2"},
   "encoding": {"longitude": {"field": "olon", "type": "quantitative"}, "latitude": {"field": "olat", "type": "quantitative"},
                "longitude2": {"field": "dlon"}, "latitude2": {"field": "dlat"},
                "strokeWidth": {"field": "value", "type": "quantitative", "scale": {"range": [0.5, 8]}}}}]}
```

`rule` draws straight lines in projected space; for curves pre-interpolate points and use a `line` mark with `detail` per flow. Render with `cw.py render --target vega-lite --in flows.vl.json --out flows.png`.

### plotly

One `scattergeo` trace per flow with `mode: "lines"`, `lon: [olon, dlon]`, `lat: [olat, dlat]`, `line: {width: w}` (Plotly interpolates great circles on `geo` axes), plus a `scattergeo` markers trace for the places; hundreds of flows means hundreds of traces, so filter first. Python: loop `fig.add_trace(go.Scattergeo(...))` over rows.

### matplotlib

`base = world.plot(color="#eee", edgecolor="white", ax=ax); for r in flows.itertuples(): ax.plot([r.olon, r.dlon], [r.olat, r.dlat], linewidth=0.5 + 7 * r.value / vmax, color="#0072B2", alpha=0.7)`. For true great circles use `cartopy` (`transform=ccrs.Geodetic()` on a `PlateCarree` axes). Arrowheads with `ax.annotate("", xy=dest, xytext=origin, arrowprops=dict(arrowstyle="->"))`. Render with `cw.py render --target matplotlib --in flows.py --out flows.png`.

### echarts

Hand-written: series type `lines` on a `geo` coordinate system. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. Keep the OD CSV filtered to the top flows before charting; the filter threshold belongs in the caption.
