---
name: Pictogram
slug: pictogram
aliases: [isotype chart, unit chart, icon array, pictograph, icon chart]
family: magnitude
also: [part-to-whole]
question: How many units are there, shown as repeated icons a general audience can count?
shapes: ["n,q", "q"]
goals: [magnitude, how many, count, units, people, icons, out of 100, general audience, infographic, isotype, one in ten, risk]
max_series: 1
max_categories: 6
evidence: medium
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: none
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://datavizcatalogue.com/methods/pictogram_chart.html, https://github.com/gyli/PyWaffle, https://vega.github.io/vega-lite/examples/isotype_bar_chart.html]
---

# Pictogram

## When to use

- Whole-number counts for a general audience: "3 in 10 adults", "each icon is 1,000 households"; the icon carries the unit and the count is literal.
- Risk and frequency communication (icon arrays of 100 people with some shaded): the format that health communication research recommends for lay readers.
- Up to about 6 categories compared as rows of icons, each row a count on the same unit, aligned at the left so the rows read as bars.
- Infographics and reports where memorability matters (Haroz, Kosara and Franconeri 2015; Bateman et al. 2010).
- Excels at: making a number concrete and countable; the "one icon equals N" rule stated once.

## When not to use

- Non-integer or large-range values: partial icons (FT: "do not slice off an arm") and thousands of icons both fail; use a `bar`.
- Precise comparison between rows: readers count or compare row lengths; both are slower than reading a bar; a `bar` with values.
- Icons scaled by size instead of repeated: area is read poorly (Cleveland and McGill 1984) and readers cannot tell if height or area encodes the value.
- Many categories or series: the grid becomes a texture; use a `waffle` for one part-to-whole or a `bar`.
- Formal or scientific audiences who read the icons as decoration.

## Substitutes

- Part of a whole as a 10 by 10 grid: `waffle`.
- Precise amounts: `bar` or `lollipop`.
- Shares: `stacked-bar-100` or `donut`.
- A single number with context: `stat-tile`.

## Evidence

- Haroz, Kosara and Franconeri 2015 (ISOTYPE visualisation, CHI) found repeated pictographs did not reduce accuracy compared with bars for counts and improved memory and engagement when the icon carries meaning; icons that vary in size did hurt. `medium`: one study plus consistent practitioner guidance.
- Bateman et al. 2010: meaningful embellishment aids recall without hurting immediate reading.
- Each row is effectively a bar made of units, so left-aligned rows are read as length on a common baseline (Cleveland and McGill 1984); the count is exact only while the icons stay countable (under about 50 per row).
- Health communication (icon arrays) consistently outperforms percentages alone for lay risk perception (see Franconeri et al. 2021 for the review).

## Accessibility

- State the unit once ("each icon = 1,000 people") in the subtitle and print the total number at the end of each row; never rely on counting.
- Use simple, high-contrast silhouettes at 3:1, one colour for "counted" and a light grey for "remaining" in icon arrays.
- Icons from an open set (Font Awesome, Material) with a text alternative; decorative icons are `aria-hidden` and the numbers are in text.
- Text alternative: "Pictogram: <category A> <value> (<n> icons), <category B> <value>; each icon represents <unit>." Offer the table.
- Grid spacing at least a quarter of the icon size so rows do not merge.

## Build

### mermaid

`image`: Mermaid has no icon mark. Render with matplotlib (pywaffle) and link the image; a Mermaid `bar` is the in-place fallback.

### vega-lite

`approx`: the gallery's isotype bar chart uses a `point` mark with `"shape"` set to an SVG path string and a `sequence` or `flatten` transform to emit one row per unit (`{"calculate": "sequence(1, datum.count + 1)", "as": "unit"}, {"flatten": ["unit"]}`), then `x` ordinal by unit and `y` nominal by category. Works, but the SVG path must be supplied and partial units are not possible. Hand-written; render with `cw.py render --target vega-lite --in chart.vl.json --out chart.svg`.

### plotly

`approx`: a `scatter` trace with `mode: "markers"`, `marker.symbol` from Plotly's symbol list (no arbitrary icons) or `mode: "text"` with an emoji per unit, positioned on a grid computed in advance. Hand-written; passable for icon arrays of circles, not for real pictograms.

### matplotlib

`from pywaffle import Waffle; fig = plt.figure(FigureClass=Waffle, rows=5, values={"Yes": 30, "No": 70}, icons="person", icon_size=18, legend={"loc": "lower left"})` (pywaffle bundles Font Awesome icons); for a row per category pass `plots={...}` with one entry each. `pip install pywaffle`. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. Chart.js has no icon plugin in the targets file (`none`).
