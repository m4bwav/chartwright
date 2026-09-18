---
name: Chart as a URL image (QuickChart)
slug: quickchart
kind: image
renders_in: [any place that shows an image URL: chat messages, Slack, email, GitHub comments, Notion, wikis]
version_checked: "quickchart.io hosted API, Chart.js 4 via version=4; typpo/quickchart AGPL-3.0 for self-hosting"
last_verified: 2026-09-18
renderer: none
sources: [https://quickchart.io/documentation/, https://github.com/typpo/quickchart]
---

# Chart as a URL image (QuickChart)

The zero-install image path: a Chart.js config in a URL, rendered remotely to PNG (or SVG, WebP, PDF) when the URL is opened. About 80 to 200 tokens for a whole chart in a chat message, and nothing to run locally. The data travels in the URL, so it is public to anyone holding the link; never use it for confidential numbers.

## What it can draw

| chart | support | note |
|---|---|---|
| line, multi-line, area, step, bar, column, grouped-bar, stacked-bar, pie, donut, scatter, bubble, radar, polar-area | native | whatever `cw.py build --target chartjs` produces; `cw.py build --target quickchart` wraps it |
| sparkline, progress bar, gauge, radial gauge, sankey, boxplot, violin, histogram, treemap | approx | QuickChart ships extra Chart.js plugins (sparkline, progressBar, gauge, radialGauge, sankey, boxplot, violin, treemap) documented on quickchart.io; hand-written config |
| everything else | none | use the vega-lite target and attach the PNG |

## Syntax essentials

```
https://quickchart.io/chart?version=4&w=800&h=400&c=<url-encoded Chart.js config>
```

- `version=4` selects Chart.js 4; `format=svg|webp|pdf`; `bkg=white`; `devicePixelRatio=2` for sharp images.
- Long configs (over about 2 kB) should use the POST endpoint `https://quickchart.io/chart/create`, which returns a short URL.
- Markdown: `![title](url)`; Slack and email accept the URL directly.
- Self-host with Docker (`ianw/quickchart`) when data must not leave the network (AGPL-3.0 applies to modifications of the server).

## Limits

- Data in the URL is visible and may be logged by intermediaries; hosted service has rate limits and a URL length cap.
- Requires network at view time; a broken link shows nothing, so for documents that must last, download the PNG and embed it.
- Chart.js accessibility limits apply (a raster image; write the text alternative in the alt text).

## Render

- `cw.py build --chart line --target quickchart --data prices.csv --x date --y price` prints the markdown image line with the URL. Fetch the PNG to keep a local copy: `curl -o chart.png "<url>"` (or `python -c "import urllib.request,sys; urllib.request.urlretrieve(sys.argv[1], 'chart.png')" "<url>"`).

## Notes

- 2026-09-18: added from the 2026-09-17 library research; verified with a live fetch (HTTP 200, image/png).
