# Selection rules (evidence-based)

Read this once per session before choosing a chart. The full evidence with citations is in [evidence.md](evidence.md); the per-chart caveats are in `kb/charts/`. `cw.py pick` encodes the mechanical part (family, data shape, caps, target support); these rules are the judgment part.

## 1. Start from the sentence, not the data

Write the headline the reader should take away. Its verb picks the family (Financial Times Visual Vocabulary; Datawrapper 2025):

| The sentence says... | Family | Default chart | Reach for instead when... |
|---|---|---|---|
| X grew / fell / changed over time | change-over-time | line (bar for few periods or discrete totals) | many series: small multiples; rank changes: bump; distributions over time: ridgeline or boxplots per period |
| X is bigger than Y | magnitude | bar (horizontal for long labels) | one measure, many items sorted: dot plot or lollipop; two measures: dumbbell or scatter |
| X ranks first | ranking | ordered bar | change in rank between two points: slope; over many points: bump |
| X is N% of the whole | part-to-whole | stacked bar (100%) | up to 5 parts and a "majority?" question: pie or donut; hierarchy: treemap; parts over time: stacked area |
| X is above or below target / zero / average | deviation | diverging bar | ordered survey scale: diverging stacked bar; running total of pluses and minuses: waterfall |
| X relates to Y | correlation | scatter | third measure: bubble; over time: connected scatter; many pairs: scatterplot matrix or heatmap; large n: hexbin or density |
| X is spread / typical / skewed | distribution | histogram | compare groups: box plots (or violin/raincloud when shape matters); small n: strip or beeswarm; cumulative questions: ECDF |
| X flows to Y | flow | sankey | many-to-many symmetrical: chord; process stages with drop-off: funnel; a sequence of steps: flow diagram |
| X is here | spatial | choropleth (rates) or bubble map (counts) | equal-weight regions: tile grid map; point events: dot density. Only when location is part of the finding; otherwise a sorted bar or dot plot, with a small locator map at most (Cairo 2013 ch. 2) |
| X contains Y contains Z | hierarchy | treemap | depth matters more than size: sunburst or icicle; structure only: tree |
| X is connected to Y | relationship | node-link network | dense graphs: adjacency matrix; hierarchy plus links: edge bundling |
| The number is N | single-value | stat tile (value, delta, sparkline) | progress to a limit: bullet chart or meter; never a gauge for a serious audience |
| Readers need exact values, or look up one known item | table | sorted table with inline bars or heat colouring | never force a chart on a lookup task (Munzner 2014 ch. 3); about 20 numbers or fewer with no trend or shape question also reads better as a table (Tufte 2001 ch. 1) |

## 2. Prefer the encoding the eye reads best

Position on a common scale beats length beats angle beats area beats colour (Cleveland and McGill 1984; Heer and Bostock 2010). So: dot and bar beat pie; bar beats treemap and bubble; heatmaps show pattern, not values. Reach for area or colour only when hierarchy, geography, extreme range, or density demands it. Area, shade and symbol maps serve overall pattern; any "how much more" or "which ranks first" question goes to position, even when the data are geographic (Cairo 2013 ch. 2, 6). `cw.py pick` warns `precision-on-area` and `map-not-needed` on such picks (book rule, unverified).

Expressiveness (Munzner 2014 ch. 5): ordered data goes on magnitude channels (position, length, area, lightness), categories on identity channels (hue, shape, region). Hue has no order, and a lightness ramp makes categories look ranked. Never put two fields on channels that fuse into one read, such as width and height of one mark or colour and opacity.

## 3. Caps that keep a chart honest

- Lines on one chart: about 5 distinct series, or grey-plus-one-highlight for more. Above that, small multiples.
- Grouped bars: 3 series. Stacked bars: 4 segments, with the segment readers must compare on the baseline.
- Pie: 5 slices, one whole, big differences; label directly. Donut is a pie (same accuracy, Kosara 2016).
- Categorical colours: 8, and only for identity; the background, the default grey and "Other" count toward about 12 distinguishable colours (Munzner 2014 ch. 10). A 9th hue is never generated; fold to "Other" or facet.
- Categories on an axis: about 12 in Mermaid, 30 in an image before switching to a table or a ranked subset.

## 4. Things to refuse or redesign

