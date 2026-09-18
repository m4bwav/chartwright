# chartwright

Evergreen chart and graph skills for AI coding agents. A knowledge base of about 80 chart types (when to use, what each excels at, when not to, substitutes, perceptual evidence, accessibility, per-target build recipes, dated notes), eleven render targets (Markdown via Mermaid; web via Vega-Lite, ECharts, Plotly and Chart.js; static PNG/SVG via Python; editable PowerPoint and Excel charts; Google Docs via image import; chart-as-URL images via QuickChart; terminal sparklines), a standard-library CLI that picks and builds charts from a CSV so the data never passes through the model, and a curation skill that researches novel requests and grows the base so the next request is cheaper.

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
python scripts/cw.py new-chart horizon --name "Horizon chart" --family change-over-time --shapes time,q*n
python scripts/cw.py note pie "fine for two slices when the question is majority"
python scripts/cw.py doctor                      # which renderers this machine has
```

Renderers are optional: `pip install vl-convert-python` for Vega-Lite to PNG/SVG without a browser, `pip install matplotlib` for the Python target, Node plus `@mermaid-js/mermaid-cli` only to rasterise Mermaid (the markdown hosts render it themselves).

## Install

Claude Code: add the repo as a marketplace and install (`/plugin marketplace add m4bwav/chartwright` then `/plugin install chartwright@chartwright`), or clone it into a local directory marketplace. Elsewhere, copy `skills/*` into the agent's skill store and keep the plugin folder where the skills can find `scripts/` and `kb/` (two levels up from each SKILL.md). Optional renderers: `pip install vl-convert-python matplotlib python-pptx openpyxl`; Node plus `@mermaid-js/mermaid-cli` only to rasterise Mermaid.

## Versioning

Semantic version in `.claude-plugin/plugin.json`; every change is logged in the skill `CHANGELOG.md` files and the plugin `CHANGELOG.md`. Tags on the repo match the plugin version.

## Sources

The knowledge base was written from primary-source research on 2026-09-17 (`ai-docs/research/`): the Financial Times Visual Vocabulary, the Data Visualisation Catalogue, From Data to Viz, Datawrapper's guides, Cleveland and McGill 1984, Heer and Bostock 2010, Skau and Kosara 2016, Franconeri et al. 2021, and the current docs and release notes of Mermaid 12, Vega-Lite 6, Plotly 4, Chart.js 4, ECharts 6 and matplotlib 3.11.

License: MIT.
