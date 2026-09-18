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
| X is here | spatial | choropleth (rates) or bubble map (counts) | equal-weight regions: tile grid map; point events: dot density |
| X contains Y contains Z | hierarchy | treemap | depth matters more than size: sunburst or icicle; structure only: tree |
| X is connected to Y | relationship | node-link network | dense graphs: adjacency matrix; hierarchy plus links: edge bundling |
| The number is N | single-value | stat tile (value, delta, sparkline) | progress to a limit: bullet chart or meter; never a gauge for a serious audience |
| Readers need exact values | table | sorted table with inline bars or heat colouring | never force a chart on a lookup task |

## 2. Prefer the encoding the eye reads best

Position on a common scale beats length beats angle beats area beats colour (Cleveland and McGill 1984; Heer and Bostock 2010). So: dot and bar beat pie; bar beats treemap and bubble; heatmaps show pattern, not values. Reach for area or colour only when hierarchy, geography, extreme range, or density demands it.

## 3. Caps that keep a chart honest

- Lines on one chart: about 5 distinct series, or grey-plus-one-highlight for more. Above that, small multiples.
- Grouped bars: 3 series. Stacked bars: 4 segments, with the segment readers must compare on the baseline.
- Pie: 5 slices, one whole, big differences; label directly. Donut is a pie (same accuracy, Kosara 2016).
- Categorical colours: 8, and only for identity. A 9th hue is never generated; fold to "Other" or facet.
- Categories on an axis: about 12 in Mermaid, 30 in an image before switching to a table or a ranked subset.

## 4. Things to refuse or redesign

- Dual y-axes: two panels sharing x, index both to 100, or a connected scatter. If forced, colour-code the axes and label values.
- 3D anything, exploded pies, bar-of-pie, gauges, word clouds: pick the substitute in the chart file.
- Truncated bar axes: bars start at zero. Lines and dots may not, and the axis says so.
- Log scale: only for multiplicative data, never under stacked or area charts, always announced.
- Rainbow sequential palettes and colour-only encoding: sequential is one hue light to dark; diverging is two hues with a neutral midpoint that means something; every colour has a label or a shape twin.
- Uncertainty as bare error bars when a band, quantile dots, or a distribution would be read more accurately.

## 5. Small multiples vs overlay

Overlay when the comparison is between series at the same x and there are few series. Small multiples when comparing shapes across many categories or when lines cross a lot; share axes, order panels by a meaning (size, region, rank), and repeat a reference line (overall mean) in every panel because cross-panel value comparison is slow.

## 6. Annotate

Label lines at their ends, put values on bars when there are few, write the "so what" on the chart, and title with the finding, not the variable. Legends force slow lookups; direct labels do not.

## 7. Charts in documents

When asked to add charts to a document rather than draw a named chart: find the claims in the text that carry numbers or comparisons; each claim that a reader would want to verify or feel gets one chart, placed next to the claim, titled with the claim, and no chart is added for decoration. Two to five charts per report section is typical; a chart per paragraph is noise. Prefer the target the document renders natively (see [choosing-a-target.md](choosing-a-target.md)).
