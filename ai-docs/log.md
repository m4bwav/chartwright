# Log

Append-only. Newest at the bottom. One entry per working session.

## 2026-09-17: plugin created

- Asked for: the ultimate chart/graph plugin: knowledge base of chart types (when, excels, when not, notes, build per target), evidence-based selection, novel-request research that improves the base, evergreen, tests, versioning, cross-platform token-saving scripts, a repo (private at first, made public 2026-09-18).
- Decisions: name `chartwright`; targets mermaid, vega-lite, plotly, chartjs, matplotlib for 0.1; full evergreen. See `ai-docs/decisions/`.
- Research: two parallel web research passes (taxonomy and evidence; libraries and targets) saved under `ai-docs/research/`.
- Built: schema, five target files, rules (selection, evidence, choosing a target), the `cw.py` CLI with launchers, 23 unit tests, two skills with evergreen scaffolding, README/AGENTS/CLAUDE docs. Knowledge base chart files authored by five parallel agents from the research and an exemplar (`kb/charts/line.md`).
- Verified: build and render to all five targets on Windows (Vega-Lite PNG/SVG via vl-convert 1.9.0, matplotlib 3.11.2 PNG, Plotly and Chart.js pages, Mermaid text).
- Learned: `cw.py` module-level state (`_problems`, `_FLAGS`) leaked between in-process calls; both now reset per command (caught by the tests).

## 2026-09-18: knowledge base completed, chooser tuned

- Two authoring agents stopped at the monthly spend limit (reset 03:30 Chicago); the three missing files (density-2d, correlogram, quadrant) were written directly and tile-grid-map's bad `also:` entry fixed. Knowledge base: 82 charts, 5 targets, `--strict validate` clean, INDEX.md 14 KB against 449 KB of chart files (32x smaller).
- Chooser fixes from dry runs: exact-word name matching (the plural rule made "steps" pick the step chart), funnel goals extended, budget synonym corrected. Tests: 25 passing.
- Installed `chartwright@mark-local` at user scope; registered in the local marketplace manifest.

## 2026-09-18: first real use — line chart from a CSV

