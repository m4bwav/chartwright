# HANDOFF

Updated 2026-09-18 (v0.4.0: eleven targets including Excel and Google Docs; repo public). Read this first, then `ai-docs/log.md`.

## State

- Plugin `chartwright` 0.4.0 in the local plugin marketplace folder (installed in Claude Code from the `mark-local` marketplace), published at https://github.com/m4bwav/chartwright (public since 2026-09-18).
- Knowledge base: 82 chart files, 5 targets, rules; `python scripts/cw.py --strict validate` clean and 26 unit tests pass at handoff. Tags v0.1.0 and v0.1.1 on the repo.
- Skills are evergreen: `chartwright` due 2026-10-01 (fast), `chartwright-curate` due 2026-10-17 (moderate). Evals in `skills/*/evals/evals.json`; results in `skills/*/TESTS.md`.

## Next steps (in order of value)

0. Done 2026-09-18: fresh `claude -p` sessions from a neutral directory invoke both skills (T-20260918-2/3). Run future trigger evals from outside the repo (L-20260918-2 in chartwright-curate).
1. Done 2026-09-18 for a markdown document (`examples/report/`) and for Google Docs (a Doc created from HTML with QuickChart images through the Drive connector; the user should confirm the images rendered: https://docs.google.com/document/d/1VsoBJgPsZBiWSiFkhQtRjEfxgNCKGd_KXwUiVX-JdGw/edit). Still to do: a real README in another repo, and a Word (.docx) destination through the docx skill.
2. Done: `echarts`, `pptx`, `quickchart`, `terminal`, `xlsx`, `gdocs`. Remaining candidates: `gsheets` (Sheets API EmbeddedChart), `plantuml`, `d2`, `observable-plot`, `docx` (PNG via python-docx).
3. Extend `cw.py build` further: bullet, range-band, connected-scatter, bump in Vega-Lite; composed recipes for Plotly and matplotlib (0.2.0 added seven Vega-Lite compositions).
4. Done in 0.2.0: `--flag namedSeries` emits named Mermaid series; consider auto-enabling it when the host is known to be 11.16+.
5. Run the evergreen refresh when due; Mermaid 12 host adoption (GitHub, Obsidian) is the claim most likely to change.

## Gotchas

- `cw.py` fails soft (exit 0 with a note) unless `--strict`; tests and CI use `--strict`.
- `kb/INDEX.md` and `kb/index.json` are generated; regenerate after any kb edit.
- Optional renderers: vl-convert-python (installed here), matplotlib (installed), mmdc (not installed; `npx` fallback downloads Chromium on first use).
