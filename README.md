# chartwright

![An artisan's workshop wall covered in handcrafted wooden bar charts, pie charts and line graphs, carving tools on the bench](https://raw.githubusercontent.com/m4bwav/chartwright/master/.github/images/banner.jpg)

Evergreen chart and graph skills for AI coding agents. A knowledge base of about 80 chart types (when to use, what each excels at, when not to, substitutes, perceptual evidence, accessibility, per-target build recipes, dated notes), sixteen render targets (Markdown via Mermaid and PlantUML; web via Vega-Lite, ECharts, Plotly, Chart.js and Observable Plot; static PNG/SVG via Python; editable PowerPoint, Excel and Google Sheets charts; Word and Google Docs via pictures; D2 for networks and trees; chart-as-URL images via QuickChart; terminal sparklines), a standard-library CLI that picks and builds charts from a CSV so the data never passes through the model, and a curation skill that researches novel requests and grows the base so the next request is cheaper.

## Skills

| Skill | Does |
|---|---|
| `chartwright` | Any chart request: a named chart, the right chart for a question, or charts chosen from a document's claims. Picks with the knowledge base, builds with the CLI, renders, verifies, places the chart, saves the source beside it. |
| `chartwright-curate` | Grows the knowledge base: research a chart type or question, add a chart or target, record a note or correction, audit for gaps and rot. |

Both are evergreen units (research refresh on an adaptive schedule, learnings, changelog, eval suite) under the [evergreen protocol](https://github.com/m4bwav/evergreen-protocol). They call the bundled Claude `dataviz` skill for palette validation and mark styling when it is present.

## Layout

```
kb/charts/<slug>.md      one file per chart type (schema: kb/SCHEMA.md)
kb/targets/<slug>.md     one file per render target
kb/rules/                selection rules, the evidence, choosing a target
kb/INDEX.md, index.json  generated compact index (what the agent reads first)
scripts/cw.py            the CLI (stdlib Python; cw.ps1 and cw.sh launchers)
tests/test_cw.py         unittest suite (python -m unittest discover -s tests)
skills/                  the two skills with their evergreen files and evals
ai-docs/                 research, decisions, log, handoff for any agent or human
```

Entry points: [kb/INDEX.md](kb/INDEX.md) links every chart, target and rule (the knowledge base reads as a graph in Obsidian or on GitHub); [kb/SCHEMA.md](kb/SCHEMA.md); the skills [chartwright](skills/chartwright/SKILL.md) and [chartwright-curate](skills/chartwright-curate/SKILL.md); worked examples [sales-by-region](examples/sales-by-region.md), [eval-trigger](examples/eval-trigger.md) and a [quarterly report](examples/report/quarterly-summary.md); [ai-docs/INDEX.md](ai-docs/INDEX.md); the reasoned history in [CHANGELOG.md](CHANGELOG.md); agent rules in [AGENTS.md](AGENTS.md), which [CLAUDE.md](CLAUDE.md) points at.

## CLI

```
python scripts/cw.py index                       # regenerate kb/INDEX.md and index.json
python scripts/cw.py validate                    # lint the knowledge base
python scripts/cw.py pick --question "line graph, time on x, price on y" --shape time,q
python scripts/cw.py show line --section when not substitutes
python scripts/cw.py data prices.csv             # column kinds and shape guess
python scripts/cw.py build --chart line --target mermaid --data prices.csv --x date --y price
python scripts/cw.py build --chart grouped-bar --target vega-lite --data sales.csv --x region --y sales --series product --html --out chart.html
python scripts/cw.py render --target vega-lite --in chart.vl.json --out chart.png
python scripts/cw.py build --chart column --target pptx --data sales.csv --x region --y sales --out chart.py --png deck.pptx
python scripts/cw.py render --target pptx --in chart.py --out deck.pptx      # editable PowerPoint chart
python scripts/cw.py build --chart line --target terminal --data prices.csv --x date --y price   # block sparkline
python scripts/cw.py build --chart bar --target docx --data sales.csv --x region --y sales --out chart.py --png report.docx
python scripts/cw.py render --target docx --in chart.py --out report.docx      # Word document with the chart as a picture and caption
python scripts/cw.py build --chart column --target gsheets --data sales.csv --x region --y sales --out chart.json   # values + addChart request for the Sheets API
python scripts/cw.py new-chart horizon --name "Horizon chart" --family change-over-time --shapes time,q*n
python scripts/cw.py note pie "fine for two slices when the question is majority"
python scripts/cw.py doctor                      # which renderers this machine has
```

Renderers are optional: `pip install vl-convert-python` for Vega-Lite to PNG/SVG without a browser, `pip install matplotlib` for the Python target, Node plus `@mermaid-js/mermaid-cli` only to rasterise Mermaid (the markdown hosts render it themselves).

## Tested where

Each render target records where its build and render were actually proven (`tested:` in `kb/targets/<slug>.md`, summarised in `kb/INDEX.md`). The plugin was built on one Windows PC. Targets marked `untested`, or with no entry for your platform, are not broken, just unproven: the chartwright skill will tell you so and ask before continuing. If it works for you, let it record the result (`python scripts/cw.py tested <target> --platform <OS> "<what worked>"`) and send a pull request; failures are just as useful, recorded the same way.

## Install

Claude Code: add the repo as a marketplace and install (`/plugin marketplace add m4bwav/chartwright` then `/plugin install chartwright@chartwright`), or clone it into a local directory marketplace. Elsewhere, copy `skills/*` into the agent's skill store and keep the plugin folder where the skills can find `scripts/` and `kb/` (two levels up from each SKILL.md). Optional renderers: `pip install vl-convert-python matplotlib python-pptx openpyxl`; Node plus `@mermaid-js/mermaid-cli` only to rasterise Mermaid.

## Privacy

chartwright keeps nothing and runs on your machine: the skills are instructions for the agent, and `scripts/cw.py` is a standard-library Python script that reads the data files you point it at. A few routes reach the network, and only when you choose them:

- The QuickChart target encodes the chart, data included, into a quickchart.io URL. Anyone who opens the image fetches it from quickchart.io, so don't use this target for private data.
- Rendering PlantUML without a local `plantuml` sends the diagram source to kroki.io to draw the image.
- A web page target (Vega-Lite, ECharts, Plotly, Chart.js, Observable Plot) writes HTML that loads its charting library from cdn.jsdelivr.net or cdn.plot.ly when the page is opened. The data stays in the page.
- Rendering Mermaid without `mmdc` installed has `npx` download `@mermaid-js/mermaid-cli@12.0.0` from npm and run it locally.

Nothing else is sent anywhere. Whatever your AI app does with the conversation is covered by that app's own privacy policy.

## Versioning

Semantic version in `.claude-plugin/plugin.json`; every change is logged in the skill `CHANGELOG.md` files and the plugin `CHANGELOG.md`. Tags on the repo match the plugin version.

## Sources

The knowledge base was written from primary-source research on 2026-09-17 (`ai-docs/research/`): the Financial Times Visual Vocabulary, the Data Visualisation Catalogue, From Data to Viz, Datawrapper's guides, Cleveland and McGill 1984, Heer and Bostock 2010, Skau and Kosara 2016, Franconeri et al. 2021, and the current docs and release notes of Mermaid 12, Vega-Lite 6, Plotly 4, Chart.js 4, ECharts 6 and matplotlib 3.11.

License: MIT.
