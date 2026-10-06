# Changelog (plugin)

Semantic versions of the chartwright plugin. Per-skill and knowledge changes are logged in `skills/*/CHANGELOG.md`.

## 0.8.5 (2026-10-05)

- Copilot-ready: a root `plugin.json` (Agent Plugins 1.0 shape: `$schema`, at most 10 lowercase-hyphenated keywords, author URL) so GitHub Copilot CLI and the awesome-copilot marketplace find the plugin; the awesome-copilot intake gates look only at `.github/plugin/`, `.plugin/` or the root, never `.claude-plugin/`. Claude Code still reads `.claude-plugin/plugin.json`; keep both versions equal. Installed with Copilot CLI 1.0.92 and `vally lint` (0.17.0) passes. The release tag v0.8.5 is the ref awesome-copilot pins.

## 0.8.4 (2026-10-04)

- Ready for the Claude directory. `cw.py` pins the Mermaid CLI that `npx` runs when `mmdc` is not installed to `@mermaid-js/mermaid-cli@12.0.0` (it ran whatever npm served that day); rendered to SVG through the pinned path and the 45 tests pass on Windows. The README gains a Privacy section that lists every route that reaches the network (QuickChart URLs, kroki.io for PlantUML, CDN libraries in the web page targets, the npx download). plugin.json gains `documentationUrl` (the wiki), `supportUrl` and `privacyPolicyUrl` for the directory listing. kb/INDEX.md and index.json regenerated (date only). Details: `skills/chartwright/CHANGELOG.md` C-20261004-1.

## 0.8.3 (2026-10-03)

- Evergreen refresh of the chartwright skill (was due 2026-10-01). The skill now names Microsoft's Flint (`microsoft/flint-chart`, an MIT chart compiler and MCP server) as an optional backend for users who already run it, after chartwright picks the chart type; nothing is installed or delegated. Mermaid 12.1.0 noted in the research (no chart syntax change); every other library unchanged since 2026-09-17. Learning IDs in the skill renumbered to the protocol's `L-NNN` form. Details: `skills/chartwright/CHANGELOG.md` C-20261003-1 and -2, RESEARCH.md R-20261003-1 to -3. Trigger and decoy evals 5/5.

## 0.8.2 (2026-09-26)

- Both skill descriptions rewritten so a model can tell them apart. `chartwright` now opens with "Builds a chart or graph from data" and keeps the chart words; `chartwright-curate` opens with "Maintains chartwright's knowledge base" and drops chart-type lists. Each ends with one "Not for ..." clause naming the other. Lengths 970 and 829 characters (were 1,523 and 1,303), both under the Agent Skills limit of 1,024 that Copilot enforces. TF-IDF cosine between the two fell from 0.77 (near-duplicate) to 0.33 in the context-health selection check.
- New `evals/` folder at the plugin root: nine trigger and decoy cases in the `claude plugin eval` format (prompt.md plus `tool_used` graders on the Skill tool). Run: `claude plugin eval . --ablation none --no-publish -j 4`. First run 9/9 on Windows 11.

## 0.8.1 (2026-09-18)

- `kb/INDEX.md` now links every chart slug to `charts/<slug>.md`, every target to `targets/<slug>.md`, and ends with a Rules section linking `kb/rules/*.md`; its header links `SCHEMA.md` and the plugin README. Nothing parses the table back (`cw.py` reads `index.json`), so agents read it as before, and the index stays about 1/26 the size of the charts folder. Reason: the knowledge base is read by people in Obsidian and on GitHub as well as by agents; without links its 99 entries were orphans in a graph view (the obsidian-notes lint reported 108 orphans in this repo, now 0). The README gained an entry-points paragraph for the same reason. `tests/test_cw.py` asserts the linked form.

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
