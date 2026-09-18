---
name: Beeswarm plot
slug: beeswarm
aliases: [swarm plot, bee swarm, dodge plot, packed dot strip]
family: distribution
also: [ranking, magnitude]
question: Where does every individual sit along one measure, and which ones stand out?
shapes: ["q", "n,q", "q,n"]
goals: [distribution, every value, individuals, each country, each player, highlight one, where does x sit, outliers, small n, beeswarm]
max_series: 0
max_categories: 8
evidence: medium
popularity: rising
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: image
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://seaborn.pydata.org/generated/seaborn.swarmplot.html, https://observablehq.com/plot/transforms/dodge, https://plotly.com/python/strip-charts/, https://vega.github.io/vega/docs/transforms/force/]
---

# Beeswarm plot

## When to use

- Every unit matters and is nameable: countries, teams, respondents, products; the reader wants to find "us" among them.
- n from about 20 to a few hundred per group; the swarm packs points without overlap up to that size.
- Highlighting one or a few units against the field (grey swarm, one coloured dot with a label).
- Comparing a few groups side by side when the exact spread of individuals is the point, not a summary.
- Excels at: an honest small-n distribution with no invented shape; density is visible as the swarm's width, and no point hides another.

## When not to use

- Large n (above a few hundred): the swarm grows wider than the axis allows and the layout collapses into a blob; use `violin`, `histogram` or `hexbin`.
- When readers need exact values: the dodge shifts points off the axis in the packing direction; only the measure axis is exact.
- Many groups: each swarm needs width; above about eight, use `strip` or `boxplot`.
- Static hosts with tight width: the layout is computed, not declared, and renders differently at different sizes.
- Time-ordered data: the swarm ignores order; use a `line` or `strip` over time.

## Substitutes

- Larger n or exact positions: `strip` with jitter or transparency.
- Summary across many groups: `boxplot`.
- Shape with large n: `violin`, `density`, `histogram`.
- Shape plus summary plus points: `raincloud`.
- One value per category, sorted: `dot-plot` or `lollipop`.

## Evidence

- The measure axis is position on a common scale (Cleveland and McGill 1984) and no point is occluded, so individual lookups are accurate; the packing direction carries no data. Adoption across Observable Plot (dodge), Flourish, seaborn and ggbeeswarm is broad practitioner consensus: `medium`.
- FT Visual Vocabulary caveat for dot strips: too many dots at the same value hide each other, which the swarm fixes by design.
- No study compares beeswarm with jittered strip for accuracy; the argument is occlusion.

## Accessibility

- Grey for the field, one saturated colour plus a text label for highlighted units; never colour-only identity.
- Markers at least 4 px with a 1 px darker outline so adjacent dots separate.
- Text alternative: "Beeswarm of <measure> for <n> <units>; most cluster between A and B; <unit> sits at C, the highest."
- Keep the measure axis labelled with units; the other axis has no scale and should have no ticks.

## Build

### mermaid

Not drawable in Mermaid. Render with the matplotlib target and link the image.

### vega-lite

No dodge in Vega-Lite; a jittered `point` (`"calculate": "random()"` into `yOffset`) is a `strip`, not a swarm. A real swarm needs full Vega's `force` transform with `collide`, which vl-convert also renders (`vega_to_svg`). Hand-written; substantial work, hence `approx`.

### plotly

No swarm layout; `px.strip(df, x="value", y="group")` gives a jittered strip, which is the usual stand-in. For a true swarm, compute positions in Python (`seaborn.swarmplot` collections' offsets, or a simple greedy packer) and plot them as a `scatter` trace with `mode: "markers"`. Hand-written.

### chartjs

No layout transform; a jittered scatter is possible but a swarm is not worth hand-packing here. Render an image with the matplotlib target.

### matplotlib

`seaborn.swarmplot(data=df, x="group", y="value", size=4, ax=ax)` computes the packing; add `hue="highlight"` with a two-colour palette to pick out units and `ax.annotate` for labels. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`. seaborn warns when points cannot fit; reduce `size` or fall back to `stripplot`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
