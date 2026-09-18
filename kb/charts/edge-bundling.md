---
name: Hierarchical edge bundling
slug: edge-bundling
aliases: [edge bundling, bundled edges, radial edge bundling, hierarchical bundling, dependency wheel]
family: relationship
also: [hierarchy, flow]
question: Which parts of a hierarchy are linked to which other parts, and where do the links concentrate?
shapes: ["hier,flow", "flow", "n,n,q"]
goals: [relationship, hierarchy, dependencies, cross links, bundled, imports, calls between modules, radial, which groups talk to which, software architecture]
max_series: 0
max_categories: 300
evidence: medium
popularity: niche
status: stable
support:
  mermaid: none
  vega-lite: image
  plotly: image
  chartjs: none
  matplotlib: image
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/edge_bundling.html, https://vega.github.io/vega/examples/edge-bundling/, https://observablehq.com/@d3/hierarchical-edge-bundling, https://doi.org/10.1109/TVCG.2006.147]
---

# Hierarchical edge bundling

## When to use

- Entities that live in a hierarchy (packages contain modules contain classes; regions contain countries) and links that cross the hierarchy (imports, calls, trade). Nodes sit on a circle grouped by their branch; each link is routed along the tree path so links between the same two branches merge into a visible bundle (Holten 2006).
- Software dependency maps, gene interactions by chromosome, flows between grouped entities: the question is "which groups talk to which", not individual links.
- Hundreds of nodes and links, where a `network` is a hairball and an `adjacency-matrix` loses the grouping picture.
- Excels at: turning many links into a few thick bundles that read as group-to-group relations.

## When not to use

- No meaningful hierarchy: the bundling routes along an arbitrary tree and the bundles lie; use `network` or `adjacency-matrix`.
- Reading individual links or their weights: bundles hide them by design; provide a filtered `arc-diagram`, an interactive version with highlight, or a matrix.
- Few links (under about 30): bundling adds nothing; draw an `arc-diagram` or a `network`.
- Markdown or office documents that cannot host D3 or Vega: it is a rendered image, and the interactive highlight that makes it usable is lost; consider the `adjacency-matrix` sorted by hierarchy instead.
- Directed flows with volumes: `sankey` or `chord`.

## Substitutes

- Grouped links with exact values: `adjacency-matrix` with rows and columns sorted by the hierarchy.
- Small weighted set: `chord`.
- Ordered nodes: `arc-diagram`; unordered sparse graph: `network`.
- The hierarchy alone: `tree`, `dendrogram`, `sunburst`.
- Group-to-group flows only: aggregate to groups and draw a `sankey` or `chord`.

## Evidence

- Holten 2006 (IEEE TVCG 12(5), "Hierarchical Edge Bundles") introduced the technique with a user evaluation showing reduced clutter and better recognition of high-level relations versus unbundled radial layouts; one study with later follow-ups on bundling strength, hence `medium` for the "which groups" question and `low` for anything about individual links.
- Bundle thickness is not a calibrated encoding; readers overestimate the strength of dense bundles (Data to Viz caveat). Give group-to-group counts as numbers.
- Franconeri et al. 2021: interactive highlighting of one node's links is what makes the individual relations readable; a static image should highlight the one relation the text discusses.

## Accessibility

- Node labels around the circle in branch order with branch names as arcs or colour bands; colour-blind-safe palette for at most 8 branches, with names.
- Bundles at 20 to 40 percent opacity in one hue, with highlighted bundles in a second hue; on the web, a click-to-highlight (not hover only) that lists the linked nodes.
- Text alternative: "Edge bundling of <n> <nodes> in <k> groups with <m> links; strongest group-to-group relation <A> to <B> (<count>); <finding>." Offer the group-to-group matrix as a table.
- Static images need a legend stating that thickness shows bundled link count, not a scale.

## Build

Not supported by `cw.py build`. All five targets are `image` or `none`: none of them has a bundling primitive. Produce the picture with one of these and link it, keeping the source data and script beside it:

- Full Vega (not Vega-Lite): the `edge-bundling` example spec (`tree` transform with `cluster` layout, `treelinks`, `treepath` lines with `bundle` interpolation and `tension` 0.85). Render without a browser: `vl-convert` exposes `vega_to_svg` and `vega_to_png` for full Vega specs (`python -c "import vl_convert as vlc; open('bundle.svg','w').write(vlc.vega_to_svg(open('bundle.vg.json').read()))"`). This is the route that fits the plugin's toolchain.
- D3 in an HTML page: `d3.cluster()` on the hierarchy, `d3.lineRadial().curve(d3.curveBundle.beta(0.85))` for links (Observable "Hierarchical edge bundling"); the only route with the interactive highlight.
- Python: `pyecharts` or a matplotlib script that draws bezier paths through the tree ancestors by hand; long and not recommended when Vega is available.

The `plotly` and `matplotlib` targets are `image` because a hand-drawn bundle in either is more work than the Vega spec and gives a worse result; when the document already ships those libraries, still make the picture with Vega and embed it.

### echarts

Hand-written: series type `graph` with `layout: "circular"` and curved edges (no bundling). See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. If a request needs interactivity, deliver the D3 page; if it needs a picture, the Vega spec through vl-convert.
