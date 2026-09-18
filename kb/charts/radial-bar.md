---
name: Radial bar chart
slug: radial-bar
aliases: [circular bar chart, radial column chart, polar bar chart, Nightingale rose, coxcomb, circular barplot]
family: magnitude
also: [part-to-whole, change-over-time]
question: How do many categories compare in size, drawn around a circle for compactness or cyclical order?
shapes: ["n,q", "o,q"]
goals: [magnitude, circular, radial, around a circle, cyclical, months, hours, rose, polar, decorative, compact, many categories]
max_series: 1
max_categories: 40
evidence: low
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: native
  chartjs: approx
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://datavizcatalogue.com/methods/radial_bar_chart.html, https://www.data-to-viz.com/graph/circularbarplot.html, https://plotly.com/javascript/polar-chart/, https://www.chartjs.org/docs/latest/charts/polar.html, https://matplotlib.org/stable/gallery/pie_and_polar_charts/polar_bar.html]
---

# Radial bar chart

## When to use

- Cyclical categories (hours of the day, months, compass directions) where the circle mirrors the data's own loop and the last category should sit next to the first.
- Many categories (20 to 40) in a square space, for a poster or infographic where compactness and visual appeal outrank precise reading.
- The pattern matters more than the values: a wind rose, a "busiest hour" ring.
- The bars start at a shared inner radius and the values are labelled directly, so the chart is a decorated table.
- Excels at: fitting many bars into a small square and showing periodicity; nothing else.

## When not to use

- Any task where the reader compares values: outer bars look longer than inner bars of the same value (arc length grows with radius), and radial length is read worse than aligned length; use a `bar`.
- Non-cyclical categories: the circle implies a loop that does not exist; use a sorted `bar`.
- A Nightingale rose with bars wedged from the centre: the wedge area grows with the square of the value, so it exaggerates; if used, scale the radius by the square root and say so.
- Few categories: a plain `bar`.
- Values that must sum to a whole around the circle: that is a `pie` or `donut`, and they have their own limits.

## Substitutes

- Precise comparison: `bar` (horizontal, sorted) or `lollipop`.
- Cyclical time with a value per period over several years: `heatmap` (period by year) or a `line` per year.
- Shares of a whole: `donut`.
- Hourly or daily pattern over a long span: `calendar-heatmap`.

## Evidence

- `low`: radial length and angle rank below aligned position and length (Cleveland and McGill 1984; Heer and Bostock 2010), and no study finds a task where the radial form reads better than a straight bar. The Data Visualisation Catalogue and From Data to Viz both file it under "decorative, use with caution".
- The distortion is geometric: at radius r the arc for one category spans r times theta, so equal values look unequal at different radii, and wedges (rose) scale as r squared.
- Practical defence when it is used: an inner hole (so no bar starts at zero radius), labelled rings, and value labels on each bar.

## Accessibility

- Value labels on every bar or a table beside the chart; ring gridlines labelled at round values.
- One colour, with a highlight colour for the bar the headline names; never a rainbow by category.
- Category labels rotated to follow the bar or placed outside the ring, at least 12 px.
- Text alternative: "Radial bar chart of <measure> by <cyclical category>; peak at <category> (<value>), trough at <category> (<value>)." Offer the table.
- 3:1 contrast on bars; gaps between bars at least 2 px so counts are readable.

## Build

### mermaid

`image`: Mermaid's `radar-beta` draws a polygon, not bars, so it is not a substitute. Render with matplotlib or plotly and link the image, or draw a straight `bar` in Mermaid.

### vega-lite

`approx`: the `arc` mark with `theta` by category (nominal) and `radius` by value (`"scale": {"type": "sqrt", "zero": true, "rangeMin": 20}`) gives a radial bar (the gallery's "radial plot"); there are no polar axes or ring gridlines, so add `text` marks for labels by hand. Hand-written; render with `cw.py render --target vega-lite --in chart.vl.json --out chart.svg`.

### plotly

`{"type": "barpolar", "r": values, "theta": categories, "width": 1}` with `layout.polar = {"radialaxis": {"showticklabels": true}, "angularaxis": {"direction": "clockwise"}}`; a `hole` on the radial axis range (`"range": [-max*0.3, max]`) keeps bars off the centre. Hand-written; open with `cw.py render --target plotly --in fig.json --out chart.html`.

### chartjs

`approx`: `{"type": "polarArea", "data": {"labels": categories, "datasets": [{"data": values}]}}` draws equal-angle wedges from the centre with radius by value (a rose, not a ring of bars), and it colours each wedge differently by default; set one `backgroundColor` and `scales.r.beginAtZero: true`. Hand-written.

### matplotlib

`ax = fig.add_subplot(polar=True); theta = numpy.linspace(0, 2*numpy.pi, n, endpoint=False); ax.bar(theta, values, width=2*numpy.pi/n*0.9, bottom=inner); ax.set_xticks(theta, labels); ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)`. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. Kept as a niche type for cyclical data and infographics; the selection rules send precise comparisons to `bar`.
