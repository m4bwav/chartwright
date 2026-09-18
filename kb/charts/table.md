---
name: Table
slug: table
aliases: [data table, heat table, table with bars, ranked table, sortable table, table as visualization]
family: table
also: [magnitude, ranking]
question: What are the exact values, across several measures per row, and where are the patterns?
shapes: ["n,q+", "n,text+", "n,q,text", "text"]
goals: [table, exact values, look up, precise, several measures, many columns, list, reference, sortable, numbers, heat table, ranked list]
max_series: 0
max_categories: 50
evidence: high
popularity: rising
status: stable
support:
  mermaid: approx
  vega-lite: approx
  plotly: native
  chartjs: none
  matplotlib: native
  terminal: approx
  echarts: none
  pptx: approx
  quickchart: none
  xlsx: image
  gdocs: image
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://www.datawrapper.de/blog/chart-types-guide, https://datavizcatalogue.com/methods/table.html, https://plotly.com/javascript/table/, https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.table.html, https://www.w3.org/WAI/tutorials/tables/]
---

# Table

## When to use

- Readers need exact values: prices, targets, dates, identifiers; a chart forces estimation where a number was wanted.
- Several measures per row (name, revenue, growth, margin, headcount): no single chart holds five measures readably; a sorted table does.
- Look-up tasks: the reader arrives with a category in mind and wants its row, not the overall pattern.
- Up to about 50 rows in a document; more needs sorting, search, or pagination in an interactive table.
- Add visual encodings inside the table when a pattern also matters: inline bars for one measure, a sequential fill (heat table) for another, sparklines for trend; the table stays the primary reading.
- Excels at: precision, many measures, and accessibility (the most screen-reader-friendly format).

## When not to use

- The message is a trend, a distribution, or a relationship: readers cannot see shape in a column of numbers; draw the `line`, `histogram`, or `scatter` and offer the table as the alternative.
- One measure across many categories where the ranking is the point: a sorted `bar` reads faster.
- Rainbow or red-green heat colouring as the only cue: the pattern is lost for colour-blind readers and the numbers must remain printed.
- Unsorted rows: a table in arbitrary order is a lookup only; sort by the measure the headline is about.
- Too many columns to fit: split into two tables or drop columns nobody will read.

## Substitutes

- One measure, ranking: `bar` or `lollipop`.
- Two measures, relationship: `scatter`.
- Many rows by many measures, pattern only: `heatmap`.
- One number: `stat-tile`.
- Every chart in this knowledge base should offer a table as its accessible alternative, so the table is also the universal fallback.

## Evidence

- Reading a printed number is exact, so for the lookup task nothing beats a table; Cleveland and McGill 1984's ranking applies to estimation, not to reading text, and the accuracy of a table for exact values is not in dispute, hence `high`.
- Inline bars and heat fills add length and colour encodings on top of the numbers: bars (length on a common baseline) are accurate for scanning; colour saturation is at the bottom of the ranking and shows only pattern, so keep the numbers printed.
- Datawrapper (Muth 2025) and Few both treat tables as the right answer when precise values or many measures matter; the 2026-09-17 taxonomy research lists table-as-visualisation as rising across editorial tools.
- Franconeri et al. 2021: sorting turns a lookup table into a fast ranking; alignment of decimal points makes magnitude comparison a shape task.

## Accessibility

- A real HTML table (`<table>`, `<th scope="col">`, a `<caption>`) or a markdown table, never an image of a table; screen readers navigate by cell.
- Numbers right-aligned with consistent decimals and thousands separators; text left-aligned; units in the header, not in every cell.
- Inline bars and heat fills are decoration; the value stays printed in the cell at 4.5:1 contrast against any fill (use light fills only).
- Row striping or 1 px rules so rows of 8 or more columns can be followed.
- Sortable interactive tables need keyboard-operable headers; state the current sort in the caption.

## Build

### mermaid

`approx`: not a Mermaid diagram; a markdown table renders on every Mermaid host:

```markdown
| Product | Revenue (USD m) | Growth |
|---|---:|---:|
| Alpha | 42.0 | +8% |
| Beta | 31.5 | -2% |
```

Sort rows before writing; a block-character bar column (`████░░`) gives an inline bar in plain markdown. Hand-written.

### vega-lite

`approx`: a table is `text` marks on a grid: `y` nominal by row, one `text` layer per column each with a fixed `"x": {"datum": ...}` position, plus a `rect` layer coloured by a value for a heat table or a thin `bar` layer for inline bars. Fine for a static heat table under 30 rows; no sorting or interaction. Hand-written; render with `cw.py render --target vega-lite --in chart.vl.json --out chart.svg`.

### plotly

`{"type": "table", "header": {"values": ["Product", "Revenue", "Growth"], "align": ["left", "right", "right"]}, "cells": {"values": [products, revenues, growths], "align": ["left", "right", "right"], "fill": {"color": [...]}}}`; `cells.fill.color` per column gives a heat table. Hand-written; open with `cw.py render --target plotly --in fig.json --out chart.html`. In a web page a plain HTML table is more accessible than the canvas-like table trace.

### matplotlib

`ax.axis("off"); tbl = ax.table(cellText=rows, colLabels=headers, loc="center", cellLoc="right"); tbl.auto_set_font_size(False); tbl.set_fontsize(9)`; colour cells with `tbl[(i, j)].set_facecolor(cmap(norm(value)))` for a heat table. Hand-written; run with `cw.py render --target matplotlib --in chart.py --out chart.png`. Prefer a real table in the host document whenever it supports one.

### terminal

A markdown table in a code block; sort it and right-align numbers.

### pptx

Approximate: a native table (`slide.shapes.add_table`), not a chart.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. Chart.js draws no tables (`none`); use HTML.
