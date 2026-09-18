# Changelog: chartwright

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: the installed evergreen plugin (`protocol: "plugin"` in evergreen.json).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20260918-10 · 2026-09-18 · Plotly and matplotlib compositions; wide-form dumbbell
- because: HANDOFF next step 2 (the last builder gap this machine can close)
- files: scripts/cw.py (_two_ends, build_plotly waterfall/dumbbell/bullet, build_matplotlib waterfall/dumbbell/bullet, _vl_composed dumbbell fold), kb/charts/{waterfall,dumbbell,bullet}.md (recipe lines; plotly support native for dumbbell and bullet), references/build-and-verify.md, tests/fixtures/dumbbell.csv, tests/test_cw.py
- Plotly uses its native waterfall trace; matplotlib stacks floating bars. Both dumbbells and bullets rendered and checked.

### C-20260918-9 · 2026-09-18 · `--y2` and four more Vega-Lite compositions
- because: HANDOFF next step 2 (builder gaps) after the 0.5.0 release
- files: scripts/cw.py (_Y2, _vl_composed bullet/range-band/connected-scatter/bump, build_observable_plot y2 marks, build --y2), kb/charts/{bullet,range-band,connected-scatter,bump}.md (vega-lite recipe line), references/build-and-verify.md (column roles, builder coverage), tests/fixtures/{bullet,band,connected,bump}.csv, tests/test_cw.py
- A second numeric column was the missing role for targets and bounds; the four compositions were rendered and inspected (band y-axis no longer starts at zero; bump rank axis runs 1..n).

### C-20260918-8 · 2026-09-18 · Fixes from the README and Word fresh-session runs
- because: T-20260918-3 (two evergreen-tester runs from a neutral directory), L-20260918-3
- files: scripts/cw.py (_hoist_globals, build_mermaid y-axis range, build_vega_lite bar sort, GENERIC words and magnitude synonyms in pick, mermaid render cleanup), references/build-and-verify.md (Word row now points at the `docx` target), tests/test_cw.py
- `cw.py pick ... --json` now works with the flag in either position; Mermaid bars carry `0 --> max`; the Vega-Lite bar is sorted by value; "how long does each take" picks bar, not beeswarm; the Word destination has a route instead of a bare "PNG path for documents".
- Also: Vega-Lite temporal axes with first-of-month dates get `tickCount: month` and `%b %Y` labels (T-20260918-4 outcome-1 had to hand-edit fortnightly ticks).

### C-20260918-7 · 2026-09-18 · Targets plantuml, d2, observable-plot, gsheets, docx
- because: HANDOFF next step 2 (remaining targets); research R-20260917-2 plus primary-source checks on 2026-09-18 (plantuml.com/chart-diagram, d2lang.com shapes, npm registry for Plot 0.6.17, Sheets API charts reference)
- files: scripts/cw.py (build_plantuml, build_d2, build_observable_plot, build_gsheets, build_docx, HTML_PLOT, render branches), kb/targets/{plantuml,d2,observable-plot,gsheets,docx}.md, every kb/charts file (five support lines; 14 plantuml, 4 d2, 51 observable-plot, 21 gsheets recipes), kb/rules/choosing-a-target.md, references/build-and-verify.md, tests/test_cw.py
- Sixteen targets. D2 is recorded honestly as a diagram language with `none` for every data chart so the chooser can refuse it. The docx render was proven end to end (word/media/image1.png in the zip).

### C-20260918-6 · 2026-09-18 · Targets xlsx and gdocs
- because: HANDOFF next step 2 (remaining office targets) and the user's Google Docs test request
- files: scripts/cw.py (build_xlsx, render xlsx), kb/targets/{xlsx,gdocs}.md, every kb/charts file (support lines; 21 xlsx recipes), kb/rules/choosing-a-target.md, references/build-and-verify.md, tests/test_cw.py
- Excel: openpyxl script writing the data sheet and a native chart (rendered and tested). Google Docs: no chart API, so the target documents the three image routes; verified by creating a Doc from HTML with QuickChart images through the Drive connector (image embedding to be confirmed visually by the user).

### C-20260918-5 · 2026-09-18 · SKILL.md slimmed to a router; detail moved to references/
- because: user request (keep the main file small; load detail only at the step that needs it), evergreen protocol budget rule
- files: SKILL.md, references/build-and-verify.md, references/document-charts.md
- Steps 2a and 3 to 5 now live in two reference files; SKILL.md keeps the outcome, freshness, classification, pick steps and pointers (about 6 KB).

### C-20260918-4 · 2026-09-18 · Targets echarts, pptx, quickchart
- because: HANDOFF next step 2; research R-20260917-2 already covered all three
- files: scripts/cw.py (build_echarts, build_pptx, build_quickchart, HTML_ECHARTS, render pptx/echarts), kb/targets/{echarts,pptx,quickchart}.md, every kb/charts file (support lines and recipes), kb/rules/choosing-a-target.md, tests/test_cw.py
- ECharts option JSON with a standalone page; python-pptx script producing an editable native chart; QuickChart URL wrapping the Chart.js config. Verified: pptx deck written (34 KB), QuickChart live fetch returned image/png.

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
