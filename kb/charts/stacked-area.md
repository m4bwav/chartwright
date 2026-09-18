---
name: Stacked area chart
slug: stacked-area
aliases: [stacked area graph, cumulative area chart, 100% stacked area, layered area]
family: change-over-time
also: [part-to-whole]
question: How does a total change over time, and how do its parts contribute?
shapes: ["time,q*n", "time,n,q"]
goals: [stacked area, composition over time, parts of total, contribution, breakdown over time, share over time, segments, total and parts]
max_series: 4
max_categories: 0
evidence: medium
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: native
  matplotlib: native
  terminal: none
  echarts: native
  pptx: native
  quickchart: none
  xlsx: native
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/stacked-column-charts, https://www.data-to-viz.com/caveat/stacking.html, https://vega.github.io/vega-lite/docs/stack.html]
---

# Stacked area chart

## When to use

- A total made of a few parts (up to 4) over many periods, where the reader needs the total first and the composition second (energy by source, revenue by product line).
- The part that matters most sits on the baseline, so its own shape is read on a common scale.
- Many periods (months over years): stacked columns would crowd, the area version stays smooth.
- The 100 percent variant when only shares matter and the total is not interesting.
- Excels at: showing the total's shape and one baseline component accurately at the same time.

## When not to use

- More than about 4 parts: middle layers become unreadable ribbons (Financial Times: "seeing change in components can be very difficult").
- The question is about a middle or top component: its baseline wobbles with everything below it; use `line` per part or `small-multiples`.
- Parts that are not additive (rates, averages, percentages of different bases): stacking invents a meaningless total.
- Negative values: stacking breaks; use `diverging-bar` per period or lines.
- Few periods (2 to 6): `stacked-bar` labels better.
- A log axis: never stack on a log scale.

## Substitutes

- Component shapes matter: `small-multiples` of `line` or `area`, one per part.
- Few periods: `stacked-bar` or `stacked-bar-100`.
- Shares over time with many parts: `line` of each part's share.
- Many parts, aesthetic overview, no precise reading: `streamgraph`.
- One series only: `area`.

## Evidence

- Only the baseline layer is position on a common scale; every other layer is a length judgment between two curves, the second-tier task of Cleveland and McGill 1984, and one made harder by non-aligned baselines. Datawrapper (Muth, February 2025) documents readers failing to compare non-baseline segments and recommends small multiples or split charts. One replicated principle plus strong practitioner consensus: `medium`.
- Ordering: put the most important or most stable part at the bottom; sort the rest by size or by a meaningful order and keep that order in the legend (Vega-Lite 6 aligns stack order with the colour domain).
- The total's top edge is read accurately; label the total at the right end.

## Accessibility

- Four colours at most, adjacent layers clearly different in lightness, plus direct labels inside or at the right end of each layer; a legend alone forces slow lookups.
- Draw a thin separator line between layers so they read in greyscale.
- Text alternative: "Stacked area chart of <total> by <part> from <start> to <end>; total rose from A to B; <part> grew from X percent to Y percent of the total."
- Provide the table, since middle layers cannot be read to a number from the picture.

## Build

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "energy.csv"},
 "mark": "area",
 "encoding": {"x": {"field": "year", "type": "temporal"},
              "y": {"field": "twh", "type": "quantitative", "stack": "zero"},
              "color": {"field": "source", "type": "nominal"}}}
```

`cw.py build --chart stacked-area --target vega-lite --data energy.csv --x year --y twh --series source [--html]`. `"stack": "normalize"` gives the 100 percent version; `"order"` encoding controls which part sits on the baseline.

### plotly

One `{"type": "scatter", "mode": "lines", "stackgroup": "one", "name": ..., "x": [...], "y": [...]}` trace per part; `"groupnorm": "percent"` on the first trace for 100 percent. `cw.py build --chart stacked-area --target plotly --data energy.csv --x year --y twh --series source --html`.

### chartjs

`type: "line"` with one dataset per part, each `fill: "-1"` (first dataset `fill: "origin"`), and `options.scales.y.stacked = true`. Hand-written: `cw.py build` has no stacked-area builder for Chart.js.

### matplotlib

`ax.stackplot(years, *[series[p] for p in parts], labels=parts)`; for 100 percent divide each column by the total first. Hand-written from this recipe (no builder), then `cw.py render --target matplotlib --in chart.py --out chart.png`.

Markdown hosts: Mermaid has no area or stacked mark; render the vega-lite spec to SVG (`cw.py render --target vega-lite --in chart.vl.json --out chart.svg`) and link it.

### echarts

`cw.py build --chart stacked-area --target echarts --data file.csv --x <x> --y <y> [--series <s>] --html` writes the option and page.

### pptx

`cw.py build --chart stacked-area --target pptx --data file.csv --x <x> --y <y> [--series <s>] --out chart.py --png chart.pptx` then `cw.py render --target pptx --in chart.py --out chart.pptx` (editable native chart).

### xlsx

`cw.py build --chart stacked-area --target xlsx --data file.csv --x <x> --y <y> [--series <s>] --out chart.py --png chart.xlsx` then `cw.py render --target xlsx --in chart.py --out chart.xlsx` (data sheet plus editable chart).

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
