# Tests: chartwright

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: ../../protocol/PROTOCOL.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20260918-4 · 2026-09-18 · evergreen-tester from a neutral scratch folder (sonnet, 1 run per case), full suite · DESKTOP (Windows) · 7/7
- trigger-1 (line graph from prices.csv) · trigger · pass · `Skill(chartwright:chartwright)` was tool call 1 of 1.
- trigger-2 (add graphs to quarterly-summary.md) · trigger · pass · Skill call first, no file reads before it.
- trigger-3 (which chart for funnel drop-off) · trigger · pass · Skill call first.
- decoy-1 (add horizon chart to the knowledge base) · trigger · pass · chartwright-curate invoked, chartwright not.
- decoy-2 (sequence diagram) · trigger · pass · no Skill call; Mermaid sequenceDiagram written directly.
- action-1 (bar of sales by region for a README) · action · pass · Skill first; `cw.py show bar --section not`, `cw.py data`, `cw.py build --chart bar --target mermaid --agg sum`, `cw.py render --target mermaid` (SVG 8,165 bytes) in the trace; README.md holds the xychart block with `y-axis "sales" 0 --> 250` and summed bars 200/225/130. Tester grepped the SVG text instead of viewing the image.
- outcome-1 (PNG line chart into out/price.png) · outcome · pass · Skill first; `cw.py show line --section not`, `cw.py data`, `cw.py build --chart line --target vega-lite`, `cw.py render` (exit 0) in the trace; out/price.png 140,528 bytes, viewed twice; reply named the type and rule in two lines. Gap fixed in C-20260918-8: monthly dates got fortnightly ticks, hand-edited by the tester.
- led to: none (the 0.5.0 fixes from T-20260918-3 held: zero baseline present, summing on, no flag-order error)

### T-20260918-3 · 2026-09-18 · evergreen-tester from the neutral Ai folder (sonnet, 1 run each), two real destinations · DESKTOP (Windows) · 2/2
- readme (action+outcome, another repo) · pass · Skill call first; cw.py data, pick, show, build, render in the trace; two Mermaid bar blocks placed after the `--size` table and at the end of Batch sizing in video-pipeline/README.md, both rendered to SVG through npx mmdc and inspected. Gaps found: `--json` trailing the subcommand failed; pick ranked beeswarm above bar; bars lacked `0 --> max`; render left `.mmd.mmd` files.
- docx (action+outcome, Word destination) · pass · Skill call first, then the docx skill; cw.py build bar vega-lite, render PNG at 2x; sales-summary.docx 60,526 bytes with word/media/image1.png, one 6 in inline shape, caption and data table. Gap found: no Word route in the references.
- Note: `claude -p` from this session was refused by the permission classifier, so both runs used the tester agent with the session's neutral working directory.
- led to: C-20260918-7, C-20260918-8, L-20260918-3

### T-20260918-2 · 2026-09-18 · claude -p fresh sessions (sonnet, 1 run per case) · DESKTOP (Windows) · 2/2
- trigger-1 · trigger · pass · trace shows `Skill{"skill":"chartwright:chartwright"}`; examples/eval-trigger.md holds the xychart block built by cw.py.
- decoy-2 (sequence diagram) · trigger · pass · no Skill call in the trace.
- led to: none (resolves the inconclusive trigger of T-20260918-1)

### T-20260918-1 · 2026-09-18 · evergreen-tester (sonnet, 1 run per case) · DESKTOP (Windows) · 3/3 action+decoy, 1 trigger inconclusive
- trigger-1 · trigger · harness · Skill("chartwright") returned "Unknown skill": the plugin was installed after this session started, so the tester's registry lacked it. Inconclusive, not a failure; re-run from a fresh session.
- decoy-1 · trigger · pass · chartwright was not invoked; the tester reached for chartwright-curate (also unregistered) and did the note via cw.py, then reverted.
- action-1 · action · pass · `cw.py --json pick ...` and `cw.py build --chart bar --target mermaid ...` in the trace; examples/sales-by-region.md contains the xychart block; rendered via npx mmdc. Surfaced the duplicate-x aggregation bug (C-20260918-2).
- outcome (trigger-1's run doubled as outcome) · pass · examples/prices/price-line.png rendered from cw.py build + render and viewed.
- led to: L-20260918-1, C-20260918-2

### T-20260917-1 · 2026-09-17 · not yet run · skill · 0/0
- Suite scaffolded; no run recorded. Write the cases in `evals/evals.json` (at least two trigger prompts, two decoys, one action case with evidence, one outcome case), run the baseline without the skill, then run with it (`evergreen-test`).
- led to: none
