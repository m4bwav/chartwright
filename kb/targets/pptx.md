---
name: PowerPoint native chart (python-pptx)
slug: pptx
kind: office
renders_in: [PowerPoint, Keynote and Google Slides (imported .pptx), LibreOffice Impress]
version_checked: "python-pptx 1.0.2"
last_verified: 2026-09-18
renderer: python
sources: [https://python-pptx.readthedocs.io/en/latest/user/charts.html, https://python-pptx.readthedocs.io/en/latest/api/enum/XlChartType.html]
---

# PowerPoint native chart (python-pptx)

Pick this when the deck must stay editable: the chart is a real Office chart object whose data, colours and labels the reader can change in PowerPoint. For any type outside the native list, insert a PNG from the vega-lite target instead (`slide.shapes.add_picture`).

## What it can draw

| chart | support | note |
|---|---|---|
| bar, column, grouped-bar, stacked-bar, stacked-bar-100, line, multi-line, area, stacked-area, pie, donut, radar, scatter, bubble | native | `XL_CHART_TYPE` members BAR_CLUSTERED, COLUMN_CLUSTERED, COLUMN_STACKED, COLUMN_STACKED_100, LINE_MARKERS, AREA, AREA_STACKED, PIE, DOUGHNUT, RADAR, XY_SCATTER, BUBBLE; all covered by `cw.py build --target pptx` |
| step, lollipop, dumbbell, diverging-bar, waterfall, bullet, slope, range-band, error-bars | approx | composed from clustered or stacked series with transparent fills, or a line with markers; hand-written |
| everything else (treemap, sunburst, funnel, waterfall as chartex, histogram, box, sankey, maps) | image | PowerPoint's own chartex types are not writable by python-pptx; add a PNG |

## Syntax essentials

```python
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches
prs = Presentation(); slide = prs.slides.add_slide(prs.slide_layouts[5])
data = CategoryChartData(); data.categories = ["North", "South", "East"]
data.add_series("Sales", [200, 225, 130])
chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.7), Inches(1.5), Inches(8.6), Inches(5), data).chart
prs.save("chart.pptx")
```

- Scatter and bubble use `XyChartData` / `BubbleChartData` with `add_series(name).add_data_point(x, y[, size])`.
- Colours: `plot.series[i].format.fill.solid(); .fore_color.rgb = RGBColor(0x2a, 0x78, 0xd6)`; data labels: `plot.has_data_labels = True`, `plot.data_labels.number_format`.
- Add to an existing deck: `Presentation("deck.pptx")` and pick the slide; charts keep their data sheet embedded, so the reader can edit numbers in PowerPoint.

## Limits

- No chartex types (waterfall, funnel, treemap, sunburst, histogram, box), no per-point colour on line charts, no annotations beyond data labels.
- Category axes only for bar and line (a date axis needs `chart.category_axis` tweaks); time series work as category labels.
- `pip install python-pptx` is required to run the generated script.

## Render

- `cw.py build --chart column --target pptx --data sales.csv --x region --y sales --series product --out chart.py --png chart.pptx` writes the script; `cw.py render --target pptx --in chart.py --out chart.pptx` runs it. Open the .pptx to check; python-pptx cannot rasterise.

## Notes

- 2026-09-18: added from the 2026-09-17 library research (python-pptx 1.0.2 chart API).
