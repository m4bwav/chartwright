---
name: Terminal and plain chat (Unicode)
slug: terminal
kind: terminal
renders_in: [any terminal, chat replies with no image support, commit messages, log output, Slack code blocks]
version_checked: "Unicode block elements U+2581..U+2588 (no library); plotext 6.1.0 (2026-09) for full terminal plots"
last_verified: 2026-09-18
renderer: none
tested:
  - Windows 2026-09-18: sparklines and block bars printed with UTF-8 forced
sources: [https://github.com/piccolomo/plotext, https://github.com/mkaz/termgraph, https://en.wikipedia.org/wiki/Block_Elements]
---

# Terminal and plain chat (Unicode)

The cheapest target: about one token per data point, no renderer, readable anywhere monospace text shows. Use it for a quick answer in a chat reply, a status line, a commit or log summary, or when the reader asked for "just show me the trend" and no document is involved. Anything with more than one series or more than about 40 points belongs in another target.

## What it can draw

| chart | support | note |
|---|---|---|
| sparkline, line, area, step | native | eight-level block sparkline `▁▂▃▄▅▆▇█` with first, last, min and max printed beside it |
| bar, column | native | horizontal block bars, one row per category, value at the end |
| multi-line | approx | one sparkline per series, stacked vertically |
| table, stat-tile | approx | a markdown table or a single formatted number does the job |
| everything else | none | use an image |

## Syntax essentials

```
price by date
▁▂▁▅█▆  100 -> 112 (min 100, max 115, 6 points, 2026-01-01 to 2026-06-01)

sales by region
North  ███████████████████████████    200
South  ██████████████████████████████ 225
East   █████████████████              130
```

- `cw.py build --chart line --target terminal --data prices.csv --x date --y price` and `--chart bar` are the two recipes.
- A sparkline carries no scale: always print the endpoints and the range beside it, as the builder does.
- Wrap in a fenced code block in markdown so the monospace alignment survives.

## Limits

- No axes, no labels on points, no colour. Fine for a trend or a ranking of a few items; wrong for anything the reader must read values from.
- Fonts without Block Elements (rare) show boxes; Windows consoles need UTF-8 output (the CLI sets it).
- For real terminal plots (scatter, histogram, candlestick, datetime axes) `pip install plotext` and `plotext` draws them with braille and block characters.

## Render

Nothing to render: the text is the chart. Paste it into the reply or the file.

## Notes

- 2026-09-18: added as the sixth target; builder recipes for line/sparkline and bar/column, UTF-8 stdout forced on Windows.
