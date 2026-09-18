---
name: Streamgraph
slug: streamgraph
aliases: [stream graph, ThemeRiver, wiggle stacked area, flowing area chart]
family: change-over-time
also: [part-to-whole]
question: How do many components ebb and flow over time, as an overall picture rather than exact values?
shapes: ["time,q*n", "time,n,q"]
goals: [streamgraph, ebb and flow, many categories over time, popularity over time, themes, genres, aesthetic, overview, volume of topics]
max_series: 20
max_categories: 0
evidence: low
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: image
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.data-to-viz.com/graph/streamgraph.html, https://vega.github.io/vega-lite/docs/stack.html, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stackplot.html]
---

# Streamgraph

## When to use

- Many components (10 to 20 or more) over a long time span, where the reader should see which ones swell and fade, not read values (music genres by decade, topics in a corpus, baby names).
- An editorial or exploratory overview where the organic shape is part of the appeal and precision is explicitly not expected.
- Each component has a clear rise and fall; the wiggle layout minimises the slope distortion of a plain stack (Byron and Wattenberg 2008).
- Excels at: a memorable overview of many changing volumes in one picture.

## When not to use

- Any question that needs a value or a comparison between two components: no baseline means no reliable reading of thickness.
- Fewer than about 6 components: a `stacked-area` with a zero baseline does the same job and can be read.
- Data with sharp spikes or many zeros: the wiggle layout produces jagged, misleading shapes.
- Audiences who need to trust the numbers (reports, finance): reach for `small-multiples`.
- A markdown host: no text chart syntax draws it; an image is the only route.

## Substitutes

- Total plus a few parts, read accurately: `stacked-area`.
- Component shapes compared: `small-multiples` of `area`.
- Distribution shifts across ordered groups: `ridgeline`.
- Rank changes among components: `bump`.
- Many series in little vertical space, precise: `horizon`.

## Evidence

- Byron and Wattenberg 2008 ("Stacked Graphs: Geometry and Aesthetics") define the wiggle offset and argue for it on aesthetic and slope-distortion grounds, not on reading accuracy; no perception study shows readers extract values from a streamgraph. Rating `low`: the chart is chosen for engagement (Bateman et al. 2010 supports that embellished charts are remembered), and the rules say so.
- Every layer is a length between two curves with a moving baseline, the weakest form of the length task in Cleveland and McGill 1984.
- Practitioner guides (Financial Times, From Data to Viz) list it as an overview device with a caveat about precision.

## Accessibility

- Label the larger streams directly inside their widest part; a legend of 20 colours is unusable.
- Use an ordered palette (light to dark, or hue families for groups) rather than 20 unrelated hues; streams next to each other must differ in lightness.
- Text alternative: "Streamgraph of <measure> by <category> from <start> to <end>; <category A> dominates early and fades by <period>, <category B> grows from <period>." Always provide the data table.
- Interactive versions: hover highlights one stream and shows its value; that is the only way a reader gets a number.

## Build

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "genres.csv"},
 "mark": "area",
 "encoding": {"x": {"field": "year", "type": "temporal"},
              "y": {"field": "count", "type": "quantitative", "stack": "center", "axis": null},
              "color": {"field": "genre", "type": "nominal"}}}
```

Hand-written (no builder). `"stack": "center"` is a symmetric offset, not the wiggle offset of Byron and Wattenberg, hence `approx`; full Vega has the `stack` transform with `"offset": "center"` only as well, so the true wiggle needs precomputed offsets. Add `"interpolate": "monotone"` to the mark for smooth edges.

### plotly

One `{"type": "scatter", "mode": "lines", "stackgroup": "one", ...}` trace per component gives a stack from zero; for the centred look precompute the baseline offset in Python and pass `fill: "tonexty"` traces with the shifted values. Hand-written; the loss is the missing wiggle offset.

### matplotlib

`ax.stackplot(years, *rows, labels=names, baseline="wiggle")` (`"sym"` for centred, `"weighted_wiggle"` for the Byron and Wattenberg variant); hide the y axis with `ax.yaxis.set_visible(False)`. Hand-written, then `cw.py render --target matplotlib --in chart.py --out chart.png`.

Markdown and Chart.js hosts: render the matplotlib or vega-lite version to SVG or PNG and link it; Chart.js has no offset stacking.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
