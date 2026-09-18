# HANDOFF

Updated 2026-09-18 (v0.2.0 pushed: terminal target, composed Vega-Lite recipes, fresh-session evals). Read this first, then `ai-docs/log.md`.

## State

- Plugin `chartwright` 0.1.0 at `D:\m4bwa\Claude\Projects\Ai\chartwright`, installed in Claude Code from the `mark-local` marketplace, pushed to the private repo `m4bwav/chartwright`.
- Knowledge base: 82 chart files, 5 targets, rules; `python scripts/cw.py --strict validate` clean and 26 unit tests pass at handoff. Tags v0.1.0 and v0.1.1 on the repo.
- Skills are evergreen: `chartwright` due 2026-10-01 (fast), `chartwright-curate` due 2026-10-17 (moderate). Evals in `skills/*/evals/evals.json`; results in `skills/*/TESTS.md`.

## Next steps (in order of value)

0. Done 2026-09-18: fresh `claude -p` sessions from a neutral directory invoke both skills (T-20260918-2/3). Run future trigger evals from outside the repo (L-20260918-2 in chartwright-curate).
1. Use it on a real document and a real README; capture learnings and notes with `cw.py note`.
2. Add targets that were researched but not built: `echarts` (v6.1, chord and beeswarm native), `pptx` (python-pptx native charts), `terminal` (plotext), `quickchart` (Chart.js config as a URL image).
3. Extend `cw.py build` to more types in Vega-Lite (dumbbell, slope, waterfall, bullet, calendar heatmap are all layer or transform recipes already described in the chart files).
4. Mermaid: emit named series (`line "name" [...]`) when the host is known to be 11.16+; today the builder emits unnamed series for the 11.13 floor.
5. Run the evergreen refresh when due; Mermaid 12 host adoption (GitHub, Obsidian) is the claim most likely to change.

## Gotchas

- `cw.py` fails soft (exit 0 with a note) unless `--strict`; tests and CI use `--strict`.
- `kb/INDEX.md` and `kb/index.json` are generated; regenerate after any kb edit.
- Optional renderers: vl-convert-python (installed here), matplotlib (installed), mmdc (not installed; `npx` fallback downloads Chromium on first use).
