---
name: Step chart
slug: step
aliases: [step line, stair chart, staircase chart, piecewise constant line]
family: change-over-time
also: [magnitude]
question: When did a level change, and what was it in between?
shapes: ["time,q", "time,q*n"]
goals: [step, level change, interest rate, price change, inventory, status over time, holds until, discrete changes, thresholds, policy rate]
max_series: 4
max_categories: 0
evidence: high
popularity: common
status: stable
support:
  mermaid: approx
  vega-lite: native
  plotly: native
  chartjs: native
  matplotlib: native
  terminal: native
  echarts: native
  pptx: approx
  quickchart: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://vega.github.io/vega-lite/docs/line.html, https://plotly.com/javascript/line-charts/, https://www.chartjs.org/docs/latest/charts/line.html, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.step.html]
---

# Step chart

## When to use

- A value that holds until it is explicitly changed: a policy interest rate, a list price, a tax band, inventory on hand, a service tier, a machine state.
- Event-driven data recorded only when something changes, so that connecting the points with slopes would invent values that never existed.
- Showing the exact moment of a change and the size of the jump: the vertical riser is the event.
- Up to about 4 series with distinct levels (rates of several central banks).
- Excels at: honesty about what happened between observations; the flat tread says "nothing changed here".

## When not to use

- Continuously varying measurements sampled regularly (temperature, traffic): the treads suggest false constancy; use `line`.
- Many changes per pixel: risers merge into a solid block; aggregate or use `line`.
- The reader must compare the timing of many series: risers overlap; use `small-multiples` or a `timeline`.
- Cumulative counts over time: a step is technically right but an `area` or `line` usually reads better unless the individual increments are the point.

## Substitutes

- Continuous change: `line`.
- Few periods with totals: `column`.
- Start and end of states per entity: `timeline` or `gantt`.
- Level and its uncertainty band: `range-band` with step interpolation.
- Cumulative distribution (a step by construction): `ecdf`.

## Evidence

- Same encoding as a line, position over time, hence `high` (Cleveland and McGill 1984; Heer and Bostock 2010).
- The interpolation choice is a matter of correctness, not perception: a step is right when the underlying process is piecewise constant, wrong when it is continuous (Financial Times Visual Vocabulary lists step under change over time for this reason).
- Choose the step direction to match the process: step-after (the new value starts at the change date) is nearly always correct for rates and prices; step-before implies the change was known ahead.

## Accessibility

- Label each level at its right end with the current value; annotate the biggest jump with its date and size.
- Distinguish series by colour and dash pattern; risers of different series can cross, so a legend alone is not enough.
- Text alternative: "Step chart of <measure> from <start> to <end>; it changed N times, from A to B, the largest step on <date>."
- Treads at 2 px; keep risers the same weight so they are not mistaken for gridlines.

## Build

### mermaid

```mermaid
xychart-beta
    title "Policy rate"
    x-axis [2024-01, 2024-03, 2024-03, 2024-09, 2024-09, 2025-01]
    y-axis "%" 0 --> 6
    line [5.25, 5.25, 5.0, 5.0, 4.5, 4.5]
```

`approx`: Mermaid has no step interpolation. `cw.py build --chart step --target mermaid` emits a plain line; to fake the treads duplicate each change date as shown, which forces repeated x labels. For a clean result render an image instead.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "rate.csv"},
 "mark": {"type": "line", "interpolate": "step-after"},
 "encoding": {"x": {"field": "date", "type": "temporal"}, "y": {"field": "rate", "type": "quantitative"}}}
```

`cw.py build --chart step --target vega-lite --data rate.csv --x date --y rate [--html]`. Add `"point": true` to mark the change events.

### plotly

`{"type": "scatter", "mode": "lines", "line": {"shape": "hv"}, "x": [...], "y": [...]}` (`"hv"` is step-after). `cw.py build --chart step --target plotly --data rate.csv --x date --y rate --html`.

### chartjs

`{"type": "line", "data": {"datasets": [{"label": "rate", "data": [...], "stepped": true}]}}` (`stepped: "after"` explicitly, or `"before"` / `"middle"`). `cw.py build --chart step --target chartjs ... --html`.

### matplotlib

`ax.step(dates, values, where="post", linewidth=2)` (`where="post"` is step-after). `cw.py build --chart step --target matplotlib --data rate.csv --x date --y rate --out chart.py --png chart.png` then `cw.py render --target matplotlib --in chart.py --out chart.png`.

### terminal

Same block sparkline as `line` (`cw.py build --chart step --target terminal ...`).

### echarts

`cw.py build --chart step --target echarts --data file.csv --x <x> --y <y> [--series <s>] --html` writes the option and page.

### pptx

Approximate: a LINE chart with the data duplicated at each change.

### quickchart

`cw.py build --chart step --target quickchart --data file.csv --x <x> --y <y> [--series <s>]` prints a markdown image line whose URL renders the chart (data is public in the URL).

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
