# Tests: chartwright

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: ../../protocol/PROTOCOL.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

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
