# Learnings: chartwright-curate

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: ../../protocol/PROTOCOL.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first (add / update / retire / none). Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

<!-- Example (delete once you have a real entry):
### L-001 · 2026-09-17 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20260917-1, T-20260917-1, confirmed 2026-09-17
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-17
-->

### L-20260918-1 · 2026-09-18 · A plugin installed mid-session is invisible to that session's Skill tool
- Trigger: every eval run in the creating session got "Unknown skill: chartwright" although `claude plugin install` had succeeded; testers fell back to reading SKILL.md and running cw.py by hand.
- Hypothesis: the skill registry is built at session start; subagents inherit it.
- Evidence: six tester runs on 2026-09-18, each with the Skill call failing and the skill absent from the available-skills list, while `claude plugin install` had reported success and the folder existed.
- Rule: trigger evals run from a session started after the install; same-session trigger results are recorded as inconclusive.
- Apply: after installing or renaming a skill, run evergreen-test from a fresh session; treat same-session trigger results as inconclusive, not failing.

### L-20260918-2 · 2026-09-18 · Trigger evals run inside the plugin's own repo are biased
- Trigger: two fresh-session runs in D:\...\chartwright wrote the note through cw.py without invoking chartwright-curate; the same prompt from an empty directory invoked the skill.
- Hypothesis: the repo's AGENTS.md and CLAUDE.md name the CLI first, so the model takes the documented route before considering skills.
- Evidence: T-20260918-2 (in repo, no Skill call) vs T-20260918-3 (neutral directory, Skill call in the trace).
- Rule: run trigger cases from a neutral working directory; in-repo results count only for action evidence.
- Apply: evergreen-test for this plugin starts `claude -p` from a scratch folder.

