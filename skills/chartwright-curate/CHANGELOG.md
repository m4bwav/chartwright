# Changelog: chartwright-curate

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: the installed evergreen plugin (`protocol: "plugin"` in evergreen.json).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20260918-3 · 2026-09-18 · Procedure C: check for an existing note before appending
- because: T-20260918-4 action-1 (the tester found the note already in HEAD and had no rule for that case)
- files: references/procedures.md (path C)
- Grep the chart file for the note's key words first; an equivalent note means "say so and stop", not a duplicate dated line.

### C-20260918-4 · 2026-09-18 · Added the cycle plot (seasonal subseries plot) to the knowledge base
- because: user request ("add a chart type called 'cycle plot' ... family change-over-time"); R-20260918-1
- files: kb/charts/cycle-plot.md (new), kb/charts/calendar-heatmap.md (Substitutes: prose mention became the `cycle-plot` slug), kb/INDEX.md and kb/index.json (regenerated)
- New entry with aliases (seasonal subseries plot, month plot), a support line for all 16 targets (matplotlib native via statsmodels month_plot; vega-lite, plotly, chartjs, echarts, pptx, xlsx, gsheets, observable-plot approx as facet plus mean rule; mermaid, gdocs, docx image; terminal, quickchart, d2, plantuml none) and a hand-written recipe per native or approx target. No `cw.py build` recipe yet. Validate: 83 charts, 16 targets, exit 0.

### C-20260918-2 · 2026-09-18 · SKILL.md slimmed to a router; procedures moved to references/procedures.md
- because: user request (small main file, detail on demand), evergreen protocol budget rule
- files: SKILL.md, references/procedures.md
- The five procedures (research, add chart, note, add target, audit) are sections A to E of the reference; SKILL.md keeps routing, the proof step and the output shape.

### C-20260918-1 · 2026-09-18 · Description: "add a note to the <chart> entry" phrasings
- because: T-20260918-2 (fresh-session run wrote the note through the CLI without invoking the skill: undertrigger)
- files: SKILL.md (description)
- Added the "add a note to the pie chart entry", "note on the line chart entry" and "anything that mentions the chart knowledge base or a chart's entry" phrasings.

### C-20260917-1 · 2026-09-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20260917-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
