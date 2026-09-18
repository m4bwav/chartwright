---
name: Bubble chart
slug: bubble
aliases: [bubble plot, sized scatter, three-variable scatter, Gapminder chart]
family: correlation
also: [magnitude, distribution]
question: How do two numeric variables relate, with a third rough magnitude shown by size?
shapes: ["q,q,q", "q,q,q,n", "q,q,q,text"]
goals: [correlation, three variables, size, magnitude, weighted, population, versus, relationship, bubble]
max_series: 4
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
  terminal: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.semanticscholar.org/paper/55d3281f6b34c50df975b7261044689bf73ec610, https://vega.github.io/vega-lite/docs/circle.html, https://plotly.com/python/bubble-charts/, https://www.chartjs.org/docs/latest/charts/bubble.html, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html]
---

# Bubble chart

## When to use

- A `scatter` where a third variable is worth showing roughly: population, revenue, sample size, weight.
- The third variable's role is context ("the big ones cluster here"), not a value to be read.
- Tens to a few hundred bubbles; enough room that most do not overlap.
- Gapminder-style stories: income against life expectancy sized by population, coloured by region.
- Excels at: adding weight to a relationship so the reader does not treat a tiny unit and a huge one as equal points.

## When not to use

- Reading size precisely: circular area is one of the worst-read encodings (Heer and Bostock 2010); if the third value matters, put it on an axis or in a `small-multiples` panel.
- Scaling radius instead of area: a value twice as big then looks four times as big. Always scale area.
- Many overlapping bubbles: the small ones vanish under the big ones; sort so small bubbles draw last, use transparency, or drop to `scatter`.
- Negative or zero values for size: no honest circle exists; use colour instead.
- Bubbles as a "map" with no meaningful axes (packed bubbles): that is `circle-packing` and a `bar` reads better.

## Substitutes

- Third variable only roughly needed: colour ramp on a `scatter`.
- Third variable read precisely: `scatter` per level in `small-multiples`, or a `table`.
- Relationship over time: `connected-scatter`; per-unit change: animated bubbles are a `slope` in disguise.
- Many variable pairs: `splom`.
- Large n: `hexbin`.

## Evidence

- The x and y positions are read as accurately as in a `scatter` (Cleveland and McGill 1984). The size channel is circular area, ranked below length and rectangular area by Heer and Bostock 2010, with roughly 20 percent error in size ratio judgements: `medium`, honest when size is a rough cue.
- FT caveat: like a scatter but the third variable's scale must be explained; a size legend with three reference circles is the standard fix.

## Accessibility

- Size legend with two or three labelled reference circles; state "area proportional to <variable>".
- Colour groups also distinguished by outline or label; bubbles at 40 to 60 percent opacity with a darker 1 px outline.
- Minimum bubble diameter 4 px so the smallest units remain visible.
- Text alternative: "Bubble chart of <y> against <x>, bubbles sized by <z>; large <units> sit at the top right; <unit> is the largest at <z>."

## Build

### mermaid

Not drawable in Mermaid. Render with the vega-lite target and link the image.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "countries.csv"},
 "mark": {"type": "circle", "opacity": 0.6, "stroke": "#333", "strokeWidth": 0.5},
 "encoding": {"x": {"field": "income", "type": "quantitative", "scale": {"type": "log"}},
              "y": {"field": "life_expectancy", "type": "quantitative", "scale": {"zero": false}},
              "size": {"field": "population", "type": "quantitative", "scale": {"range": [16, 2000]}},
              "color": {"field": "region", "type": "nominal"}}}
```

`cw.py build --chart bubble --target vega-lite --data countries.csv --x income --y life_expectancy --size population [--series region] [--html]`. `size` maps to area by default in Vega-Lite, which is the honest scaling; `"order": {"field": "population", "sort": "descending"}` draws big bubbles first.

### plotly

`{"type": "scatter", "mode": "markers", "marker": {"size": pop, "sizemode": "area", "sizeref": 2 * max(pop) / 40 ** 2, "sizemin": 4}}`; `px.scatter(df, x=..., y=..., size="population", color="region", size_max=40)` in Python. `cw.py build --chart bubble --target plotly --data countries.csv --x income --y life_expectancy --size population --html`.

### chartjs

`{"type": "bubble", "data": {"datasets": [{"label": "Europe", "data": [{"x": 1, "y": 2, "r": 12}]}]}}`: `r` is a radius in pixels, so compute `r = k * sqrt(value)` yourself to keep area proportional. `cw.py build --chart bubble --target chartjs --data countries.csv --x income --y life_expectancy --size population --html`.

### matplotlib

`ax.scatter(x, y, s=area_scale * pop / pop.max(), alpha=0.6, edgecolor="k", linewidth=0.5)`: `s` is area in points squared, so pass the value scaled linearly, not its square root. Legend circles via `ax.scatter([], [], s=...)` with labels. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
