---
title: GitHub wiki written and published for chartwright 0.8.4 (tag v0.8.4, 34b1871)
kind: note
date: 2026-10-03
verified: 2026-10-03
stale_after: 2027-04-03
tags: [wiki, docs, 0.8.4, github]
summary: "the chartwright wiki's pages, where the working copy is, how every example was verified against a fresh GitHub clone, facts found, inaccuracies in the shipped docs, and how to update the wiki"
---

# GitHub wiki for chartwright 0.8.4

This folder sits outside the chartwright repository on purpose: on 2026-10-03 another session was preparing chartwright for the Claude plugin directory from `master`, and the brief forbade commits there. Move these four files into `chartwright/ai-docs/notes/` (and add a HANDOFF line and a log entry) once that settles.

## Summary

Written with the wikiwright skill (0.9.0). Ten pages plus sidebar and footer, wiki commit `63c3f7d` on https://github.com/m4bwav/chartwright/wiki, pushed over Mark's placeholder Home page (plain fast-forward). `wikiwright.py live`: 10 pages, 0 failures, sidebar and footer render, 23 anchor links fine. `check --version 0.8.4`: 0 errors. `outputs` (both saved outputs): 83 checked, 0 missing, 8 skipped (Claude Code commands, hand-run transcripts, usage synopsis, release command). `snippets`: 1 block checked, 5 commands. `tells.py --wiki`: 0 strong on every page, 7 weak (sentences of 31 to 34 words, two "rather than", one repeated opening).

Pages: Home, Getting-Started, How-The-Skills-Work, How-Charts-Are-Picked-And-Built, Render-Targets, Commands, Recipes, Versions-and-Upgrading, FAQ, Development, _Sidebar, _Footer.

Page set: the agent-skill set (command-line tool set with Commands, no API reference), with one behaviour page for the skills (How-The-Skills-Work) and one for the CLI (How-Charts-Are-Picked-And-Built), plus Render-Targets as a data page (16 targets, builder coverage, tested records, network routes).

Master moved twice during the run: 7d24408 (0.8.3) to 34b1871 (0.8.4, tagged) mid-survey, then 464890a (icon only, no behaviour change) after the first push. The wiki describes the tag v0.8.4.

## Where the pages are

`../chartwright.wiki`, branch `master`, remote https://github.com/m4bwav/chartwright.wiki.git. LF, no BOM.

## Updating the wiki later

1. `git -C ../chartwright.wiki pull --ff-only`.
2. Fresh clone: `git clone https://github.com/m4bwav/chartwright.git <scratch>/src`, then `python 2026-10-03-wiki-verify.py <scratch>/src > new.txt`, and again with a Python 3.9 interpreter as the second argument (`<a uv-managed CPython 3.9>` here; it has no renderers). `wikiwright.py diffout 2026-10-03-wiki-verify.out.txt new.txt`. Expect noise in three lines: the pptx and xlsx byte counts (zip timestamps) and the unit-test timing. Bump `v0.8.4` in the gs-copy-route case.
3. `wikiwright.py outputs <wiki> new.txt new39.txt`, `wikiwright.py snippets <wiki> 2026-10-03-wiki-verify.py`, `wikiwright.py check <wiki> --version <v>`, `python <everwrite>/skills/everwrite/scripts/tells.py --wiki <wiki>/*.md`.
4. Commit, push, `wikiwright.py live m4bwav/chartwright <wiki>`.

Pages naming the version, commit or counts: _Footer (0.8.4, 34b1871, date), Home (last line, 83 chart types), Getting-Started (claude 2.1.281 transcript showing 0.8.4, `--branch v0.8.4`, gh 2.100.0 output), Versions-and-Upgrading (table, update transcript 0.8.3 to 0.8.4), How-The-Skills-Work (due date 2026-10-13, 83 chart files), Render-Targets (tested records), Commands and Recipes (run date, Python and renderer versions), Development (45 tests, timings, eval runs T-20261003-1 and T-20260926-1).

## How the examples were verified

`2026-10-03-wiki-verify.py` copies `scripts/`, `kb/`, `skills/`, `tests/` and `.claude-plugin/` from a fresh GitHub clone into a new temp folder per case (40 cases), writes the case's CSV fixtures, and runs each command through Git Bash with stdin closed, printing `$ command`, merged output and `echo $?`; the temp path prints as `<work>`. Two cases reach the network on purpose: a `git clone --branch v0.8.4` (copy route) and `gh skill install`. Saved outputs: `2026-10-03-wiki-verify.out.txt` (Python 3.14.6 with vl-convert 1.9.0, matplotlib 3.11.2, python-pptx 1.0.2, openpyxl 3.1.5, python-docx 1.2.0) and `2026-10-03-wiki-verify.py39.out.txt` (3.9.25, no renderers). Unit tests 45/45 on 3.14, 45 with 5 skipped on 3.9; `--strict validate` clean.

