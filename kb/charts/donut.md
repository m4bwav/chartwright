---
name: Donut chart
slug: donut
aliases: [doughnut chart, ring chart, hollow pie]
family: part-to-whole
also: [single-value]
question: How big is each slice of one whole, with a headline figure in the centre?
shapes: ["n,q"]
goals: [share, percentage, proportion, part to whole, breakdown, dashboard, headline number, ring, portion, of the total]
max_series: 0
max_categories: 5
evidence: medium
popularity: core
status: stable
support:
  mermaid: approx
  vega-lite: native
  plotly: native
  chartjs: native
  matplotlib: native
  terminal: none
  echarts: native
  pptx: native
  quickchart: native
  xlsx: native
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://eagereyes.org/pie-charts, https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/chart-types-guide, https://vega.github.io/vega-lite/docs/arc.html]
---

# Donut chart

## When to use

- Exactly the pie's cases (one whole, at most five parts, big differences, sum-of-slices questions) when the centre should carry the total, the headline share, or a label: "58% mobile" in the hole.
- Dashboards and KPI rows where a compact ring with one number reads as a single-value tile with context.
- A single-part donut (one slice against the rest) as a progress ring for a share reached: it is a rounded stat tile, not a gauge.
- Excels at: one number plus its composition in the space of a tile; the hole gives the headline a home the pie lacks (FT).

## When not to use

- Everything that rules out a pie: more than five slices, similar slices, several donuts side by side, change over time, parts that do not sum to a whole.
- A thin ring: readers use arc length, so a ring so thin that arcs are hard to compare loses the little accuracy the form has; keep the hole at about half the radius.
- Nested rings for hierarchy or for several periods: that is a `sunburst` misused; use `stacked-bar-100` instead.
- Progress towards a target with thresholds: a `bullet` shows target and bands more accurately than a ring.

## Substitutes

- No headline number needed: `pie` (identical accuracy).
- Ranking of parts: sorted `bar`; several wholes: `stacked-bar-100`.
- Whole-number shares for the public: `waffle`.
- One number with a delta and a trend: `stat-tile`; progress to a target: `bullet`.
- Nested categories: `sunburst`.

## Evidence

- Donuts read as accurately as pies because readers use arc length and area rather than angle, so removing the centre costs nothing (Skau and Kosara 2016). `medium` for the same reason as the pie: one focused study plus consensus.
- Angle and area still rank below position and length (Cleveland and McGill 1984), so the donut inherits the pie's limits: rough shares, not precise comparison.
- FT Visual Vocabulary: the hole is a good place for the total or the key figure; Datawrapper 2025 lists donuts among the share charts with the same caveats as pies.

## Accessibility

- Label slices directly with name and percent; the centre text is the headline, in the largest type on the chart.
- Five colour-blind-safe hues at most, lightness steps between neighbours, white separators.
- Text alternative: "Donut chart of <measure> by <category>, total <N>: <A> <p>%, <B> <p>%..." The centre value must also be in the alt text, not only drawn.
- Contrast for the centre text and the ring segments at 3:1 or better against the background.

## Build

### mermaid

Mermaid `pie` has no hole, so `cw.py build --chart donut --target mermaid --data traffic.csv --x device --y visits` emits a pie (`approx`); put the headline number in the title (`title Traffic by device (12.4k visits)`).

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "traffic.csv"},
 "layer": [{"mark": {"type": "arc", "innerRadius": 60},
            "encoding": {"theta": {"field": "visits", "type": "quantitative"}, "color": {"field": "device", "type": "nominal"}}},
           {"mark": {"type": "text", "fontSize": 24}, "encoding": {"text": {"value": "58% mobile"}}}]}
```

`cw.py build --chart donut --target vega-lite --data traffic.csv --x device --y visits [--html]` emits the arc with `innerRadius: 60`; add the text layer by hand for the centre figure.

### plotly

`{"type": "pie", "hole": 0.5, "labels": [...], "values": [...], "sort": false, "textinfo": "label+percent"}` and a `layout.annotations` entry with `showarrow: false` for the centre. `cw.py build --chart donut --target plotly ... --html`.

### chartjs

`{"type": "doughnut", "data": {"labels": [...], "datasets": [{"data": [...]}]}, "options": {"cutout": "50%"}}`; centre text needs a small inline plugin (`afterDraw` writing on the canvas). `cw.py build --chart donut --target chartjs ... --html`.

### matplotlib

`ax.pie(values, labels=names, autopct="%1.0f%%", startangle=90, wedgeprops=dict(width=0.4)); ax.text(0, 0, "58%\nmobile", ha="center", va="center")`. `cw.py build --chart donut --target matplotlib --data traffic.csv --x device --y visits --out chart.py --png chart.png` then `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

`cw.py build --chart donut --target echarts --data file.csv --x <x> --y <y> [--series <s>] --html` writes the option and page.

### pptx

`cw.py build --chart donut --target pptx --data file.csv --x <x> --y <y> [--series <s>] --out chart.py --png chart.pptx` then `cw.py render --target pptx --in chart.py --out chart.pptx` (editable native chart).

### quickchart

`cw.py build --chart donut --target quickchart --data file.csv --x <x> --y <y> [--series <s>]` prints a markdown image line whose URL renders the chart (data is public in the URL).

### xlsx

`cw.py build --chart donut --target xlsx --data file.csv --x <x> --y <y> [--series <s>] --out chart.py --png chart.xlsx` then `cw.py render --target xlsx --in chart.py --out chart.xlsx` (data sheet plus editable chart).

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
