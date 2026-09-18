# Changelog (plugin)

Semantic versions of the chartwright plugin. Per-skill and knowledge changes are logged in `skills/*/CHANGELOG.md`.

## 0.8.0 (2026-09-18)

- Every target now carries `tested:` (platform, date, what was proven, or `untested`), shown in `kb/INDEX.md` and `cw.py targets`. The chartwright skill compares it with the user's platform before building, says when a target is unproven there, and asks before continuing; a successful or failed test is recorded with the new `cw.py tested` command and a changelog entry. README section "Tested where" invites reports from other platforms.

## 0.7.0 (2026-09-18)

- Composed recipes beyond Vega-Lite: Plotly and matplotlib now build waterfall, dumbbell and bullet; the dumbbell accepts wide form (`--y2`) in all three targets and long form (`--series` with two ends) as before. All rendered and inspected.

## 0.6.0 (2026-09-18)

- `--y2` names a second numeric column. Vega-Lite now composes bullet (actual bar, target tick, optional poor band), range-band (area between `--y` and `--y2`, optional centre line), connected-scatter (path in `--series` order with labels) and bump (rank 1 on top, entity labels); observable-plot gains range-band, timeline and dumbbell through the same flag. All four rendered and checked.
- Chooser regression set: seven real questions locked in `tests/test_cw.py`.

## 0.5.0 (2026-09-18)

- Five more targets with builders and tests: `plantuml` (`@startchart`, 1.2026.0+), `d2` (network and tree edges; D2 has no data charts), `observable-plot` (mark snippet and page, Plot 0.6.17), `gsheets` (values plus `addChart` request for the Sheets API), `docx` (python-docx script that renders the Vega-Lite PNG and writes heading, picture, caption). Sixteen targets, wired into all 82 chart files.
- From two fresh-session runs on a real README and a Word destination: `--json` and `--strict` are accepted after the subcommand; Mermaid bars get an explicit `0 --> max` axis; the Vega-Lite ranked bar sorts by value; the chooser no longer lets generic words (each, one, take) score, and "how long" or "how much" reads as magnitude; `render --target mermaid` deletes its extracted `.mmd`.

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
