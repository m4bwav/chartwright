---
name: Waterfall chart
slug: waterfall
aliases: [bridge chart, cascade chart, flying bricks, walk chart, Mario chart]
family: deviation
also: [part-to-whole, flow, change-over-time]
question: How do successive positive and negative contributions build from a starting total to an ending total?
shapes: ["o,q", "n,q", "time,q"]
goals: [deviation, bridge, walk, from start to end, contributions, breakdown of change, what drove the change, running total, cumulative, reconciliation, profit bridge, variance]
max_series: 1
max_categories: 12
evidence: medium
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: approx
  quickchart: approx
  xlsx: approx
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://vega.github.io/vega-lite/examples/waterfall_chart.html, https://plotly.com/javascript/waterfall-charts/, https://www.storytellingwithdata.com/blog/2020/2/26/what-is-a-waterfall-chart]
---

# Waterfall chart

## When to use

- A starting value, a series of signed contributions, and an ending value, where the order is meaningful: revenue to net profit through costs, headcount from January to December through hires and leavers, a budget variance walk.
- Between 3 and about 12 steps; each floating bar starts where the previous ended, so the reader sees both the size of each step and the running total.
- Finance and operations audiences who know the form (Storytelling with Data lists it in its core set).
- Subtotals at meaningful points (gross margin, operating profit) drawn as full bars from zero.
- Excels at: explaining what drove a change, one contribution at a time, with the totals anchored.

## When not to use

- Contributions with no order or no start and end totals: a sorted `diverging-bar` shows the same signed values more accurately.
- Many small steps: the bars become slivers and the running total wobbles; group into fewer named steps.
- Values on very different scales (a huge start, tiny steps): the steps vanish; chart the steps alone as a `diverging-bar` and print the totals.
- Parts of a whole without signs: a `stacked-bar` or `bar`.
- Floating bars read as lengths from zero by readers who do not know the form: connector lines between bars and a short key fix this.

## Substitutes

- Unordered signed contributions: `diverging-bar`.
- Composition of a total: `stacked-bar` or `treemap`.
- Flow of a quantity between named stages with branching: `sankey`.
- Running total over time: `line` of the cumulative sum, or `column` of the steps with the total as a line.
- Two totals and the gap: `dumbbell`.

## Evidence

- Each step is a length (second tier of Cleveland and McGill 1984, since the bars float), and the running total is position on a common scale (top tier); the start, end and subtotal bars from zero anchor the reading. `medium`: consistent practitioner adoption (FT under deviation and part-to-whole; Storytelling with Data; every BI tool) without a dedicated perception study, and floating bars are known to confuse first-time readers.
- Franconeri et al. 2021: connector lines make each step's start explicit, turning a hard non-aligned comparison into a follow-the-line task.
- Datawrapper and FT both note it should be used only when the sequence and the totals matter; otherwise a bar of the contributions.

## Accessibility

- Increases and decreases in two colour-blind-safe hues (Okabe-Ito bluish green #009E73 and vermilion #D55E00), totals in a neutral dark grey, with a three-entry legend; the sign also printed on each bar.
- Thin connector lines (1 px) from each bar's end to the next bar's start.
- Values printed on or above every bar; the start and end totals in bold.
- Text alternative: "Waterfall chart from <start label> (<value>) to <end label> (<value>); largest increase <step> (+<value>), largest decrease <step> (-<value>)." Offer the table with step, value, and running total columns.
- Category labels horizontal; if they do not fit, run the waterfall vertically (horizontal bars) so labels sit on the left.

## Build

### mermaid

`image`: Mermaid's `xychart` cannot float bars. Render the vega-lite recipe and link the image; the in-place fallback is a Mermaid `bar` of the signed steps with totals in the title.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "bridge.csv"},
 "transform": [{"window": [{"op": "sum", "field": "amount", "as": "end"}]},
               {"calculate": "datum.end - datum.amount", "as": "start"},
               {"calculate": "datum.amount < 0 ? 'decrease' : (datum.total ? 'total' : 'increase')", "as": "kind"}],
 "encoding": {"x": {"field": "step", "type": "ordinal", "sort": null}},
 "layer": [{"mark": "bar", "encoding": {"y": {"field": "start", "type": "quantitative"}, "y2": {"field": "end"},
                                        "color": {"field": "kind", "scale": {"domain": ["increase", "decrease", "total"], "range": ["#009E73", "#D55E00", "#555"]}}}},
           {"mark": {"type": "text", "dy": -6}, "encoding": {"y": {"field": "end", "type": "quantitative"}, "text": {"field": "amount"}}}]}
```

Data rows `step, amount, total` in order, with total rows carrying the full value and `total: true` (for a true total bar from zero set its `start` to 0 with a conditional calculate). The `window` running sum computes the floats; connectors are an extra `rule` layer. Hand-written; render with `cw.py render --target vega-lite --in chart.vl.json --out chart.svg`.

`cw.py build --chart waterfall --target vega-lite --data steps.csv --x step --y change` computes the running total in the spec (window sum) and colours increases blue, decreases red.

### plotly

`{"type": "waterfall", "x": steps, "y": amounts, "measure": ["absolute", "relative", "relative", "total"], "connector": {"line": {"width": 1}}, "increasing": {"marker": {"color": "#009E73"}}, "decreasing": {"marker": {"color": "#D55E00"}}, "totals": {"marker": {"color": "#555"}}, "textposition": "outside", "text": amounts}`. Native trace; hand-written and opened with `cw.py render --target plotly --in fig.json --out chart.html`.

### chartjs

`approx`: floating bars, one dataset with `data: [[start, end], ...]` computed in advance and `backgroundColor` per bar by sign; totals as `[0, value]`. No connectors without a custom plugin. Hand-written.

### matplotlib

Compute `starts = cumsum shifted` and draw `ax.bar(steps, amounts, bottom=starts, color=colours)` with totals as `ax.bar(step, total, bottom=0, color="#555")`, `ax.bar_label` for values, and `ax.plot([i, i + 1], [end_i, end_i], color="0.5", linewidth=1)` per connector. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: stacked `bar` with a transparent base series (`itemStyle.color: "transparent"`). See `kb/targets/echarts.md`.

### pptx

Approximate: COLUMN_STACKED with a transparent base series.

### quickchart

Approximate: floating bars `[start, end]`; write the Chart.js config by hand and URL-encode it (see `kb/targets/quickchart.md`).

### xlsx

Approximate: stacked BarChart with a transparent base series.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
