"""Tests for scripts/cw.py. Standard library only: `python -m unittest discover -s tests -v`.

Rendering tests skip when the renderer (vl_convert, matplotlib, mmdc/npx) is absent, so the
suite passes on a bare machine and proves more where the tools exist.
"""
import io, json, os, shutil, subprocess, sys, tempfile, unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import cw  # noqa: E402

FIX = ROOT / "tests" / "fixtures"


def run(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cw.main(["--strict", *argv])
    return rc, buf.getvalue()


class FrontmatterTests(unittest.TestCase):
    def test_parse_scalars_lists_maps(self):
        fm, body = cw.parse_frontmatter('---\nname: X\nn: 3\nf: 1.5\nb: true\nl: [a, "b, c", 2]\nm:\n  k: native\n  j: none\nq: "quoted: colon"\n---\nbody\n')
        self.assertEqual(fm["name"], "X")
        self.assertEqual(fm["n"], 3)
        self.assertEqual(fm["f"], 1.5)
        self.assertIs(fm["b"], True)
        self.assertEqual(fm["l"], ["a", "b, c", 2])
        self.assertEqual(fm["m"], {"k": "native", "j": "none"})
        self.assertEqual(fm["q"], "quoted: colon")
        self.assertEqual(body.strip(), "body")

    def test_sections_and_subsections(self):
        secs = cw.split_sections("# T\n\n## When to use\n\n- a\n\n## Build\n\n### mermaid\n\nx\n\n### plotly\n\ny\n")
        self.assertEqual(secs["When to use"], "- a")
        sub = cw.subsections(secs["Build"])
        self.assertEqual(sub, {"mermaid": "x", "plotly": "y"})


class KnowledgeBaseTests(unittest.TestCase):
    def test_validate_passes(self):
        rc, out = run("validate")
        self.assertEqual(rc, 0, out)

    def test_every_chart_has_all_targets_and_build_recipes(self):
        charts, targets = cw.charts(), cw.targets()
        self.assertGreaterEqual(len(targets), 5)
        for slug, c in charts.items():
            sup = c["support"]
            self.assertEqual(set(sup), set(targets), f"{slug}: support map != targets")
            build = cw.subsections(cw.split_sections(c["_body"]).get("Build", ""))
            for t, lvl in sup.items():
                if lvl in ("native", "approx"):
                    self.assertIn(t, build, f"{slug}: no build recipe for {t}")

    def test_index_generates_compact_table(self):
        rc, out = run("index")
        self.assertEqual(rc, 0, out)
        idx = json.loads((cw.KB / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(len(idx["charts"]), len(cw.charts()))
        text = (cw.KB / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn("| line |", text)
        # the index must stay far cheaper than the folder it summarises
        full = sum(len(p.read_text(encoding="utf-8")) for p in cw.CHARTS.glob("*.md"))
        self.assertLess(len(text) * 4, full, "INDEX.md is not compact enough")

    def test_line_exemplar_shape(self):
        c = cw.charts()["line"]
        self.assertEqual(c["family"], "change-over-time")
        self.assertIn("time,q", c["shapes"])
        self.assertEqual(c["support"]["mermaid"], "native")


class PickTests(unittest.TestCase):
    def pick(self, q, **kw):
        argv = ["--json", "pick", "--question", q]
        for k, v in kw.items():
            argv += [f"--{k}", str(v)]
        buf = io.StringIO()
        with redirect_stdout(buf):
            cw.main(argv)
        return json.loads(buf.getvalue())

    def test_named_line_chart_wins(self):
        r = self.pick("make a line graph with time as x and price as y", shape="time,q")
        self.assertEqual(r["picks"][0]["slug"], "line")

    def test_shape_mismatch_penalised(self):
        r = self.pick("compare sales by region", shape="n,q")
        self.assertTrue(all(p["slug"] != "line" or p["score"] < 6 for p in r["picks"][:1]))

    def test_target_none_warns(self):
        charts = cw.charts()
        none_slugs = [s for s, c in charts.items() if c["support"].get("mermaid") == "none"]
        if not none_slugs:
            self.skipTest("no chart lacks mermaid support yet")
        slug = none_slugs[0]
        r = self.pick(charts[slug]["name"], target="mermaid")
        hit = next((p for p in r["picks"] if p["slug"] == slug), None)
        if hit:
            self.assertTrue(any("not drawable" in w for w in hit["warnings"]))

    def test_series_cap_warning(self):
        r = self.pick("line chart of price over time", shape="time,q*n", series=12)
        line = next(p for p in r["picks"] if p["slug"] == "line")
        self.assertTrue(any("series" in w for w in line["warnings"]))

    def test_funnel_question_and_no_plural_name_trap(self):
        r = self.pick("how should I show the drop-off between signup steps")
        self.assertEqual(r["picks"][0]["slug"], "funnel")
        self.assertNotIn("step", [p["slug"] for p in r["picks"]])

    def test_survey_picks_diverging_stacked_bar(self):
        r = self.pick("survey answers agree disagree by question")
        self.assertEqual(r["picks"][0]["slug"], "diverging-stacked-bar")


class DataTests(unittest.TestCase):
    def test_profile_kinds(self):
        rc, out = run("data", str(FIX / "prices.csv"))
        prof = json.loads(out)
        self.assertEqual(prof["shape_guess"], "time,q")
        self.assertEqual(prof["rows"], 6)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def build(self, *argv):
        rc, out = run("build", *argv)
        self.assertEqual(rc, 0, out)
        return out

    def test_mermaid_line(self):
        out = self.build("--chart", "line", "--target", "mermaid", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price")
        self.assertIn("xychart-beta", out)
        self.assertIn("line [100, 104, 101, 110, 115, 112]", out)

    def test_duplicate_x_values_are_summed(self):
        out = self.build("--chart", "bar", "--target", "mermaid", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales")
        self.assertIn("bar [200, 225, 130]", out)
        out = self.build("--chart", "bar", "--target", "mermaid", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--agg", "mean")
        self.assertIn("bar [100, 112.5, 65]", out)

    def test_composed_vega_lite_recipes(self):
        out = self.build("--chart", "waterfall", "--target", "vega-lite", "--data", str(FIX / "waterfall.csv"), "--x", "step", "--y", "change")
        spec = json.loads(out)
        self.assertEqual(spec["transform"][0]["window"][0]["op"], "sum")
        self.assertEqual(spec["encoding"]["y2"], {"field": "end"})
        out = self.build("--chart", "slope", "--target", "vega-lite", "--data", str(FIX / "slope.csv"), "--x", "period", "--y", "value", "--series", "city")
        spec = json.loads(out)
        self.assertEqual(len(spec["layer"]), 2)
        self.assertEqual(spec["layer"][1]["transform"][0]["filter"], {"field": "period", "equal": "2026"})
        out = self.build("--chart", "small-multiples", "--target", "vega-lite", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        self.assertEqual(json.loads(out)["facet"]["field"], "product")
        out = self.build("--chart", "stacked-bar-100", "--target", "vega-lite", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        self.assertEqual(json.loads(out)["encoding"]["y"]["stack"], "normalize")
        rc, out = run("build", "--chart", "dumbbell", "--target", "vega-lite", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales")
        self.assertEqual(rc, 1)
        self.assertIn("needs --series", out)

    def test_mermaid_named_series_flag(self):
        out = self.build("--chart", "line", "--target", "mermaid", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product", "--flag", "namedSeries")
        self.assertIn("xychart\n", out)
        self.assertIn('line "A" [120, 95, 60]', out)
        self.assertNotIn("%%", out)

    def test_terminal_sparkline_and_bars(self):
        out = self.build("--chart", "line", "--target", "terminal", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price")
        self.assertIn("100 -> 112", out)
        self.assertEqual(len([c for c in out.splitlines()[1].split()[0] if c in cw.BLOCKS]), 6)
        out = self.build("--chart", "bar", "--target", "terminal", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales")
        self.assertIn("South", out)
        self.assertIn("225", out)

    def test_echarts_option_shapes(self):
        out = self.build("--chart", "stacked-bar", "--target", "echarts", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        opt = json.loads(out)
        self.assertEqual(opt["xAxis"]["data"], ["North", "South", "East"])
        self.assertEqual([s["stack"] for s in opt["series"]], ["total", "total"])
        out = self.build("--chart", "sankey", "--target", "echarts", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        self.assertEqual(json.loads(out)["series"][0]["links"][0], {"source": "North", "target": "A", "value": 120.0})
        html = self.tmp / "e.html"
        self.build("--chart", "pie", "--target", "echarts", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--html", "--out", str(html))
        self.assertIn("echarts.init", html.read_text(encoding="utf-8"))

    def test_pptx_script_compiles_and_quickchart_url(self):
        out = self.build("--chart", "column", "--target", "pptx", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product", "--png", str(self.tmp / "c.pptx"))
        compile(out, "c.py", "exec")
        self.assertIn("XL_CHART_TYPE.COLUMN_CLUSTERED", out)
        out = self.build("--chart", "line", "--target", "quickchart", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price")
        self.assertTrue(out.startswith("![price by date](https://quickchart.io/chart?version=4"))
        self.assertIn("%22type%22%3A%22line%22", out)

    def test_xlsx_script_and_render(self):
        out = self.build("--chart", "stacked-bar", "--target", "xlsx", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product", "--png", str(self.tmp / "c.xlsx"))
        compile(out, "c.py", "exec")
        self.assertIn("chart.grouping = 'stacked'", out)
        try:
            import openpyxl  # noqa: F401
        except ImportError:
            self.skipTest("openpyxl not installed")
        script, book = self.tmp / "c.py", self.tmp / "c.xlsx"
        script.write_text(out, encoding="utf-8")
        rc, msg = run("render", "--target", "xlsx", "--in", str(script), "--out", str(book))
        self.assertEqual(rc, 0, msg)
        self.assertGreater(book.stat().st_size, 5000)

    def test_mermaid_pie_and_sankey(self):
        out = self.build("--chart", "pie", "--target", "mermaid", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales")
        self.assertIn('"North" : 120', out)
        out = self.build("--chart", "sankey", "--target", "mermaid", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        self.assertIn("sankey-beta", out)
        self.assertIn("North,A,120", out)

    def test_vega_lite_types_and_series(self):
        out = self.build("--chart", "grouped-bar", "--target", "vega-lite", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        spec = json.loads(out)
        self.assertEqual(spec["mark"], "bar")
        self.assertEqual(spec["encoding"]["x"]["type"], "nominal")
        self.assertEqual(spec["encoding"]["xOffset"]["field"], "product")
        self.assertEqual(spec["data"]["values"][0]["sales"], 120.0)
        out = self.build("--chart", "line", "--target", "vega-lite", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price")
        self.assertEqual(json.loads(out)["encoding"]["x"]["type"], "temporal")

    def test_vega_lite_data_by_url(self):
        out = self.build("--chart", "line", "--target", "vega-lite", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price", "--flag", "dataByUrl")
        self.assertEqual(json.loads(out)["data"], {"url": "prices.csv"})

    def test_plotly_and_chartjs_and_html(self):
        out = self.build("--chart", "stacked-bar", "--target", "plotly", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        fig = json.loads(out)
        self.assertEqual(fig["layout"]["barmode"], "stack")
        self.assertEqual(len(fig["data"]), 2)
        html = self.tmp / "c.html"
        self.build("--chart", "line", "--target", "chartjs", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price", "--html", "--out", str(html))
        text = html.read_text(encoding="utf-8")
        self.assertIn("new Chart(", text)
        self.assertIn('"type": "line"', text)

    def test_matplotlib_script_is_valid_python(self):
        out = self.build("--chart", "bar", "--target", "matplotlib", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--png", str(self.tmp / "x.png"))
        compile(out, "chart.py", "exec")
        self.assertIn("ax.bar(", out)

    def test_unknown_column_fails_strict(self):
        rc, out = run("build", "--chart", "line", "--target", "mermaid", "--data", str(FIX / "prices.csv"), "--x", "nope", "--y", "price")
        self.assertEqual(rc, 1)
        self.assertIn("not in", out)

    def test_unknown_recipe_fails_soft_without_strict(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cw.main(["build", "--chart", "chord", "--target", "mermaid", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales"])
        self.assertEqual(rc, 0)
        self.assertIn("no recipe", buf.getvalue())


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_vega_lite_png_and_svg(self):
        try:
            import vl_convert  # noqa: F401
        except ImportError:
            self.skipTest("vl_convert not installed")
        spec = self.tmp / "s.vl.json"
        run("build", "--chart", "line", "--target", "vega-lite", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price", "--out", str(spec))
        for ext in ("png", "svg"):
            out = self.tmp / f"c.{ext}"
            rc, msg = run("render", "--target", "vega-lite", "--in", str(spec), "--out", str(out))
            self.assertEqual(rc, 0, msg)
            self.assertGreater(out.stat().st_size, 1000)

    def test_matplotlib_png(self):
        try:
            import matplotlib  # noqa: F401
        except ImportError:
            self.skipTest("matplotlib not installed")
        script, png = self.tmp / "c.py", self.tmp / "c.png"
        run("build", "--chart", "line", "--target", "matplotlib", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price", "--out", str(script), "--png", str(png))
        rc, msg = run("render", "--target", "matplotlib", "--in", str(script), "--out", str(png))
        self.assertEqual(rc, 0, msg)
        self.assertGreater(png.stat().st_size, 1000)

    def test_pptx_render_writes_file(self):
        try:
            import pptx  # noqa: F401
        except ImportError:
            self.skipTest("python-pptx not installed")
        script, deck = self.tmp / "c.py", self.tmp / "c.pptx"
        run("build", "--chart", "bar", "--target", "pptx", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--out", str(script), "--png", str(deck))
        rc, msg = run("render", "--target", "pptx", "--in", str(script), "--out", str(deck))
        self.assertEqual(rc, 0, msg)
        self.assertGreater(deck.stat().st_size, 10000)


class AuthoringTests(unittest.TestCase):
    def test_new_chart_and_note_roundtrip(self):
        slug = "zz-test-chart"
        p = cw.CHARTS / f"{slug}.md"
        try:
            rc, out = run("new-chart", slug, "--name", "Test chart", "--family", "magnitude", "--shapes", "n,q")
            self.assertEqual(rc, 0, out)
            self.assertTrue(p.exists())
            rc, out = run("validate")
            self.assertEqual(rc, 1)  # the stub has TODOs; validate must catch them
            self.assertIn(f"{slug}.md: contains TODO", out)
            rc, out = run("note", slug, "pies are fine for two slices")
            self.assertEqual(rc, 0, out)
            self.assertIn("pies are fine for two slices", p.read_text(encoding="utf-8"))
        finally:
            if p.exists():
                p.unlink()

    def test_cli_launchers_exist(self):
        self.assertTrue((ROOT / "scripts" / "cw.ps1").exists())
        self.assertTrue((ROOT / "scripts" / "cw.sh").exists())
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "cw.py"), "targets"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("mermaid", r.stdout)



class NewTargetTests(unittest.TestCase):
    """plantuml, d2, observable-plot, gsheets, docx (0.5.0) and the fixes from the fresh-session runs."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def build(self, *argv):
        rc, out = run("build", *argv)
        self.assertEqual(rc, 0, out)
        return out

    def test_plantuml_chart_block(self):
        out = self.build("--chart", "bar", "--target", "plantuml", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        self.assertTrue(out.startswith("@startchart" + chr(10)))
        self.assertIn('v-axis "sales" 0 --> 150', out)
        self.assertIn('bar "A" [120, 95, 60]', out)
        self.assertIn("legend right", out)
        out = self.build("--chart", "stacked-bar", "--target", "plantuml", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        self.assertIn("stackMode stacked", out)
        rc, out = run("build", "--chart", "pie", "--target", "plantuml", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales")
        self.assertEqual(rc, 1)

    def test_d2_network_and_refusal(self):
        out = self.build("--chart", "network", "--target", "d2", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        self.assertIn("North -> A: 120", out)
        self.assertIn("direction: right", out)
        rc, out = run("build", "--chart", "bar", "--target", "d2", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales")
        self.assertEqual(rc, 1)
        self.assertIn("diagrams, not data charts", out)

    def test_observable_plot_snippet_and_page(self):
        out = self.build("--chart", "line", "--target", "observable-plot", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price")
        self.assertIn('new Date("2026-01-01")', out)
        self.assertIn('Plot.lineY(data, {x: "x", y: "y"})', out)
        out = self.build("--chart", "grouped-bar", "--target", "observable-plot", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        self.assertIn('fx: "x"', out)
        self.assertIn("color: {legend: true}", out)
        html = self.tmp / "p.html"
        self.build("--chart", "column", "--target", "observable-plot", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--html", "--out", str(html))
        text = html.read_text(encoding="utf-8")
        self.assertIn("@observablehq/plot@0.6", text)
        self.assertIn("append(chart)", text)

    def test_gsheets_values_and_add_chart(self):
        out = self.build("--chart", "stacked-bar", "--target", "gsheets", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product")
        d = json.loads(out)
        self.assertEqual(d["values"][0], ["region", "A", "B"])
        spec = d["requests"][0]["addChart"]["chart"]["spec"]["basicChart"]
        self.assertEqual((spec["chartType"], spec["stackedType"], len(spec["series"])), ("COLUMN", "STACKED", 2))
        self.assertEqual(spec["domains"][0]["domain"]["sourceRange"]["sources"][0]["endRowIndex"], 4)
        out = self.build("--chart", "donut", "--target", "gsheets", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales")
        self.assertEqual(json.loads(out)["requests"][0]["addChart"]["chart"]["spec"]["pieChart"]["pieHole"], 0.5)

    def test_docx_script_and_render(self):
        script, doc = self.tmp / "c.py", self.tmp / "report.docx"
        out = self.build("--chart", "bar", "--target", "docx", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--out", str(script), "--png", str(doc))
        text = script.read_text(encoding="utf-8")
        compile(text, "c.py", "exec")
        self.assertIn("doc.add_picture", text)
        try:
            import docx, vl_convert  # noqa: F401
        except ImportError:
            self.skipTest("python-docx or vl_convert not installed")
        rc, msg = run("render", "--target", "docx", "--in", str(script), "--out", str(doc))
        self.assertEqual(rc, 0, msg)
        import zipfile
        self.assertTrue(any(n.startswith("word/media/") for n in zipfile.ZipFile(doc).namelist()))

    def test_y2_compositions(self):
        out = self.build("--chart", "bullet", "--target", "vega-lite", "--data", str(FIX / "bullet.csv"), "--x", "kpi", "--y", "actual", "--y2", "target", "--series", "poor")
        d = json.loads(out)
        self.assertEqual(len(d["layer"]), 3)
        self.assertEqual(d["layer"][2]["encoding"]["x"]["field"], "target")
        out = self.build("--chart", "range-band", "--target", "vega-lite", "--data", str(FIX / "band.csv"), "--x", "date", "--y", "low", "--y2", "high", "--series", "mean")
        d = json.loads(out)
        self.assertEqual(d["layer"][0]["encoding"]["y2"]["field"], "high")
        self.assertEqual(d["encoding"]["x"]["axis"]["tickCount"], "month")
        out = self.build("--chart", "connected-scatter", "--target", "vega-lite", "--data", str(FIX / "connected.csv"), "--x", "unemployment", "--y", "inflation", "--series", "year")
        self.assertEqual(json.loads(out)["encoding"]["order"]["field"], "year")
        out = self.build("--chart", "bump", "--target", "vega-lite", "--data", str(FIX / "bump.csv"), "--x", "period", "--y", "rank", "--series", "team")
        self.assertEqual(json.loads(out)["encoding"]["y"]["scale"]["domain"], [0.5, 3.5])
        rc, out = run("build", "--chart", "bullet", "--target", "vega-lite", "--data", str(FIX / "bullet.csv"), "--x", "kpi", "--y", "actual")
        self.assertEqual(rc, 1)
        rc, out = run("build", "--chart", "bullet", "--target", "vega-lite", "--data", str(FIX / "bullet.csv"), "--x", "kpi", "--y", "actual", "--y2", "nope")
        self.assertEqual(rc, 1)
        out = self.build("--chart", "range-band", "--target", "observable-plot", "--data", str(FIX / "band.csv"), "--x", "date", "--y", "low", "--y2", "high")
        self.assertIn('y2: "y2"', out)
        self.assertIn('"y2": 110.0', out)

    def test_real_questions_regression(self):
        cases = [("how did monthly active users change over the last two years", "time,q", "line"),
                 ("distribution of response times across servers", "n,q*n", "boxplot"),
                 ("which steps of the checkout lose the most users", "o,q", "funnel"),
                 ("compare 2025 and 2026 revenue for each region", "n,n,q", "grouped-bar"),
                 ("correlation between ad spend and signups", "q,q", "scatter"),
                 ("survey answers from strongly disagree to strongly agree per question", "n,o,q", "diverging-stacked-bar"),
                 ("flow of visitors from source to landing page to conversion", "n,n,q", "sankey")]
        for q, shape, want in cases:
            buf = io.StringIO()
            with redirect_stdout(buf):
                cw.main(["--json", "pick", "--question", q, "--shape", shape])
            self.assertEqual(json.loads(buf.getvalue())["picks"][0]["slug"], want, q)

    def test_plotly_and_matplotlib_compositions(self):
        d = json.loads(self.build("--chart", "waterfall", "--target", "plotly", "--data", str(FIX / "waterfall.csv"), "--x", "step", "--y", "change"))
        self.assertEqual(d["data"][0]["type"], "waterfall")
        d = json.loads(self.build("--chart", "dumbbell", "--target", "plotly", "--data", str(FIX / "dumbbell.csv"), "--x", "city", "--y", "before", "--y2", "after"))
        self.assertEqual(len(d["data"]), 5)
        self.assertEqual(d["data"][-1]["name"], "after")
        d = json.loads(self.build("--chart", "bullet", "--target", "plotly", "--data", str(FIX / "bullet.csv"), "--x", "kpi", "--y", "actual", "--y2", "target"))
        self.assertEqual(d["layout"]["barmode"], "overlay")
        for chart, args in (("waterfall", ["--data", str(FIX / "waterfall.csv"), "--x", "step", "--y", "change"]),
                            ("dumbbell", ["--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales", "--series", "product"]),
                            ("bullet", ["--data", str(FIX / "bullet.csv"), "--x", "kpi", "--y", "actual", "--y2", "target", "--series", "poor"])):
            out = self.build("--chart", chart, "--target", "matplotlib", *args, "--png", str(self.tmp / (chart + ".png")))
            compile(out, chart + ".py", "exec")
            self.assertIn("fig.savefig", out)
        d = json.loads(self.build("--chart", "dumbbell", "--target", "vega-lite", "--data", str(FIX / "dumbbell.csv"), "--x", "city", "--y", "before", "--y2", "after"))
        self.assertEqual(d["transform"][0]["fold"], ["before", "after"])
        rc, out = run("build", "--chart", "dumbbell", "--target", "plotly", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales")
        self.assertEqual(rc, 1)

    def test_global_flags_after_subcommand(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cw.main(["pick", "--question", "bar chart of sales by region", "--shape", "n,q", "--json"])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(buf.getvalue())["picks"][0]["slug"], "bar")

    def test_magnitude_question_picks_bar_not_beeswarm(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cw.main(["--json", "pick", "--question", "how long does one clip take to render at each quality preset", "--shape", "n,q", "--categories", "3"])
        self.assertEqual(json.loads(buf.getvalue())["picks"][0]["slug"], "bar")

    def test_mermaid_bars_start_at_zero_and_vega_bar_sorted(self):
        out = self.build("--chart", "bar", "--target", "mermaid", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales")
        self.assertIn('y-axis "sales" 0 --> 250', out)
        out = self.build("--chart", "line", "--target", "mermaid", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price")
        self.assertNotIn("-->", out)
        out = self.build("--chart", "bar", "--target", "vega-lite", "--data", str(FIX / "sales.csv"), "--x", "region", "--y", "sales")
        self.assertEqual(json.loads(out)["encoding"]["x"]["sort"], "-y")
        out = self.build("--chart", "line", "--target", "vega-lite", "--data", str(FIX / "prices.csv"), "--x", "date", "--y", "price")
        self.assertEqual(json.loads(out)["encoding"]["x"]["axis"], {"tickCount": "month", "format": "%b %Y"})

if __name__ == "__main__":
    unittest.main()
