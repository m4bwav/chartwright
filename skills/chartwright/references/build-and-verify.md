# Build and verify (chartwright Steps 3 to 5, full detail)

Read this when you are about to build. `CW` = `python "<plugin root>/scripts/cw.py"`.

## Pick the target

`kb/rules/choosing-a-target.md` has the full table. Short form:

| Destination | Target | Notes |
|---|---|---|
| Markdown file, GitHub, GitLab, Obsidian, Notion, wiki | `mermaid` when the type is native there (line, bar, pie, sankey, radar, quadrant, timeline, gantt); otherwise an SVG/PNG from `vega-lite`, linked | stay on the Mermaid 11.13 floor unless the host is known; `--flag namedSeries` on 11.16+ |
| Web page, dashboard, HTML report, artifact | `vega-lite` (default); `echarts` for sankey, chord, treemap, sunburst, gauge, large data, dark mode; `plotly` for candlestick, 3D, statistical traces; `chartjs` when the page already uses it | all get `--html` standalone pages |
| Word (.docx) | `docx` target: one-figure document from a Vega-Lite PNG at 2x with caption (python-docx); for a longer document render the PNG and place it with the snippet in `kb/targets/docx.md` or through the docx skill | Word charts cannot be written by python-docx; the picture is the chart |
| Slides, Slack, email, PDF | PNG at 2x from `vega-lite`; `matplotlib` for types outside it; `pptx` for an editable PowerPoint chart | these hosts reject or degrade SVG |
| Chat reply, terminal, commit message | `terminal` (block sparkline or bars) | one token per point |
| Excel workbook | `xlsx` (data sheet plus native chart) | editable in Excel |
| Google Sheet | `gsheets`: `values` plus an `addChart` request for the Sheets API (`batchUpdate`) | needs the Sheets API; connector-only sessions insert the chart by hand |
| Asciidoctor, Confluence or IntelliJ docs that already use PlantUML | `plantuml` (`@startchart`, 1.2026.0+) for bar, line, area, scatter | no pie; Mermaid reaches more hosts |
| Web page that wants the tersest SVG spec, Observable notebook or Framework site | `observable-plot` (`--html` for a page) | no polar marks, no headless PNG |
| A network or tree in a D2 document | `d2` (edges with labels) | D2 has no data charts at all |
| Google Doc | `gdocs`: new Doc from HTML with `quickchart` or hosted PNG images through the Drive connector; Docs API `insertInlineImage` for an existing Doc | no chart API; verify visually |
| Chat or email where an image URL works and the data is not confidential | `quickchart` | data travels in the URL |

If the destination is not obvious from the request or the open file, ask in one line.

## Untested targets and platforms (ask first)

Every target file carries `tested:` (also summarised in `kb/INDEX.md`): the platforms and dates on which its build and render were actually proven, or `untested`. Before building for a target, compare it with the user's platform (`python -c "import platform; print(platform.system())"` if unknown):

- If the target is `untested`, or has no entry for this platform, or the entry says the output was not opened in the destination program: say so in one line ("`plantuml` has not been tested anywhere yet" / "`pptx` has only been proven on Windows and the deck was never opened in PowerPoint") and ask whether to continue and, if it works, to record the result. Do not silently proceed and do not silently switch targets.
- On a yes: build, render, have the user open the output where it will be read, then `CW tested <target> --platform <OS> "<what was proven, versions>"` followed by `CW index`, and log a `C-` entry in the chartwright-curate CHANGELOG (path D). If it failed, fix or note the gap in the target file's Limits, and record the failure the same way so the next person does not repeat it.
- On a no: use the nearest tested target from the table above and say which.

The plugin was built on one Windows PC; macOS and Linux entries are what other users contribute. Untested is a status, not a warning off.

## Build

