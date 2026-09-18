---
name: Dumbbell chart
slug: dumbbell
aliases: [range plot, connected dot plot, barbell chart, gap chart, dumbbell plot, arrow plot]
family: deviation
also: [change-over-time, magnitude, ranking]
question: How far apart are two values per category, and which way did each move?
shapes: ["n,q,q", "n,o,q"]
goals: [deviation, gap, difference, before and after, change between, two points, range, from to, min max, moved, between two years, dumbbell]
max_series: 2
max_categories: 30
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
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/chart-types-guide, https://vega.github.io/vega-lite/examples/, https://www.data-to-viz.com/graph/lollipop.html]
---

# Dumbbell chart

## When to use

- Two values per category in the same unit and the gap between them is the story: before and after, men and women, 2016 and 2026, minimum and maximum.
- Up to about 30 categories, sorted by one endpoint or by the size of the gap, depending on the headline.
- The direction of change matters: colour or an arrowhead marks which end is "after".
- Replacing a two-series `grouped-bar` when the absolute amounts matter less than the difference.
- Excels at: showing both endpoints and the gap at once, with each read as position on a common scale.

## When not to use

- More than two points per category: connecting three dots makes a false path; use a `dot-plot` with markers or a `line` per category.
- Values in different units (revenue and headcount): a connecting bar implies a shared scale that does not exist; use two charts.
- Categories where the gap is negligible for most rows: the chart shows nothing; report the few that moved in a `bar` of differences.
- Many periods over time: a `slope` for two or three, a `line` or `bump` for more.
- Readers need the difference as a number: add it as a label or use a `bar` of the differences directly (a `diverging-bar` when signs vary).

## Substitutes

- Two periods with rank crossings to show: `slope`.
- Only the difference matters and it has signs: `diverging-bar`.
- Absolute amounts from zero for both values: `grouped-bar`.
- More than two values per category: `dot-plot`.
- Many periods: `line` or `bump`.
- Uncertainty ranges rather than two measurements: `error-bars` or `range-band`.

## Evidence

- Both endpoints are positions on a common scale, the most accurate encoding (Cleveland and McGill 1984; Heer and Bostock 2010), and the connector's length is a second, redundant cue for the gap. `medium` because the combined form has practitioner consensus (FT, Datawrapper's "range plot", ggalt) rather than a dedicated study.
- Franconeri et al. 2021: the connector makes each row's comparison a single aligned pair, which is the fast kind; sorting by gap turns "which changed most" into a glance.
- Datawrapper (Muth 2025) lists the range plot as the way to show two points per category without the cross-group problem of grouped bars.

## Accessibility

- The two endpoints differ by colour and by shape or fill (filled and hollow circles), with a legend naming both.
- Direction shown by an arrowhead or by a consistent convention stated in the subtitle ("dark dot is 2026").
- Label the gap value at the end of each row when 20 or fewer rows.
- Text alternative: "Dumbbell chart of <measure> in <A> and <B> by <category>; the largest gap is <category> (<value A> to <value B>); <n> categories moved up, <m> down." Offer the table with a difference column.
- Connector at least 2 px and 3:1 contrast; dots at least 8 px.

## Build

### mermaid

`image`: Mermaid has no point or rule marks. Render the vega-lite recipe to SVG and link it; a Mermaid `bar` of the differences is the in-place fallback.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "gap.csv"},
 "encoding": {"y": {"field": "country", "type": "nominal", "sort": {"field": "y2026", "order": "descending"}}},
 "layer": [{"mark": {"type": "rule", "strokeWidth": 2, "color": "#999"},
            "encoding": {"x": {"field": "y2016", "type": "quantitative"}, "x2": {"field": "y2026"}}},
           {"mark": {"type": "point", "filled": true, "size": 90, "color": "#56B4E9"}, "encoding": {"x": {"field": "y2016", "type": "quantitative"}}},
           {"mark": {"type": "point", "filled": true, "size": 90, "color": "#0072B2"}, "encoding": {"x": {"field": "y2026", "type": "quantitative"}}}]}
```

Not in `cw.py build`; hand-write from this recipe with wide data (one column per endpoint). For long data use `"x": {"aggregate": "min"}` and `"x2": {"aggregate": "max"}` on the rule layer and `color` by the period field on the point layer. Render with `cw.py render --target vega-lite --in chart.vl.json --out chart.svg`.

`cw.py build --chart dumbbell --target vega-lite --data file.csv --x category --y value --series period` (two rows per category, one per end) layers a rule between the min and max and a point per end.

### plotly

`approx`: one `scatter` trace per endpoint (`mode: "markers"`) and one `scatter` trace per row (`mode: "lines"`, `x: [a, b]`, `y: [cat, cat]`, `showlegend: false`) for the connectors, or a single `shapes` list in the layout. Hand-written; the connectors are many small traces rather than one mark.

### chartjs

`approx`: a floating `bar` dataset with `data: [[a, b], ...]`, `barThickness: 2`, `indexAxis: "y"` for connectors plus two `line` datasets with `showLine: false` for the endpoint dots. Hand-written mixed chart.

### matplotlib

`ax.hlines(categories, a, b, color="0.6", linewidth=2); ax.plot(a, categories, "o", label="2016"); ax.plot(b, categories, "o", label="2026"); ax.legend()` on rows sorted by `b`. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: two `scatter` series plus `line` series per category. See `kb/targets/echarts.md`.

### pptx

Approximate: a BAR_STACKED with a transparent first series and two scatter markers; simpler as a PNG.

### quickchart

Approximate: floating bars `[low, high]`; write the Chart.js config by hand and URL-encode it (see `kb/targets/quickchart.md`).

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