- Dual y-axes: for a trend or correlation question, two panels sharing x, index both to 100, or a connected scatter. A dual axis is acceptable when readers need the absolute levels of two measures on very different scales ("when one moved, what did the other do"); then colour-key each axis to its series and label values (Muth 2026, Datawrapper, which now ships the type).
- 3D anything, exploded pies, bar-of-pie, gauges, word clouds: pick the substitute in the chart file.
- Truncated bar axes: bars start at zero. Lines and dots may not, and the axis says so. The drawn change over the data change (Tufte's lie factor) stays within 0.95 to 1.05 (Tufte 2001 ch. 2).
- Icons and bubbles scale by area, never by height or radius: a 1-D change drawn in 2-D inflates by the square.
- Dates sit at their real spacing (a temporal axis, not ordinal). Money over many years is inflation-adjusted or labelled nominal.
- A lone short series answers no "compared with what": add an earlier period, a peer, a target or a note (Tufte 2001 ch. 2).
- A node-link network needs a question about structure; for lookups a sorted list carries more labels per area (Munzner 2014 ch. 6).
- Log scale: only for multiplicative data, never under stacked or area charts, always announced. For a general audience avoid it; if kept, say what one step means in plain words in the axis title or subtitle ("log scale: each gridline is 10 times the last"), since lay readers misread log axes even when told (Engebretsen and Kennedy 2020 ch. 12, n = 18; book rule, unverified).
- Counts across places or groups of unequal size are normalized to a rate (per capita, per 100,000, share) before comparing, and the axis title says per what (Cairo 2013 ch. 2). When the question is the gap between two series, plot the difference as its own series.
- A line never joins unordered categories: bars, a dot plot, a dumbbell for two dates, a slope chart for change (Knaflic, Cisneros and Velez 2024 ch. 2). Forecasts are drawn dashed or lighter than actuals and labelled "forecast" (ch. 7; `cw.py build --forecast-from`). No fitted trendline unless the reader asked for a model. Totals and composition go in separate charts.
- Specialist charts (box, violin, survival curve, jittered strip, bubble, correlation matrix) for a general audience: pull the few values that carry the message into bars, a pie or a waffle and name the groups in plain words (Knaflic et al. 2024 ch. 1, 8).
- Colour weight and contrast (Ware 2012 ch. 3-4): large areas light and low-saturation, small marks saturated; points, lines and text at least 3:1 luminance contrast with their ground, with a contrasting outline where the ground varies (maps, images). A highlight colour lies outside the other series' colours (a saturated hue among greys, never grey among hues) and the rest is dimmed. Saturation alone carries about 3 levels, grey alone 2 to 4. Where readers must read values off a continuous key, a scale that cycles hue while lightness rises steadily (viridis) beats one hue; a raw spectrum only where the audience's convention demands it.
- Rainbow sequential palettes and colour-only encoding: sequential is one hue light to dark; diverging is two hues with a neutral midpoint that means something; every colour has a label or a shape twin.
- Uncertainty as bare error bars when a band, quantile dots, or a distribution would be read more accurately.

## 5. Small multiples vs overlay

Overlay when the comparison is between series at the same x and there are few series. Small multiples when comparing shapes across many categories or when lines cross a lot; share axes, order panels by a meaning (size, region, rank), and repeat a reference line (overall mean) in every panel because cross-panel value comparison is slow.

## 6. Annotate

Label lines at their ends, put values on bars when there are few, write the "so what" on the chart, and title with the finding, not the variable. Legends force slow lookups; direct labels do not, and a legend for one series is never needed (name it in the title). Sort categorical bars by the value the message is about. Keep tick labels flat: shorten them or use a two-level date axis instead of angling them (Knaflic et al. 2024 ch. 4, 5, 11).

Put the source inside the image ("Source: X, year" as subtitle or footer; `cw.py build --source`), because charts travel without their page. Caveats about the data (estimates, provisional, incomplete) go in the visible subtitle or caption, never only in a tooltip or info icon, which few readers open. Restate technical units in plain terms (Engebretsen and Kennedy 2020 ch. 5, 11, 12; small qualitative samples, book rules, unverified).

## 7. Charts in documents

When asked to add charts to a document rather than draw a named chart: find the claims in the text that carry numbers or comparisons; each claim that a reader would want to verify or feel gets one chart, placed next to the claim, titled with the claim, and no chart is added for decoration. Two to five charts per report section is typical; a chart per paragraph is noise. Prefer the target the document renders natively (see [choosing-a-target.md](choosing-a-target.md)).