1. Builder first. `CW build --chart <slug> --target <target> --data file.csv --x <col> --y <col> [--series <col>] [--title "<the claim>"] --out <file> [--html] [--agg sum|mean|none] [--flag ...]`. Data goes from the file into the spec; duplicate x values are summed unless `--agg` says otherwise; `CW data` reports them first (`duplicate-keys`), since summing the same entity twice double-counts.
2. Builder coverage (anything else is hand-written from the chart file's recipe: `CW show <slug> --section build --target <target>`):
   - mermaid: line, multi-line, step, bar, column, area, grouped-bar (lossy), pie, donut, sankey, alluvial, quadrant, radar.
   - vega-lite: line, multi-line, step, bar, column, grouped-bar, stacked-bar, stacked-bar-100, area, stacked-area, scatter, bubble, heatmap, histogram, boxplot, pie, donut, strip, dot, lollipop, dumbbell, slope, waterfall, calendar-heatmap, diverging-bar, small-multiples, bullet, range-band, connected-scatter, bump.
   - echarts: line, multi-line, step, area, stacked-area, bar, column, grouped-bar, stacked-bar, stacked-bar-100, scatter, bubble, pie, donut, radar, funnel, sankey, alluvial, heatmap.
   - plotly: line, multi-line, step, area, stacked-area, scatter, bubble, bar, column, grouped-bar, stacked-bar, pie, donut, histogram, boxplot, heatmap, waterfall, dumbbell, bullet.
   - chartjs and quickchart: line, multi-line, area, step, bar, column, grouped-bar, stacked-bar, pie, donut, scatter, bubble, radar, polar-area.
   - matplotlib: line, multi-line, step, area, bar, column, grouped-bar, scatter, histogram, pie, donut, boxplot, waterfall, dumbbell, bullet.
   - pptx: bar, column, grouped-bar, stacked-bar, stacked-bar-100, line, multi-line, area, stacked-area, pie, donut, radar, scatter, bubble.
   - terminal: line, sparkline, area, step, bar, column.
   - xlsx: bar, column, grouped-bar, stacked-bar, stacked-bar-100, line, multi-line, area, stacked-area, pie, donut, radar, scatter, bubble.
   - gdocs: no builder; use quickchart URLs or PNGs inside HTML.
   - docx: everything vega-lite builds (the script renders the PNG and writes heading, picture, caption).
   - gsheets: bar, column, grouped-bar, stacked-bar, stacked-bar-100, line, multi-line, area, stacked-area, step, scatter, pie, donut.
   - plantuml: bar, column, grouped-bar, stacked-bar, line, multi-line, sparkline, area, stacked-area, scatter.
   - observable-plot: line, multi-line, sparkline, step, connected-scatter, area, stacked-area, column, bar, grouped-bar, stacked-bar, stacked-bar-100, diverging-bar, lollipop, dot-plot, scatter, bubble, strip, beeswarm, boxplot, histogram, heatmap, correlogram, adjacency-matrix, calendar-heatmap, waffle, small-multiples, density-2d, hexbin, slope.
   - d2: network, tree, dendrogram (x=source or child, series=target or parent).
3. Column roles for composed charts: dumbbell x=category y=first value `--y2` second value (wide), or y=value series=end with two values (long); slope x=period y=value series=entity; waterfall x=step y=signed change; small-multiples series=panel; sankey and alluvial x=source series=target y=weight; heatmap x=column series=row y=value; quadrant series=label; bullet x=measure y=actual `--y2` target [series=poor band]; range-band x=time y=lower `--y2` upper [series=centre line]; connected-scatter x and y=the two measures, series=time label; bump x=period y=rank series=entity. `--y2` names a second numeric column and also unlocks observable-plot range-band, timeline and dumbbell.
4. Data by reference where the target allows: `--flag dataByUrl` for a Vega-Lite spec that will live next to its CSV.
5. Styling: if the bundled `dataviz` skill is available, run its procedure (palette validator, mark specs, hover, anti-patterns) on the spec. Without it, use the Okabe-Ito palette and the chart file's Accessibility section.
6. Title with the finding, label directly, bars from zero, and write the text alternative (type, what it shows, key finding) as caption or alt text. Deliver accessibility as a bundle: short alt text, a longer description for maps and charts with more than one finding, the data as a CSV beside the image (not only the spec), and SVG where the host allows. World choropleths use `equalEarth`, never Mercator; no-data regions get a neutral swatch and a legend entry (Engebretsen and Kennedy 2020 ch. 7, 24; book rule, unverified).
   Vega-Lite and docx build flags: `--source "Agency, 2026"` puts the source line in the image as subtitle; `--forecast-from <x value>` draws line rows from that x on dashed with an actual/forecast key (the last actual point is repeated so the segments join); `--highlight-latest` drops the per-point markers and puts a dot and value label on the newest point of each series (Knaflic, Cisneros and Velez 2024 ch. 7, 15; Engebretsen and Kennedy 2020 ch. 11).
7. Defaults when no style is given (Tufte 2001 ch. 4, 5, 9): no plot border or background fill, no pattern fills, grid thin and light or none, data strokes heavier than grid and axes, the y-axis title horizontal above the axis, sentence case, time series about 1.5 wide to 1 tall unless the data set the shape. Keep bar fills; stripping them hurts reading.
8. Interactive targets: hover feedback within about 0.1 s, transitions about 1 s, a progress sign past 1 s (Munzner 2014 table 6.1). Overview first, then filter, then details on demand; the finding, its key numbers and any data caveat are visible without hover or click. For general readers ship a fixed explanatory default view (time on x, the measure on position); pickers are extras. Controls keep their place across views and work from the keyboard (Cairo 2013 ch. 9; Engebretsen and Kennedy 2020 ch. 7, 12).

## Verify

- Render or parse: `CW render --target vega-lite --in spec.vl.json --out chart.png|svg|pdf|html`; `CW render --target matplotlib --in chart.py --out chart.png`; `CW render --target pptx --in chart.py --out deck.pptx`; `CW render --target xlsx --in chart.py --out book.xlsx`; `CW render --target docx --in chart.py --out report.docx`; `CW render --target observable-plot --in chart.js --out page.html`; `CW render --target d2 --in graph.d2 --out graph.svg` (needs `d2`); `CW render --target plantuml --in chart.puml --out chart.svg` (needs `plantuml`, else it prints a Kroki URL); `CW render --target mermaid --in chart.md --out chart.svg` when `mmdc` or `npx` exists (otherwise check the block against `kb/targets/mermaid.md` syntax essentials); `CW render --target echarts|plotly|chartjs --in spec.json --out page.html`. A build that fails to render is not done.
- Lint a Vega-Lite spec: `CW --strict lint spec.vl.json` (exit 1 on a fail). Fails: `lie-factor` (bar or area lengths off zero, outside 0.95-1.05), `uneven-time` (dates on an ordinal axis), `area-scale`. Warnings: `hue-for-order`, `false-order`, `integral-channels`, `colour-budget`, `red-green-pair`, `grey-collapse` (range colours under 10 L* apart), `heavy-grid` (darker than about #ccc), `small-data` (20 numbers or fewer), `no-comparison`, `all-caps`, `tall-timeseries`, `low-contrast-mark` (a point, line or text colour under 3:1 against the background and no stroke; outline it), `heavy-fill` (bars or areas in dark saturated colour), `rainbow-scale` (rainbow, sinebow or turbo; use viridis unless the audience's convention needs a spectrum) (Ware 2012 pp. 82, 123-131). The grid, grey and 20-number thresholds are reader-set, not the book's, so they stay warnings. Report the lie factor result with area-based charts. Book-rule warnings (practitioner and small-sample sources, unverified): `not-normalized` (a count-named measure compared across places or groups, no rate in the name or title), `line-over-categories` (a line over unordered nominal x), `forecast-as-actual` (a forecast column or value and nothing dashed or faded), `legend-single-series`, `angled-tick-labels`, `unsorted-bars` (more than 5 unordered categories in default order), `source-in-image` (no "Source" text in the image; `build --source`), `log-axis-unexplained`, `caveat-in-tooltip-only` (Cairo 2013; Knaflic, Cisneros and Velez 2024; Engebretsen and Kennedy 2020). Round 7 warnings: `missing-chart-title`, `secondary-axis` (independent y scales in one panel fake crossings), `meaningless-zero` (bars of temperature, life expectancy and the like), `endpoint-only-line` (a time line of two dates), `uneven-time-intervals` (a line over missing periods; gap over 1.5 times the median step, reader-set), `band-no-coverage` (a band or error bar with no stated span), `heatmap-no-key`, `highlight-too-much` (grey context plus more than two accents, reader-set), `adjacent-contrast` (touching stacked or pie segments under 3:1 with no stroke), `text-contrast` (label or axis text under 4.5:1, WCAG 1.4.3) (Few 2006; Knaflic 2015; Cairo 2019; Abbott 2024). Dashboards and document chart sets: `CW lint a.vl.json b.vl.json` or `CW lint --dashboard board.vl.json` lints every concat panel and adds `colour-drift` (one category, two colours), `colour-collision` (one colour, two meanings) and `mixed-media` (same fields, different chart types) (Few 2006 pp. 51, 142).
- Look at the image (Read the PNG or SVG): label collisions, empty plots, wrong axis types, dates shifted by a day. Fix and re-render.
- Makeover check on the image (Knaflic et al. 2024 ch. 1, 4, 8, 10, 18; book rule, unverified): (1) the first thing the eye lands on is what the title claims, else move the contrast; (2) every mark means what a casual reader will take it for (a raw value, not a gap, rank or index), else label it or plot the raw values; (3) one accent colour, used for the title's point, the rest neutral; (4) one takeaway sentence fits the chart: none means cut it, several mean split it; (5) for a general audience, swap specialist forms (box, violin, survival, bubble, matrix) for bars, a pie or a waffle of the few values that matter; (6) on interactive pages, overview before detail and nothing essential only on hover.
- Place it: fenced block or image link at the claim's position; HTML file or artifact for web; PNG path for documents. Save the spec or script beside the image.
- Report in one to three lines: chart type and the rule that picked it, the target, the file or block written, and the render evidence.

### Hand-written D3 (no builder)

chartwright has no D3 target. When a page needs hand-written D3 (Dale 2016 ch. 16-18; check method names against current D3 docs, the book predates some):
- One `selection.join()` call per update, keyed by an identity field (`.data(rows, d => d.id)`), never by array index: index keys misplace marks once filtered data has gaps.
- Coerce JSON number strings with `+` before they reach a scale. Filter zero categories, then recompute data-dependent domains inside the update; fixed domains (the full year range, a historic maximum) are set once outside it.
- Bars: `d3.scaleBand().padding(...).round(true)`; y range `[height, 0]`.
- Linked views: one data-change function calls every view's update callback with the same filtered rows.
- After each join, check the bound data in the browser devtools.
