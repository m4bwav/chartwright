# Curation procedures (chartwright-curate, full detail)

`CW` = `python "<plugin root>/scripts/cw.py"`. Schema: `kb/SCHEMA.md`. Authoring standard: `ai-docs/notes/kb-authoring-brief.md`. Read only the section for the path you are on.

## A. Research a chart type or question

Search primary sources, newest first, on four tracks, and keep the notes:

1. Subject: what the chart is, what it encodes, its aliases. Sources in order: the Financial Times Visual Vocabulary, the Data Visualisation Catalogue, From Data to Viz, Datawrapper's blog, then the paper or tool that introduced it.
2. Evidence: perception studies on the encoding (start from `kb/rules/evidence.md`; search `"<chart>" perception study`, `"<chart>" Cleveland McGill`, `site:eagereyes.org <chart>`) and practitioner guidance on misuse.
3. Popularity and velocity: which of Vega-Lite, Plotly, ECharts, Chart.js, Observable Plot, D3, matplotlib, seaborn, Datawrapper, Flourish, Mermaid and python-pptx support it natively; release notes that added it in the last three years (rising) or guides that discourage it (declining). Record what was checked and the date.
4. Build: the idiomatic minimal recipe per target from official docs; mark `approx` or `image` honestly.

Write an `R-` entry in `RESEARCH.md` next to the skill (date, question, sources with URLs, what changed) before touching the knowledge base. Unverified facts are said to be unverified in the chart file's Evidence section.

## B. Add a chart type

1. `CW new-chart <slug> --name "<Name>" --family <family> --shapes "<shape>" ...` writes the stub with every section and a `support:` line per target.
2. Fill it to the standard of `kb/charts/line.md`: frontmatter (aliases, family, also, question, shapes, goals, caps, evidence, popularity, status, support for every target, sources); When to use; When not to use; Substitutes (existing slugs in backticks); Evidence (author-year, how strong); Accessibility; Build (a `###` per native or approx target; name `CW build` only for charts the builder supports, listed in `skills/chartwright/references/build-and-verify.md`); Notes with the dated origin line.
3. If the chart is common enough for the builder, add the recipe to `scripts/cw.py` (`build_vega_lite` or `_vl_composed` first, then other targets), a test in `tests/test_cw.py`, and run `python -m unittest discover -s tests`.
4. `CW --strict validate` then `CW index`; both must pass.
5. Log a `C-` entry in `CHANGELOG.md` next to the skill (what, why, the `R-` id) and bump: `python <evergreen plugin>/scripts/evergreen.py bump <this skill dir> --changes`.

## C. Note or correct an existing chart

- Preference or lesson about one chart: `CW note <slug> "<text>"` appends a dated line under `## Notes`. If it changes the guidance (a cap, a "when not"), edit that section too and log a `C-` entry. A preference that applies to every chart ("never pies") goes to `LEARNINGS.md` next to the skill; the chartwright skill reads it in its Step 6.
- Factual correction with a source: edit the section, update `last_verified` and `sources`, log the `C-` entry citing the source. If it contradicts `kb/rules/`, fix the rule and set `contradiction` in `evergreen.json` so the next refresh re-checks the area.

## D. Add or update a render target

1. `CW new-target <slug> --name "<Name>" --kind markdown|web|image|office|terminal`; fill: what it can draw (slugs with support levels), syntax essentials, limits, render (how to get a file out, installs), notes. Candidates researched but not built: `xlsx` (openpyxl), `gsheets` (Sheets API EmbeddedChart), `plantuml` (`@startchart`), `d2`, `observable-plot`.
2. Every chart file needs a `<slug>:` support line (`CW --strict validate` lists the gaps) and a `### <slug>` recipe for native or approx. A small script that inserts the lines and one-line recipes from a table is the token-efficient route (see `ai-docs/log.md` 2026-09-18 for the pattern used for echarts, pptx and quickchart).
3. If the target can be built mechanically, add `build_<slug>` to `scripts/cw.py`, a branch in `cmd_render` when a headless renderer exists, an `HTML_<SLUG>` wrapper for web targets, and tests.
4. `CW index`, `CHANGELOG.md` entry, a row in `kb/rules/choosing-a-target.md` and in `skills/chartwright/references/build-and-verify.md`.

## E. Audit the knowledge base

1. `CW --strict validate` (schema).
2. List charts whose `last_verified` is older than the skill's interval (`evergreen.json`) or whose Evidence section says unverified; re-check with the tracks in A; update `last_verified` only when a source was actually read.
3. Compare `kb/INDEX.md` with the current menus of Datawrapper, Flourish, Vega-Lite, Plotly, ECharts and Mermaid; add types with real use (in two or more menus, or rising in release notes).
4. Report: counts, what was verified, what was added, what remains unverified.
