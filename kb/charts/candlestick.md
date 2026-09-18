---
name: Candlestick chart
slug: candlestick
aliases: [OHLC chart, open-high-low-close, stock chart, price bars, Japanese candlestick]
family: change-over-time
also: [distribution]
question: What were the open, high, low and close of a traded price in each period?
shapes: ["time,q,q,q,q", "time,q+"]
goals: [candlestick, OHLC, stock price, trading, open high low close, daily range, ticker, volatility, market data]
max_series: 1
max_categories: 0
evidence: low
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: native
  plotly: native
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: native
  pptx: image
  quickchart: none
  xlsx: approx
  gdocs: image
  docx: image
  gsheets: native
  observable-plot: approx
  d2: none
  plantuml: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://vega.github.io/vega-lite/examples/layer_candlestick.html, https://plotly.com/javascript/candlestick-charts/, https://github.com/chartjs/chartjs-chart-financial]
---

# Candlestick chart

## When to use

- Traded prices (shares, currencies, commodities, crypto) for readers who know the convention: each period is a body from open to close and a wick from low to high.
- Intraday range and direction per period matter, not just the closing level: volatility, gaps, reversals.
- Roughly 20 to 200 periods; fewer looks empty, more turns into a smear.
- Paired with a volume `column` panel below sharing the x axis, which is the standard layout.
- Excels at: four numbers per period in one glyph, direction by colour, all on one price scale.

## When not to use

- General audiences or a narrative about the level: a `line` of the close is read faster and more accurately.
- Long spans at daily resolution (years): aggregate to weekly or monthly candles, or use a line.
- Comparing several instruments: candles cannot overlay; use indexed `line` charts.
- Non-financial data with a min, max and mean: that is `error-bars` or a `range-band`, and the open/close semantics would mislead.
- A markdown host: no text chart syntax draws it; render an image.

## Substitutes

- Closing level over time: `line`.
- Range per period without direction: `range-band` (low to high) with the close as a line.
- Several instruments compared: `line` indexed to 100.
- Distribution of daily returns: `histogram` or `boxplot` per month.
- Volume per period: `column` under the price chart.

## Evidence

- No perception study measures candlestick reading against alternatives; the encoding mixes position (the wick ends), length (the body) and colour (direction), and the form is a trading convention from technical analysis. Rating `low`: use it because the audience expects it, not because it reads better.
- The Financial Times Visual Vocabulary lists it under change over time with the caveat that it is for specialist readers.
- What would raise the rating: a study showing practitioners read direction and range from candles more accurately than from OHLC bars or lines.

## Accessibility

- Direction needs more than red and green: use hollow versus filled bodies (or two colour-blind-safe hues such as blue and orange) and say which is which in the caption.
- Bodies at least 3 px wide; wicks 1 px but with 3:1 contrast.
- Text alternative: "Candlestick chart of <ticker> from <start> to <end>; it opened the span at A and closed at B, high of H on <date>, low of L on <date>." Provide the OHLC table.
- Tooltips on every candle in interactive targets; static images need the key dates annotated.

## Build

### vega-lite

```json
{"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "data": {"url": "ohlc.csv"},
 "encoding": {"x": {"field": "date", "type": "temporal"},
              "color": {"condition": {"test": "datum.open < datum.close", "value": "#0072B2"}, "value": "#D55E00"}},
 "layer": [
  {"mark": "rule", "encoding": {"y": {"field": "low", "type": "quantitative", "scale": {"zero": false}}, "y2": {"field": "high"}}},
  {"mark": "bar", "encoding": {"y": {"field": "open", "type": "quantitative"}, "y2": {"field": "close"}}}]}
```

Hand-written from the gallery example (`layer_candlestick`); no builder. `"scale": {"zero": false}` on the price axis is required.

### plotly

`{"type": "candlestick", "x": dates, "open": [...], "high": [...], "low": [...], "close": [...], "increasing": {"line": {"color": "#0072B2"}}, "decreasing": {"line": {"color": "#D55E00"}}}`; `layout.xaxis.rangeslider.visible = false` unless the slider is wanted. `type: "ohlc"` gives the bar variant. Hand-written.

### chartjs

`approx`: needs the community plugin `chartjs-chart-financial` (`type: "candlestick"`, data points `{x, o, h, l, c}`) plus a date adapter; maintenance is thin. Prefer plotly or vega-lite when the page is free to choose.

### matplotlib

`ax.vlines(dates, low, high, color="grey", linewidth=1)` then `ax.bar(dates, close - open, bottom=open, width=0.6, color=[up if c >= o else down for o, c in zip(open, close)])`; or `pip install mplfinance` and `mpf.plot(df, type="candle", volume=True, savefig="chart.png")`. Hand-written, then `cw.py render --target matplotlib --in chart.py --out chart.png`.

Markdown hosts: render the vega-lite spec to SVG and link it.

### echarts

Hand-written: series type `candlestick` with [open, close, low, high] rows. See `kb/targets/echarts.md`.

### xlsx

Approximate: StockChart with open/high/low/close series.

### observable-plot

`Plot.ruleX(data, {x: "date", y1: "low", y2: "high"})` under `Plot.ruleX({y1: "open", y2: "close", stroke: d => d.close > d.open ? "green" : "red", strokeWidth: 4})`.

### gsheets

`candlestickChart` with `domain` and one `data` entry of `lowSeries`, `openSeries`, `closeSeries`, `highSeries` ranges.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
