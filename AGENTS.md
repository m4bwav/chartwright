# AGENTS.md

Rules for any AI agent (Claude Code, Copilot, Cursor, Codex) working in this repository. `CLAUDE.md` and `.github/copilot-instructions.md` only point here.

## What this is

A plugin: two skills under `skills/`, a chart knowledge base under `kb/`, one CLI at `scripts/cw.py`, tests under `tests/`. The README has the layout and the CLI. Handoff notes, decisions and the log are under `ai-docs/` (start with `ai-docs/HANDOFF.md`).

## Rules

- The knowledge base is the product. Edit `kb/charts/*.md` and `kb/targets/*.md` by the schema in `kb/SCHEMA.md` and the standard in `ai-docs/notes/kb-authoring-brief.md`; then run `python scripts/cw.py --strict validate` and `python scripts/cw.py index`. Never edit `kb/INDEX.md` or `kb/index.json` by hand.
- `scripts/cw.py` stays standard-library Python that runs on Windows, macOS and Linux. Optional renderers are imported lazily and their absence is a message, not a crash.
- Every change to the CLI has a test in `tests/test_cw.py`; run `python -m unittest discover -s tests` before committing. Tests must pass on a machine with no optional renderer (they skip, not fail).
- Every change is logged: the skill's `CHANGELOG.md` for skill or knowledge changes, the root `CHANGELOG.md` for the plugin version, `ai-docs/log.md` for the session. Bump the version in `.claude-plugin/plugin.json` (semver: knowledge additions are minor, fixes are patch, schema or CLI breaking changes are major) and tag the repo to match.
- Research beats recall: chart library versions, syntax and host support change; the skills are evergreen units, so refresh through the evergreen plugin (`evergreen-refresh`) rather than editing versions from memory. Record sources with dates.
- No AI attribution anywhere: no Co-Authored-By trailers, no "generated with" lines in commits, PRs or files.
- Prose style in knowledge files: plain, short sentences, no em dashes, cite by author-year, say when something is unverified.
