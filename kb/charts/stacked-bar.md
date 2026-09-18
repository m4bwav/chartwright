---
name: Stacked bar chart
slug: stacked-bar
aliases: [stacked column chart, stacked bar, composition bar, segmented bar chart]
family: part-to-whole
also: [magnitude, change-over-time]
question: How big is each total, and how does it split into a few parts?
shapes: ["n,q*n", "o,q*n", "time,q*n"]
goals: [part to whole, composition, breakdown, split, total, share, segments, by category, stacked, contribution, make up]
max_series: 4
max_categories: 12
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
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/stacked-column-charts, https://www.datawrapper.de/blog/chart-types-guide, https://journals.sagepub.com/doi/10.1177/15291006211051956]
---

# Stacked bar chart

## When to use

- The total per category matters and so does its split into a few parts: revenue by region split by product line, headcount by department split by contract type.
- Up to about four segments, with the segment readers must compare placed on the baseline where it reads as position on a common scale.
- Categories over time (quarters, years) when the message is "the total grew and part X drove it"; columns for few periods, bars for long labels.
- The reader's first question is "how big" and the second is "made of what"; a stacked bar answers both in that order.
- Excels at: totals with an approximate composition; one glance gives the ranking of totals and the size of the baseline segment.

## When not to use

- The reader must compare the middle or top segments across bars: their bases float, so those comparisons are slow and inaccurate (Cleveland and McGill 1984). Use a grouped bar, a small multiple per segment, or a split bar.
- More than four segments: the stack turns into a colour key exercise; fold small segments into "Other" or use small multiples (Datawrapper 2025).
- Shares are the point and totals are noise: use `stacked-bar-100`.
- Negative values: a stack of mixed signs misreads; use a `diverging-bar` or a `waterfall`.
- Many periods (dozens of points): a `stacked-area` reads the same data as a shape.
- Log axis: stacked lengths on a log scale mean nothing; never combine the two.

## Substitutes

- Shares only: `stacked-bar-100`; a single whole with a majority question: `pie` or `donut`.
- Compare each segment across categories accurately: `grouped-bar` or `small-multiples` of bars.
- Many periods: `stacked-area`; many categories and segments: a `heatmap` or a `table`.
- Two-dimensional composition where widths also carry a total: `marimekko`.
- Signed parts that add to a running total: `waterfall`; survey scales: `diverging-stacked-bar`.
- Hierarchy of parts: `treemap`.

## Evidence

- The baseline segment and the total are position on a common scale (highest accuracy); every other segment is length on a non-aligned scale, which reads worse (Cleveland and McGill 1984; Heer and Bostock 2010). Hence `medium`: the chart is accurate for exactly the comparisons its layout privileges.
- Readers compare adjacent, aligned marks quickly and everything else slowly (Franconeri et al. 2021): put the key segment on the baseline and order segments consistently across bars.
- Practitioner consensus caps stacks at about four segments and recommends split or small-multiple bars when cross-bar segment comparison matters (Datawrapper 2025-02; FT Visual Vocabulary).
- Bars start at zero; a truncated stacked axis lies about both totals and shares.

## Accessibility

- Every segment needs a label or a value, not only a colour; label segments directly inside bars when there is room, and give a legend that follows the stack order (top segment first).
- Use at most four hues from a colour-blind-safe set (Okabe-Ito) or a light-to-dark ramp of one hue when the segments are ordered; add hatching for greyscale print.
- Text alternative: "Stacked bar chart of <total> by <category>, split by <segment>; <category A> is largest at <value>, with <segment> making up <share>." Offer the underlying table.
- Contrast between adjacent segments of at least 3:1, or a thin separator stroke.

## Build

### mermaid

Mermaid `xychart` has no stacking (several bar series overlap). Render the chart with the vega-lite target to SVG or PNG and link it from the markdown; a `sankey-beta` is not a substitute.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "sales.csv"},
 "mark": "bar",
 "encoding": {"x": {"field": "region", "type": "nominal"}, "y": {"field": "revenue", "type": "quantitative"},
              "color": {"field": "product", "type": "nominal"}, "order": {"field": "product"}}}
```

`cw.py build --chart stacked-bar --target vega-lite --data sales.csv --x region --y revenue --series product [--html]`. Bars stack whenever `color` is set; control the stack order with `order` and put the key segment first. Horizontal: swap `x` and `y`. Totals on top: a `text` layer with `"aggregate": "sum"`.

### plotly

One `{"type": "bar", "name": "<segment>", "x": [...], "y": [...]}` trace per segment and `layout.barmode = "stack"`; horizontal with `orientation: "h"`. `cw.py build --chart stacked-bar --target plotly --data sales.csv --x region --y revenue --series product --html`.

### chartjs

`{"type": "bar", "data": {"labels": [...], "datasets": [{"label": "A", "data": [...]}, {"label": "B", "data": [...]}]}, "options": {"scales": {"x": {"stacked": true}, "y": {"stacked": true}}}}`; `indexAxis: "y"` for horizontal. `cw.py build --chart stacked-bar --target chartjs ... --html`.

### matplotlib

Hand-written: `ax.bar(cats, a, label="A"); ax.bar(cats, b, bottom=a, label="B")`, accumulating `bottom` per segment (`ax.barh` with `left=` for horizontal), `ax.legend()`, `ax.bar_label` on the last stack for totals. Run through `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
