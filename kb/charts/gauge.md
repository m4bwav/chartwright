---
name: Gauge
slug: gauge
aliases: [meter, speedometer chart, dial chart, radial gauge, angular gauge, progress dial]
family: single-value
also: [deviation, magnitude]
question: Where does one value sit within a fixed range, shown as a dial?
shapes: ["q", "q,q"]
goals: [single value, gauge, meter, dial, speedometer, percent of target, utilisation, score out of, level, dashboard, progress]
max_series: 1
max_categories: 0
evidence: low
popularity: declining
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: native
  chartjs: approx
  matplotlib: approx
  terminal: none
  echarts: native
  pptx: image
  quickchart: approx
  xlsx: image
  gdocs: image
  docx: image
  gsheets: image
  observable-plot: none
  d2: none
  plantuml: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://plotly.com/javascript/gauge-charts/, https://datavizcatalogue.com/methods/gauge.html, https://www.chartjs.org/docs/latest/charts/doughnut.html, https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary]
---

# Gauge

## When to use

- Only when a client or a house style demands the dial for one bounded value (CPU at 72 percent, satisfaction 4.2 of 5) on an operational dashboard, and the audience already reads gauges.
- One value, one fixed range, at most three coloured bands with thresholds set in advance; the number printed large in the centre.
- Never more than a few on one screen; they are large for the single number they show.
- Prefer the `bullet` for every serious audience; this file exists so the request is understood and redirected.

## When not to use

- Any report or analysis: the angle encoding is imprecise, the dial wastes space, and readers cannot compare several gauges (guides from the FT to Datawrapper and Few discourage it; the 2026-09-17 taxonomy research lists it as declining).
- Several metrics side by side: a row of dials cannot be compared; use `bullet` rows or a `bar`.
- A value with no natural bounds or with no thresholds: the arc implies a scale that is arbitrary.
- Trend or history: a gauge has no time; use a `stat-tile` with a sparkline or a `line`.
- Traffic-light colouring as the only cue: colour-blind readers see one arc.

## Substitutes

- Actual against target with bands: `bullet` (the default replacement).
- The number and its change: `stat-tile`.
- Share of a whole: `donut` with the value in the hole, which at least uses arc length.
- Several bounded values: `bar` with a reference line at the target.
- Progress over time: `line` with the target as a rule.

## Evidence

- `low`: angle and radial position rank below aligned position and length (Cleveland and McGill 1984; Heer and Bostock 2010), and no study shows the dial adding anything the printed number lacks. The rating rests on the encoding and on the practitioner consensus against the form (Few; FT; Datawrapper).
- Skau and Kosara 2016 found pie readers use arc length rather than angle; a gauge is a partial pie, so what readers actually use is the arc's length, which a straight bar does better.
- What would change the verdict: evidence that the dial metaphor speeds comprehension for operational monitoring; none was found in the 2026-09-17 research.

## Accessibility

- The value printed as text at the centre with its unit and the range ("72 percent of 100"); the arc is decoration and `aria-hidden`.
- Bands in three steps of one grey plus a black needle or a saturated arc; never red, amber and green alone.
- Text alternative: "Gauge showing <measure> at <value> on a scale of <min> to <max>, in the <band> band."
- Minimum size 120 px across so the needle position is legible; label the range ends.

## Build

### mermaid

`image`: Mermaid has no gauge or partial pie. Link an image rendered with plotly (via kaleido) or matplotlib, or write the value as a `stat-tile` in markdown, which is the better answer.

### vega-lite

`approx`: two `arc` marks with `theta` and `theta2` in radians over a half circle (`-PI/2` to `PI/2`), the background arc for the range and the foreground arc for the value, plus a `text` mark for the number. No needle primitive. Hand-written; render with `cw.py render --target vega-lite --in chart.vl.json --out chart.svg`.

### plotly

`{"type": "indicator", "mode": "gauge+number", "value": 72, "gauge": {"axis": {"range": [0, 100]}, "bar": {"color": "#0072B2"}, "steps": [{"range": [0, 50], "color": "#eee"}, {"range": [50, 80], "color": "#ddd"}, {"range": [80, 100], "color": "#ccc"}], "threshold": {"value": 90, "line": {"color": "black", "width": 3}}}, "title": {"text": "CPU (%)"}}`. Native; hand-written and opened with `cw.py render --target plotly --in fig.json --out chart.html`.

### chartjs

`approx`: a `doughnut` with `circumference: 180`, `rotation: 270`, `cutout: "70%"` and two data values `[value, max - value]` in a colour and a light grey; the number is drawn with a small custom plugin or an HTML overlay. The community `chartjs-gauge` plugin adds a needle; maintenance varies. Hand-written.

### matplotlib

`approx`: on a polar axes with `ax.set_thetamin(0); ax.set_thetamax(180)`, draw band arcs with `ax.barh(1, width, left=start, height=0.3, color=grey)` in radians and a needle with `ax.plot([theta, theta], [0, 1.1], color="black", linewidth=3)`, hide the polar grid, and `ax.text(0, 0, "72%")` at the centre. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`.

### echarts

Hand-written: series type `gauge` (the knowledge base prefers `bullet`). See `kb/targets/echarts.md`.

### quickchart

Approximate: QuickChart `gauge` / `radialGauge` plugin types; write the Chart.js config by hand and URL-encode it (see `kb/targets/quickchart.md`).

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. Marked `declining`; `cw.py pick` should rank `bullet` above it for the same question unless the request names a gauge explicitly.
