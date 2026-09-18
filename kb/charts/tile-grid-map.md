---
name: Tile grid map
slug: tile-grid-map
aliases: [tile map, grid map, square tile map, equal-area tile cartogram, state tile map]
family: spatial
also: [magnitude]
question: What is the value in each region, giving every region the same visual weight?
shapes: ["geo,q", "geo,o", "geo,n"]
goals: [spatial, map, by state, by region, election, equal weight, tiles, grid, small regions, every region visible, category by region]
max_series: 1
max_categories: 7
evidence: medium
popularity: rising
status: stable
support:
  mermaid: none
  vega-lite: approx
  plotly: approx
  chartjs: approx
  matplotlib: approx
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/chart-types-guide, https://vega.github.io/vega-lite/docs/rect.html, https://github.com/kurkle/chartjs-chart-matrix, https://github.com/hafen/geofacet]
---

# Tile grid map

## When to use

- One value or category per region where every region must be equally visible: US states, UK constituencies, EU members, German Länder. Rhode Island gets the same tile as Texas.
- Election results, policy status (adopted or not), rankings by state: categorical or ordinal values that a `choropleth` would hide in small regions.
- Readers who know the rough geography and need the "where" only approximately; the grid keeps neighbours near each other without true shape.
- A small chart per tile (sparkline, mini bar) when comparing shapes across regions: the geofacet form of `small-multiples`.
- Excels at: equal weight per region and space for a label and value inside every tile (FT: "good for representing voting regions").

## When not to use

- Readers who do not know the geography: without shapes the map is a coloured grid; a sorted `bar` says more.
- Continuous quantities where region size or population matters: use `choropleth` (rates) or `cartogram` (scaled).
- Regions with no established grid layout: inventing one costs time and confuses; use `hex-map` layouts that exist, or a bar chart.
- More than one measure per tile as colour: one colour scale per chart; several measures are `small-multiples` of tile maps.
- Precise value lookup across many tiles: the eye compares colour badly; print the number in each tile or use a `table`.

## Substitutes

- True shapes, rates: `choropleth`.
- Hexagonal tiles with better adjacency: `hex-map`.
- Area scaled to a value: `cartogram`.
- No map needed: `bar` sorted by value, or `dot-plot`.
- Time series per region: `small-multiples` laid out on the grid (geofacet).
- Counts at points: `bubble-map`.

## Evidence

- Rated `medium`: consistent newsroom practice (FT Visual Vocabulary, NPR, Datawrapper, Washington Post state tiles since 2015) and the perceptual argument that equal areas remove the size bias documented for choropleths; no controlled study compares tile maps with choropleths on a defined task.
- Position on a grid is stable and labels fit, which supports direct labelling, the strongest practical aid in Franconeri et al. 2021.
- Adjacency is a compromise: every published US tile grid moves some states; cite the layout used and keep it constant across a publication.

## Accessibility

- Print the region abbreviation and, when space allows, the value inside every tile; colour then confirms rather than carries.
- Categorical fills from a colour-blind-safe palette (Okabe-Ito) with a legend; ordinal fills as one hue in 3 to 7 steps.
- Text alternative: "Tile grid map of <measure> by <region>; <n> regions in <category A>, notably <list>; <pattern>." Offer the table.
- Tiles with a white gap (2 px) so adjacent same-colour tiles remain countable; 3:1 contrast for the label against the tile.

## Build

Not supported by `cw.py build`. Every target is `approx`: no library ships tile layouts, so the recipe is a lookup table (`region, row, col`) joined to the data and drawn as squares. Keep the layout CSV in the project (a US-states layout is about 50 rows) and reuse it.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "values.csv"},
 "transform": [{"lookup": "state", "from": {"data": {"url": "us-tiles.csv"}, "key": "state", "fields": ["row", "col"]}}],
 "layer": [{"mark": {"type": "rect", "stroke": "white", "strokeWidth": 2},
            "encoding": {"color": {"field": "value", "type": "quantitative", "scale": {"scheme": "blues"}}}},
           {"mark": {"type": "text", "fontSize": 10}, "encoding": {"text": {"field": "state"}}}],
 "encoding": {"x": {"field": "col", "type": "ordinal", "axis": null}, "y": {"field": "row", "type": "ordinal", "axis": null}},
 "width": 440, "height": 280}
```

Render with `cw.py render --target vega-lite --in tiles.vl.json --out tiles.png`.

### plotly

A `heatmap` trace with `z` as a 2D array holding the value at `[row][col]` and `null` elsewhere, `xgap: 2, ygap: 2`, axes hidden, plus `layout.annotations` for the abbreviations; or `scatter` with `marker.symbol = "square"`, large size and `text` labels. Python: build the matrix with pandas `pivot` on the layout CSV, then `go.Heatmap`.

### chartjs

`chartjs-chart-matrix` plugin: `type: "matrix"`, each datum `{x: col, y: row, v: value}`, `width`/`height` callbacks returning the cell size, `backgroundColor` from a colour scale function; labels need the `chartjs-plugin-datalabels` plugin. Canvas output, so add `aria-label` and a fallback table.

### matplotlib

`for r in rows: ax.add_patch(Rectangle((r.col, -r.row), 1, 1, facecolor=cmap(norm(r.value)), edgecolor="white", linewidth=2)); ax.text(r.col + 0.5, -r.row + 0.5, r.state, ha="center", va="center")`, then `ax.set_aspect("equal"); ax.set_axis_off()` and a `ScalarMappable` colour bar. Render with `cw.py render --target matplotlib --in tiles.py --out tiles.png`.

### echarts

Hand-written: `heatmap` on a hand-laid category grid. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. The `geofacet` R package and its layout CSVs are the most complete public source of tile layouts; copy one rather than inventing.
