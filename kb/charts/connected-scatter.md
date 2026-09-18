---
name: Connected scatterplot
slug: connected-scatter
aliases: [connected scatter, phase plot, trajectory plot, path chart, x-y over time]
family: change-over-time
also: [correlation]
question: How did two measures move together over time, and along what path?
shapes: ["time,q,q"]
goals: [connected scatter, two variables over time, trajectory, path, co-evolve, joint change, inflation and unemployment, phase, dual axis alternative]
max_series: 3
max_categories: 0
evidence: medium
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: native
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/dual-axis-charts, https://vega.github.io/vega-lite/examples/connected_scatterplot.html, https://ieeexplore.ieee.org/document/7192687]
---

# Connected scatterplot

## When to use

- Two measures of one entity over time where the relationship between them is the story (inflation versus unemployment, price versus volume, speed versus altitude).
- The path has a clear direction with few reversals, so arrows and a handful of year labels make it followable.
- A replacement for a dual-axis line chart: the crossing point of two axes is an artefact, the path of a connected scatter is not (Datawrapper dual-axis guidance).
- One to three entities at most, each a labelled path.
- Excels at: showing loops, reversals and regime changes that two separate lines hide.

## When not to use

- General audiences with no time to study it: readers misread direction and speed without annotation (Haroz, Kosara and Franconeri 2016).
- Many time points with a noisy path: the line scribbles over itself; smooth, thin the points, or use two panels.
- The reader must know the value at a specific date: two stacked `line` panels sharing x are faster.
- More than three entities: paths overlap into a tangle.
- The two measures are unrelated in principle: a path invents a relationship.

## Substitutes

- Values by date for two measures: two `line` panels sharing the x axis, or both indexed to 100 on one chart.
- Relationship without time: `scatter`.
- Third measure by size: `bubble` with a path.
- Change between two dates only: `slope` or `dumbbell`.
- Many entities' joint change: `small-multiples` of connected scatters.

## Evidence

- Haroz, Kosara and Franconeri 2016 ("The Connected Scatterplot for Presenting Paired Time Series", TVCG) found the form engaging and roughly as accurate as dual-axis lines for trained readers, but error-prone for direction and for judging correlation without annotation. One study plus consistent practitioner caveats: `medium`.
- Both axes are position on a common scale (Cleveland and McGill 1984), so individual points are read accurately; the cost is in following the sequence.
- The Financial Times Visual Vocabulary recommends it "if the story is the relationship over time" and warns to annotate.

## Accessibility

- Arrowheads or a lightness gradient along the path to encode direction; label the start, the end and every turning point with its date.
- Mark the points with dots so that the sampling is visible; direct-label each entity's path.
- Text alternative: "Connected scatterplot of <x measure> against <y measure> from <start> to <end>; the path moves from (a, b) to (c, d), turning in <period>."
- Contrast 3:1 for the path; a lightness gradient must keep its darkest end at 3:1 and its lightest at least 1.5:1 with a solid outline.

## Build

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "phillips.csv"},
 "layer": [
  {"mark": {"type": "line", "point": true}, "encoding": {"order": {"field": "year"}}},
  {"mark": {"type": "text", "dy": -8}, "encoding": {"text": {"field": "year"}}}],
 "encoding": {"x": {"field": "unemployment", "type": "quantitative"}, "y": {"field": "inflation", "type": "quantitative"}}}
```

Hand-written from the gallery example (`connected_scatterplot`). The `"order"` encoding is what makes it a path rather than a sorted line.

### plotly

`{"type": "scatter", "mode": "lines+markers+text", "x": [...], "y": [...], "text": years, "textposition": "top center"}` with the rows in time order; add `layout.annotations` with `arrowhead` for direction. Hand-written.

### chartjs

`{"type": "scatter", "data": {"datasets": [{"data": [{"x": u, "y": i}, ...], "showLine": true}]}}` in time order; year labels through `chartjs-plugin-datalabels` or a caption. Hand-written.

### matplotlib

`ax.plot(x, y, "-o", linewidth=1.5)` on time-ordered data, then `for xi, yi, yr in zip(x, y, years): ax.annotate(yr, (xi, yi), textcoords="offset points", xytext=(4, 4))`; arrows via `ax.annotate("", xy=(x[i+1], y[i+1]), xytext=(x[i], y[i]), arrowprops={"arrowstyle": "->"})`. Hand-written, then `cw.py render --target matplotlib --in chart.py --out chart.png`.

Markdown hosts: Mermaid has no scatter mark; render the vega-lite spec to SVG and link it.

### echarts

Hand-written: `line` series on two value axes with `symbol` and per-point labels. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
