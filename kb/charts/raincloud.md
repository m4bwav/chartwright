---
name: Raincloud plot
slug: raincloud
aliases: [rain cloud plot, half violin with points, cloud and rain plot]
family: distribution
also: [deviation]
question: What is the shape, the summary and every raw value of a numeric variable in each group, all at once?
shapes: ["n,q", "o,q"]
goals: [distribution, raw data, transparency, shape and summary, compare groups, scientific, replication, raincloud]
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
  matplotlib: approx
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
  xlsx: image
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://discovery.ucl.ac.uk/id/eprint/10178652/, https://github.com/pog87/PtitPrince, https://github.com/njudd/ggrain, https://plotly.com/python/violin/, https://vega.github.io/vega-lite/docs/layer.html]
---

# Raincloud plot

## When to use

- Scientific or analytical reporting where readers expect to see the raw data, not only a summary (Allen et al. 2019 proposed it for exactly this).
- Moderate n per group (20 to a few hundred): enough for a density, few enough that the points stay distinguishable.
- Up to about eight groups; each needs horizontal room for cloud, box and rain.
- Comparing conditions in an experiment, before-and-after measurements, or benchmark runs.
- Excels at: one panel that answers "shape?", "median and spread?" and "any odd points?" without three charts.

## When not to use

- Large n (thousands): the rain saturates into a bar; thin the points, sample, or drop to `violin` with a box.
- Small n (under about 15): the cloud is a fiction; keep the rain and the box, drop the density (that is a `strip` with a box).
- Narrow layouts or many groups: the three parts compress and the plot becomes noise; use `boxplot`.
- General audiences: three encodings in one glyph need a caption explaining each part.
- Where a single number is the message: a dot with an interval is enough.

## Substitutes

- Many groups, summary only: `boxplot`.
- Shape only: `violin`, `density`.
- Raw values only, small n: `strip`, `beeswarm`.
- Many ordered groups: `ridgeline`.
- Mean with an interval: `error-bars`.

## Evidence

- Allen et al. 2019 (Wellcome Open Research) argue from the error-bar literature (Correll and Gleicher 2014) and the "same stats, different graphs" problem that summary glyphs mislead and raw data plus distribution is more robust; one paper plus fast uptake in R, Python, JASP and MATLAB: `medium`.
- The half violin inherits the density bandwidth caveat; the points inherit the overplotting caveat of `strip`.
- No study measures reading accuracy of the combined glyph against its parts; the case is transparency, not measured accuracy.

## Accessibility

- Label the three parts once in the caption: "cloud = density, box = median and middle half, rain = individual values".
- Use a jitter for the rain that is deterministic (seeded) so re-renders match; hollow or semi-transparent markers so overlap shows.
- One fill colour per group with the group named on the axis; colour is not needed to identify anything.
- Text alternative: "Raincloud plot of <measure> by <group>, n = <n> each; <group A> median X with a right skew and two outliers above Y; <group B> median Z, symmetric."
- 3:1 contrast for the box lines and markers; markers at least 4 px.

## Build

### mermaid

Not drawable in Mermaid. Render with the matplotlib target and link the image.

### vega-lite

Three layers per group: a density transform drawn as a half-width `area` (see `violin`), a `boxplot` mark offset with `xOffset`, and a `point` mark with a jitter from a `calculate` transform (`"calculate": "random()"`). Put the layers in a `column` facet by group. Hand-written and lengthy, hence `approx`; the matplotlib target is the quicker route to an image.

### plotly

Per group, a `violin` trace with `side: "positive"`, `box: {visible: true}`, `points: "all"`, `pointpos: -1.2`, `jitter: 0.3`, `width: 1.2` and `orientation: "h"`: Plotly's violin already draws the points beside the density, so this is the closest built-in form. Hand-written.

### chartjs

No density primitive and no jitter helper; the composition is not worth doing in Chart.js. Render an image with the matplotlib target.

### matplotlib

`ptitprince.RainCloud(x="group", y="value", data=df, orient="h", width_viol=0.6, ax=ax)` (pip `ptitprince`, wraps seaborn). Plain seaborn: `sns.violinplot(..., inner=None, cut=0)` then clip each violin body to its left half, `sns.boxplot(..., width=0.15)`, `sns.stripplot(..., jitter=0.15, alpha=0.5)` on the same axes with a small offset. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`. Add-on composition, hence `approx`.

### echarts

Hand-written: custom violin series plus `scatter` jitter plus `boxplot`. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
