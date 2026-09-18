---
name: Web and static images (Vega-Lite)
slug: vega-lite
kind: web
renders_in: [any web page via vega-embed, Obsidian (obsidian-vega plugin), Jupyter (Altair), static SVG/PNG/PDF via vl-convert, Kroki]
version_checked: "Vega-Lite 6.4.3 (2026-04), Vega 6.4.0, vega-embed 7.2.0, vl-convert-python 1.9.0.post1 (2.0.0rc7 in preview), Altair 6.3.0"
last_verified: 2026-09-17
renderer: vl_convert
tested:
  - Windows 2026-09-18: build and render to PNG/SVG through vl-convert 1.9; inspected
sources: [https://vega.github.io/vega-lite/docs/, https://github.com/vega/vl-convert, https://altair-viz.github.io/, https://github.com/vega/vega-embed]
---

# Web and static images (Vega-Lite)

The default target. One compact JSON spec renders interactively in a page (vega-embed) and to SVG, PNG or PDF with no browser (vl-convert). Generators are more reliable with Vega-Lite than with code libraries (VegaChat 2026: 0% visualization errors vs 30% for code generation; arXiv 2401.11255), and a spec is roughly 150 tokens with data by URL.

## What it can draw

| chart | support | note |
|---|---|---|
| line, multi-line, step, area, stacked-area, bar, column, grouped-bar, stacked-bar, diverging-bar, lollipop, dot, dumbbell, scatter, bubble, connected-scatter, histogram, density, boxplot, strip, heatmap, calendar-heatmap, pie, donut, bullet, waterfall, slope, small-multiples, error-bars, range-band, candlestick, sparkline, stat-tile | native | marks: line, bar, area, point, circle, tick, rect, arc, boxplot, errorband, errorbar, rule, text; `facet`, `layer`, `repeat` compose |
| choropleth, bubble-map, hex-map | native | `geoshape` mark with TopoJSON; needs a boundary file |
| violin, ridgeline, beeswarm, streamgraph | approx | density transform + area/stack; beeswarm needs Vega's force transform |
| treemap, sunburst, icicle, sankey, chord, network, dendrogram, gantt-like ranges | approx or image | full Vega (not Lite) has treemap, partition, pack, force transforms; Gantt is a bar with x/x2 |
| radar, parallel-coordinates, bump | approx | radar via Vega arc math; parallel coordinates via fold + line; bump via rank transform + line |

## Syntax essentials

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "title": "Price over time",
  "data": {"url": "prices.csv"},
  "mark": {"type": "line", "point": true},
  "encoding": {
    "x": {"field": "date", "type": "temporal"},
    "y": {"field": "price", "type": "quantitative"},
    "color": {"field": "series", "type": "nominal"}
  }
}
```

- Types: `quantitative`, `temporal`, `nominal`, `ordinal`. Wrong type is the number one bug (a numeric string becomes nominal, a date becomes text).
- Data by URL (`csv`, `json`, `tsv`) keeps the data out of the model; vl-convert resolves relative paths from the working directory. `{"values": [...]}` inlines it.
- `"width": "container"` fills a div; static export needs a number.
- Layers: `"layer": [{...}, {...}]` for rule + point (lollipop, dumbbell), band + line (range). `"facet"` / `"row"` / `"column"` for small multiples; `"repeat"` for the same chart over several fields.
- Transforms: `filter`, `calculate`, `aggregate`, `bin`, `density`, `window` (rank, running sum), `fold`, `pivot`, `stack`, `regression`, `loess`.
- Colour: `"scale": {"scheme": "tableau10" | "okabeito"... }`; sequential `blues`, `viridis`; diverging `redblue`. Vega has no `okabeito` scheme name; pass `"range": ["#E69F00", ...]`.
- Accessibility: `"description"` on the spec becomes the SVG `aria-label`; add a text alternative in the page.

## Limits

- Not for hierarchies, networks or flows without dropping to Vega (which vl-convert also renders: `vega_to_svg`).
- Static export uses bundled Liberation fonts; set `VL_CONVERT_FONT_DIR` for brand fonts.
- Large data (above about 50k rows) is slow in the browser; pre-aggregate.
- Interactive selections (`params`) are ignored in static output.

## Render

- Page: `cw.py build ... --target vega-lite --html --out chart.html` writes a standalone page loading vega, vega-lite, vega-embed from jsdelivr.
- Image: `cw.py render --target vega-lite --in chart.vl.json --out chart.png` (or `.svg`, `.pdf`, `.html`); `pip install vl-convert-python` once. Scale 2 by default for docs.
- Python: `altair` (`chart.save("x.png", scale_factor=2)`) uses the same converter.
- No install at all: Kroki `https://kroki.io/vegalite/svg/<deflate+base64url>`.

## Notes

- 2026-09-17: created from the 2026-09-17 library research. vl-convert 2.0 (release candidate) adds `serve`; keep 1.9.x until it is stable.
