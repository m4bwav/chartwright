# Log

Append-only. Newest at the bottom. One entry per working session.

## 2026-09-17: plugin created

- Asked for: the ultimate chart/graph plugin: knowledge base of chart types (when, excels, when not, notes, build per target), evidence-based selection, novel-request research that improves the base, evergreen, tests, versioning, cross-platform token-saving scripts, private repo.
- Decisions: name `chartwright`; targets mermaid, vega-lite, plotly, chartjs, matplotlib for 0.1; full evergreen. See `ai-docs/decisions/`.
- Research: two parallel web research passes (taxonomy and evidence; libraries and targets) saved under `ai-docs/research/`.
- Built: schema, five target files, rules (selection, evidence, choosing a target), the `cw.py` CLI with launchers, 23 unit tests, two skills with evergreen scaffolding, README/AGENTS/CLAUDE docs. Knowledge base chart files authored by five parallel agents from the research and an exemplar (`kb/charts/line.md`).
- Verified: build and render to all five targets on Windows (Vega-Lite PNG/SVG via vl-convert 1.9.0, matplotlib 3.11.2 PNG, Plotly and Chart.js pages, Mermaid text).
- Learned: `cw.py` module-level state (`_problems`, `_FLAGS`) leaked between in-process calls; both now reset per command (caught by the tests).

## 2026-09-18: knowledge base completed, chooser tuned

- Two authoring agents stopped at the monthly spend limit (reset 03:30 Chicago); the three missing files (density-2d, correlogram, quadrant) were written directly and tile-grid-map's bad `also:` entry fixed. Knowledge base: 82 charts, 5 targets, `--strict validate` clean, INDEX.md 14 KB against 449 KB of chart files (32x smaller).
- Chooser fixes from dry runs: exact-word name matching (the plural rule made "steps" pick the step chart), funnel goals extended, budget synonym corrected. Tests: 25 passing.
- Installed `chartwright@mark-local` at user scope; registered in the local marketplace manifest.
