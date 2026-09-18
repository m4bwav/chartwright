---
name: Arc diagram
slug: arc-diagram
aliases: [arc plot, linear network diagram, arc link diagram, one-dimensional network]
family: flow
also: [relationship, change-over-time]
question: Which items in an ordered sequence are linked, and how far apart are the linked ones?
shapes: ["flow", "n,n,q", "o,o,q"]
goals: [flow, relationship, links along a line, sequence, order matters, repetition, references, co-occurrence, timeline links, chapters, connections between positions]
max_series: 0
max_categories: 40
evidence: low
popularity: niche
status: stable
support:
  mermaid: none
  vega-lite: approx
  plotly: approx
  chartjs: none
  matplotlib: approx
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/arc.html, https://datavizcatalogue.com/methods/arc_diagram.html, https://vega.github.io/vega/examples/arc-diagram/, https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Arc.html]
---

# Arc diagram

## When to use

- Nodes that have a natural order (time, position in a text, chromosome coordinate, chapter number) and links between them; the order is preserved on a line and each link becomes a semicircle above it.
- Repetition and long-range structure: Wattenberg's "The Shape of Song" (repeated passages), citations between sections of a document, protein interactions along a sequence.
- Sparse graphs: up to a few dozen nodes and a few dozen links, where the height of an arc (distance between endpoints) is itself informative.
- Excels at: keeping node order legible while still showing links; a `network` layout loses the order.

## When not to use

- Dense graphs: arcs pile up and the picture is a rainbow; use `adjacency-matrix` (always readable) or `edge-bundling`.
- Nodes with no meaningful order: the layout imposes one and the arc heights become noise; use `network` or `chord`.
- Weighted flows in both directions: arc thickness works for one weight; two directions need `chord` or a matrix.
- Reading link weights: stroke width is a weak encoding; label or table them.
- Finding paths through several links: readers must jump between arcs; a `network` or a matrix with a path highlight does better.

## Substitutes

- Dense or large: `adjacency-matrix`.
- Weighted, pairwise, small set: `chord`.
- Structure without order: `network`.
- Hierarchy plus cross links: `edge-bundling`.
- Sequence of stages with volumes: `sankey`.

## Evidence

- Rated `low`: a niche form with case-study evidence (Wattenberg 2002) and catalogue entries (Data Visualisation Catalogue, Data to Viz, FT Visual Vocabulary) but no controlled study; Data to Viz notes that arc diagrams do not show structure as well as node-link layouts and recommends them for order-preserving cases only.
- Node order is a position encoding, the strongest (Cleveland and McGill 1984), so the order carries the readable information; the arcs carry pattern.
- Franconeri et al. 2021: sort nodes so the comparison the text needs is adjacent, and highlight the arcs the text discusses.

## Accessibility

- Label every node along the baseline (rotate 45 degrees or use a vertical layout with labels to the left when there are more than about 20).
- Arcs at 40 to 60 percent opacity in one hue; colour only for a category of link, with a legend, and highlight the discussed arcs in a second hue.
- Text alternative: "Arc diagram of <n> <nodes> in <order> with <m> links; longest link <A> to <B>; <cluster or repetition pattern>." Offer the edge list as a table.
- Stroke at least 1.5 px; 3:1 contrast against the background.

## Build

Not supported by `cw.py build`; hand-written. Input is a node list in order and an edge list (`source,target[,weight]`). Every target is `approx`: the arcs are drawn from computed geometry, not a native mark.

### vega-lite

Nodes as a `point` layer on `x` (ordinal position) at fixed `y`; arcs as a `line` layer over a pre-generated CSV of arc points (for each edge, 20 to 40 points on the semicircle, with an `edge` id in `detail`), `"interpolate": "monotone"`, `opacity: 0.5`, `strokeWidth` from weight. Generate the arc points in Python or with a `calculate` transform on a sampled sequence. Full Vega has a ready example (`arc-diagram`) with `arc` paths if the page can host Vega. Render with `cw.py render --target vega-lite --in arc.vl.json --out arc.png`.

### plotly

`scatter` trace for nodes (`mode: "markers+text"`, `y: 0`), and one `scatter` line trace per arc with points on the semicircle (or `layout.shapes` with `path: "M x0,0 Q mx,h x1,0"` quadratic curves), `line.width` from weight, `hoverinfo` naming the pair. Hide the y axis and set `xaxis` ticks to node names.

### matplotlib

`for s, t, w in edges: r = (x[t] - x[s]) / 2; ax.add_patch(Arc((x[s] + r, 0), 2 * r, 2 * r, theta1=0, theta2=180, linewidth=0.5 + 3 * w / wmax, alpha=0.6, color="#0072B2"))`; nodes with `ax.scatter(x, [0] * n)` and `ax.set_xticks(x, names, rotation=45, ha="right")`; `ax.set_ylim(0, max_r * 1.05); ax.set_aspect("equal")`. Render with `cw.py render --target matplotlib --in arc.py --out arc.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. Vertical orientation (nodes down the left, arcs to the right) fits long labels and a document page better than horizontal.
