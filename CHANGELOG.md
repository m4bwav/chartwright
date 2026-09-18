# Changelog (plugin)

Semantic versions of the chartwright plugin. Per-skill and knowledge changes are logged in `skills/*/CHANGELOG.md`.

## 0.4.0 (2026-09-18)

- Targets `xlsx` (openpyxl data sheet plus native chart, with builder and render) and `gdocs` (image routes into Google Docs; verified by creating a Doc from HTML with QuickChart images). Eleven targets total.

## 0.3.0 (2026-09-18)

- Three more targets with builders: `echarts` (option JSON and page), `pptx` (editable PowerPoint chart via python-pptx), `quickchart` (Chart.js config as an image URL). Nine targets total, wired into all 82 chart files.
- Both skills rewritten as short routers with `references/` files loaded on demand.
- Document path verified end to end on `examples/report/`. Repository made public.

## 0.2.0 (2026-09-18)

- New `terminal` render target (block sparklines and bars, UTF-8 forced on Windows). `cw.py build` composes seven more Vega-Lite charts (dumbbell, slope, waterfall, calendar-heatmap, diverging-bar, stacked-bar-100, small-multiples) and emits named Mermaid series with `--flag namedSeries`. Fresh-session evals: chartwright triggers and holds on a decoy; chartwright-curate description tuned after an undertrigger.

## 0.1.1 (2026-09-18)

- Builder aggregates duplicate x values (`--agg sum|mean|none`), chooser matches chart names as exact words with funnel and budget synonyms, three chart files completed (density-2d, correlogram, quadrant), first eval run recorded (actions and decoys pass on evidence; trigger cases inconclusive because the plugin was installed mid-session).

## 0.1.0 (2026-09-17)

- First release: `chartwright` and `chartwright-curate` skills (evergreen), knowledge base of chart types across the FT Visual Vocabulary families plus hierarchy, relationship, single-value and table, five render targets (mermaid, vega-lite, plotly, chartjs, matplotlib), `scripts/cw.py` (index, validate, list, show, pick, data, build, render, new-chart, new-target, note, doctor, targets), unittest suite, ai-docs handoff set.
- Research basis: `ai-docs/research/2026-09-17-chart-taxonomy-and-evidence.md` and `ai-docs/research/2026-09-17-libraries-and-render-targets.md`.
