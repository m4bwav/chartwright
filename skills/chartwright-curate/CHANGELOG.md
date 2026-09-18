# Changelog: chartwright-curate

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: the installed evergreen plugin (`protocol: "plugin"` in evergreen.json).

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20260918-1 · 2026-09-18 · Description: "add a note to the <chart> entry" phrasings
- because: T-20260918-2 (fresh-session run wrote the note through the CLI without invoking the skill: undertrigger)
- files: SKILL.md (description)
- Added the "add a note to the pie chart entry", "note on the line chart entry" and "anything that mentions the chart knowledge base or a chart's entry" phrasings.

### C-20260917-1 · 2026-09-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20260917-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
