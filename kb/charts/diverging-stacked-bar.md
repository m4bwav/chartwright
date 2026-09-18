---
name: Diverging stacked bar chart
slug: diverging-stacked-bar
aliases: [Likert chart, diverging stacked bar, survey response chart, sentiment bar, agreement scale chart, centred stacked bar]
family: deviation
also: [part-to-whole, distribution]
question: How does agreement compare to disagreement across survey items, with the neutral answers centred?
shapes: ["n,o,q", "o,o,q"]
goals: [deviation, likert, survey, agree disagree, sentiment, satisfaction, rating scale, responses, opinion, net agreement, ordinal scale, questionnaire]
max_series: 7
max_categories: 20
evidence: medium
popularity: common
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: native
  chartjs: native
  matplotlib: native
  terminal: none
  echarts: image
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
  docx: image
  gsheets: image
  observable-plot: approx
  d2: none
  plantuml: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/stacked-column-charts, https://vega.github.io/vega-lite/examples/, https://plotly.com/javascript/bar-charts/]
---

# Diverging stacked bar chart

## When to use

- Ordered survey scales (strongly disagree to strongly agree, very unlikely to very likely) with 3 to 7 answer categories, one row per question or item, shown as percentages.
- The message is the balance of positive against negative: bars extend left for negative answers and right for positive ones from a shared centre, with the neutral category split across it or shown separately.
- Comparing many items (up to about 20) sorted by net agreement or by the share of the strongest positive answer.
- FT Visual Vocabulary: "perfect for survey results which involve sentiment"; Datawrapper's Likert guidance.
- Excels at: ranking items by sentiment at a glance, because the two outer segments start on a common line (the centre) and the row order carries the ranking.

## When not to use

- Comparing the middle segments across rows: they float at different offsets and read poorly (the stacked bar problem; Datawrapper 2025).
- Unordered categories: there is no positive or negative side; use a `stacked-bar-100`.
- Only the net score matters: a `diverging-bar` of net agreement (positive minus negative) is cleaner.
- A large neutral share that dominates: splitting it across the centre hides it; put neutral to the right in grey, or state it in a column of numbers.
- Sample sizes that differ wildly across items: print n per row; percentages alone mislead.

## Substitutes

- Net score only: `diverging-bar`.
- Unordered parts of a whole: `stacked-bar-100`.
- Full distribution per item with exact percentages: `table` with a heat fill.
- Change in sentiment between two surveys: `dumbbell` of the positive share.
- Few items and few categories: a `grouped-bar` of the two extreme categories.

## Evidence

- The outer positive and negative segments share the centre baseline, so their lengths are comparable across rows (Cleveland and McGill 1984 length on a common scale); inner segments are length only, the weaker second tier. `medium`: consistent practitioner consensus (Heiberger and Robbins 2014 on diverging stacked bars for Likert data; FT; Datawrapper) rather than a dedicated perception study, and the neutral-split choice is debated.
- Datawrapper 2025 (stacked column charts): readers struggle to compare segments that do not start on the same baseline, which is why the segments the reader must compare (strong agree, strong disagree) go on the outside.
- Franconeri et al. 2021: sorting rows by net agreement makes the ranking a global shape rather than a series of pairwise reads.

## Accessibility

- A diverging palette with one hue per side stepping in lightness (ColorBrewer RdBu or PuOr, or the Okabe-Ito blue and vermilion tinted), neutral in grey; a legend in scale order.
- Percentages printed in segments wider than about 8 percent; the total positive and negative shares printed at the row ends.
- A centre line at 2 px labelled 0 percent; the axis labelled in percent both directions.
- Text alternative: "Diverging stacked bar chart of <n> survey items; most positive <item> (<positive share> agree), most negative <item> (<negative share> disagree); n = <sample> per item." Offer the table with one column per answer category.
- Do not rely on colour to separate adjacent segments; a 1 px white gap between them.

## Build

### mermaid

`image`: Mermaid has no stacked bars. Render the vega-lite or matplotlib recipe and link the image; the in-place fallback is a Mermaid `bar` of net agreement.

### vega-lite

`approx`: Vega-Lite stacks from zero, so the diverging offsets must be computed. The gallery's Likert example uses `calculate` transforms to assign a signed value per category (negative categories negated, half of neutral each side), then a `bar` mark with `x` the signed value, `stack: "zero"` (the default) and a fixed `"order"` by category rank; long data of `item, answer, percent`. Hand-written and fiddly; render with `cw.py render --target vega-lite --in chart.vl.json --out chart.svg`.

### plotly

One horizontal `bar` trace per answer category, negatives as negative values (`x: [-p...]`), `layout.barmode = "relative"` (stacks positives right and negatives left of zero), traces ordered from neutral outward, `layout.xaxis.tickformat = "+d"` or custom tick text for absolute percentages. Hand-written; open with `cw.py render --target plotly --in fig.json --out chart.html`.

### chartjs

`{"type": "bar", "data": {"labels": items, "datasets": [{"label": "Strongly disagree", "data": [-p...]}, ..., {"label": "Strongly agree", "data": [p...]}]}, "options": {"indexAxis": "y", "scales": {"x": {"stacked": true, "ticks": {"callback": "v => Math.abs(v) + '%'"}}, "y": {"stacked": true}}}}`; stacked bars with negative values stack leftwards natively. Hand-written.

### matplotlib

`left = -(negatives.sum(axis=1) + neutral/2)` per row, then for each category in scale order `ax.barh(items, share, left=left, label=name, color=palette[i]); left += share`, `ax.axvline(0, color="black")`, `ax.xaxis.set_major_formatter(lambda v, _: f"{abs(v):.0f}%")`. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### observable-plot

`Plot.barX(data, Plot.stackX({offset: "center"}, {y, x: "count", fill: "level"}))`; a true neutral-centred offset needs a hand-computed x1/x2.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
