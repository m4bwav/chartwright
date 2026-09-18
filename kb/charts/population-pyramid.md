---
name: Population pyramid
slug: population-pyramid
aliases: [age-sex pyramid, age pyramid, back-to-back bar chart, mirrored bar chart, butterfly chart]
family: distribution
also: [deviation, magnitude]
question: How is a population distributed across age bands, and how do two groups (usually sexes) mirror each other?
shapes: ["o,q*n", "o,n,q"]
goals: [distribution, age, sex, population, demographic, age structure, cohort, mirrored, two groups compared, pyramid]
max_series: 2
max_categories: 25
evidence: medium
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: approx
  matplotlib: approx
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://vega.github.io/vega-lite/examples/concat_population_pyramid.html, https://datavizcatalogue.com/methods/population_pyramid.html, https://www.datawrapper.de/charts, https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary]
---

# Population pyramid

## When to use

- Age structure of a population split by sex: the standard demographic chart every reader of a census report expects.
- Any ordered bands (age, income brackets, tenure) split into exactly two groups to be compared band by band.
- Comparing two pyramids side by side (two countries, two years) when the change in shape is the story.
- Up to about 25 bands; five-year age bands are the norm.
- Excels at: the overall shape (expanding, stationary, contracting population) reads instantly, and bands line up across the centre for pairwise comparison.

## When not to use

- More than two groups: mirrored bars only hold two; use `grouped-bar` or `small-multiples`.
- Unordered categories: the pyramid's shape depends on order; use a `bar`.
- When precise left-right comparison matters: the two sides are non-aligned scales (Cleveland and McGill's second rank), so small differences between sexes are hard to see. Overlay the two as `dumbbell` or plot the difference as a `diverging-bar`.
- Mixed units (counts on one side, percentages on the other): both sides must share a scale.

## Substitutes

- Difference between the two sides: `diverging-bar` of male minus female per band.
- Many groups per band: `grouped-bar`, `stacked-bar-100`.
- Change in age structure over many years: `heatmap` (age by year) or `small-multiples` of pyramids.
- One group only: `bar` (horizontal).

## Evidence

- Each side is length on a common baseline (accurate, Cleveland and McGill 1984); comparison across the centre line is position on non-aligned scales, one rank lower. Long-standing convention in demography and in Datawrapper, Vega-Lite and the Data Visualisation Catalogue: `medium`.
- Franconeri et al. 2021: the global shape is read fast; the band-by-band comparison is slow, so annotate the bands that carry the finding.

## Accessibility

- Two hues at different lightness (or one hue and one grey) with the side labelled directly at the top of each half; a legend as well.
- Axis labels on both sides show absolute values (no negative numbers): format the mirrored side with `abs`.
- Age bands labelled in the centre or on the left in reading order (youngest at the bottom, the convention).
- Text alternative: "Population pyramid of <place>, <year>; the largest bands are 25 to 34; the base is narrower than the middle, indicating an ageing population; women outnumber men above 75."
- 3:1 contrast for both fills against the background.

## Build

### mermaid

Not drawable in Mermaid (no horizontal mirrored bars, no negative bar axis). Render with the vega-lite or matplotlib target and link the image.

### vega-lite

Two horizontal bar charts concatenated back to back with the left one's x axis reversed:

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "pop.csv"},
 "spacing": 0, "hconcat": [
  {"transform": [{"filter": "datum.sex == 'F'"}], "mark": "bar", "title": "Female",
   "encoding": {"y": {"field": "age", "type": "ordinal", "axis": null, "sort": "descending"},
                "x": {"field": "people", "type": "quantitative", "sort": "descending", "axis": {"format": "s"}}}},
  {"width": 24, "mark": "text", "encoding": {"y": {"field": "age", "type": "ordinal", "axis": null, "sort": "descending"}, "text": {"field": "age"}}},
  {"transform": [{"filter": "datum.sex == 'M'"}], "mark": "bar", "title": "Male",
   "encoding": {"y": {"field": "age", "type": "ordinal", "axis": null, "sort": "descending"},
                "x": {"field": "people", "type": "quantitative", "axis": {"format": "s"}}}}]}
```

Hand-written (this is the Vega-Lite gallery pattern); share the x scale by fixing `"scale": {"domain": [0, max]}` on both sides. Composition, hence `approx`.

### plotly

Two horizontal `bar` traces (`orientation: "h"`), the female one with negated values, `layout.barmode = "overlay"`, and `xaxis.tickvals`/`ticktext` set to absolute labels. Hand-written.

### chartjs

`{"type": "bar", "options": {"indexAxis": "y", "scales": {"x": {"stacked": true, "ticks": {"callback": "v => Math.abs(v)"}}, "y": {"stacked": true}}}}` with two datasets, one negated. Hand-written.

### matplotlib

`ax.barh(ages, -female, color="#CC79A7", label="Female"); ax.barh(ages, male, color="#0072B2", label="Male")`, then `ax.xaxis.set_major_formatter(lambda v, _: f"{abs(v):,.0f}")` and `ax.legend()`. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`. Composed from `barh`, hence `approx`.

### echarts

Hand-written: two horizontal `bar` series with the left one negated. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
