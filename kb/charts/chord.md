---
name: Chord diagram
slug: chord
aliases: [chord chart, circular flow diagram, radial flow diagram, circos plot, migration circle]
family: flow
also: [relationship]
question: How much flows between each pair in a small set of entities, in both directions, and who are the net winners?
shapes: ["flow", "n,n,q"]
goals: [flow, between, pairwise, two-way, mutual, trade between, migration between, exchange, matrix of flows, net flow, circular]
max_series: 0
max_categories: 10
evidence: low
popularity: niche
status: stable
support:
  mermaid: none
  vega-lite: image
  plotly: approx
  chartjs: none
  matplotlib: native
  terminal: none
  echarts: native
  pptx: image
  quickchart: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/chord.html, https://github.com/fengwangPhysics/matplotlib-chord-diagram, https://plotly.com/python/v3/filled-chord-diagram/, https://echarts.apache.org/handbook/en/basics/release-note/v6-feature/]
---

# Chord diagram

## When to use

- A square matrix of flows among a small set of entities where both directions matter: trade between 8 regions, migration between continents, calls between departments, passes between players.
- The question is the pattern of exchange and the net balance: which pairs dominate, who sends more than it receives (the ribbon is wider at the sender's end).
- Up to about 10 entities; each entity's arc length is its total in plus out, so the outer ring doubles as a `bar` of totals.
- An engaged audience willing to learn the reading rule; it is a poster chart more than a dashboard chart.
- Excels at: showing all pairwise relations of a small set in one compact circle (FT Visual Vocabulary: "two-way flows and net winners").

## When not to use

- General audiences or a quick read: most readers do not know that ribbon width at each end means outflow; use a `sankey` with the entities on both sides, or an `adjacency-matrix`.
- More than about 10 entities or many small flows: the centre fills with hair; use `adjacency-matrix` (values readable, any size).
- Exact values: ribbons and arcs are width and angle encodings, both weak (Cleveland and McGill 1984); print the matrix.
- One-directional stage flows (source to sink): `sankey`.
- Relations without quantity (who is connected to whom): `network` or `arc-diagram`.

## Substitutes

- Directional, staged flows: `sankey`; categorical cohorts: `alluvial`.
- Any size, exact values: `adjacency-matrix`.
- Net flow per entity only: `diverging-bar` (in minus out).
- Unweighted relations: `network`, `arc-diagram`.
- Flows on a map: `flow-map`.

## Evidence

- Rated `low`: the chart rests on convention (Circos in genomics, FT, Data to Viz) and on editorial success stories (Guardian migration circle), not on perception studies; Data to Viz lists reader confusion as its main caveat and recommends explaining the reading rule in the caption.
- Angle and ribbon width are ranked below length and position (Cleveland and McGill 1984); the outer arcs (lengths along a circle) are the most readable part.
- Franconeri et al. 2021: readers follow one relation at a time; interactive highlighting of one entity's ribbons is the feature that makes chord diagrams usable, so static versions should highlight the one pair the text discusses.

## Accessibility

- Label each arc with the entity name and total; label the top 3 ribbons with values; grey all other ribbons at 30 percent opacity.
- Colour ribbons by the larger-flow end (the sender) from a colour-blind-safe palette of at most 8; keep the same colour on the entity's arc.
- Text alternative: "Chord diagram of <flows> among <n> entities; largest exchange <A> to <B> (<value>); <A> is the largest net sender; <finding>." Offer the full matrix as a table.
- Interactive versions must expose the same per-ribbon values on keyboard focus, not hover only.

## Build

Not supported by `cw.py build`; hand-written. Input is a square matrix (rows send, columns receive) or `source,target,value` rows including both directions.

### plotly

No chord trace; the composition is a `scatterpolar` or `scatter` figure with `layout.shapes` bezier paths for ribbons and arcs computed in Python (the plotly.py v3 filled-chord example is the reference). Real work, hence `approx`. When the picture is what matters, the matplotlib route below is shorter; when interactivity matters, consider a `sankey` trace with entities duplicated on both sides.

### matplotlib

`pip install mpl-chord-diagram`, then `from mpl_chord_diagram import chord_diagram; chord_diagram(matrix, names=names, order=None, sort="size", ax=ax)`; `colors=` accepts a palette list, `gap=0.03` opens the ring, `chordwidth=0.7` controls ribbon curvature. Add totals to `names` yourself (`f"{n} ({t})"`). Render with `cw.py render --target matplotlib --in chord.py --out chord.png`.

### echarts

Hand-written: series type `chord` (ECharts 6.0+). See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. `vega-lite` is `image` (no chord layout in Vega-Lite or Vega without a hand-built arc and ribbon transform) and `chartjs` has no plugin in the target list; ECharts 6 added a native `chord` series for web pages that already use ECharts.
