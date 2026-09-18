---
name: Dot plot
slug: dot-plot
aliases: [Cleveland dot plot, dot chart, point plot, dot strip plot, categorical dot plot]
family: magnitude
also: [ranking, distribution, deviation]
question: What is each category's value, and how do a few values per category compare, when the baseline need not be zero?
shapes: ["n,q", "n,q+", "n,q*n", "o,q"]
goals: [magnitude, compare, rank, ranking, values close together, no zero baseline, many categories, per category, precise, position, dot]
max_series: 4
max_categories: 40
evidence: high
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: approx
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/chart-types-guide, https://vega.github.io/vega-lite/examples/, https://journals.sagepub.com/doi/10.1177/15291006211051956]
---

# Dot plot

## When to use

- One value per category, sorted, when the values are close together or far from zero: the dot's position on the axis carries the value, so the axis may start where the data starts (say so in the axis label).
- Two to four values per category (regions in 2020, 2023, 2026; min, median, max) as different markers on the same row: the reader compares positions along one scale.
- Many categories (up to about 40 rows in an image): dots need less vertical room than bars and no visual weight competes with the labels.
- Replacing a `grouped-bar` that has more than three series, or a bar whose zero baseline would squash the differences.
- Excels at: precise position reading on a common scale, the most accurate encoding (Cleveland and McGill 1984), with the least ink.

## When not to use

- A general audience that expects amounts: bars from zero communicate "how much" more directly; a dot plot reads as "where".
- Values that must sum or be compared as lengths: dots do not show magnitude relative to zero unless the axis starts there.
- Exactly two values per category whose gap is the point: connect them, which is a `dumbbell`.
- Many values per category forming a distribution: that is a `strip` or `beeswarm` (jittered), not a dot plot with a few markers.
- More than about 4 series on one row: the markers overlap; facet or switch to a `heatmap`.
- Continuous time on the category axis: use a `line`.

## Substitutes

- Amount from zero, few categories: `bar`.
- Same data with a thin stem to zero for readers who want a bar: `lollipop`.
- Two endpoints connected: `dumbbell`.
- Two periods with rank change: `slope`.
- Many values per category: `strip`, `beeswarm`, or `boxplot`.
- Many series across many categories: `heatmap` or `small-multiples`.
- Exact numbers: `table`.

## Evidence

- Cleveland 1984 proposed the dot plot as the perceptually superior replacement for bars because it uses position on a common scale, the top of the Cleveland and McGill 1984 ranking, replicated by Heer and Bostock 2010; hence `high`.
- Because position rather than length is read, a non-zero axis does not distort (unlike bars), which the FT Visual Vocabulary notes for lollipops and dot strip plots; the axis still needs a visible start value.
- Franconeri et al. 2021: aligned marks on a shared axis make each pairwise comparison a single glance; sorting rows by value turns the whole chart into a readable ranking.
- Datawrapper (Muth 2025) recommends dot plots or tables for extensive datasets where bars become a wall.

## Accessibility

- Markers at least 8 px in diameter, distinct shapes per series (circle, square, triangle) as well as colour.
- Light horizontal guide lines from label to dot so the eye can follow a row across 30 or more rows.
- Label the axis start explicitly when it is not zero ("axis starts at 60").
- Text alternative: "Dot plot of <measure> by <category>, sorted; <top> highest at <value>, <bottom> lowest at <value>; <series B> exceeds <series A> in <n> categories." Offer the table.
- Legend for 2 or more series with the same shapes as the markers; 3:1 contrast on marker fills.

## Build

### mermaid

`image`: Mermaid has no scatter or point mark, so render the vega-lite recipe to SVG (`cw.py render --target vega-lite --in chart.vl.json --out chart.svg`) and link it with `![dot plot](chart.svg)`.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "rates.csv"},
 "mark": {"type": "point", "filled": true, "size": 80},
 "encoding": {"y": {"field": "country", "type": "nominal", "sort": "-x"},
              "x": {"field": "rate", "type": "quantitative", "scale": {"zero": false}},
              "color": {"field": "year", "type": "nominal"},
              "shape": {"field": "year", "type": "nominal"}}}
```

`cw.py build --chart dot --target vega-lite --data rates.csv --x country --y rate [--series year] [--html]` (the builder's slug is `dot`). Add a `rule` layer with `"x": {"aggregate": "min"}`, `"x2": {"aggregate": "max"}` per row for a range spine; drop `color` and `shape` for a single series.

### plotly

`{"type": "scatter", "mode": "markers", "marker": {"size": 10, "symbol": "circle"}, "x": rates, "y": countries, "name": "2026"}` per series, `layout.yaxis.categoryorder = "total ascending"`, `layout.xaxis.rangemode = "normal"`. No builder support; hand-write from this recipe and open with `cw.py render --target plotly --in fig.json --out chart.html`.

### chartjs

`approx`: a `scatter` dataset needs numeric axes, so map categories to integers and label them through `scales.y.ticks.callback`, or use `type: "bar"` with `barThickness: 0` plus `pointStyle` overlays. Simpler: `{"type": "line", "data": {"labels": countries, "datasets": [{"data": rates, "showLine": false, "pointRadius": 6}]}, "options": {"indexAxis": "y"}}`, which is a line chart with the line hidden. Hand-written.

### matplotlib

`ax.scatter(values, categories, s=60, label=name)` per series on data sorted by the primary series, `ax.hlines(categories, xmin, xmax, color="0.8", zorder=0)` for guide lines, `ax.set_xlim(left=min_value * 0.95)` when not starting at zero. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. `cw.py build` knows this chart as `dot`.
