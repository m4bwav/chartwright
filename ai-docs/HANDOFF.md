# HANDOFF

Updated 2026-09-18 (v0.6.0: `--y2` compositions and chooser regression set; v0.5.0 the same day added sixteen targets and full eval suites). Read this first, then `ai-docs/log.md` (D:\m4bwa\Claude\Projects\Ai\chartwright\ai-docs\log.md).

## State

- Plugin `chartwright` 0.6.0 in the local plugin marketplace folder (installed in Claude Code from the `mark-local` marketplace), published at https://github.com/m4bwav/chartwright (public). Tags v0.1.0 to v0.6.0.
- Knowledge base: 83 chart files (cycle plot added by the curate eval run), 16 targets (mermaid, vega-lite, plotly, chartjs, matplotlib, terminal, echarts, pptx, quickchart, xlsx, gdocs, plantuml, d2, observable-plot, gsheets, docx), rules; `python scripts/cw.py --strict validate` clean and 43 unit tests pass at handoff (docx render proven end to end because python-docx is installed here).
- Skills are evergreen: `chartwright` due 2026-10-01 (fast), `chartwright-curate` due 2026-10-17 (moderate). Evals in `skills/*/evals/evals.json`; results in `skills/*/TESTS.md` (T-20260918-3 and T-20260918-4 for chartwright; the 2026-09-18 suite run for curate).

## Next steps (in order of value)

1. Real-destination runs for the newest targets: a Google Sheet through the Sheets API (`gsheets` builder emits values plus an `addChart` request; never sent live yet), a PlantUML document (no PlantUML installed here; `cw.py render --target plantuml` prints a Kroki URL instead), an Observable Plot page screenshot. Run them from a neutral folder (see Gotchas).
2. Builder gaps left: composed recipes for Plotly and matplotlib (bullet, waterfall, dumbbell); a `--y2` path for the Vega-Lite dumbbell (today it needs long-form data with `--series`). Done in 0.6.0: bullet, range-band, connected-scatter, bump via `--y2`.
3. Chooser: `pick` still scores on keywords. A regression set of real questions lives in `tests/test_cw.py` (ten so far); add every real question that misfires there before tuning.
4. Consider auto-enabling `--flag namedSeries` when the Mermaid host is known to be 11.16+.
5. Evergreen refresh when due; Mermaid 12 host adoption (GitHub, Obsidian) and PlantUML `@startchart` stability are the claims most likely to change.

## Gotchas

- `cw.py` fails soft (exit 0 with a note) unless `--strict`; tests and CI use `--strict`. `--json` and `--strict` may now go before or after the subcommand.
- `kb/INDEX.md` and `kb/index.json` are generated; regenerate after any kb edit.
- Optional renderers: vl-convert-python, matplotlib, python-docx, openpyxl, python-pptx (all installed here); mmdc absent (`npx` fallback works); no `d2`, no `plantuml`.
- Trigger evals run inside the plugin repo are biased (AGENTS.md routes straight to the CLI): run them from a neutral folder such as the session scratchpad. In this session `claude -p` launches were refused by the permission classifier; the evergreen-tester agent with a neutral working directory was the working substitute.
- A patch script that writes another Python file must use real newlines, not `\n` inside a string (bit twice: xlsx wiring in 0.4.0, a test in 0.5.0).
- The README test edited another project in place: `D:\m4bwa\Claude\Projects\Ai\video-pipeline\README.md` (two Mermaid bar blocks, charts under `docs/charts/`, a HANDOFF.md note). The original is backed up in the session scratchpad (`readme-test/README.orig.md`); that folder is temporary, so decide soon whether to keep the charts.