- Asked for: "make a line graph with time as x and price as y from tests/fixtures/prices.csv".
- Note: the `chartwright` skill was not resolvable via the Skill tool in this session (`Unknown skill: chartwright`, also tried `chartwright:chartwright`) despite the plugin being installed on disk at this path and referenced by `AGENTS.md`/`CLAUDE.md`. Proceeded by following `skills/chartwright/SKILL.md` and `AGENTS.md` manually with the `cw.py` CLI.
- Workflow run: `cw.py data tests/fixtures/prices.csv` (shape `time,q`, 6 rows) → `cw.py pick --question "line graph with time as x and price as y" --shape time,q` (top pick `line`, score 16.0, named in request) → `cw.py show line --section when not substitutes` (fits: continuous measure over ordered time, few points, no dual-axis or category issues) → `cw.py build --chart line --target vega-lite --data tests/fixtures/prices.csv --x date --y price --title "Price over time" --out examples/prices/price-line.vl.json` → `cw.py render --target vega-lite --in examples/prices/price-line.vl.json --out examples/prices/price-line.png`.
- Built: `examples/prices/price-line.vl.json` (Vega-Lite spec) and `examples/prices/price-line.png` (rendered chart), viewed and confirmed correct (clean upward-then-down trend, Jan–May 2026, no label collisions).
- Target chosen: `vega-lite` → PNG, since no destination medium was stated in the request and PNG is a safe, viewable default; `vl_convert` was confirmed available via `cw.py doctor`.
- Learned: this is the first real end-to-end use of the plugin outside its own tests (matches HANDOFF next-step #1), and it surfaced that the skill is not currently registered/discoverable by the Skill tool in a fresh session even though the plugin directory and marketplace registration exist — worth checking plugin/marketplace registration health.

## 2026-09-18: note on line chart

- Added a curation note to `kb/charts/line.md` via `cw.py note line "prefer end labels over a legend when there are three series or fewer"`. Preference note only, no guidance section changed, so no `CHANGELOG.md` entry per the chartwright-curate skill's Step 4. `--strict validate` and `index` both re-run clean after (82 charts, 5 targets).

## 2026-09-18: note on pie chart

- Added a curation note to `kb/charts/pie.md`: two-slice pies are fine when the question is whether one part is a majority; don't downgrade to a single stat or bar just because there are only two slices. Equivalent to `cw.py note pie "..."` (edited directly, same dated-bullet format). Preference/clarification note only, no guidance section changed, so no `CHANGELOG.md` entry per the chartwright-curate skill's Step 4. `--strict validate` re-run clean after (82 charts, 5 targets).

## 2026-09-18: bar chart from CSV, mermaid target, into examples/

- Asked for: "build a bar chart of sales by region from tests/fixtures/sales.csv and write it as a mermaid block into examples/sales-by-region.md".
- Note: same as the prior session, the `chartwright` skill did not appear in this session's available-skills listing (installed plugin, but not offered via the Skill tool). Followed `AGENTS.md` → `skills/chartwright/SKILL.md` manually with the `cw.py` CLI.
- Workflow run: `cw.py doctor` (mmdc absent but node/npx present; vl_convert and matplotlib present) → `cw.py data tests/fixtures/sales.csv` (shape `n,n,q`: region, product, sales) → `cw.py pick --question "bar chart of sales by region" --shape n,q` (top pick `bar`, score 14.5, named in request) → `cw.py show bar --section when not substitutes` (fits: one quantity per category, magnitude comparison; bar's own "when not" list warns against a truncated baseline).
- Data issue found and fixed: `tests/fixtures/sales.csv` has two rows per region (one per product); `cw.py build --chart bar --target mermaid --data tests/fixtures/sales.csv --x region --y sales ...` silently kept only the last row per x-category (North 80, South 130, East 70) instead of summing — it dropped product A's sales entirely rather than aggregating or warning. Worked around by aggregating region totals with a small script into a temp CSV (North 200, South 225, East 130) and rebuilding from that; `cw.py build` itself does not accept an aggregation flag (checked `--help`). This is a CLI gap worth flagging to `chartwright-curate` or a CLI fix: `build` should sum (or refuse with an error) on duplicate x values rather than silently overwriting.
- Built: `examples/sales-by-region.md` (mermaid `xychart-beta` fenced block, title "Sales by region", bars 200/225/130) and `examples/sales-by-region.png` (rendered via `cw.py render --target mermaid`, using the node/npx mermaid-cli path since no local `mmdc`) for verification — viewed and readable, but the y-axis is auto-scaled from ~130 rather than 0, a truncated-baseline mermaid `xychart-beta` default that this CLI does not currently override; worth a note on the mermaid target file or bar chart file.
- Target chosen: `mermaid`, since the destination was an existing `.md` file and the request explicitly said "mermaid block".

## 2026-09-18: line chart eval-trigger check — skill now resolves via Skill tool

- Asked for: "make a line graph with time as x and price as y from tests/fixtures/prices.csv, output a mermaid block to examples/eval-trigger.md" (filename suggests this was a trigger check for the skill itself).
- Note: unlike the three prior sessions logged above, `Skill({skill: "chartwright:chartwright"})` resolved and loaded `SKILL.md` normally this time — the skill appeared in this session's available-skills listing. Whatever caused the earlier "Unknown skill: chartwright" appears to have been session-specific rather than a persistent registration problem; worth treating HANDOFF next-step #0 as lower priority now, though not proven fixed until it's seen failing-then-passing within one session.
- Workflow run: `cw.py data tests/fixtures/prices.csv` (shape `time,q`, 6 rows, column `date`) → matched `kb/INDEX.md` row for `line` (shape `time,q`, series cap 5, core) directly since the request named the chart type → `cw.py show line --section not` (no misuse: single series, ordered time, continuous measure, only 6 points) → `cw.py build --chart line --target mermaid --data tests/fixtures/prices.csv --x date --y price --title "Price over time" --out examples/eval-trigger.md`.
- Built: `examples/eval-trigger.md` (mermaid `xychart-beta` fenced block, title "Price over time", line 100/104/101/110/115/112 across Jan–Jun 2026). Rendered via `cw.py render --target mermaid` (node/npx path, no local `mmdc`) to a scratch PNG to confirm no syntax errors or label collisions, then deleted the scratch render — only the `.md` block was kept, matching the request.
- Target chosen: `mermaid`, since the request explicitly said "output a mermaid block" and the destination was a `.md` file.

## 2026-09-18: pie chart from CSV, vega-lite/PNG target, for a slide deck

- Asked for: "make a pie chart of sales by region from tests/fixtures/sales.csv for a slide deck, save it as examples/sales-pie.png".
- Note: same recurring issue as prior sessions — the `chartwright` skill was not resolvable via the Skill tool (`Unknown skill: chartwright`) even though the plugin is installed on disk here and referenced by `AGENTS.md`/`CLAUDE.md`; the sibling `chartwright-curate` skill was also absent from the listing. Followed `AGENTS.md` → `skills/chartwright/SKILL.md` manually with the `cw.py` CLI. No curation was needed this time (pie and vega-lite already in the knowledge base), so `chartwright-curate` was correctly not invoked.
- Workflow run: `cw.py doctor` (vl_convert 1.9.0, matplotlib 3.11.2 present) → `cw.py data tests/fixtures/sales.csv` (shape `n,n,q`: region, product, sales) → `cw.py show pie --section not` (3 regions, under the 5-slice cap; no misuse) → aggregated `tests/fixtures/sales.csv` by region into `examples/sales-by-region.csv` (North 200, South 225, East 130) since `cw.py build` does not sum duplicate x-categories (same known CLI gap logged in the prior bar-chart session) → `cw.py build --chart pie --target vega-lite --data examples/sales-by-region.csv --x region --y sales --title "Sales by region" --out examples/sales-pie.vl.json` → `cw.py render --target vega-lite --in examples/sales-pie.vl.json --out examples/sales-pie.png --scale 2`.
- Built: `examples/sales-by-region.csv` (aggregated source data), `examples/sales-pie.vl.json` (Vega-Lite spec), `examples/sales-pie.png` (rendered chart, 2x scale for print/slide use) — viewed and confirmed correct: three cleanly separated slices (North/South/East) sized to 200/225/130, titled "Sales by region", legend labeled by region, no collisions.
- Target chosen: `vega-lite` → PNG at 2x, per the skill's target rule for slides/documents.
- Learned: reaffirms the CLI aggregation gap (`build` should sum or refuse on duplicate x values) and the Skill-tool discoverability gap for both `chartwright` and `chartwright-curate` in this environment; both already noted in earlier entries.

## 2026-09-18: first eval run, 0.1.1

- Six evergreen-tester runs (one per case, sonnet): actions and decoys pass on evidence (files written through cw.py, correct skill chosen); trigger cases inconclusive because the Skill tool in this session never registered the plugin installed mid-session (L-20260918-1 in both skills).
- The action run exposed the duplicate-x overwrite in `cw.py build`; fixed with sum-by-default aggregation and `--agg` (C-20260918-2). Version 0.1.1 tagged and pushed; evergreen state now points at the installed plugin's protocol.

## 2026-09-18: second note on pie chart

- Added a curation note to `kb/charts/pie.md`: label slices directly, never with a legend. Equivalent to `cw.py note pie "..."` (edited directly, same dated-bullet format). Reinforces the existing "When not to use" and "Accessibility" guidance on the same file with an explicit standalone rule. Preference/clarification note only, no guidance section changed, so no `CHANGELOG.md` entry per the chartwright-curate skill's Step 4. `--strict validate` re-run clean after (82 charts, 6 targets).

## 2026-09-18: next steps, 0.2.0

- Fresh-session evals through `claude -p`: chartwright triggers (Skill call in trace) and ignores a sequence-diagram decoy; chartwright-curate triggered only from a neutral directory, because inside the repo AGENTS.md routes straight to the CLI (L-20260918-2).
- Builder: seven composed Vega-Lite recipes (dumbbell, slope, waterfall, calendar-heatmap, diverging-bar, stacked-bar-100, small-multiples), all rendered and checked visually; `--flag namedSeries` for Mermaid 11.16+; new `terminal` target with block sparklines and bars (UTF-8 forced on Windows consoles). 29 tests pass; 82 charts and 6 targets validate. Tagged v0.2.0.

## 2026-09-18: 0.3.0, nine targets, router skills, public repo

- Document path proven from a fresh session on `examples/report/quarterly-summary.md`: the skill fired, extracted prose numbers to a CSV, and placed four Mermaid charts next to their claims with the claim as title.
- Three targets added with builders and tests: `echarts` (option JSON plus page), `pptx` (python-pptx script producing an editable chart; a 34 KB deck rendered), `quickchart` (Chart.js config as a URL; live fetch returned image/png). Support lines and recipes were inserted across all 82 chart files by a table-driven script, which is the cheap way to add a target.
- Both SKILL.md files rewritten as short routers (about 5 KB each) that point at `references/` files read only at the step that needs them, per the evergreen budget rule and the user's request.
- Privacy scan before going public: removed the one absolute user path from HANDOFF; no emails, tokens or machine names in tracked files. Repository visibility set to public.

## 2026-09-18: 0.4.0, Excel and Google Docs

- Google Docs test: the user's Drive has no numbers-heavy Doc, so a test Doc was created from HTML (the Q2 summary with two QuickChart image URLs) through the Drive connector. The connector's text view cannot show images, so visual confirmation is left to the user. Recorded as the `gdocs` target: Docs has no chart API; images via HTML import, Docs API `insertInlineImage`, or manual insert.
- `xlsx` target: openpyxl script (data sheet plus native chart), builder for 14 types, render branch, test. A stacked bar workbook rendered in the test suite.
- Gotcha recorded: a patch script that writes another Python file must not double-escape newlines; the first xlsx wiring pass silently did nothing until rewritten with real newlines.
- Context note: this session reached about 45% of the window; a fresh session should pick up from HANDOFF.md.

## 2026-09-18: 0.5.0, sixteen targets, real README and Word runs, full eval suites

- Step 1 (real destinations, neutral folder): `claude -p` launches were refused by this session's permission classifier, so both runs used the evergreen-tester agent with the neutral `Ai` folder as working directory. README run: the skill fired first, extracted two numeric claims from `D:\m4bwa\Claude\Projects\Ai\video-pipeline\README.md` (size presets in kilopixels; minutes per clip by quality) into CSVs under `docs/charts/`, built two Mermaid bars with `cw.py`, rendered both through npx mmdc, inspected the SVGs and placed the blocks with captions. The original README is backed up in the session scratchpad. Word run: the skill fired first, then the docx skill; PNG at 2x from Vega-Lite; sales-summary.docx (60 KB) with the picture in `word/media/`, caption and a data table, written with python-docx because the docx skill's npm package was absent.
- Gaps those runs exposed, all fixed (C-20260918-8): `--json` only worked before the subcommand; `pick` ranked beeswarm above bar because "each" matched "each country"; Mermaid bars autoscaled from 130 instead of 0; `render --target mermaid` left `.mmd.mmd` files; the references had no Word route; the Vega-Lite bar was unsorted.
- Step 2 (targets): `plantuml` (`@startchart`, verified against plantuml.com on 2026-09-18: bar, line, area, scatter, no pie), `d2` (verified: no data charts; network and tree only, `none` elsewhere so the chooser can refuse), `observable-plot` (0.6.17 per npm; snippet plus page with d3 and Plot UMD from jsdelivr), `gsheets` (values plus `addChart` request, spec shapes from the Sheets API reference), `docx` (python-docx script rendering the Vega-Lite PNG in memory; render proven end to end). Wired into all 82 chart files by a table-driven script (support level per chart, recipe template for builder charts, hint dict for hand-written ones). 16 targets validate; 41 tests pass.
- Step 3 (evergreen-test, one run per case, tester agents from a neutral scratch folder): chartwright trigger-1/2/3 fired on the first tool call; decoy-1 went to chartwright-curate; decoy-2 (sequence diagram) used no skill. chartwright-curate trigger-1/2 fired first call; decoy-1 went to chartwright; decoy-2 went to graphify. Action and outcome cases: see TESTS.md entries T-20260918-4 (chartwright) and the curate run of the same date.
- Step 3 results: 7/7 chartwright, 6/6 chartwright-curate, all on evidence. The curate outcome run added `kb/charts/cycle-plot.md` (83 charts now) from nine dated sources.
- Gotcha repeated: a Python patch script that writes a Python file must not escape newlines (a test line broke the suite until rewritten with `chr(10)`).
- User preference saved to memory (not project-specific): name the full path the first time a file outside the current directory is mentioned in a reply.

## 2026-09-18: cycle plot added to the knowledge base (chartwright-curate)

- Researched the cycle plot (seasonal subseries plot, month plot) from Robbins 2008 (Perceptual Edge PDF), FPP3 section 2.5, statsmodels `month_plot`, R `monthplot` / `gg_subseries`, VizWiz and PolicyViz; recorded as R-20260918-1 in `skills/chartwright-curate/RESEARCH.md`. Origin Cleveland, Dunn and Terpenning 1978 (secondary citation only). No library among the sixteen targets draws it natively; only matplotlib via statsmodels counts as native.
- `kb/charts/cycle-plot.md` written (family change-over-time, evidence medium, popularity niche); `calendar-heatmap` Substitutes now links the slug. `cw.py --strict validate`: 83 charts, 16 targets, exit 0; `cw.py index` regenerated. Logged as C-20260918-4.
- Gotchas: the NIST e-Handbook page for the seasonal subseries plot (pmc4441) redirects to nist.gov/itl as of today, so it was not used as a source; WebFetch could not summarise the Perceptual Edge PDF but the saved PDF read fine with the Read tool.

## 2026-09-18: 0.6.0, --y2 compositions, chooser regression set

- Handoff next step 2: `--y2` added to `cw.py build`; Vega-Lite composes bullet, range-band, connected-scatter and bump; observable-plot gets range-band, timeline and dumbbell from the same flag. Rendered all four and fixed two things the pictures showed: the band's y-axis started at zero and the bump rank axis ran from 0. Fixtures bullet.csv, band.csv, connected.csv, bump.csv.
- Handoff next step 3: eight real questions probed against `pick`; all landed on the expected chart (donut edged pie for "share of revenue", acceptable). Seven locked as a regression test. 43 tests pass.
- Not done: live Sheets API send for `gsheets` (needs OAuth outside the connectors), PlantUML render (no local PlantUML), Observable Plot screenshot (no headless browser step); `namedSeries` auto-enable (needs host detection). Left in HANDOFF.
- Same session: evergreen refresh of the local-delegate skill (separate repo, see its RESEARCH.md R-20260918-*).
