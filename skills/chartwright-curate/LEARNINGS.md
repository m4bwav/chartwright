# Learnings: chartwright-curate

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: ../../protocol/PROTOCOL.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first (add / update / retire / none). Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-20261017-1 · 2026-10-17 · Date a feature's arrival from release notes, not the docs page header
- Trigger: the 2026-09-17 research and the knowledge base said Mermaid 12.0 added treemap and venn, because the syntax pages carried a 12.0 heading; the release bodies put treemap in 11.8.0 and venn-beta in 11.13.0, so for a month treemap and venn were routed to images on hosts that could draw them.
- Hypothesis: docs pages are rewritten at each major (a theme or look note for the new version sits at the top), so the newest version named on the page is not the version that introduced the feature.
- Evidence: R-20261017-1, C-20261017-1.
- Rule: before writing "needs version X" in a target or chart file, find the release whose notes say the feature was added (`gh release view <tag> -R <repo>` and grep the body).
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17

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

