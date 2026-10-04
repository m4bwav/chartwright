"""Runs every example on the chartwright wiki against a fresh clone of github.com/m4bwav/chartwright.

Usage: python 2026-10-03-wiki-verify.py CLONE_DIR [PYTHON]
CLONE_DIR is a fresh `git clone https://github.com/m4bwav/chartwright.git`, never the working copy.
PYTHON (optional) is the interpreter that stands in for `python` in every command (for the 3.9 run,
which has none of the optional renderers installed).
Each case copies the clone's scripts/, kb/, skills/, tests/ and .claude-plugin/ into a new scratch folder,
writes the case's files there, then runs each command line through bash with stdin closed, printing
`$ command`, its output with stderr merged, and the exit code when the case asks for `echo $?`.
The scratch folder's path is printed as <work>.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CLONE = Path(sys.argv[1]).resolve()
PY = sys.argv[2] if len(sys.argv) > 2 else None
BASH = shutil.which("bash") or r"C:\Program Files\Git\bin\bash.exe"
COPY = ("scripts", "kb", "skills", "tests", ".claude-plugin")

PRICES = """date,price
2026-01-01,100
2026-02-01,104
2026-03-01,101
2026-04-01,110
2026-05-01,115
2026-06-01,112
"""

SALES = """region,product,sales
North,A,120
North,B,80
South,A,95
South,B,130
East,A,60
East,B,70
"""

REGIONS = """region,sales
North,200
South,225
East,130
"""

CITIES = """city,before,after
Austin,10,14
Dallas,12,11
Houston,9,15
"""

FUNNEL = """stage,users
Visited,12000
Signed up,3100
Activated,1450
Paid,380
"""

REPORT = """# Quarterly report

Sales rose in the South.
"""

LOOP = """\
for t in mermaid terminal quickchart; do
  python scripts/cw.py build --chart bar --target $t --data regions.csv --x region --y sales --out "bar.$t.txt"
done
"""

CASES = [
    # Home and Getting started
    ("home-terminal", {"prices.csv": PRICES}, """
python scripts/cw.py build --chart line --target terminal --data prices.csv --x date --y price
"""),
    ("home-mermaid", {"regions.csv": REGIONS}, """
python scripts/cw.py build --chart bar --target mermaid --data regions.csv --x region --y sales
"""),
    ("gs-doctor", {}, """
python scripts/cw.py doctor
"""),
    ("gs-copy-route", {}, """
git -c advice.detachedHead=false clone -q --depth 1 --branch v0.8.4 https://github.com/m4bwav/chartwright.git chartwright-src
mkdir -p project/.github
cp -r chartwright-src/skills chartwright-src/kb chartwright-src/scripts project/.github/
ls project/.github
ls project/.github/skills
python project/.github/scripts/cw.py --strict validate
"""),
    ("gs-gh-skill", {}, """
mkdir -p project/.github
gh skill install m4bwav/chartwright --all --dir project/.github/skills
ls project/.github/skills/chartwright
ls project/.github
"""),
    # Commands
    ("cmd-no-args", {}, """
python scripts/cw.py
echo $?
"""),
    ("cmd-data", {"prices.csv": PRICES, "sales.csv": SALES}, """
python scripts/cw.py data prices.csv
python scripts/cw.py data sales.csv
"""),
    ("cmd-pick", {}, """
python scripts/cw.py pick --question "line graph, time on x, price on y" --shape time,q
"""),
    ("cmd-pick-json", {}, """
python scripts/cw.py pick --question "how to show signup drop-off" --top 1 --json
"""),
    ("cmd-pick-warn", {}, """
python scripts/cw.py pick --question "trend over time" --shape time,q*n --series 8 --target mermaid
"""),
    ("cmd-pick-none", {}, """
python scripts/cw.py pick --question "zzz"
"""),
    ("cmd-show", {}, """
python scripts/cw.py show line --section when not substitutes
"""),
    ("cmd-show-build", {}, """
python scripts/cw.py show pie --section build --target mermaid
"""),
    ("cmd-show-missing", {}, """
python scripts/cw.py show piechart
echo $?
python scripts/cw.py --strict show piechart
echo $?
"""),
    ("cmd-list", {}, """
