---
name: Lollipop chart
slug: lollipop
aliases: [lollipop plot, stem plot, dot and stem chart, needle chart]
family: ranking
also: [magnitude]
question: How do many categories rank, shown with less ink than bars?
shapes: ["n,q", "o,q"]
goals: [ranking, rank, magnitude, compare, many categories, top, lollipop, less ink, sorted, minimal, per category]
max_series: 1
max_categories: 40
evidence: medium
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: approx
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
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/lollipop.html, https://vega.github.io/vega-lite/examples/, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stem.html]
---

# Lollipop chart

## When to use

- A ranked list of one value per category, 15 to 40 categories, where solid bars would form a heavy wall (the "moire" effect From Data to Viz warns about).
- Values are close in magnitude and the reader will read the dot's position, not the stem's length; the stem is a visual guide back to the label.
- The same data as a `bar`, in a report that already has many bars and wants a lighter variant.
- Sorted always, unless the categories carry their own order.
- Excels at: ranking many items compactly while keeping a visual link between label and value.

## When not to use

- Few categories (under about 8): a plain `bar` is clearer and expected.
- Precise length comparison matters: stems are thin and readers compare dot positions; if amounts from zero are the message, use bars.
- Several series per category: overlapping stems are unreadable; use a `dot-plot` (dots only) or `dumbbell` for two.
- Time on the category axis: a `line` or `column`.
- An axis that does not start at zero while the stems still reach the axis: the stem then implies a length that is false; either start at zero or drop the stems (a `dot-plot`).

## Substitutes

- Few categories, amounts from zero: `bar`.
- Non-zero baseline or several series: `dot-plot`.
- Two values per category: `dumbbell`.
- Values above and below a reference: `diverging-bar` (a diverging lollipop is the same recipe with a rule at zero).
- Two periods, many categories: `slope`.

## Evidence

- The dot is read as position on a common scale (top of Cleveland and McGill 1984), and the stem adds length from zero; the encoding is therefore as sound as a bar. `medium` rather than `high` because the lollipop itself has no dedicated perception study; the rating rests on the encoding it shares with bars and dots plus practitioner consensus.
- FT Visual Vocabulary: lollipops draw attention to the value and "do not HAVE to start at zero" when the reader reads the dot; but a stem to a non-zero axis still misleads, so this knowledge base keeps stems at zero.
- From Data to Viz recommends it over bars when there are many categories with similar values, and always sorted.
- Rising: native in ggplot2 recipes, Observable Plot, Datawrapper's dot plot, and Vega-Lite (rule plus point layers).

## Accessibility

- Dots at least 8 px, stems 2 px, both in one colour at 3:1 contrast; highlight one category with a second colour and a label, not colour alone.
- Value labels beside each dot when 25 or fewer rows; otherwise a light grid at round numbers.
- Text alternative: "Lollipop chart ranking <n> <categories> by <measure>; <top> leads at <value>, <bottom> lowest at <value>." Offer the table.
- Sort direction stated in the title or subtitle ("largest first").

## Build

### mermaid

`image`: Mermaid has no point or rule mark. Render the vega-lite recipe (`cw.py render --target vega-lite --in chart.vl.json --out chart.svg`) and link the image; if the chart must be Mermaid, draw a `bar` instead.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "scores.csv"},
 "encoding": {"y": {"field": "team", "type": "nominal", "sort": "-x"},
              "x": {"field": "score", "type": "quantitative"}},
 "layer": [{"mark": {"type": "rule", "strokeWidth": 2}, "encoding": {"x": {"datum": 0}, "x2": {"field": "score"}}},
           {"mark": {"type": "point", "filled": true, "size": 90}}]}
```

`cw.py build --chart lollipop --target vega-lite --data scores.csv --x team --y score [--html]`. The rule layer draws the stem from 0 to the value; the point layer draws the head. Add a `text` layer with `"dx": 8` and `"align": "left"` for value labels.

### plotly

`approx`: two traces, a `bar` with `width: 0.05` (the stem) and a `scatter` with `mode: "markers"`, `marker.size: 12` (the head), both `orientation: "h"` on the same category axis, plus `showlegend: false`. Hand-written; the stem is a very thin bar, not a true rule.

### chartjs

`approx`: a floating-free `bar` dataset with `barThickness: 2` for stems and a `line` dataset with `showLine: false`, `pointRadius: 6` for heads, `indexAxis: "y"`. Hand-written mixed chart.

### matplotlib

`ax.hlines(categories, 0, values, color="C0", linewidth=2); ax.plot(values, categories, "o", markersize=8, color="C0")` on data sorted ascending, or `ax.stem(values)` for a vertical variant. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: `bar` with `barWidth: 2` plus a `scatter` series at the tips. See `kb/targets/echarts.md`.

### pptx

Approximate: a clustered bar with narrow gap plus an XY_SCATTER overlay is not possible in one chart; use two shapes or a PNG.

### quickchart

Approximate: bar plus scatter mixed datasets; write the Chart.js config by hand and URL-encode it (see `kb/targets/quickchart.md`).

### xlsx

Approximate: not possible in one native chart; use a PNG.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
