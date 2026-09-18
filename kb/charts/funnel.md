---
name: Funnel chart
slug: funnel
aliases: [conversion funnel, sales funnel, pipeline chart, drop-off chart]
family: part-to-whole
also: [flow, ranking]
question: How much drops out at each stage of a fixed sequence?
shapes: ["o,q"]
goals: [funnel, conversion, drop-off, pipeline, stages, retention, sign-up, checkout, leads, step by step, remaining, steps, signup]
max_series: 2
max_categories: 7
evidence: low
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: native
  chartjs: approx
  matplotlib: approx
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://plotly.com/javascript/funnel-charts/, https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://datavizcatalogue.com/methods/funnel_chart.html, https://www.data-to-viz.com]
---

# Funnel chart

## When to use

- A strictly nested sequence of stages where each stage's population is a subset of the previous one: visited, added to cart, checked out, paid.
- The audience expects the form (marketing, sales, product analytics) and the message is "where do we lose people".
- Up to about seven stages; the number and the conversion rate from the previous stage are printed on each band.
- Two funnels side by side for a before-and-after or an A/B comparison of the same stages.
- Excels at: naming the leaky stage; it is a sorted bar chart with a familiar silhouette.

## When not to use

- Stages that are not nested (users can skip or re-enter): the funnel implies containment that does not exist; use a `sankey` for real paths.
- Width read as a symmetric shape: the centred bands are twice as hard to compare as left-aligned bars (position is lost); for an analytical audience use a horizontal `bar` with conversion labels.
- Many stages or several series: bands become thin and the silhouette meaningless.
- Smoothed or curved "funnel" outlines and 3D cones: they encode nothing; refuse.
- Small absolute drops that matter: the funnel shows relative width; print the percentages or use a bar of drop-off per stage.

## Substitutes

- Analytical audience: horizontal `bar` sorted by stage with conversion labels (the funnel's honest form).
- Real paths with branching and re-entry: `sankey`; categorical cohorts across stages: `alluvial`.
- Signed steps from a start total to an end total: `waterfall`.
- Conversion rate over time: `line`.

## Evidence

- No perception study supports the centred silhouette; the data is an ordered bar chart and reads best as one (Cleveland and McGill 1984 position over length). `low`: the form is convention in business intelligence, and guides (Data Visualisation Catalogue, From Data to Viz) note that funnels are bars with a costume.
- Franconeri et al. 2021: put the comparison readers must make on an aligned edge; a funnel aligns nothing but the centre line, so print the numbers.
- Popularity `common`: native in Plotly and ECharts, a plugin in Chart.js, absent from Vega-Lite and Mermaid.

## Accessibility

- Print stage name, count and percent-of-previous on every band; colour is decoration here.
- One hue in descending lightness, or a single colour: the stages are ordered, not categories.
- Text alternative: "Funnel chart of <process>: <stage 1> <n>, <stage 2> <n> (<p>% of previous), ..., <last> <n>; the largest drop is at <stage>." The table is the same list with the rates.
- Keep the bands left-labelled with adequate contrast (3:1) rather than text inside narrow bands.

## Build

### mermaid

No Mermaid funnel exists. Render with the plotly target for an interactive page or the vega-lite recipe for an image, then link it; a `flowchart` with counts in the nodes is a schematic alternative for pure text hosts.

### vega-lite

Hand-written: centred bars via `calculate` of `-datum.count / 2` and `datum.count / 2` into `x`/`x2` on a `bar` mark with `y` as the ordinal stage, plus a `text` layer for the counts.

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "funnel.csv"},
 "transform": [{"calculate": "-datum.count / 2", "as": "x0"}, {"calculate": "datum.count / 2", "as": "x1"}],
 "layer": [{"mark": "bar", "encoding": {"x": {"field": "x0", "type": "quantitative", "axis": null}, "x2": {"field": "x1"},
                                        "y": {"field": "stage", "type": "ordinal", "sort": null}}},
           {"mark": "text", "encoding": {"y": {"field": "stage", "type": "ordinal", "sort": null}, "text": {"field": "count"}}}]}
```

`approx`: composed from bars. Drop the `x0` calculation for the left-aligned bar form.

### plotly

`{"type": "funnel", "y": ["Visited", "Cart", "Checkout", "Paid"], "x": [10000, 3200, 1400, 900], "textinfo": "value+percent previous"}`; `funnelarea` gives the stacked-area variant. Hand-written, then `cw.py render --target plotly --in fig.json --out chart.html`.

### chartjs

Hand-written with the community `chartjs-chart-funnel` plugin (`type: "funnel"`), or floating bars (`[low, high]` data per stage) on a horizontal `bar` chart for the same silhouette. `approx`.

### matplotlib

Hand-written: `ax.barh(stages, counts, left=-counts / 2, color="#0072B2")` for a centred funnel (or `ax.barh(stages, counts)` for the honest bar), `ax.invert_yaxis()`, `ax.bar_label` with the counts and rates, x axis hidden. Render with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
