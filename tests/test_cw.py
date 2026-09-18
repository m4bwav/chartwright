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


if __name__ == "__main__":
    unittest.main()
