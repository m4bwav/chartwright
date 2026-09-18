# Knowledge base schema

One file per chart type in `kb/charts/<slug>.md`, one per render target in `kb/targets/<slug>.md`, cross-cutting rules in `kb/rules/`. `scripts/cw.py index` compiles the frontmatter into `kb/index.json` and `kb/INDEX.md` (the compact table an agent reads first; it costs about 1/20 of the tokens of the full folder). `scripts/cw.py validate` enforces this schema.

## Chart file frontmatter

```yaml
---
name: Line chart                # canonical display name
slug: line                      # = file name
aliases: [line graph, time series plot]
family: change-over-time        # exactly one primary FT Visual Vocabulary family (list below)
also: [correlation]             # other families it can serve (optional)
question: How does a value change over time?
shapes: ["time,q", "time,q*n"]  # data shapes it takes (grammar below)
goals: [trend, change, over time, forecast, series]   # words a request contains when this chart fits
max_series: 8                   # soft cap before the chart degrades (0 = n/a)
max_categories: 0               # soft cap on categories on the main axis (0 = n/a)
evidence: high                  # high | medium | low : strength of perceptual evidence for this chart doing its job
popularity: core                # core | common | niche | rising | declining
status: stable                  # stable | experimental | deprecated
support:                        # per target: native | approx | image | none  (image = only as a rendered picture)
  mermaid: native
  vega-lite: native
  plotly: native
  chartjs: native
  matplotlib: native
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://..., https://...]
---
```

### Families (from the Financial Times Visual Vocabulary, plus three practical extras)

`deviation`, `correlation`, `ranking`, `distribution`, `change-over-time`, `magnitude`, `part-to-whole`, `spatial`, `flow`, and the extras `hierarchy`, `relationship` (network), `single-value` (KPI tiles, meters), `table`.

### Data shape grammar

A shape is a comma-separated list of field kinds in the order the chart consumes them:

| Kind | Meaning |
|---|---|
| `time` | temporal field (date, datetime, period) |
| `q` | quantitative (numbers on a continuous scale) |
| `n` | nominal category |
| `o` | ordered category (Likert, size classes, months as labels) |
| `geo` | geographic key or geometry |
| `hier` | a hierarchy (path or parent/child) |
| `flow` | source, target, weight triples |
| `text` | free text (word clouds, tables) |

Suffix `*n` on the last kind means "one series per category value" (multi-series); `+` means one or more of that kind (`q+` = several quantitative columns). Examples: `n,q` bar chart; `time,q*n` multi-line; `q,q` scatter; `q,q,q` bubble; `n,n,q` heatmap; `q` histogram; `hier,q` treemap; `flow` sankey; `geo,q` choropleth.

## Body sections (in this order; the CLI reads them by heading)

1. `## When to use` : the questions it answers and what it excels at (3-8 bullets).
2. `## When not to use` : the misuse patterns and the limit conditions.
3. `## Substitutes` : the chart to reach for instead, and when.
4. `## Evidence` : the perceptual or practitioner evidence, cited, with the honest confidence.
5. `## Accessibility` : what it needs to be readable by everyone.
6. `## Build` : one `### <target slug>` subsection per supported target with the idiomatic minimal recipe, or the reason it is `approx`/`image`.
7. `## Notes` : dated free-form notes (`- 2026-09-17: ...`), appended by `cw.py note`. User corrections land here first.

## Target file frontmatter

```yaml
---
name: Markdown (Mermaid)
slug: mermaid
kind: markdown | web | image | office | terminal
renders_in: [GitHub, GitLab, Obsidian, VS Code]
version_checked: "11.x"
last_verified: 2026-09-17
renderer: mmdc                # what cw.py render calls, or none
tested: untested              # or a list of "<platform> <date>: <what was proven>"; the chartwright skill warns the user when their platform is missing and offers to test and record (cw.py tested)
sources: [...]
---
```

Body: `## What it can draw` (a table of chart slugs and support level), `## Syntax essentials`, `## Limits`, `## Render` (how to get a file out), `## Notes`.

## Adding a chart type

`python scripts/cw.py new-chart <slug> --name "<Name>" --family <family>` writes a stub with every section and TODO markers; fill it, then `cw.py validate` and `cw.py index`. Anything learned in use goes in `## Notes` via `cw.py note <slug> "<text>"`; a note that changes the guidance is promoted into the section it belongs to on the next curation pass, and the change is logged in the skill's CHANGELOG.md.