By hand, not in the script, in isolated `CLAUDE_CONFIG_DIR` folders with Claude Code 2.1.281: `claude plugin marketplace add https://github.com/m4bwav/chartwright.git` and `install chartwright@chartwright` (0.8.3 at the time; then `marketplace update` and `plugin update` took it to 0.8.4); the shorthand `m4bwav/chartwright` add and install (0.8.4; cloned over HTTPS, no SSH error, no `~/.ssh/known_hosts` on this machine); `plugin uninstall`; `claude plugin validate .` passed. The installed cache holds `kb/` and `scripts/`, and `cw.py doctor` ran from it.

Not tested: macOS and Linux; Copilot, Codex or Cursor loading the copied skills; `gh skill install --agent/--scope` and `gh skill update`; the Claude directory (submission in progress, the wiki says "once it is listed"); the plantuml, d2, gsheets, observable-plot, plotly and chartjs builders; `render --target mermaid` (no mmdc; npx path not run); opening any pptx, xlsx, docx or HTML output in its program; the trigger and action evals.

## Facts verified while writing (not in the README)

- `gh skill install m4bwav/chartwright --all --dir X/skills` installs only the two skill folders (it picked tag v0.8.4); `kb/` and `scripts/` must be copied beside `skills/` by hand. It adds a `metadata` block (repo, path, ref, tree SHA) to each SKILL.md.
- The copy route works in any `<folder>/skills/<name>/SKILL.md` layout if `kb/` and `scripts/` go in `<folder>`; `cw.py` finds `kb/` from its own path, not the cwd.
- Errors print to stdout as plain lines and exit 0 unless `--strict`; argparse errors exit 2. Only the `--agg` duplicate note goes to stderr.
- `build` does not check the chart slug: `linechart` gives "mermaid has no recipe for 'linechart'", the same as a real chart without a builder.
- `pick` always returns three charts: evidence and popularity bonuses keep core charts above zero, so `pick --question "zzz"` ranks bar, column, diverging-bar at 1.0, and the "no match ... chartwright-curate" note is unreachable for ordinary questions.
- `data` reports `first`/`last` of time columns in text order, not time order (`03/01/2026` before `2026-Q2`); thousands separators are stripped (`"1,200"` is 1200).
- `doctor` does not check `python-docx` and reports `plotly`/`altair`, which no target uses.
- `new-target` writes a stub without `tested:`, so `validate` fails on the new file itself as well as on every chart lacking a support line.
- Running the unit tests restamps the date in `kb/INDEX.md` and `kb/index.json`.
- pptx and xlsx outputs differ by a few bytes per run.
- Without a renderer, `render` prints the generated script's Python traceback (matplotlib, pptx, xlsx, docx) or `vl_convert missing: ...`, and exits 0 without `--strict`.
- No CI workflows in the repository.

## Inaccuracies and gaps in the shipped docs

1. README CLI block: `new-chart horizon --name "Horizon chart" ...` fails, because `kb/charts/horizon.md` already exists ("exists (use --force)"). Suggest another slug in the example.
2. README Install and the renderer line list `vl-convert-python matplotlib python-pptx openpyxl` but not `python-docx`, which the `docx` target needs.
3. README Install gives only the `m4bwav/chartwright` shorthand; suggest also the HTTPS URL, the `gh skill` route (with the kb/scripts copy) and the Copilot `.github/` layout.
4. README and skill description say "about 80 chart types"; there are 83.
5. `cw.py --help` lists `--json` on every command, but only `list` and `pick` honour it (`data` and `doctor` always print JSON).
6. The `pick` "no match" path described in SKILL.md Step 2.6 ("No match or unknown type: hand over to chartwright-curate") cannot be triggered by `pick` output; the skill must judge an empty `why` line itself.
7. `ai-docs/HANDOFF.md` still says 0.8.2.

## Gotchas

- Bash heredocs with apostrophes failed again (fix script written with the Write tool instead).
- `outputs` read an input block after "With mixed date formats that shows. Take this `mixed.csv`:" as output (the word "shows" within six words of the colon); ending the lead-in with a period fixed it (L-149).
- Nested Mermaid fences inside a console transcript need a four-backtick outer fence; `check` and `outputs` handled it.
- Do not rerun the verify script over the saved output after the pages are written without updating the pptx/xlsx sizes and test timing on the pages.

Related: see also the wiki itself, https://github.com/m4bwav/chartwright/wiki, and the everwrite run it followed, `https://github.com/m4bwav/everwrite/blob/master/ai-docs/notes/2026-10-03-wiki-run/2026-10-03-github-wiki.md`.
