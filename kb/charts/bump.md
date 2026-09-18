---
name: Bump chart
slug: bump
aliases: [rank chart, ranking over time, bumps chart, position chart]
family: change-over-time
also: [ranking]
question: How did the rank order of a set of entities change across several periods?
shapes: ["time,n,q", "time,q*n", "o,q*n"]
goals: [bump, rank over time, league table, standings, position, who leads, ranking changes, top ten over years, season, overtaken]
max_series: 10
max_categories: 0
evidence: medium
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
  docx: image
  gsheets: image
  observable-plot: approx
  d2: none
  plantuml: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/bump.html, https://vega.github.io/vega-lite/docs/window.html, https://github.com/davidsjoberg/ggbump]
---

# Bump chart

## When to use

- A ranking recomputed each period (league standings by week, top 10 languages by year, browser share rank) and the story is who overtook whom.
- Up to about 10 entities over 5 to 20 periods; each entity is one line from its rank at the first period to its rank at the last.
- The magnitudes behind the ranks are unimportant or incomparable across periods, so rank alone is the honest measure.
- Excels at: crossing lines make every overtaking event visible; a flat line says "held its place".

## When not to use

- Magnitude matters: rank 1 and rank 2 may differ by a hair or by a mile; a bump hides it. Use `line` of the values, or a bump with line width by value.
- Only two periods: `slope`.
- More than about 10 entities: the crossings become a tangle; show the top N and grey the rest, or use `small-multiples`.
- Entities that enter and leave the ranking: broken lines confuse; state the rule for missing periods.
- Readers who need the value in a period: pair it with a table.

## Substitutes

- Two periods: `slope`.
- Values rather than ranks over time: `line` (few entities) or `small-multiples`.
- Share of a total by entity over time: `stacked-area` or `streamgraph`.
- A single period's ranking: `bar` sorted by value.
- Rank plus magnitude in one picture: a ribbon bump (area whose width is the value), drawn by hand in Vega or D3.

## Evidence

- Rank is an ordinal position on a common scale, so the reading of each line is accurate (Cleveland and McGill 1984), but the equal spacing of ranks discards the values, which practitioner guides flag as the main caveat (Financial Times Visual Vocabulary; From Data to Viz). No dedicated perception study: `medium`.
- Crossing detection is a fast global feature (Franconeri et al. 2021), which is why overtakes read instantly.
- Rank 1 goes at the top: invert the y axis and label it "rank".

## Accessibility

- Label every line at its right end (and left end when space allows); a colour legend for 10 entities is not readable.
- Highlight the entities in the story with saturated colour and grey the rest; add markers at each period so screen readers and greyscale users can follow crossings.
- Text alternative: "Bump chart of the rank of N entities from <start> to <end>; <entity> moved from rank A to rank B, overtaking <entity> in <period>."
- Provide the rank table.

## Build

### vega-lite

`cw.py build --chart bump --target vega-lite --data ranks.csv --x period --y rank --series team` (rank 1 at the top, monotone curves, entity labels at the last period).

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "sales.csv"},
 "transform": [{"window": [{"op": "rank", "as": "rank"}], "sort": [{"field": "value", "order": "descending"}], "groupby": ["year"]}],
 "mark": {"type": "line", "point": true},
 "encoding": {"x": {"field": "year", "type": "ordinal"},
              "y": {"field": "rank", "type": "quantitative", "scale": {"reverse": true}, "axis": {"tickMinStep": 1}},
              "color": {"field": "entity", "type": "nominal"}}}
```

Hand-written (no builder). `approx` because the rank comes from a window transform and end labels need an extra text layer; the rendered result is a proper bump chart.

### plotly

Compute ranks per period in Python (`df.groupby("year")["value"].rank(ascending=False)`), then one `{"type": "scatter", "mode": "lines+markers", ...}` trace per entity and `layout.yaxis = {"autorange": "reversed", "dtick": 1}`. Hand-written.

### chartjs

`type: "line"` with one dataset per entity holding precomputed ranks, `options.scales.y = {reverse: true, ticks: {stepSize: 1}}`, `tension: 0.4` for the classic curves. Hand-written.

### matplotlib

`for name, ranks in table.items(): ax.plot(periods, ranks, marker="o", label=name)` then `ax.invert_yaxis()`, `ax.set_yticks(range(1, n + 1))` and end labels with `ax.text`. Hand-written, then `cw.py render --target matplotlib --in chart.py --out chart.png`.

Markdown hosts: Mermaid xychart cannot reverse its y axis or label line ends; render the vega-lite spec to SVG and link it.

### echarts

Hand-written: `line` series per entity over rank on an inverted value axis. See `kb/targets/echarts.md`.

### observable-plot

`Plot.lineY(data, {x, y: "rank", stroke: "team", curve: "bump-x"})` with `y: {reverse: true}` and a text mark for labels.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
