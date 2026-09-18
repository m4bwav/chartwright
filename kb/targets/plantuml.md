---
name: PlantUML chart (@startchart)
slug: plantuml
kind: markdown
renders_in: [PlantUML 1.2026.0+, Kroki, IntelliJ and VS Code PlantUML plugins, Confluence (PlantUML app), Asciidoctor Diagram]
version_checked: "PlantUML 1.2026.0 (chart diagram introduced), checked 2026-09-18"
last_verified: 2026-09-18
renderer: plantuml
tested: untested
sources: [https://plantuml.com/chart-diagram, https://kroki.io]
---

# PlantUML chart (@startchart)

Pick this when the document already speaks PlantUML (Asciidoctor, Confluence with the PlantUML app, IntelliJ docs, a repo whose diagrams are `.puml`) and a plain bar, line, area or scatter is enough. Outside those hosts Mermaid reaches more readers.

## What it can draw

| chart | support | note |
|---|---|---|
| bar, column, grouped-bar, stacked-bar, line, multi-line, sparkline, area, stacked-area, scatter | native | `bar`, `line`, `area`, `scatter` series on `h-axis` / `v-axis`; several series share the axes; `stackMode stacked` for stacks (stack keyword not verified against a live render); all built by `cw.py build --target plantuml` |
| gantt, tree | native | PlantUML's own `@startgantt` and `@startmindmap` / `@startwbs`, not `@startchart` |
| step, lollipop, connected-scatter, range-band, dot-plot, bubble, timeline, dendrogram, network | approx | composed from the four series types or from other PlantUML diagrams; see each chart's recipe |
| pie, donut, and everything else | none | `@startchart` has no pie; use Mermaid `pie` or an image target |

## Syntax essentials

```plantuml
@startchart
title "Revenue by quarter"
h-axis [Q1, Q2, Q3, Q4]
v-axis "Revenue" 0 --> 100
bar "2025" [45, 62, 58, 70]
bar "2026" [50, 66, 61, 80]
legend right
@endchart
```

- `h-axis` takes category labels in brackets or a numeric range `0 --> 100`; `v-axis "label" min --> max`; `v2-axis` adds a second scale (avoid: dual axes mislead).
- Series: `bar "name" [values]`, `line "name" [values]` or `line "name" [(x1,y1), (x2,y2)]`, `area "name" [...]`, `scatter "name" [(x,y), ...]`; an optional colour `#3498db` after the values.
- Always give the value axis an explicit `0 --> max` for bars.

## Limits

- No pie, treemap, heatmap, box or any statistical mark; no legend interaction; styling is limited to colours.
- New in 1.2026.0: older PlantUML servers (Confluence Cloud app, some IDE bundles) reject `@startchart`; check the host version first.
- No native GitHub or GitLab rendering; the block is text until a PlantUML renderer runs.

## Render

- `cw.py build --chart bar --target plantuml --data sales.csv --x region --y sales --out chart.puml` then `cw.py render --target plantuml --in chart.puml --out chart.svg` when `plantuml` is on PATH; otherwise the command prints a Kroki URL (`https://kroki.io/plantuml/svg/<deflate+base64url>`) that renders the same text.

## Notes

- 2026-09-18: added from the 2026-09-17 library research; syntax read from plantuml.com/chart-diagram on 2026-09-18. Not yet rendered live on this machine (no PlantUML installed).
