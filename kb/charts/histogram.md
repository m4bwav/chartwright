---
name: Histogram
slug: histogram
aliases: [frequency distribution, binned bar chart, frequency histogram]
family: distribution
also: [magnitude]
question: What is the shape of one numeric variable: where is it centred, how spread out is it, is it skewed or bimodal?
shapes: ["q", "q,n"]
goals: [distribution, shape, spread, frequency, how many fall, bins, skew, outliers, range of values, histogram]
max_series: 3
max_categories: 0
evidence: high
popularity: core
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: image
  quickchart: approx
  xlsx: image
  gdocs: image
  docx: image
  gsheets: native
  observable-plot: native
  d2: none
  plantuml: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/histogram.html, https://vega.github.io/vega-lite/docs/bin.html, https://plotly.com/python/histograms/, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html]
---

# Histogram

## When to use

- One numeric variable and the question is its shape: centre, spread, skew, gaps, more than one peak.
- Checking assumptions before summarising with a mean or a box plot (a bimodal variable has a meaningless mean).
- Moderate to large n (about 30 upwards): with fewer values the bins are mostly noise; show the points instead.
- Two or three groups overlaid with transparency, or faceted, when the reader must compare shapes.
- Excels at: the default distribution chart every reader understands; counts are lengths on a common baseline, the encoding read most accurately (Cleveland and McGill 1984).

## When not to use

- Categorical data: that is a bar chart; a histogram's bars touch because the axis is continuous.
- Many groups (more than three): overlaid histograms occlude each other; use `ridgeline`, `boxplot` per group, or `ecdf`.
- Bin width games: too few bins hide structure, too many show noise; never pick the width that makes the story. Start from the Freedman-Diaconis or Sturges default the library gives and show the alternative when it changes the reading.
- When the reader needs "what share is below x": read that off an `ecdf`, not by summing bars.
- Very small n (under 20): a `strip` or `beeswarm` shows every value and no false shape.
- Unequal bin widths without scaling the height to density: the area, not the height, then carries the count and readers get it wrong.

## Substitutes

- Smooth shape with large n: `density`.
- Compare several groups: `boxplot`, `violin`, `ridgeline` (ordered groups), `ecdf` (precise comparison).
- Small n, show every value: `strip`, `beeswarm`.
- Shape plus summary plus raw values in one panel: `raincloud`.
- Two numeric variables: `scatter`; where the mass sits in a big scatter: `hexbin` or `density-2d`.
- Counts per category (not a distribution): `bar`.

## Evidence

- Bar height on a common baseline is length and position, the top of the Cleveland and McGill 1984 ranking, replicated by Heer and Bostock 2010: `high`.
- Shape is extracted as a fast global feature (Franconeri et al. 2021), which is what a histogram is for; comparing two specific bins is slow, so annotate when one bin matters.
- The bin choice changes the shape the reader sees; that is the main risk, and it is a design risk rather than a perception one. State the bin width in the axis or caption.
- The y axis must start at zero (counts are lengths).

## Accessibility

- Label the x axis with units and the bin width; label the y axis "count" or "share".
- Text alternative: "Histogram of <variable>, n = <n>; most values fall between A and B, peak near C, long tail to the right." Offer the binned table on request.
- Overlaid groups: transparency plus a distinct outline colour per group, and a legend; never rely on fill colour alone. Faceting is safer than overlay for colour-blind readers.
- 3:1 contrast between bar fill and background; a thin gap or outline between bars helps low-vision readers count bins.

## Build

### mermaid

Mermaid has no histogram and `xychart` bars overlap rather than bin. Pre-bin the data and draw a bar chart only when the message survives category labels like "0-10, 10-20"; otherwise render an image with the vega-lite or matplotlib target and link it.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "values.csv"},
 "mark": "bar",
 "encoding": {"x": {"field": "value", "bin": {"maxbins": 30}, "type": "quantitative"},
              "y": {"aggregate": "count", "type": "quantitative"}}}
```

`cw.py build --chart histogram --target vega-lite --data values.csv --x value [--html]`. `"bin": {"step": 5}` fixes the width; add `"color": {"field": "group", "type": "nominal"}` and `"opacity": {"value": 0.6}` with `"mark": {"type": "bar", "binSpacing": 0}` for up to three overlaid groups, or `"row": {"field": "group"}` to facet.

### plotly

`{"type": "histogram", "x": [...], "nbinsx": 30}`; one trace per group with `layout.barmode = "overlay"` and `opacity: 0.6`, or `histnorm: "probability"` to compare shares. `cw.py build --chart histogram --target plotly --data values.csv --x value --html`.

### chartjs

No histogram type: bin in code first, then `{"type": "bar", "data": {"labels": ["0-10", "10-20", ...], "datasets": [{"data": counts}]}}` with `options.scales.x.offset = false` and `barPercentage: 1, categoryPercentage: 1` so the bars touch. Hand-written; `cw.py build` does not emit it.

### matplotlib

`ax.hist(values, bins=30, edgecolor="white")`; several groups as `ax.hist([a, b], bins=30, alpha=0.6, label=[...])` then `ax.legend()`; `density=True` for a share axis. `cw.py build --chart histogram --target matplotlib --data values.csv --x value --out chart.py --png chart.png` then `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: ecStat `histogram` transform feeding a `bar` series. See `kb/targets/echarts.md`.

### quickchart

Approximate: pre-binned counts as a bar config; write the Chart.js config by hand and URL-encode it (see `kb/targets/quickchart.md`).

### observable-plot

`cw.py build --chart histogram --target observable-plot --data file.csv --x <x> --y <y> [--series <s>]` emits the `Plot.plot({...})` snippet; add `--html --out page.html` for a page (d3 and Plot 0.6 from jsdelivr).

### gsheets

`histogramChart` with `series[].data` and `bucketSize`; Sheets bins for you.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
