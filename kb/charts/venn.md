---
name: Venn diagram
slug: venn
aliases: [Euler diagram, set diagram, overlapping circles, intersection diagram]
family: part-to-whole
also: [relationship]
question: Which sets overlap, and roughly how much do they share?
shapes: ["n,q", "n"]
goals: [overlap, intersection, sets, both, either, shared, common, union, membership, venn, euler]
max_series: 3
max_categories: 3
evidence: low
popularity: niche
status: stable
support:
  mermaid: native
  vega-lite: image
  plotly: image
  chartjs: none
  matplotlib: approx
  terminal: none
  echarts: none
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://mermaid.js.org/, https://github.com/konstantint/matplotlib-venn, https://ieeexplore.ieee.org/document/6876017, https://datavizcatalogue.com/methods/venn_diagram.html]
---

# Venn diagram

Caveat: a Venn diagram is a schematic, not a quantitative chart (FT: "generally only used for schematic representation"). It belongs in a chart knowledge base because people ask for it by name; the honest answer for counted overlaps of more than three sets is an UpSet plot or a bar of intersections.

## When to use

- Two or three sets and the message is logical: which combinations exist, what "both" and "either" mean, with the counts written in each region.
- Explaining a concept (the sweet spot between three qualities) where no data is being read at all; that is a diagram, and Mermaid or a slide tool is the right home.
- Small counted overlaps (customers who bought A, B, both) for a general audience, with numbers in every region and no claim that areas are proportional.
- Excels at: making the idea of overlap instantly legible; nothing else says "both" as fast.

## When not to use

- Four or more sets: the regions become unreadable shapes and most tools cannot draw them; use an `upset` plot (set-size bars plus an intersection matrix) or a `table`.
- Reading sizes from areas: circle areas and lens-shaped intersections are almost never proportional (an Euler diagram tries; a Venn does not), and readers cannot compare lens areas anyway.
- Comparing overlaps across groups or over time: nothing aligns; use bars of intersection counts.
- Any case where the counts are the point and the audience is analytical: label a `bar` of the seven regions instead.

## Substitutes

- Counted intersections of many sets: `upset` plot; a sorted `bar` of intersection sizes for few sets.
- Membership of items in sets: `adjacency-matrix` or a `heatmap` of items by set.
- Shares of one whole: `pie`, `stacked-bar-100`, `waffle`.
- Relationships between entities: `network`.

## Evidence

- No perceptual support: intersection areas are irregular shapes, and area is already a weak encoding (Cleveland and McGill 1984; Heer and Bostock 2010). `low`, and the schematic caveat applies. Lex et al. 2014 (UpSet, TVCG) document how Venn diagrams fail beyond three sets and propose the matrix-plus-bars alternative.
- Practitioner guidance (FT, Data Visualisation Catalogue) keeps it for schematic use with two or three sets.
- Popularity `niche`: Mermaid added a `venn` diagram in 2026; most charting libraries do not draw it, which says how it is used.

## Accessibility

- Write the count or label inside every region, including the outside-all region when it exists; colour is decoration.
- Translucent fills so the overlap reads as a mix, with 3:1 border contrast; two or three colour-blind-safe hues.
- Text alternative: "Venn diagram of <A> (<n>), <B> (<n>): <n> in both, <n> only A, <n> only B." The table of regions is the real data.
- For anything counted, provide the region table next to the diagram, since areas are not proportional.

## Build

### mermaid

Mermaid 12.0 has a `venn` diagram (keyword and syntax new in 2026; GitHub and Obsidian were on 11.x as of 2026-09, so it will not render there yet). Hand-written from the Mermaid docs for the exact syntax of the host's version; on older hosts, embed an image. `native` only on 12.0 hosts.

### vega-lite

No set-diagram mark. Render the diagram elsewhere (matplotlib) and link the image; for counted sets, build a `bar` of the intersection counts with the vega-lite target instead.

### plotly

No Venn trace; `layout.shapes` circles with annotations can fake one but earn nothing. Render with matplotlib and embed the image, or use a bar of intersections.

### chartjs

Not available. Use an image or a bar of intersections.

### matplotlib

Hand-written: `pip install matplotlib-venn` then `from matplotlib_venn import venn2, venn3; venn3(subsets=(a, b, ab, c, ac, bc, abc), set_labels=("A", "B", "C"))` (the add-on scales areas roughly, so state that in the caption). Render with `cw.py render --target matplotlib --in chart.py --out chart.png`. `approx`: an add-on, and areas are approximate by design.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. `upset` is named as the substitute although it has no file yet in the first fan-out; add it when set-intersection requests appear.
