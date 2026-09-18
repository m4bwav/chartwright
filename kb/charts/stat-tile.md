---
name: Stat tile
slug: stat-tile
aliases: [KPI tile, big number, KPI card, metric card, number card, scorecard, indicator]
family: single-value
also: [magnitude, change-over-time]
question: What is the current value, and how has it changed?
shapes: ["q", "q,q", "time,q"]
goals: [single value, kpi, metric, big number, headline number, current value, latest, change since, delta, dashboard, tile, card, score]
max_series: 1
max_categories: 0
evidence: medium
popularity: rising
status: stable
support:
  mermaid: approx
  vega-lite: native
  plotly: native
  chartjs: none
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://www.datawrapper.de/blog/chart-types-guide, https://plotly.com/javascript/indicator/, https://vega.github.io/vega-lite/docs/text.html, https://journals.sagepub.com/doi/10.1177/15291006211051956]
---

# Stat tile

## When to use

- One number is the message: revenue this quarter, active users today, uptime; Datawrapper's "simple text" advice, when a chart would only decorate a single value.
- The number needs context in the same glance: the change against the previous period (delta with sign and unit) and, when the trend matters, a `sparkline` of the recent history.
- Dashboards with a row of 3 to 6 tiles, each answering one question, ordered by importance.
- Report openings: the headline number above the chart that explains it.
- Excels at: speed; a reader takes in a big number and its direction faster than any chart.

## When not to use

- Several comparable values (revenue by region): a row of tiles hides the comparison; use a `bar`.
- A delta without its baseline or period ("up 12 percent" of what, since when): the tile misleads; always name the comparison.
- A value that needs distribution or uncertainty context: a tile states false precision; show the `boxplot` or `range-band`.
- Progress against a target with thresholds: use a `bullet`, which keeps the number and adds the target.
- Red and green deltas as the only sign encoding: colour-blind readers see nothing; use the sign, an arrow, and the words.

## Substitutes

- Progress to a target: `bullet`.
- The recent shape matters more than the current value: `sparkline` with the last value labelled, or a `line`.
- Several metrics side by side: `table` with a sparkline column.
- Comparison across categories: `bar`.

## Evidence

- Reading a printed number is exact; the tile's value adds nothing perceptual and loses nothing. `medium`: practitioner consensus (Datawrapper, Few's dashboard design, the dataviz skill's stat tile guidance) rather than a perception study; what would change the verdict is evidence on how readers misjudge deltas without baselines.
- Franconeri et al. 2021: a single global statistic is extracted fast; the risk is in comparison, so the delta needs an explicit reference period and the sparkline needs a consistent time window across tiles.
- Rising across BI tools and AI dashboards (2026-09-17 taxonomy research section 1.3).

## Accessibility

- The value, unit, comparison period and delta are all text: "USD 4.2 m, up 12 percent vs Q1". Screen readers get the whole tile without extra work.
- Delta sign shown three ways: sign character, arrow, and word (up, down); colour is the fourth, from a colour-blind-safe pair.
- Sparkline is decorative (`aria-hidden`) with its trend described in the delta text.
- Text size: value at least 24 px, label at least 14 px, 4.5:1 contrast.
- Tiles in a row share the same time window and the same number format.

## Build

### mermaid

`approx`: not a Mermaid diagram; write it as markdown, which every Mermaid host renders:

```markdown
### Revenue, Q2 2026
**USD 4.2 m** (up 12 percent vs Q1)
```

For a sparkline in plain markdown, append block characters: `▁▂▃▄▅▆▇█` mapped over the last 8 values. Hand-written.

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "width": 200, "height": 90,
 "data": {"values": [{"label": "Revenue, Q2 2026", "value": "USD 4.2 m", "delta": "up 12% vs Q1"}]},
 "layer": [{"mark": {"type": "text", "fontSize": 32, "fontWeight": "bold", "dy": -10}, "encoding": {"text": {"field": "value"}}},
           {"mark": {"type": "text", "fontSize": 13, "dy": 22}, "encoding": {"text": {"field": "delta"}}},
           {"mark": {"type": "text", "fontSize": 13, "dy": -42, "color": "#555"}, "encoding": {"text": {"field": "label"}}}],
 "config": {"view": {"stroke": null}}}
```

Hand-written; add a `line` layer with `"width": 200, "height": 30` below via `vconcat` for the sparkline (see `sparkline`). Render with `cw.py render --target vega-lite --in chart.vl.json --out chart.svg`.

### plotly

`{"type": "indicator", "mode": "number+delta", "value": 4.2, "number": {"prefix": "USD ", "suffix": " m"}, "delta": {"reference": 3.75, "relative": true}, "title": {"text": "Revenue, Q2 2026"}}`. Hand-written; open with `cw.py render --target plotly --in fig.json --out chart.html`.

### matplotlib

`fig, ax = plt.subplots(figsize=(3, 1.4)); ax.axis("off"); ax.text(0, 0.9, "Revenue, Q2 2026", fontsize=11, color="0.3"); ax.text(0, 0.45, "USD 4.2 m", fontsize=26, fontweight="bold"); ax.text(0, 0.1, "up 12% vs Q1", fontsize=11)`; an inset `ax.inset_axes([0.6, 0.1, 0.4, 0.4]).plot(history)` adds the sparkline. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`. In a web page, plain HTML beats an image.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. The bundled `dataviz` skill has its own stat tile guidance for artifacts; defer to it when that skill is loaded.