python scripts/cw.py list --family ranking
python scripts/cw.py list --target terminal
python scripts/cw.py list | wc -l
"""),
    ("cmd-targets", {}, """
python scripts/cw.py targets
"""),
    ("cmd-build-vl", {"sales.csv": SALES}, """
python scripts/cw.py build --chart grouped-bar --target vega-lite --data sales.csv --x region --y sales --series product --out chart.vl.json
python scripts/cw.py render --target vega-lite --in chart.vl.json --out chart.svg
python scripts/cw.py render --target vega-lite --in chart.vl.json --out chart.png
python scripts/cw.py render --target vega-lite --in chart.vl.json --out chart.gif
"""),
    ("cmd-build-html", {"sales.csv": SALES}, """
python scripts/cw.py build --chart grouped-bar --target vega-lite --data sales.csv --x region --y sales --series product --html --out chart.html
head -c 300 chart.html
"""),
    ("cmd-build-agg", {"sales.csv": SALES}, """
python scripts/cw.py build --chart bar --target terminal --data sales.csv --x region --y sales
python scripts/cw.py build --chart bar --target terminal --data sales.csv --x region --y sales 2>/dev/null
python scripts/cw.py build --chart bar --target terminal --data sales.csv --x region --y sales --agg mean
"""),
    ("cmd-mermaid-series", {"sales.csv": SALES}, """
python scripts/cw.py build --chart grouped-bar --target mermaid --data sales.csv --x region --y sales --series product
python scripts/cw.py build --chart grouped-bar --target mermaid --data sales.csv --x region --y sales --series product --flag namedSeries
"""),
    ("cmd-build-quickchart", {"regions.csv": REGIONS}, """
python scripts/cw.py build --chart bar --target quickchart --data regions.csv --x region --y sales
"""),
    ("cmd-build-errors", {"prices.csv": PRICES}, """
python scripts/cw.py build --chart line --target mermaid --data nothere.csv --x date --y price
echo $?
python scripts/cw.py build --chart line --target mermaid --data prices.csv --x day --y price
echo $?
python scripts/cw.py --strict build --chart line --target mermaid --data prices.csv --x day --y price
echo $?
python scripts/cw.py build --chart line --target svg --data prices.csv --x date --y price
python scripts/cw.py build --chart line --target gdocs --data prices.csv --x date --y price
python scripts/cw.py build --chart heatmap --target mermaid --data prices.csv --x date --y price
python scripts/cw.py build --chart linechart --target mermaid --data prices.csv --x date --y price
python scripts/cw.py build --chart line --target mermaid --data prices.csv --x date --y price --html
"""),
    ("cmd-strict-front-or-back", {"prices.csv": PRICES}, """
python scripts/cw.py build --chart line --target mermaid --data prices.csv --x day --y price --strict
echo $?
"""),
    ("cmd-render-errors", {}, """
python scripts/cw.py render --target vega-lite --in missing.vl.json --out chart.png
echo $?
python scripts/cw.py render --target gdocs --in x --out y
"""),
    ("cmd-matplotlib", {"regions.csv": REGIONS}, """
python scripts/cw.py build --chart bar --target matplotlib --data regions.csv --x region --y sales --out chart.py --png chart.png
python scripts/cw.py render --target matplotlib --in chart.py --out chart.png
"""),
    ("cmd-authoring", {}, """
python scripts/cw.py note pie "fine for two slices when the question is majority"
tail -2 kb/charts/pie.md
python scripts/cw.py tested d2 --platform Linux "d2 0.7 rendered an SVG of a five-node network"
python scripts/cw.py new-chart horizon --name "Horizon chart" --family change-over-time --shapes time,q*n
python scripts/cw.py new-chart spiral --name "Spiral plot" --family change-over-time --shapes time,q
python scripts/cw.py --strict validate
echo $?
python scripts/cw.py index
"""),
    ("cmd-new-target", {}, """
python scripts/cw.py new-target svgsketch --name "Hand-drawn SVG" --kind image
python scripts/cw.py validate | head -3
python scripts/cw.py validate | tail -1
"""),
    # How charts are picked and built
    ("pick-named", {}, """
