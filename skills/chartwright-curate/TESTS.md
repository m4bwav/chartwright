# Tests: chartwright-curate

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: ../../protocol/PROTOCOL.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20260918-4 · 2026-09-18 · evergreen-tester from a neutral scratch folder (sonnet, 1 run per case), full suite · DESKTOP (Windows) · 6/6
- trigger-1 (add the horizon chart) · trigger · pass · `Skill(chartwright:chartwright-curate)` was the first and only call.
- trigger-2 (note on the pie entry) · trigger · pass · Skill call first; routing table path C shown in the loaded SKILL.md.
- decoy-1 (pie of the budget for a slide deck) · trigger · pass · chartwright invoked, curate not.
- decoy-2 (knowledge graph of the codebase) · trigger · pass · graphify invoked, curate not.
- action-1 (note on the line entry) · action · pass · Skill first; the tester found the identical dated note already in HEAD, did not duplicate it, and ran `cw.py --strict validate` and `cw.py index` (both clean). Gap: procedure C does not say what to do when the note already exists (it chose to skip, which is right; documented in references/procedures.md).
- outcome-1 (add the cycle plot) · outcome · pass · Skill first; nine web sources fetched and dated; `cw.py new-chart cycle-plot`; kb/charts/cycle-plot.md (10.6 KB, support for 16 targets, recipes for the nine native/approx); `--strict validate` ok (83 charts); index regenerated; R-20260918-1 and C-20260918-4 written; calendar-heatmap substitutes link added. Renumbered its changelog entry when a concurrent C-3 appeared.
- led to: C-20260918-2 (procedure C: existing-note rule)

### T-20260918-3 · 2026-09-18 · claude -p fresh session from a neutral directory (sonnet, 1 run) · DESKTOP (Windows) · 1/1
- trigger-1 (note on the pie entry) · trigger · pass · trace shows `Skill{"skill":"chartwright:chartwright-curate"}` and kb/charts/pie.md gained the dated note. A second in-repo run after C-20260918-1 still bypassed the skill: inside the plugin repo, AGENTS.md points straight at cw.py, so in-repo runs are not a fair trigger test (L-20260918-2).
- led to: L-20260918-2

### T-20260918-2 · 2026-09-18 · claude -p fresh session (sonnet, 1 run) · DESKTOP (Windows) · 0/1 trigger, action evidence present
- trigger-1 (note on the pie entry) · trigger · undertrigger · no Skill call in the trace, yet kb/charts/pie.md gained the dated note (the CLI route was found from AGENTS.md). Fix: C-20260918-1 (description phrasings); re-run recorded as T-20260918-3.
- led to: C-20260918-1

### T-20260918-1 · 2026-09-18 · evergreen-tester (sonnet, 1 run per case) · DESKTOP (Windows) · 2/2 action+decoy, trigger inconclusive
- trigger-2/action-1 · action · pass · `python scripts/cw.py note line "prefer end labels..."` in the trace; kb/charts/line.md ends with the dated note. Skill call itself returned "Unknown skill" (plugin installed mid-session), so the trigger half is inconclusive.
- decoy-1 · trigger · pass · chartwright-curate never invoked; the pie was built and rendered to examples/sales-pie.png (46 KB) through the chartwright procedure.
- led to: L-20260918-1 (shared with chartwright)

### T-20260917-1 · 2026-09-17 · not yet run · skill · 0/0
- Suite scaffolded; no run recorded. Write the cases in `evals/evals.json` (at least two trigger prompts, two decoys, one action case with evidence, one outcome case), run the baseline without the skill, then run with it (`evergreen-test`).
- led to: none
