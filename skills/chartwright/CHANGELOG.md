# Changelog: chartwright

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: the installed evergreen plugin (`protocol: "plugin"` in evergreen.json).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20260918-3 · 2026-09-18 · Terminal target, composed Vega-Lite recipes, named Mermaid series
- because: HANDOFF next steps 2 to 4 (user asked to continue); fresh-session trigger run T-20260918-2
- files: scripts/cw.py (build_terminal, _vl_composed, namedSeries flag, UTF-8 stdout), kb/targets/terminal.md, every kb/charts file (terminal support line; nine terminal recipes; seven vega-lite recipes), kb/rules/choosing-a-target.md, SKILL.md Step 3, tests/test_cw.py
- Sixth target `terminal` (block sparkline and block bars); `cw.py build` now composes dumbbell, slope, waterfall, calendar-heatmap, diverging-bar, stacked-bar-100 and small-multiples in Vega-Lite; `--flag namedSeries` emits Mermaid `xychart` with a legend.

### C-20260918-2 · 2026-09-18 · Builder sums duplicate x values (new --agg sum|mean|none)
- because: T-20260918-1 action-1 (a bar of sales by region kept only the last product row per region)
- files: scripts/cw.py (_series_split, cmd_build), tests/test_cw.py
- Rows sharing an x value within a series are aggregated (sum by default, note on stderr); `--agg none` restores raw rows.

### C-20260918-1 · 2026-09-18 · Chooser: exact-word chart names, funnel and budget synonyms
- because: first dry runs of `cw.py pick` (session log 2026-09-17); "signup steps" named the step chart and "budget" routed to sankey
- files: scripts/cw.py (cmd_pick, SYN), kb/charts/funnel.md (goals), tests/test_cw.py (PickTests)
- Chart names match as exact words (plurals only for multi-word or long names); `drop-off`, `signup`, `checkout` map to stages; `budget` maps to part-to-whole and magnitude. Two regression tests added.

### C-20260917-1 · 2026-09-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `fast`, interval 14d. See R-20260917-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
