---
name: Google Sheets native chart (Sheets API EmbeddedChart)
slug: gsheets
kind: office
renders_in: [Google Sheets, Google Docs and Slides (linked Sheets chart)]
version_checked: "Sheets API v4 ChartSpec: basicChart, pieChart, bubbleChart, candlestickChart, orgChart, histogramChart, waterfallChart, treemapChart, scorecardChart (checked 2026-09-18)"
last_verified: 2026-09-18
renderer: none
sources: [https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/charts, https://developers.google.com/workspace/sheets/api/samples/charts]
---

# Google Sheets native chart (Sheets API EmbeddedChart)

Pick this when the reader lives in Google Sheets, or when a Google Doc or Slide needs a chart that stays editable and linked to its data. A Sheets chart is an `EmbeddedChart` created by `spreadsheets.batchUpdate` with an `addChart` request whose `spec` references cell ranges; the data must be in the sheet first.

## What it can draw

| chart | support | note |
|---|---|---|
| bar, column, grouped-bar, stacked-bar, stacked-bar-100, line, multi-line, area, stacked-area, step, scatter, pie, donut | native | `basicChart` (BAR, COLUMN, LINE, AREA, STEPPED_AREA, SCATTER with `stackedType` NOT_STACKED, STACKED, PERCENT_STACKED) and `pieChart` (`pieHole` for a donut); all built by `cw.py build --target gsheets` |
| bubble, candlestick, histogram, waterfall, treemap, stat-tile | native | `bubbleChart`, `candlestickChart`, `histogramChart`, `waterfallChart`, `treemapChart`, `scorecardChart`; hand-written specs, recipe in each chart file |
| tree, sparkline | approx | `orgChart` for a boxed hierarchy; the `SPARKLINE()` cell formula for in-cell sparklines |
| everything else | image | insert a PNG (`vega-lite` render) with `Insert > Image` or the Drive API; no radar, sankey, box or map chart in the API |

## Syntax essentials

```json
{"requests": [{"addChart": {"chart": {
  "spec": {"title": "Sales by region",
    "basicChart": {"chartType": "COLUMN", "stackedType": "NOT_STACKED", "legendPosition": "NO_LEGEND", "headerCount": 1,
      "axis": [{"position": "BOTTOM_AXIS", "title": "region"}, {"position": "LEFT_AXIS", "title": "sales"}],
      "domains": [{"domain": {"sourceRange": {"sources": [{"sheetId": 0, "startRowIndex": 0, "endRowIndex": 4, "startColumnIndex": 0, "endColumnIndex": 1}]}}}],
      "series": [{"series": {"sourceRange": {"sources": [{"sheetId": 0, "startRowIndex": 0, "endRowIndex": 4, "startColumnIndex": 1, "endColumnIndex": 2}]}}, "targetAxis": "LEFT_AXIS"}]}},
  "position": {"overlayPosition": {"anchorCell": {"sheetId": 0, "rowIndex": 0, "columnIndex": 4}, "widthPixels": 720, "heightPixels": 400}}}}}]}
```

- Ranges are `GridRange`s: zero-based, end indices exclusive, the header row included when `headerCount` is 1.
- One `series` entry per column; `pieChart` takes a single `domain` and `series`; `position.newSheet: true` puts the chart on its own sheet.
- Write the data first: `spreadsheets.values.update` with `range: "Sheet1!A1"` and `valueInputOption: USER_ENTERED`.

## Limits

- Needs the Sheets API (OAuth) or Apps Script; the Claude Drive connector can create a spreadsheet from CSV but cannot send `batchUpdate`, so in a connector-only session the chart is added by hand (Insert > Chart) after the data lands.
- Chart styling options are coarse; no annotations or reference lines beyond a series.
- Linking a Sheets chart into a Doc or Slide is manual (Insert > Chart > From Sheets) or through the Docs/Slides API `sheetsChartId`.

## Render

- `cw.py build --chart column --target gsheets --data sales.csv --x region --y sales --series product --out chart.json` writes `{"range": "A1", "values": [[...]], "requests": [{"addChart": ...}]}`: send `values` with `values.update`, then `requests` with `batchUpdate`. No local renderer; open the sheet to check.

## Notes

- 2026-09-18: added from the 2026-09-17 library research; spec shapes re-read from the Sheets API reference on 2026-09-18. The `addChart` request has not been sent against a live spreadsheet from this plugin yet.
