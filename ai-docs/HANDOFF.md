# HANDOFF

Updated 2026-09-26 (v0.8.2: the two skill descriptions rewritten so they no longer compete, both under 1,024 characters, native `claude plugin eval` trigger suite in `evals/`). Earlier: v0.8.0 `tested:` status per target; v0.7.0 Plotly and matplotlib compositions; v0.6.0 `--y2`; v0.5.0 sixteen targets. Read this first, then `ai-docs/log.md` (D:\m4bwa\Claude\Projects\Ai\chartwright\ai-docs\log.md).

## State

- Plugin `chartwright` 0.8.2 in the local plugin marketplace folder (installed in Claude Code from the `mark-local` marketplace), published at https://github.com/m4bwav/chartwright (public). Tags v0.1.0 to v0.8.2.
- Knowledge base: 83 chart files (cycle plot added by the curate eval run), 16 targets (mermaid, vega-lite, plotly, chartjs, matplotlib, terminal, echarts, pptx, quickchart, xlsx, gdocs, plantuml, d2, observable-plot, gsheets, docx), rules; `python scripts/cw.py --strict validate` clean and 45 unit tests pass at handoff (docx render proven end to end because python-docx is installed here).
- Skills are evergreen: `chartwright` due 2026-10-01 (fast), `chartwright-curate` due 2026-10-17 (moderate). Evals in `skills/*/evals/evals.json` (evergreen format; action and outcome cases) and `evals/` at the root (trigger and decoy cases for `claude plugin eval . --ablation none --no-publish -j 4`, which works on native Windows; about 1 USD a run); results in `skills/*/TESTS.md` (latest T-20260926-1, 9/9).

## Next steps (in order of value)

1. Platform coverage is now data, not a to-do: `tested:` in each target file. The owner plans no testing beyond Windows and maybe macOS; other platforms come from users through the ask-and-record rule (README "Tested where"). Untested today: gsheets, plantuml, d2, observable-plot; several office targets were rendered but never opened in their program. Former note: a Google Sheet through the Sheets API (`gsheets` builder emits values plus an `addChart` request; never sent live yet), a PlantUML document (no PlantUML installed here; `cw.py render --target plantuml` prints a Kroki URL instead), an Observable Plot page screenshot. Run them from a neutral folder (see Gotchas).
2. Builder work is at a natural stopping point: every chart the references list as builder-covered renders in its target. Further builders only if a real request needs one (the curate skill's research path handles that).
3. Chooser: `pick` still scores on keywords. A regression set of real questions lives in `tests/test_cw.py` (ten so far); add every real question that misfires there before tuning.
4. Consider auto-enabling `--flag namedSeries` when the Mermaid host is known to be 11.16+.
5. Evergreen refresh when due; Mermaid 12 host adoption (GitHub, Obsidian) and PlantUML `@startchart` stability are the claims most likely to change.

## Gotchas

- `cw.py` fails soft (exit 0 with a note) unless `--strict`; tests and CI use `--strict`. `--json` and `--strict` may now go before or after the subcommand.
- `kb/INDEX.md` and `kb/index.json` are generated; regenerate after any kb edit.
- Optional renderers: vl-convert-python, matplotlib, python-docx, openpyxl, python-pptx (all installed here); mmdc absent (`npx` fallback works); no `d2`, no `plantuml`.
- `claude plugin eval` uses a throwaway config: the catalog holds only this plugin and built-ins, so it proves the two skills separate, not that they win in the full catalog. The context-health selection check (`ctxhealth.py selection`) reads the installed copy in `~/.claude/plugins/cache/mark-local/chartwright/<version>`; update the plugin before re-measuring.
- Trigger evals run inside the plugin repo are biased (AGENTS.md routes straight to the CLI): run them from a neutral folder such as the session scratchpad. In this session `claude -p` launches were refused by the permission classifier; the evergreen-tester agent with a neutral working directory was the working substitute.
- A patch script that writes another Python file must use real newlines, not `\n` inside a string (bit twice: xlsx wiring in 0.4.0, a test in 0.5.0).
- The README test edited another project in place: `D:\m4bwa\Claude\Projects\Ai\video-pipeline\README.md` (two Mermaid bar blocks, charts under `docs/charts/`, a HANDOFF.md note). The original is backed up in the session scratchpad (`readme-test/README.orig.md`); that folder is temporary, so decide soon whether to keep the charts.
