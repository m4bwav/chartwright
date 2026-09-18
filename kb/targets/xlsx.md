---
name: Excel native chart (openpyxl)
slug: xlsx
kind: office
renders_in: [Excel, LibreOffice Calc, Google Sheets (imported .xlsx)]
version_checked: "openpyxl 3.1.5"
last_verified: 2026-09-18
renderer: python
tested:
  - Windows 2026-09-18: openpyxl script rendered a workbook; not opened in Excel
sources: [https://openpyxl.readthedocs.io/en/stable/charts/introduction.html]
---

# Excel native chart (openpyxl)

Pick this when the reader wants the numbers and an editable chart in one workbook. The data lands on a sheet and the chart references it, so edits in Excel update the chart.

## What it can draw

| chart | support | note |
|---|---|---|
| bar, column, grouped-bar, stacked-bar, stacked-bar-100, line, multi-line, area, stacked-area, pie, donut, radar, scatter, bubble | native | BarChart (type bar/col, grouping stacked/percentStacked), LineChart, AreaChart, PieChart, DoughnutChart, RadarChart, ScatterChart, BubbleChart; all covered by `cw.py build --target xlsx` |
| candlestick, range-band, step, lollipop, dumbbell, diverging-bar, waterfall, bullet | approx | StockChart for OHLC; stacked bars with transparent series for waterfall and bullet; hand-written |
| everything else (treemap, sunburst, histogram, box, sankey, maps, funnel) | image | Excel's chartex types are not writable by openpyxl; insert a PNG with `openpyxl.drawing.image.Image` |

## Syntax essentials

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
wb = Workbook(); ws = wb.active
ws.append(["region", "sales"]); ws.append(["North", 200]); ws.append(["South", 225]); ws.append(["East", 130])
chart = BarChart(); chart.type = "col"; chart.title = "Sales by region"
chart.add_data(Reference(ws, min_col=2, min_row=1, max_row=4), titles_from_data=True)
chart.set_categories(Reference(ws, min_col=1, min_row=2, max_row=4))
ws.add_chart(chart, "D2"); wb.save("chart.xlsx")
```

- Stacked: `chart.grouping = "stacked"` (or `"percentStacked"`) and `chart.overlap = 100`.
- Scatter: `Series(yref, xref, title_from_data=True)` per series; `chart.style` picks a built-in style.
- Colours: `series.graphicalProperties.solidFill = "2A78D6"`; axis titles via `chart.x_axis.title`.

## Limits

- No chartex types, no annotations, limited label control; dates on a category axis are labels unless a date axis is configured.
- `pip install openpyxl` to run the generated script; openpyxl cannot rasterise, so open the workbook to check.

## Render

- `cw.py build --chart column --target xlsx --data sales.csv --x region --y sales --series product --out chart.py --png chart.xlsx` then `cw.py render --target xlsx --in chart.py --out chart.xlsx`.

## Notes

- 2026-09-18: added from the 2026-09-17 library research (openpyxl 3.1.5 chart module).
