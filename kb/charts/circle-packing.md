---
name: Circle packing
slug: circle-packing
aliases: [circular treemap, bubble hierarchy, packed circles, nested circles]
family: hierarchy
also: [part-to-whole, magnitude]
question: How does a hierarchy nest, with each node sized by a value, in a picture readers find inviting?
shapes: ["hier,q", "hier", "n,q"]
goals: [hierarchy, nested, bubbles, cluster, groups, sizes, containment, overview, explore, packed, circles]
max_series: 0
max_categories: 50
evidence: low
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: image
  chartjs: none
  matplotlib: approx
  terminal: none
  echarts: none
  pptx: image
  quickchart: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://vega.github.io/vega/examples/circle-packing/, https://d3js.org/d3-hierarchy/pack, https://www.data-to-viz.com/graph/circularpacking.html, https://github.com/elmotec/circlify, https://www.semanticscholar.org/paper/55d3281f6b34c50df975b7261044689bf73ec610]
---

# Circle packing

## When to use

- A hierarchy where containment is the message and sizes are only rough: which groups exist, which are large, what sits inside what.
- Exploratory or editorial overviews (a "map" of a portfolio, an organisation, a body of documents) where an inviting form matters more than precision, with hover for values.
- Nodes without a size at all: pack equal circles to show the grouping structure.
- A flat set of a few dozen items sized by value when a bubble cloud is the intended look and a bar is available beside it.
- Excels at: making nesting obvious at a glance; circles inside circles read as "part of" without explanation.

## When not to use

- Comparing sizes: circular area is the weakest area encoding (Heer and Bostock 2010) and packing wastes up to a third of the space in gaps, so a `treemap` or `bar` is always more accurate.
- Reading shares of the whole: the gaps mean the parent circle's area is not the sum of the children.
- Labels: only the largest circles fit text; deep nesting hides everything below level two.
- Static reports for decision makers: the form invites but does not inform; use a `treemap` or a `table`.

## Substitutes

- Sizes and hierarchy, space-filling: `treemap`; depth with labels: `icicle`; radial: `sunburst`.
- Structure only: `tree` or `dendrogram`.
- Flat sizes: `bar`, `lollipop`, or `bubble` when two other measures position the circles.
- Group membership without sizes: a `network` with community colouring.

## Evidence

- Circular area is read less accurately than rectangular area, which is itself below length and position (Heer and Bostock 2010; Cleveland and McGill 1984). `low`: no study finds a task the packing does better; From Data to Viz and FT treat it as an attractive but imprecise variant of the treemap.
- Bateman et al. 2010 give a partial defence: engaging forms are remembered; use it where memorability outweighs value reading and label the values.
- Popularity `niche`: D3, Vega and Flourish have it; Plotly, Chart.js, Mermaid and matplotlib do not without add-ons.

## Accessibility

- Label the top-level circles and any circle wider than the text; everything else via tooltip and an indented table.
- One hue per top-level group with lighter fills at deeper levels; borders with 3:1 contrast against fills and background.
- Text alternative: "Circle packing of <measure> by <hierarchy>: <N> groups; <A> is the largest with <n> members and <value>; <B> next." Always accompany with the table, since values are not readable from the picture.
- Avoid encoding a second measure in colour on top of area; readers cannot separate the two.

## Build

### mermaid

No Mermaid packing layout. Render with vega (through the vega-lite target) or matplotlib and link the image; a `mindmap` shows the nesting alone.

### vega-lite

Full Vega: `stratify` then `pack` transform (`"type": "pack", "field": "size", "size": [{"signal": "width"}, {"signal": "height"}]`) and a `symbol` mark with `size` from `datum.r`, rendered by vl-convert (`vega_to_svg`). Hand-written from the Vega circle-packing example. `approx`.

### plotly

Plotly has no pack layout; compute circle positions elsewhere (`circlify` in Python) and plot them as `scatter` markers or `layout.shapes` circles, or render a static image with matplotlib and embed it. Treated as `image`.

### chartjs

Not available. Use a rendered image.

### matplotlib

Hand-written: `pip install circlify` then `circles = circlify.circlify([{"id": "A", "datum": 60, "children": [...]}, ...], show_enclosure=True)`, draw each as `ax.add_patch(plt.Circle((c.x, c.y), c.r, fill=..., edgecolor="white"))`, `ax.set_aspect("equal"); ax.axis("off")`, label circles with `c.r` above a threshold. Render with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