python scripts/cw.py pick --question "a sankey of where visitors go"
"""),
    ("pick-shape-only", {}, """
python scripts/cw.py pick --shape n,q
"""),
    ("data-kinds", {"mixed.csv": "month,units,note\n2026-Q1,\"1,200\",ok\n2026-Q2,980,\n03/01/2026,1100,late\n"}, """
python scripts/cw.py data mixed.csv
"""),
    # Recipes
    ("recipe-markdown", {"regions.csv": REGIONS, "report.md": REPORT}, """
python scripts/cw.py build --chart bar --target mermaid --data regions.csv --x region --y sales --title "South leads on sales" >> report.md
cat report.md
"""),
    ("recipe-pptx", {"sales.csv": SALES}, """
python scripts/cw.py build --chart column --target pptx --data sales.csv --x region --y sales --series product --out chart.py --png deck.pptx
python scripts/cw.py render --target pptx --in chart.py --out deck.pptx
"""),
    ("recipe-docx", {"regions.csv": REGIONS}, """
python scripts/cw.py build --chart bar --target docx --data regions.csv --x region --y sales --title "South leads on sales" --out chart.py --png report.docx
python scripts/cw.py render --target docx --in chart.py --out report.docx
"""),
    ("recipe-xlsx", {"sales.csv": SALES}, """
python scripts/cw.py build --chart grouped-bar --target xlsx --data sales.csv --x region --y sales --series product --out chart.py --png book.xlsx
python scripts/cw.py render --target xlsx --in chart.py --out book.xlsx
"""),
    ("recipe-echarts-page", {"funnel.csv": FUNNEL}, """
python scripts/cw.py build --chart funnel --target echarts --data funnel.csv --x stage --y users --html --out funnel.html
"""),
    ("recipe-dumbbell", {"cities.csv": CITIES}, """
python scripts/cw.py build --chart dumbbell --target vega-lite --data cities.csv --x city --y before --y2 after --out dumbbell.vl.json
python scripts/cw.py render --target vega-lite --in dumbbell.vl.json --out dumbbell.png
"""),
    ("recipe-pick-json", {}, """
python scripts/cw.py pick --question "share of budget by department" --shape n,q --json | python -c "import json,sys; print(json.load(sys.stdin)['picks'][0]['slug'])"
"""),
    ("recipe-loop", {"regions.csv": REGIONS, "loop.sh": LOOP}, """
sh loop.sh
cat bar.terminal.txt
"""),
    # Development
    ("dev-tests", {}, """
python -m unittest discover -s tests 2>&1 | tail -3
"""),
    ("dev-validate", {}, """
python scripts/cw.py --strict validate
echo $?
"""),
]


def run_case(label, files, commands):
    print("== %s ==" % label)
    work = Path(tempfile.mkdtemp(prefix="cw-"))
    try:
        for top in COPY:
            shutil.copytree(CLONE / top, work / top)
        for name, text in files.items():
            path = work / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode("utf-8"))
        env = dict(os.environ)
        env.pop("PYTHONUTF8", None)
        if PY:
            env["PATH"] = str(Path(PY).parent) + os.pathsep + env["PATH"]
        masks = [str(work), str(work).replace("\\", "/"), str(work).replace("\\", "\\\\")]
        rc = 0
        for line in [c for c in commands.strip().splitlines() if c.strip()]:
            print("$ " + line)
            if line == "echo $?":
                print(rc)
                continue
            p = subprocess.run([BASH, "-c", "{ " + line + "; } 2>&1"], cwd=work, env=env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE)
            text = p.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
            for m in masks:
                text = text.replace(m, "<work>")
            sys.stdout.write(text)
            if text and not text.endswith("\n"):
                sys.stdout.write("\n")
            rc = p.returncode
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    v = subprocess.run([PY or "python", "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("== installed ==")
    print("clone: %s" % subprocess.run(["git", "-C", str(CLONE), "log", "--format=%h %ad", "--date=short", "-1"],
                                         stdout=subprocess.PIPE).stdout.decode().strip())
    print(v.stdout.decode().strip())
    only = os.environ.get("CW_ONLY")
    for case in CASES:
        if only and case[0] not in only.split(","):
            continue
        run_case(*case)


main()
