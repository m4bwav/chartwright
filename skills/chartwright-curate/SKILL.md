---
name: chartwright-curate
description: "Grow and correct chartwright's chart knowledge base so the next chart request is cheaper and better: research a chart type or chart question the knowledge base cannot answer ('what is a raincloud plot and when is it better than a violin', 'is there a chart for showing two distributions before and after', a request that chartwright's chooser returned no match for), add a chart type ('add the horizon chart to the knowledge base'), add or update a render target ('add ECharts as a target', 'add PowerPoint native charts'), record a note or correction on a chart type ('add a note to the pie chart entry', 'note on the line chart entry', 'note that pies are fine for two slices', 'never suggest gauges to me', anything that mentions the chart knowledge base or a chart's entry), re-rank popularity and velocity from current sources, or check the knowledge base for gaps and rot ('audit the chart knowledge base', 'which chart entries are unverified'). Use whenever the user says add a chart type, add a target, note on a chart, research this chart, update the chart knowledge base, or when the chartwright skill hands over a novel request; also for 'refresh chartwright-curate' and 'is chartwright-curate stale'. Building an actual chart is the chartwright skill; codebase knowledge graphs are graphify."
---

# chartwright-curate

Outcome: the knowledge base under `<plugin root>/kb/` gained or corrected an entry that `cw.py --strict validate` accepts, `kb/INDEX.md` was regenerated, the change is logged with its reason, and research is recorded with sources so the entry can be re-verified later.

Plugin root: two levels above this file. `CW` = `python "<plugin root>/scripts/cw.py"`. Schema: `kb/SCHEMA.md`. The full procedure for each path is in [references/procedures.md](references/procedures.md); read only the section you need.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `verify_at_use` is true, re-check the listed `volatile_claims` before relying on them. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then run the refresh (`evergreen-refresh`) in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task. Never block the task on a refresh unless the task depends on the stale claim.

## Step 1: route

Check first: `CW list` and a grep of `kb/charts/*.md` for the name and its aliases. A chart that exists under another name gets an alias, not a new file.

| Ask | Path (section in references/procedures.md) | Core action and its evidence |
|---|---|---|
| A chart type or question the index lacks | A (research) then B (add) | an `R-` entry in RESEARCH.md; a new `kb/charts/<slug>.md` that validates |
| A note or correction on an existing chart | C | `CW note <slug> "<text>"` (dated line in the file) or an edited section plus a `C-` entry |
| A new place to render charts | D | `kb/targets/<slug>.md`, a support line in every chart, recipes, builder and tests when mechanical |
| "Audit", "gaps", "what is stale" | E | validate output, re-verified entries with `last_verified` updated, the report |

## Step 2: prove it

Every path ends with `CW --strict validate` (exit 0) and `CW index`; a change to `scripts/cw.py` also runs `python -m unittest discover -s tests`. Log the change as a `C-` entry in [CHANGELOG.md](CHANGELOG.md) (what, why, the `R-`, `L-` or `T-` id it answers) and bump the counter with the evergreen plugin's `evergreen.py bump <this dir> --changes`. Nothing is reported done until validate and index have run.

## Output

One to three lines: what was added or changed (file paths), the validate and index result, and the `R-`/`C-` ids written.

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` now (check existing entries first: add, update, retire, or nothing). If a learning proves a claim above wrong, fix it here, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (topic: sources for chart taxonomy, perception evidence, and library chart menus used to grow the chart knowledge base; tier `moderate`, currently every 30 days, next due 2026-10-17). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md) and `evals/evals.json`; procedures in `references/`. Protocol: the installed evergreen plugin (`protocol: "plugin"` in evergreen.json). Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`; audit with `evergreen-audit`.
