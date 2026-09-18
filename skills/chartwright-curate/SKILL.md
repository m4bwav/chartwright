---
name: chartwright-curate
description: "Grow and correct chartwright's chart knowledge base so the next chart request is cheaper and better: research a chart type or chart question the knowledge base cannot answer ('what is a raincloud plot and when is it better than a violin', 'is there a chart for showing two distributions before and after', a request that chartwright's chooser returned no match for), add a chart type ('add the horizon chart to the knowledge base'), add or update a render target ('add ECharts as a target', 'add PowerPoint native charts'), record a note or correction on a chart type ('note that pies are fine for two slices', 'never suggest gauges to me'), re-rank popularity and velocity from current sources, or check the knowledge base for gaps and rot ('audit the chart knowledge base', 'which chart entries are unverified'). Use whenever the user says add a chart type, add a target, note on a chart, research this chart, update the chart knowledge base, or when the chartwright skill hands over a novel request; also for 'refresh chartwright-curate' and 'is chartwright-curate stale'. Building an actual chart is the chartwright skill; codebase knowledge graphs are graphify."
---

# chartwright-curate

Outcome: the knowledge base under `<plugin root>/kb/` gained or corrected an entry that `cw.py --strict validate` accepts, `kb/INDEX.md` was regenerated, the change is logged with its reason, and, for research, the sources and their velocity signals are recorded so the entry can be re-verified later.

Plugin root: two levels above this file. `CW` means `python "<plugin root>/scripts/cw.py"`. Schema: `kb/SCHEMA.md`. Authoring standard: `ai-docs/notes/kb-authoring-brief.md`.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `verify_at_use` is true, re-check the listed `volatile_claims` before relying on them. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then run the refresh (`evergreen-refresh`) in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task. Never block the task on a refresh unless the task depends on the stale claim.

## Step 1: what kind of curation

| Ask | Path |
|---|---|
| A chart type or question the index lacks | Research (Step 2), then Add chart (Step 3) |
| A note or correction on an existing chart | Note (Step 4) |
| A new place to render charts | Add target (Step 5) |
| "Audit", "gaps", "what is stale" | Audit (Step 6) |

Check first: `CW list` and a grep of `kb/charts/*.md` for the name and its aliases. A chart that exists under another name gets an alias, not a new file.

## Step 2: research a chart type or question

Search primary sources, newest first, on four tracks, and keep the notes:

1. Subject: what the chart is, what it encodes, its aliases; sources in this order: the Financial Times Visual Vocabulary, the Data Visualisation Catalogue, From Data to Viz, Datawrapper's blog, then the original paper or the tool that introduced it.
2. Evidence: any perception study on the encoding (start from `kb/rules/evidence.md`; search `"<chart>" perception study`, `"<chart>" Cleveland McGill`, `site:eagereyes.org <chart>`), and practitioner guidance on misuse.
3. Popularity and velocity: which of Vega-Lite, Plotly, ECharts, Chart.js, Observable Plot, D3, matplotlib, seaborn, Datawrapper, Flourish and Mermaid support it natively; release notes that added it in the last three years (rising) or guides that discourage it (declining). Record what was checked and the date.
4. Build: the idiomatic minimal recipe per target from official docs; mark `approx` or `image` honestly.

Write the findings to `RESEARCH.md` next to this file as an `R-` entry (date, question, sources with URLs, what changed) before touching the knowledge base. If a fact could not be verified, the chart file says so in its Evidence section rather than smoothing it over.

## Step 3: add a chart type

1. `CW new-chart <slug> --name "<Name>" --family <family> --shapes "<shape>" ...` writes the stub with every section.
2. Fill it to the standard of `kb/charts/line.md`: frontmatter (aliases, family, also, question, shapes, goals, caps, evidence, popularity, status, support for every target, sources), then When to use, When not to use, Substitutes (existing slugs in backticks), Evidence (cite by author-year; say how strong), Accessibility, Build (a `###` per native or approx target; name `CW build` only for charts it supports, listed in the authoring brief), Notes with the dated origin line.
3. If the chart is common enough that `cw.py build` should support it, add the recipe to the builder (`build_vega_lite` first, then others), add a test in `tests/test_cw.py`, and run the tests.
4. `CW --strict validate` then `CW index`. Both must pass; the index is what the chartwright skill reads.
5. Log: a `C-` entry in `CHANGELOG.md` next to this file (what, why, source `R-` id), and `python <evergreen plugin>/scripts/evergreen.py bump <this skill dir> --changes`.

## Step 4: note or correct an existing chart

- A user preference or a lesson about a chart: `CW note <slug> "<text>"` appends a dated line under `## Notes`. If the note changes the guidance (a cap, a "when not"), edit that section too and log it in `CHANGELOG.md`; a preference that applies to every chart ("never pies") goes to `LEARNINGS.md` next to this file and the chartwright skill reads it via Step 6 there.
- A factual correction with a source: edit the section, update `last_verified` and `sources`, log the `C-` entry citing the source. If the correction contradicts `kb/rules/`, fix the rule and set `contradiction` in `evergreen.json` so the next refresh re-checks the area.

## Step 5: add or update a render target

1. `CW new-target <slug> --name "<Name>" --kind markdown|web|image|office|terminal` and fill the stub: what it can draw (a table of slugs with support levels), syntax essentials, limits, render (how to get a file out, what to install), notes. Candidates already researched (versions in `kb/rules/choosing-a-target.md`): `echarts`, `pptx`, `xlsx`, `gsheets`, `plantuml`, `terminal`, `quickchart`.
2. Every chart file needs a `<slug>:` line in `support:`; `CW --strict validate` lists the gaps. Add a `### <slug>` build recipe to every chart marked native or approx (a short one-liner is fine when the target's own file carries the details).
3. If the target can be built mechanically, add a `build_<slug>` function and, when there is a headless renderer, a branch in `cmd_render`, with tests.
4. `CW index`, `CHANGELOG.md` entry, `kb/rules/choosing-a-target.md` row.

## Step 6: audit the knowledge base

`CW --strict validate` (schema), then list charts whose `last_verified` is older than the skill's interval (`evergreen.json` next to this file) or whose Evidence section says unverified; re-check those with Step 2's tracks, update `last_verified` only when a source was actually read. Compare the index with the current chart menus of Datawrapper, Flourish, Vega-Lite, Plotly, ECharts and Mermaid for types the base lacks; add the ones with real use (present in two or more menus, or rising in release notes). Report: counts, what was verified, what was added, what remains unverified.

## Output

One to three lines: what was added or changed (file paths), the validate and index result, and the `R-`/`C-` ids written.

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` now (check existing entries first: add, update, retire, or nothing). If a learning proves a claim above wrong, fix it here, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (topic: sources for chart taxonomy, perception evidence, and library chart menus used to grow the chart knowledge base; tier `moderate`, currently every 30 days, next due 2026-10-17). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md) (every change, with reasons), [LEARNINGS.md](LEARNINGS.md) (lessons), [TESTS.md](TESTS.md) and `evals/evals.json` (the cases that prove it and the runs). Protocol: the evergreen plugin's `protocol/PROTOCOL.md` (../../protocol/PROTOCOL.md when this plugin is vendored beside it). Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`; audit with `evergreen-audit`.
