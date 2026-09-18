---
name: Area chart
slug: area
aliases: [filled line chart, area graph, mountain chart]
family: change-over-time
also: [magnitude]
question: How does the volume of one measure change over time?
shapes: ["time,q", "o,q"]
goals: [area, volume, total over time, cumulative, filled, magnitude over time, traffic, revenue over time, trend]
max_series: 1
max_categories: 0
evidence: medium
popularity: core
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: native
  matplotlib: native
  terminal: native
  echarts: native
  pptx: native
  quickchart: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/chart-types-guide, https://www.data-to-viz.com/graph/area.html, https://vega.github.io/vega-lite/docs/area.html]
---

# Area chart

## When to use

- One series over time where the quantity is a volume or a total (revenue, traffic, stock of something) and the fill says "this much".
- Many periods: the fill keeps a long series readable where columns would crowd.
- A cumulative measure (total signups to date) where the growing mass is the story.
- Emphasising magnitude alongside trend: the reader sees both the shape and the size.
- Excels at: giving weight to a single trend; the filled shape reads as "amount" where a bare line reads as "level".

## When not to use

- Several series: overlapping fills occlude each other and stacked fills change the reading (see `stacked-area`); for 2 or more independent series use `line`.
- A non-zero baseline: the fill encodes area from the baseline, so a truncated axis lies about size. If the data live far from zero, use `line`.
- Rates, ratios, temperatures, indices: they are levels, not volumes; a fill suggests accumulation that is not there.
- A log axis: area under a log scale is meaningless.
- Negative values crossing zero: the fill flips sides and confuses; use `column` or a `diverging-bar` per period.

## Substitutes

- Level rather than volume, or more than one series: `line`.
- Parts of a total over time: `stacked-area`; shares only: `stacked-bar-100` per period.
- Few periods: `column`.
- Values that hold between changes: `step`.
- Uncertainty around a central line: `range-band`.
- Many components with an aesthetic goal: `streamgraph`.

## Evidence

- The top edge is position over time (the accurate encoding of Cleveland and McGill 1984); the fill adds an area cue that is read less accurately but supports the "how much" impression. One series with a zero baseline is well supported by practitioner guidance (Financial Times Visual Vocabulary; From Data to Viz) rather than by a dedicated perception study, hence `medium`.
- Overlapping semi-transparent areas are the classic misuse (From Data to Viz caveats): occlusion and colour mixing make series unreadable.
- Aspect ratio matters as for lines (Cleveland 1993): bank the top edge to about 45 degrees.

## Accessibility

- Fill at about 30 to 50 percent opacity with a solid 2 px top line in the same hue so the shape survives low contrast and greyscale print.
- Label the series name directly at the right end; no legend is needed for one series.
- Text alternative: "Area chart of <measure> from <start> to <end>; it grew from A to B, peaking in <period>."
- Contrast: the top line must reach 3:1 against the background even when the fill is pale.

## Build

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "traffic.csv"},
 "mark": {"type": "area", "line": true, "opacity": 0.4},
 "encoding": {"x": {"field": "date", "type": "temporal"}, "y": {"field": "visits", "type": "quantitative"}}}
```

`cw.py build --chart area --target vega-lite --data traffic.csv --x date --y visits [--html]`. Keep the y scale starting at zero (the default for area).

### plotly

`{"type": "scatter", "mode": "lines", "fill": "tozeroy", "x": [...], "y": [...]}`. `cw.py build --chart area --target plotly --data traffic.csv --x date --y visits --html`.

### chartjs

`{"type": "line", "data": {"datasets": [{"label": "visits", "data": [...], "fill": "origin", "tension": 0.2}]}}`; `fill: "origin"` is the area. `cw.py build --chart area --target chartjs ... --html`.

### matplotlib

`ax.fill_between(dates, values, 0, alpha=0.4)` plus `ax.plot(dates, values, linewidth=2)` for the edge; `ax.set_ylim(bottom=0)`. `cw.py build --chart area --target matplotlib --data traffic.csv --x date --y visits --out chart.py --png chart.png` then `cw.py render --target matplotlib --in chart.py --out chart.png`.

Markdown hosts: Mermaid has no area mark (`cw.py build --target mermaid` emits a plain line). Render the vega-lite spec to SVG with `cw.py render --target vega-lite --in chart.vl.json --out chart.svg` and link the image.

### terminal

Same block sparkline as `line` (`cw.py build --chart area --target terminal ...`); the fill is implied.

### echarts

`cw.py build --chart area --target echarts --data file.csv --x <x> --y <y> [--series <s>] --html` writes the option and page.

### pptx

`cw.py build --chart area --target pptx --data file.csv --x <x> --y <y> [--series <s>] --out chart.py --png chart.pptx` then `cw.py render --target pptx --in chart.py --out chart.pptx` (editable native chart).

### quickchart

`cw.py build --chart area --target quickchart --data file.csv --x <x> --y <y> [--series <s>]` prints a markdown image line whose URL renders the chart (data is public in the URL).

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
