#!/usr/bin/env python3
"""cw.py - chartwright command line. Pure standard library, Windows/macOS/Linux.

The agent reads kb/INDEX.md (compact) instead of the whole knowledge base, asks
`pick` for a ranked, reasoned recommendation, asks `show` for only the sections it
needs, and asks `build` to turn a CSV plus column names into a chart spec so the
data never has to pass through the model. Every command prints JSON with --json
and fails soft (exit 0 with a note) unless --strict.

Commands
  index                         compile kb/charts/*.md + kb/targets/*.md -> kb/index.json, kb/INDEX.md
  validate                      lint the knowledge base against kb/SCHEMA.md
  list [--family F] [--target T]
  show <slug> [--section S ...] [--target T]     S in: when, not, substitutes, evidence, accessibility, build, notes, all
  pick --question "..." [--shape "time,q"] [--series N] [--categories N] [--target T] [--top 3]
  data FILE.csv                 profile a CSV (column kinds, ranges, shape guess) without reading it into the model
  build --chart SLUG --target T --data FILE.csv --x COL --y COL [--series COL] [--title T] [--out FILE] [--html]
  render --target T --in SPEC --out FILE          vega-lite -> svg/png/pdf/html (vl_convert); mermaid -> svg/png (mmdc); matplotlib -> runs the script
  new-chart SLUG --name N --family F [--shapes ...]
  new-target SLUG --name N --kind K
  note SLUG "text"              append a dated note to the chart (or target) file
  doctor                        which renderers are available on this machine
  targets                       list render targets
"""
from __future__ import annotations
import argparse, csv, datetime as dt, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "kb"
CHARTS = KB / "charts"
TARGETS = KB / "targets"
TODAY = dt.date.today().isoformat()
FAMILIES = ["deviation", "correlation", "ranking", "distribution", "change-over-time", "magnitude",
            "part-to-whole", "spatial", "flow", "hierarchy", "relationship", "single-value", "table"]
SUPPORT_LEVELS = ["native", "approx", "image", "none"]
SECTIONS = ["When to use", "When not to use", "Substitutes", "Evidence", "Accessibility", "Build", "Notes"]
SECTION_KEYS = {"when": "When to use", "not": "When not to use", "substitutes": "Substitutes", "evidence": "Evidence",
                "accessibility": "Accessibility", "build": "Build", "notes": "Notes"}
STRICT = False
_problems: list[str] = []
_FLAGS: set[str] = set()


def a_flag(name: str) -> bool:
    return name in _FLAGS


# ---------------------------------------------------------------- tiny YAML
def _split_list(s: str) -> list[str]:
    out, cur, q = [], "", None
    for ch in s:
        if q:
            cur += ch
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            cur += ch
        elif ch == ",":
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return out


def _scalar(v: str):
    v = v.strip()
    if v in ("", "~", "null"):
        return None
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [] if not inner else [_scalar(x) for x in _split_list(inner)]
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v in ("true", "false"):
        return v == "true"
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    block, body = text[3:end].strip("\n"), text[end + 4:]
    data: dict = {}
    cur_key, cur_map = None, None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if indent == 0:
            cur_map = None
            if line.startswith("- "):
                continue
            key, _, val = line.partition(":")
            key = key.strip()
            if val.strip() == "":
                data[key] = {}
                cur_key, cur_map = key, data[key]
            else:
                data[key] = _scalar(val)
                cur_key = key
        else:
            if line.startswith("- "):
                if not isinstance(data.get(cur_key), list):
                    data[cur_key] = []
                data[cur_key].append(_scalar(line[2:]))
            elif cur_map is not None:
                k, _, v = line.partition(":")
                cur_map[k.strip()] = _scalar(v)
    return data, body


def split_sections(body: str) -> dict[str, str]:
    """Top-level '## ' headings -> text. '### ' subsections stay inside their parent."""
    out: dict[str, str] = {}
    cur, buf = None, []
    for line in body.splitlines():
        if line.startswith("## "):
            if cur is not None:
                out[cur] = "\n".join(buf).strip("\n")
            cur, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip("\n")
    return out


def subsections(text: str) -> dict[str, str]:
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("### "):
            if cur is not None:
                out[cur] = "\n".join(buf).strip("\n")
            cur, buf = line[4:].strip(), []
        else:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip("\n")
    return out


# ---------------------------------------------------------------- loading
def load_dir(folder: Path) -> dict[str, dict]:
    items = {}
    for p in sorted(folder.glob("*.md")):
        if p.name.upper() in ("INDEX.MD", "README.MD"):
            continue
        fm, body = parse_frontmatter(p.read_text(encoding="utf-8"))
        fm["_path"] = str(p)
        fm["_body"] = body
        fm.setdefault("slug", p.stem)
        items[fm["slug"]] = fm
    return items


def charts() -> dict[str, dict]:
    return load_dir(CHARTS)


def targets() -> dict[str, dict]:
    return load_dir(TARGETS)


def problem(msg: str):
    _problems.append(msg)


# ---------------------------------------------------------------- index
def cmd_index(a):
    ch, tg = charts(), targets()
    keys = ("slug", "name", "family", "also", "question", "shapes", "goals", "max_series", "max_categories",
            "evidence", "popularity", "status", "support", "aliases", "last_verified")
    rows = [{k: c.get(k) for k in keys} for c in ch.values()]
    trows = [{k: t.get(k) for k in ("slug", "name", "kind", "renders_in", "version_checked", "renderer", "last_verified", "tested")}
             for t in tg.values()]
    idx = {"generated": TODAY, "charts": rows, "targets": trows, "families": FAMILIES}
    (KB / "index.json").write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tslugs = list(tg.keys())
    lines = ["# Chart index (generated by `cw.py index`; do not edit)", "",
             f"{len(rows)} chart types, {len(trows)} targets, generated {TODAY}. Read this first; open a chart file only for the section you need (`cw.py show <slug> --section when`). "
             "Every slug links its file, so the knowledge base also reads as a graph (Obsidian, GitHub); the schema is [SCHEMA.md](SCHEMA.md), the rules are listed at the end, the plugin is [../README.md](../README.md).",
             "", "Support: N native, A approximate, I image only, . none. Target columns in order: " + ", ".join(tslugs), "",
             "| slug | family | question | shapes | series/cat cap | evid | pop | " + " ".join(tslugs) + " |",
             "|---|---|---|---|---|---|---|---|"]
    abbr = {"native": "N", "approx": "A", "image": "I", "none": ".", None: "?"}
    for r in rows:
        sup = r.get("support") or {}
        cells = "".join(abbr.get(sup.get(t), "?") for t in tslugs)
        caps = f"{r.get('max_series') or '-'}/{r.get('max_categories') or '-'}"
        lines.append(f"| [{r['slug']}](charts/{r['slug']}.md) | {r['family']} | {r.get('question') or ''} | {' '.join(str(s) for s in (r.get('shapes') or []))} | {caps} | "
                     f"{str(r.get('evidence') or '?')[:1]} | {r.get('popularity') or '?'} | {cells} |")
    lines += ["", "## Families", "", ", ".join(FAMILIES), "", "## Targets", ""]
    for t in trows:
        tested = t.get("tested")
        tested_s = "untested anywhere" if tested in (None, "untested", []) else "tested: " + "; ".join(str(v).split(":")[0] for v in (tested if isinstance(tested, list) else [tested]))
        lines.append(f"- **[{t['slug']}](targets/{t['slug']}.md)** ({t.get('kind')}): {t.get('name')}; renders in {', '.join(t.get('renders_in') or [])}; renderer `{t.get('renderer')}`; {tested_s}")
    rules = sorted(p for p in (KB / "rules").glob("*.md"))
    if rules:
        lines += ["", "## Rules", ""]
        for p in rules:
            first = next((ln.lstrip("# ").strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.startswith("# ")), p.stem)
            lines.append(f"- [{first}](rules/{p.name})")
    (KB / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"indexed {len(rows)} charts, {len(trows)} targets -> kb/index.json, kb/INDEX.md")


# ---------------------------------------------------------------- validate
SHAPE_RE = r"(time|q|n|o|geo|hier|flow|text)\+?(,(time|q|n|o|geo|hier|flow|text)\+?)*(\*n)?"


def cmd_validate(a):
    _problems.clear()
    ch, tg = charts(), targets()
    tslugs = set(tg.keys())
    req = ["name", "slug", "family", "question", "shapes", "goals", "evidence", "popularity", "status", "support", "last_verified"]
    for slug, c in ch.items():
        p = Path(c["_path"]).name
        for k in req:
            if c.get(k) in (None, "", [], {}):
                problem(f"{p}: missing frontmatter '{k}'")
        if c.get("family") not in FAMILIES:
            problem(f"{p}: family '{c.get('family')}' not in {FAMILIES}")
        for f in c.get("also") or []:
            if f not in FAMILIES:
                problem(f"{p}: also-family '{f}' unknown")
        if c.get("slug") != Path(c["_path"]).stem:
            problem(f"{p}: slug '{c.get('slug')}' != file name")
        for s in c.get("shapes") or []:
            if not re.fullmatch(SHAPE_RE, str(s)):
                problem(f"{p}: bad shape '{s}'")
        sup = c.get("support") or {}
        for t, lvl in sup.items():
            if t not in tslugs:
                problem(f"{p}: support target '{t}' has no kb/targets/{t}.md")
            if lvl not in SUPPORT_LEVELS:
                problem(f"{p}: support level '{lvl}' for {t} not in {SUPPORT_LEVELS}")
        for t in sorted(tslugs - set(sup)):
            problem(f"{p}: no support entry for target '{t}'")
        secs = split_sections(c["_body"])
        for s in SECTIONS:
            if s not in secs:
                problem(f"{p}: missing section '## {s}'")
        build = subsections(secs.get("Build", ""))
        for t, lvl in sup.items():
            if lvl in ("native", "approx") and t not in build:
                problem(f"{p}: support says {t}={lvl} but no '### {t}' under Build")
        if "TODO" in c["_body"] or "TODO" in json.dumps({k: v for k, v in c.items() if not k.startswith("_")}):
            problem(f"{p}: contains TODO")
        if c.get("evidence") not in ("high", "medium", "low"):
            problem(f"{p}: evidence must be high|medium|low")
        if c.get("popularity") not in ("core", "common", "niche", "rising", "declining"):
            problem(f"{p}: popularity must be core|common|niche|rising|declining")
    for slug, t in tg.items():
        p = Path(t["_path"]).name
        for k in ("name", "slug", "kind", "renderer", "last_verified", "tested"):
            if t.get(k) in (None, ""):
                problem(f"{p}: missing frontmatter '{k}'")
        secs = split_sections(t["_body"])
        for s in ("What it can draw", "Syntax essentials", "Limits", "Render", "Notes"):
            if s not in secs:
                problem(f"{p}: missing section '## {s}'")
    if _problems:
        print(f"{len(_problems)} problem(s):")
        for m in _problems:
            print("  -", m)
    else:
        print(f"ok: {len(ch)} charts, {len(tg)} targets valid")
    return 1 if _problems else 0


# ---------------------------------------------------------------- list / show
def cmd_list(a):
    ch = charts()
    rows = []
    for slug, c in ch.items():
        if a.family and c.get("family") != a.family and a.family not in (c.get("also") or []):
            continue
        if a.target and (c.get("support") or {}).get(a.target) in (None, "none"):
            continue
        rows.append((slug, c.get("family"), c.get("question")))
    if a.json:
        print(json.dumps([{"slug": s, "family": f, "question": q} for s, f, q in rows], indent=1))
    else:
        for s, f, q in rows:
            print(f"{s:22} {str(f):18} {q}")


def cmd_show(a):
    ch, tg = charts(), targets()
    item = ch.get(a.slug) or tg.get(a.slug)
    if not item:
        print(f"no chart or target '{a.slug}'")
        return 1
    secs = split_sections(item["_body"])
    want = a.section or ["when", "not", "substitutes"]
    if "all" in want:
        want = list(SECTION_KEYS)
    fm = {k: v for k, v in item.items() if not k.startswith("_")}
    out = [f"# {item.get('name')} ({a.slug})",
           f"family: {fm.get('family')}  shapes: {fm.get('shapes')}  caps: series {fm.get('max_series')} / categories {fm.get('max_categories')}  evidence: {fm.get('evidence')}  popularity: {fm.get('popularity')}", ""]
    for w in want:
        title = SECTION_KEYS.get(w, w)
        text = secs.get(title)
        if text is None:
            continue
        if title == "Build" and a.target:
            sub = subsections(text)
            text = sub.get(a.target, f"(no {a.target} recipe)")
            title = f"Build: {a.target}"
        out += [f"## {title}", text, ""]
    print("\n".join(out))


# ---------------------------------------------------------------- pick
STOP = set("a an the of for to in on by with and or as at is are be show me make plot chart graph draw please want need i we it this that".split())
SYN = {  # request words -> goal vocabulary used in chart frontmatter `goals`
    "trend": ["trend", "over time"], "trends": ["trend", "over time"], "timeline": ["over time", "sequence", "events"], "history": ["over time"],
    "long": ["magnitude", "duration"], "much": ["magnitude"], "big": ["magnitude"], "duration": ["magnitude", "duration"], "minutes": ["magnitude"], "hours": ["magnitude"],
    "compare": ["comparison", "magnitude"], "comparison": ["comparison"], "rank": ["ranking"], "ranking": ["ranking"], "top": ["ranking"], "largest": ["ranking"],
    "share": ["part-to-whole", "proportion"], "shares": ["part-to-whole"], "proportion": ["part-to-whole"], "percent": ["part-to-whole"], "percentage": ["part-to-whole"],
    "breakdown": ["part-to-whole", "composition"], "composition": ["part-to-whole", "composition"], "makeup": ["part-to-whole"],
    "distribution": ["distribution"], "spread": ["distribution"], "histogram": ["distribution"], "outliers": ["distribution"], "quartiles": ["distribution"],
    "correlation": ["correlation"], "relationship": ["correlation"], "relate": ["correlation"], "versus": ["correlation", "comparison"], "vs": ["correlation", "comparison"],
    "flow": ["flow"], "flows": ["flow"], "funnel": ["flow", "stages"], "conversion": ["flow", "stages"], "drop-off": ["stages", "flow"], "dropoff": ["stages", "flow"], "signup": ["stages"], "checkout": ["stages"], "budget": ["part-to-whole", "magnitude"], "migration": ["flow"],
    "map": ["spatial"], "region": ["spatial"], "regions": ["spatial"], "country": ["spatial"], "countries": ["spatial"], "geographic": ["spatial"], "states": ["spatial"], "county": ["spatial"],
    "hierarchy": ["hierarchy"], "nested": ["hierarchy"], "tree": ["hierarchy"], "folders": ["hierarchy"],
    "network": ["relationship"], "connections": ["relationship"], "dependencies": ["relationship"], "graph": ["relationship"],
    "kpi": ["single-value"], "metric": ["single-value"], "target": ["deviation", "single-value"], "deviation": ["deviation"], "difference": ["deviation"], "delta": ["deviation"], "variance": ["deviation"], "profit": ["deviation"], "loss": ["deviation"],
    "schedule": ["schedule"], "gantt": ["schedule"], "tasks": ["schedule"], "milestones": ["schedule"], "project": ["schedule"],
    "price": ["price", "over time"], "prices": ["price", "over time"], "stock": ["price", "ohlc"], "candlestick": ["ohlc"], "revenue": ["magnitude"], "sales": ["magnitude"],
    "survey": ["likert", "ordinal"], "likert": ["likert"], "agree": ["likert"], "sentiment": ["likert"],
    "before": ["before-after", "change"], "after": ["before-after"], "cumulative": ["cumulative"], "running": ["cumulative"],
    "seasonal": ["seasonal", "over time"], "calendar": ["calendar", "over time"], "daily": ["over time", "calendar"], "monthly": ["over time"], "weekly": ["over time"], "yearly": ["over time"], "year": ["over time"], "years": ["over time"], "time": ["over time"], "date": ["over time"],
    "density": ["distribution"], "many": ["large-n"], "thousands": ["large-n"], "millions": ["large-n"],
    "progress": ["single-value", "progress"], "goal": ["single-value", "deviation"], "gauge": ["single-value"],
    "steps": ["stages", "flow"], "stages": ["stages", "flow"], "pipeline": ["stages", "flow"],
    "rating": ["ordinal"], "score": ["magnitude"], "scores": ["magnitude", "distribution"],
    "matrix": ["matrix"], "grid": ["matrix"], "table": ["table"],
}


GENERIC = {"each", "every", "one", "does", "take", "takes", "long", "much", "many", "what", "which", "show", "chart", "graph", "plot", "per", "value", "values"}


def _tokens(s: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9\-]+", s.lower()) if w not in STOP]


def cmd_pick(a):
    ch = charts()
    q = a.question or ""
    words = _tokens(q)
    goals: list[str] = []
    for w in words:
        goals += SYN.get(w, [])
    goals = list(dict.fromkeys(goals + words))
    shape = a.shape
    results = []
    for slug, c in ch.items():
        if c.get("status") == "deprecated":
            continue
        score, why, warn = 0.0, [], []
        cg = [str(g).lower() for g in (c.get("goals") or [])]
        names = [str(c.get("name", "")).lower()] + [str(x).lower() for x in (c.get("aliases") or [])] + [slug.replace("-", " ")]
        # exact word match; plurals only for multi-word or long names ("steps" must not name the step chart)
        if any(n and re.search(r"\b" + re.escape(n) + (r"s?\b" if " " in n or len(n) > 6 else r"\b"), q.lower()) for n in names):
            score += 6
            why.append("named in request")
        hits = [g for g in goals if any(g == x or (len(g) > 3 and g not in GENERIC and g in x) for x in cg)]
        if hits:
            score += 1.5 * len(set(hits))
            why.append("goals: " + ", ".join(sorted(set(hits))))
        fam = c.get("family")
        if fam in goals:
            score += 3
            why.append(f"family {fam}")
        elif any(f in goals for f in (c.get("also") or [])):
            score += 1.5
            why.append("secondary family")
        if shape:
            shapes = [str(s) for s in (c.get("shapes") or [])]
            if shape in shapes:
                score += 3
                why.append(f"shape {shape}")
            elif any(s.replace("*n", "") == shape.replace("*n", "") for s in shapes):
                score += 1.5
                why.append("shape family")
            else:
                score -= 3
        ms, mc = c.get("max_series") or 0, c.get("max_categories") or 0
        if a.series and ms and a.series > ms:
            score -= 2
            warn.append(f"{a.series} series > cap {ms}: facet (small multiples) or fold to Other")
        if a.categories and mc and a.categories > mc:
            score -= 2
            warn.append(f"{a.categories} categories > cap {mc}")
        if a.target:
            lvl = (c.get("support") or {}).get(a.target, "none")
            if lvl == "none":
                score -= 4
                warn.append(f"not drawable in {a.target}")
            elif lvl == "image":
                score -= 1
                warn.append(f"{a.target}: image only")
            elif lvl == "approx":
                score -= 0.5
                warn.append(f"{a.target}: approximate")
        score += {"high": 0.5, "medium": 0.25}.get(c.get("evidence"), 0)
        score += {"core": 0.5, "common": 0.25, "rising": 0.25, "declining": -0.5}.get(c.get("popularity"), 0)
        if score > 0:
            results.append({"slug": slug, "name": c.get("name"), "score": round(score, 2), "why": why, "warnings": warn,
                            "family": fam, "question": c.get("question")})
    results.sort(key=lambda r: (-r["score"], r["slug"]))
    top = results[: a.top]
    out = {"question": q, "goals": goals, "shape": shape, "picks": top,
           "next": "cw.py show <slug> --section when not substitutes; then cw.py build ...; palette and marks: the dataviz skill when present"}
    if not top:
        out["note"] = "no match; give --shape or a goal word, or research the request with chartwright-curate"
    if a.json:
        print(json.dumps(out, indent=1))
    else:
        for i, r in enumerate(top, 1):
            print(f"{i}. {r['slug']} ({r['score']}): {r['name']} - {r['question']}")
            if r["why"]:
                print("   why:", "; ".join(r["why"]))
            for w in r["warnings"]:
                print("   warn:", w)
        if not top:
            print(out["note"])


# ---------------------------------------------------------------- data
def read_csv(path: str) -> tuple[list[str], list[dict]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        rows = list(r)
        return list(r.fieldnames or []), rows


def _num(v):
    try:
        return float(str(v).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _is_time(v) -> bool:
    return bool(re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?([T ]\d{2}:\d{2}(:\d{2})?)?|\d{4}-Q[1-4]|\d{1,2}/\d{1,2}/\d{2,4}", str(v).strip()))


def cmd_data(a):
    cols, rows = read_csv(a.data)
    prof = {"file": a.data, "rows": len(rows), "columns": []}
    for c in cols:
        vals = [r[c] for r in rows if r.get(c) not in (None, "")]
        nums = [_num(v) for v in vals]
        if vals and all(_is_time(v) for v in vals):
            kind, extra = "time", {"first": min(vals), "last": max(vals)}
        elif vals and all(n is not None for n in nums):
            kind, extra = "q", {"min": min(nums), "max": max(nums)}
        else:
            distinct = sorted(set(vals))
            kind, extra = "n", {"distinct": len(distinct), "sample": distinct[:8]}
        prof["columns"].append({"name": c, "kind": kind, "non_empty": len(vals), **extra})
    prof["shape_guess"] = ",".join(c["kind"] for c in prof["columns"])
    print(json.dumps(prof, indent=1))


# ---------------------------------------------------------------- build
_AGG = "sum"
_Y2 = None  # --y2: a second numeric column (target, upper bound) for bullet, range-band and the like


def _series_split(rows, x, y, series):
    """Group rows into series -> [(x, y)], aggregating duplicate x values within a series
    (sum by default, --agg mean|none) so a bar of sales by region sums the products."""
    out: dict[str, list] = {}
    for r in rows:
        out.setdefault(r[series] if series else "", []).append((r[x], _num(r[y])))
    if _AGG == "none":
        return out
    agg: dict[str, list] = {}
    for name, pts in out.items():
        groups: dict = {}
        for xv, yv in pts:
            groups.setdefault(xv, []).append(yv)
        dup = any(len(v) > 1 for v in groups.values())
        agg[name] = [(xv, (sum(v) / len(v) if _AGG == "mean" else sum(v)) if dup else v[0]) for xv, v in groups.items()]
        if dup:
            print(f"note: duplicate {x} values aggregated by {_AGG} ({len(pts)} rows -> {len(groups)} points)", file=sys.stderr)
    return agg


def _mq(s) -> str:
    return '"' + str(s).replace('"', "'") + '"'


def _g(v) -> str:
    return "0" if v is None else f"{v:g}"


def build_mermaid(chart, rows, x, y, series, title):
    t = title or f"{y} by {x}"
    if chart in ("line", "bar", "column", "area", "multi-line", "grouped-bar", "step"):
        kind = "line" if chart in ("line", "multi-line", "area", "step") else "bar"
        groups = _series_split(rows, x, y, series)
        xs = list(dict.fromkeys(r[x] for r in rows))
        named = a_flag("namedSeries")  # Mermaid 11.16+: named series get a legend; default stays on the 11.13 floor
        lines = ["xychart" if named else "xychart-beta", f"    title {_mq(t)}",
                 "    x-axis [" + ", ".join(_mq(v) for v in xs) + "]", f"    y-axis {_mq(y)}"]
        vals = [v for pts in groups.values() for _, v in pts if v is not None]
        if kind == "bar" and vals and min(vals) >= 0:
            lines[-1] += f" 0 --> {_g(_nice_max(vals))}"  # xychart autoscale truncates the baseline; bars need zero
        for name, pts in groups.items():
            d = dict(pts)
            label = f" {_mq(name or y)}" if named else ""
            lines.append(f"    {kind}{label} [" + ", ".join(_g(d.get(v)) for v in xs) + "]")
        note = "" if (len(groups) == 1 or named) else f"%% xychart has no legend: series in order are {', '.join(groups)}\n"
        return "```mermaid\n" + note + "\n".join(lines) + "\n```\n"
    if chart in ("pie", "donut"):
        lines = ["pie" + (" showData" if a_flag("showData") else ""), f"    title {_mq(t)}"]
        for r in rows:
            lines.append(f"    {_mq(r[x])} : {_g(_num(r[y]))}")
        return "```mermaid\n" + "\n".join(lines) + "\n```\n"
    if chart in ("sankey", "alluvial"):
        lines = ["sankey-beta", ""]
        for r in rows:
            lines.append(f"{r[x]},{r[series]},{_g(_num(r[y]))}")
        return "```mermaid\n" + "\n".join(lines) + "\n```\n"
    if chart == "quadrant":
        lines = ["quadrantChart", f"    title {_mq(t)}", f"    x-axis {_mq(x)}", f"    y-axis {_mq(y)}"]
        for r in rows:
            lines.append(f"    {r[series]}: [{_g(_num(r[x]))}, {_g(_num(r[y]))}]")
        return "```mermaid\n" + "\n".join(lines) + "\n```\n"
    if chart == "radar":
        groups = _series_split(rows, x, y, series)
        axes = list(dict.fromkeys(r[x] for r in rows))
        lines = ["radar-beta", f"    title {_mq(t)}",
                 "    axis " + ", ".join(f"a{i}[{_mq(v)}]" for i, v in enumerate(axes))]
        for name, pts in groups.items():
            d = dict(pts)
            ident = re.sub(r"[^a-zA-Z0-9]", "", name or "v") or "v"
            lines.append(f"    curve {ident}[{_mq(name or y)}]{{" + ", ".join(_g(d.get(v)) for v in axes) + "}")
        return "```mermaid\n" + "\n".join(lines) + "\n```\n"
    raise ValueError(f"mermaid has no recipe for '{chart}'; use an image target (cw.py show {chart} --section build)")


VL_MARKS = {"line": "line", "multi-line": "line", "bar": "bar", "column": "bar", "grouped-bar": "bar", "stacked-bar": "bar",
            "area": "area", "stacked-area": "area", "scatter": "point", "bubble": "circle", "heatmap": "rect", "histogram": "bar",
            "boxplot": "boxplot", "pie": "arc", "donut": "arc", "strip": "tick", "dot": "point", "lollipop": "point", "step": "line"}


VL_COMPOSED = ("dumbbell", "slope", "waterfall", "calendar-heatmap", "diverging-bar", "stacked-bar-100", "small-multiples", "bullet", "range-band", "connected-scatter", "bump")


def _vl_composed(chart, rows, x, y, series, base):
    """Layer and transform recipes. Column roles per chart:
    dumbbell: x=category, y=value, series=the two ends (before/after)
    slope: x=period (two values), y=value, series=entity
    waterfall: x=step label, y=signed change (running total computed in the spec)
    calendar-heatmap: x=date, y=value
    diverging-bar: x=category, y=signed value
    stacked-bar-100: x=category, y=value, series=part
    small-multiples: x=time or category, y=value, series=panel
    bullet: x=measure name, y=actual, --y2 target (optional series=qualitative band column)
    range-band: x=time, y=lower, --y2 upper, optional series=centre line column
    connected-scatter: x=first measure, y=second measure, series=time or order label
    bump: x=period, y=rank (1 = top), series=entity"""
    q = {"field": y, "type": "quantitative"}
    n = {"field": x, "type": "nominal"}
    yq = json.dumps(y)
    if chart == "dumbbell":
        if _Y2:  # wide form: fold the two value columns into (end, value) pairs inside the spec
            base["transform"] = [{"fold": [y, _Y2], "as": ["end", "value"]}]
            q = {"field": "value", "type": "quantitative"}; series = "end"
        base["encoding"] = {"y": {**n, "sort": "-x"}, "x": {**q, "title": y if not _Y2 else f"{y} to {_Y2}"}}
        base["layer"] = [{"mark": "rule", "encoding": {"x": {**q, "aggregate": "min"}, "x2": {"field": q["field"], "aggregate": "max"}}},
                         {"mark": {"type": "point", "filled": True, "size": 90}, "encoding": {"color": {"field": series, "type": "nominal"}}}]
    elif chart == "slope":
        last = rows[-1][x]
        base["encoding"] = {"x": {**n, "axis": {"labelAngle": 0}}, "y": {**q, "scale": {"zero": False}}, "color": {"field": series, "type": "nominal", "legend": None}}
        base["layer"] = [{"mark": {"type": "line", "point": True}},
                         {"mark": {"type": "text", "align": "left", "dx": 6}, "transform": [{"filter": {"field": x, "equal": last}}], "encoding": {"text": {"field": series}}}]
        base["width"] = 300
    elif chart == "waterfall":
        base["transform"] = [{"window": [{"op": "sum", "field": y, "as": "end"}]}, {"calculate": f"datum.end - datum[{yq}]", "as": "start"},
                             {"calculate": f"datum[{yq}] < 0 ? 'decrease' : 'increase'", "as": "dir"}]
        base["encoding"] = {"x": {**n, "sort": None, "axis": {"labelAngle": 0}}, "y": {"field": "start", "type": "quantitative", "title": y}, "y2": {"field": "end"},
                            "color": {"field": "dir", "type": "nominal", "scale": {"domain": ["increase", "decrease"], "range": ["#2a78d6", "#e34948"]}, "legend": None}}
        base["mark"] = "bar"
    elif chart == "calendar-heatmap":
        base["mark"] = "rect"
        base["encoding"] = {"x": {"field": x, "type": "ordinal", "timeUnit": "week", "title": "week"}, "y": {"field": x, "type": "ordinal", "timeUnit": "day", "title": None},
                            "color": {**q, "scale": {"scheme": "greens"}}, "tooltip": [{"field": x, "type": "temporal"}, q]}
        base["height"] = 140
    elif chart == "diverging-bar":
        base["mark"] = "bar"
        base["transform"] = [{"calculate": f"datum[{yq}] < 0 ? 'negative' : 'positive'", "as": "sign"}]
        base["encoding"] = {"y": {**n, "sort": "-x"}, "x": q, "color": {"field": "sign", "type": "nominal", "scale": {"domain": ["positive", "negative"], "range": ["#2a78d6", "#e34948"]}, "legend": None}}
    elif chart == "stacked-bar-100":
        base["mark"] = "bar"
        base["encoding"] = {"x": {**n, "axis": {"labelAngle": 0}}, "y": {**q, "stack": "normalize", "axis": {"format": "%"}}, "color": {"field": series, "type": "nominal"}}
    elif chart == "bullet":
        if not _Y2:
            raise ValueError("bullet needs --y2 <target column>")
        base["encoding"] = {"y": {**n, "axis": {"title": None}}}
        base["layer"] = [{"mark": {"type": "bar", "size": 14, "color": "#2a78d6"}, "encoding": {"x": {**q, "title": y}}},
                         {"mark": {"type": "tick", "thickness": 3, "size": 26, "color": "#222"}, "encoding": {"x": {"field": _Y2, "type": "quantitative"}}}]
        if series:
            base["layer"].insert(0, {"mark": {"type": "bar", "size": 26, "color": "#d9d9d9"}, "encoding": {"x": {"field": series, "type": "quantitative"}}})
        base["height"] = max(60, 28 * len({r[x] for r in rows}))
    elif chart == "range-band":
        if not _Y2:
            raise ValueError("range-band needs --y2 <upper column> (--y is the lower)")
        xk = "temporal" if all(_is_time(r[x]) for r in rows) else "quantitative"
        xe = {"field": x, "type": xk, **({"scale": {"type": "utc"}} if xk == "temporal" else {})}
        if xk == "temporal" and all(re.fullmatch(r"\d{4}-\d{2}-01", str(r[x])) for r in rows):
            xe["axis"] = {"tickCount": "month", "format": "%b %Y"}
        base["encoding"] = {"x": xe}
        base["layer"] = [{"mark": {"type": "area", "opacity": 0.3}, "encoding": {"y": {**q, "title": f"{y} to {_Y2}", "scale": {"zero": False}}, "y2": {"field": _Y2}}}]
        if series:
            base["layer"].append({"mark": "line", "encoding": {"y": {"field": series, "type": "quantitative"}}})
    elif chart == "connected-scatter":
        if not series:
            raise ValueError("connected-scatter needs --series <time or order column> for the path order and labels")
        base["encoding"] = {"x": {"field": x, "type": "quantitative", "scale": {"zero": False}}, "y": {**q, "scale": {"zero": False}}, "order": {"field": series}}
        base["layer"] = [{"mark": {"type": "line", "color": "#2a78d6"}}, {"mark": {"type": "point", "filled": True, "size": 60, "color": "#2a78d6"}},
                         {"mark": {"type": "text", "align": "left", "dx": 7, "dy": -4}, "encoding": {"text": {"field": series}}}]
    elif chart == "bump":
        if not series:
            raise ValueError("bump needs --series <entity column>; --y is the rank (1 = top)")
        top = max(_num(r[y]) or 0 for r in rows)
        base["encoding"] = {"x": {**n, "axis": {"labelAngle": 0}}, "y": {**q, "scale": {"domain": [0.5, top + 0.5], "reverse": True, "nice": False}, "axis": {"tickMinStep": 1, "values": list(range(1, int(top) + 1))}, "title": "rank"},
                            "color": {"field": series, "type": "nominal", "legend": None}}
        last = rows[-1][x]
        base["layer"] = [{"mark": {"type": "line", "point": True, "interpolate": "monotone", "strokeWidth": 3}},
                         {"mark": {"type": "text", "align": "left", "dx": 8}, "transform": [{"filter": {"field": x, "equal": last}}], "encoding": {"text": {"field": series}}}]
    elif chart == "small-multiples":
        xk = "temporal" if all(_is_time(r[x]) for r in rows) else "nominal"
        xe = {"field": x, "type": xk}
        if xk == "temporal":
            xe["scale"] = {"type": "utc"}
        base.pop("width"); base.pop("height")
        base["facet"] = {"field": series, "type": "nominal", "columns": 3, "title": None}
        base["spec"] = {"mark": {"type": "line", "point": len(rows) <= 60}, "width": 180, "height": 120,
                        "encoding": {"x": xe, "y": {**q, "scale": {"zero": False}}}}
    return base


def build_vega_lite(chart, rows, x, y, series, title, data_path):
    if chart not in VL_MARKS and chart not in VL_COMPOSED:
        raise ValueError(f"vega-lite has no recipe for '{chart}'")
    xk = "temporal" if all(_is_time(r[x]) for r in rows) else ("quantitative" if all(_num(r[x]) is not None for r in rows) else "nominal")
    spec = {"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "title": title or f"{y} by {x}",
            "data": {"url": Path(data_path).name} if a_flag("dataByUrl") else {"values": rows},
            "mark": VL_MARKS.get(chart, "bar"), "width": "container" if a_flag("container") else 600, "height": 320, "encoding": {}}
    for r in rows:  # numbers as numbers so Vega-Lite does not treat them as strings
        for k in (x, y, series, _Y2):
            if k and _num(r.get(k)) is not None and not _is_time(r.get(k)):
                r[k] = _num(r[k])
    if chart in VL_COMPOSED:
        if chart in ("slope", "stacked-bar-100", "small-multiples", "connected-scatter", "bump") and not series:
            raise ValueError(f"{chart} needs --series (column roles in cw.py _vl_composed)")
        if chart == "dumbbell" and not series and not _Y2:
            raise ValueError(f"{chart} needs --series (column roles in cw.py _vl_composed)")
        spec.pop("encoding"); spec.pop("mark")
        return json.dumps(_vl_composed(chart, rows, x, y, series, spec), indent=1, ensure_ascii=False) + "\n"
    if chart in ("pie", "donut"):
        spec["mark"] = {"type": "arc", "innerRadius": 60} if chart == "donut" else "arc"
        spec["encoding"] = {"theta": {"field": y, "type": "quantitative"}, "color": {"field": x, "type": "nominal"}}
        spec.pop("width"); spec.pop("height")
    elif chart == "histogram":
        spec["encoding"] = {"x": {"field": y, "type": "quantitative", "bin": True}, "y": {"aggregate": "count"}}
    elif chart == "heatmap":
        spec["encoding"] = {"x": {"field": x, "type": "nominal"}, "y": {"field": series, "type": "nominal"},
                            "color": {"field": y, "type": "quantitative", "scale": {"scheme": "blues"}}}
    elif chart == "boxplot":
        spec["encoding"] = {"x": {"field": x, "type": "nominal"}, "y": {"field": y, "type": "quantitative"}}
    else:
        horizontal = chart in ("bar", "lollipop", "dot") and xk == "nominal" and len(rows) > 6
        xe = {"field": x, "type": xk}
        if chart == "bar" and xk == "nominal" and not series:
            xe["sort"] = "-x" if horizontal else "-y"  # the bar is the ranking chart (kb/charts/bar.md): sort by value
        if xk == "temporal":
            xe["scale"] = {"type": "utc"}  # ISO dates parse as UTC; a local scale shifts them by a day
            if all(re.fullmatch(r"\d{4}-\d{2}-01", str(r[x])) for r in rows):
                xe["axis"] = {"tickCount": "month", "format": "%b %Y"}  # monthly data: one tick per month, not fortnightly defaults
        elif xk == "nominal" and len(rows) <= 12:
            xe["axis"] = {"labelAngle": 0}  # short category lists read better unrotated
        ye = {"field": y, "type": "quantitative"}
        if chart in ("line", "multi-line", "step"):
            ye["scale"] = {"zero": False}  # lines need not start at zero (kb/charts/line.md); bars keep zero
        if chart == "step":
            spec["mark"] = {"type": "line", "interpolate": "step-after"}
        if chart in ("line", "multi-line", "area", "stacked-area"):
            spec["mark"] = {"type": spec["mark"], "point": len(rows) <= 40}
        if horizontal:
            xe["sort"] = "-x"
            spec["encoding"] = {"y": xe, "x": ye}
        else:
            spec["encoding"] = {"x": xe, "y": ye}
        if series:
            spec["encoding"]["color"] = {"field": series, "type": "nominal"}
            if chart == "grouped-bar":
                spec["encoding"]["xOffset"] = {"field": series}
            if chart == "bubble":
                spec["encoding"]["size"] = {"field": series, "type": "quantitative"}
                spec["encoding"].pop("color")
        if chart == "lollipop":
            enc = spec.pop("encoding"); spec.pop("mark")
            vk, v2 = ("x", "x2") if horizontal else ("y", "y2")
            spec["layer"] = [{"mark": "rule", "encoding": {**enc, v2: {"datum": 0}}},
                             {"mark": {"type": "point", "filled": True, "size": 80}, "encoding": enc}]
    return json.dumps(spec, indent=1, ensure_ascii=False) + "\n"


def _two_ends(rows, x, y, series):
    """Dumbbell inputs: wide form (--y2 second value) or long form (--series with exactly two values).
    Returns (categories, first values, second values, (name1, name2))."""
    if _Y2:
        return [r[x] for r in rows], [_num(r[y]) for r in rows], [_num(r[_Y2]) for r in rows], (y, _Y2)
    if not series:
        raise ValueError("dumbbell needs --y2 <second value column> or --series <column with two ends>")
    ends = list(dict.fromkeys(r[series] for r in rows))
    if len(ends) != 2:
        raise ValueError(f"dumbbell --series must have exactly two values, got {ends}")
    d = {(r[x], r[series]): _num(r[y]) for r in rows}
    cats = list(dict.fromkeys(r[x] for r in rows))
    return cats, [d.get((c, ends[0])) for c in cats], [d.get((c, ends[1])) for c in cats], (ends[0], ends[1])


def build_plotly(chart, rows, x, y, series, title):
    groups = _series_split(rows, x, y, series)
    traces = []
    kind = {"line": "scatter", "multi-line": "scatter", "area": "scatter", "stacked-area": "scatter", "scatter": "scatter",
            "bar": "bar", "column": "bar", "grouped-bar": "bar", "stacked-bar": "bar", "pie": "pie", "donut": "pie",
            "histogram": "histogram", "boxplot": "box", "heatmap": "heatmap", "bubble": "scatter", "step": "scatter"}.get(chart)
    layout = {"title": {"text": title or f"{y} by {x}"}, "xaxis": {"title": {"text": x}}, "yaxis": {"title": {"text": y}},
              "template": "plotly_white", "margin": {"t": 50, "r": 20}}
    if chart == "waterfall":  # x=step, y=signed change; Plotly has a native waterfall trace
        traces.append({"type": "waterfall", "x": [r[x] for r in rows], "y": [_num(r[y]) for r in rows], "connector": {"line": {"color": "#999"}},
                       "increasing": {"marker": {"color": "#2a78d6"}}, "decreasing": {"marker": {"color": "#e34948"}}, "totals": {"marker": {"color": "#555"}}})
        return json.dumps({"data": traces, "layout": layout}, indent=1, ensure_ascii=False) + "\n"
    if chart == "dumbbell":  # x=category, y=value, --y2 second value (wide) or --series with two ends (long)
        cats, a, b, names = _two_ends(rows, x, y, series)
        for c, v1, v2 in zip(cats, a, b):
            traces.append({"type": "scatter", "mode": "lines", "x": [v1, v2], "y": [c, c], "line": {"color": "#bbb", "width": 3}, "showlegend": False, "hoverinfo": "skip"})
        traces.append({"type": "scatter", "mode": "markers", "name": names[0], "x": a, "y": cats, "marker": {"size": 11, "color": "#2a78d6"}})
        traces.append({"type": "scatter", "mode": "markers", "name": names[1], "x": b, "y": cats, "marker": {"size": 11, "color": "#e34948"}})
        layout["xaxis"]["title"]["text"] = y; layout["yaxis"]["title"]["text"] = x; layout["yaxis"]["autorange"] = "reversed"
        return json.dumps({"data": traces, "layout": layout}, indent=1, ensure_ascii=False) + "\n"
    if chart == "bullet":  # x=measure name, y=actual, --y2 target, optional --series poor band
        if not _Y2:
            raise ValueError("bullet needs --y2 <target column>")
        cats = [r[x] for r in rows]
        if series:
            traces.append({"type": "bar", "orientation": "h", "name": series, "y": cats, "x": [_num(r[series]) for r in rows], "marker": {"color": "#d9d9d9"}, "width": 0.8})
        traces.append({"type": "bar", "orientation": "h", "name": y, "y": cats, "x": [_num(r[y]) for r in rows], "marker": {"color": "#2a78d6"}, "width": 0.4})
        traces.append({"type": "scatter", "mode": "markers", "name": _Y2, "y": cats, "x": [_num(r[_Y2]) for r in rows], "marker": {"symbol": "line-ns", "size": 22, "line": {"width": 3, "color": "#222"}}})
        layout["barmode"] = "overlay"; layout["xaxis"]["title"]["text"] = y; layout["yaxis"]["title"]["text"] = None; layout["yaxis"]["autorange"] = "reversed"
        return json.dumps({"data": traces, "layout": layout}, indent=1, ensure_ascii=False) + "\n"
    if not kind:
        raise ValueError(f"plotly has no recipe for '{chart}'")
    if kind == "pie":
        traces.append({"type": "pie", "labels": [r[x] for r in rows], "values": [_num(r[y]) for r in rows],
                       "hole": 0.5 if chart == "donut" else 0, "sort": False, "textinfo": "label+percent"})
        layout.pop("xaxis"); layout.pop("yaxis")
    elif kind == "histogram":
        traces.append({"type": "histogram", "x": [_num(r[y]) for r in rows]})
    elif kind == "heatmap":
        xs = list(dict.fromkeys(r[x] for r in rows)); ys = list(dict.fromkeys(r[series] for r in rows))
        z = [[next((_num(r[y]) for r in rows if r[x] == xv and r[series] == yv), None) for xv in xs] for yv in ys]
        traces.append({"type": "heatmap", "x": xs, "y": ys, "z": z, "colorscale": "Blues"})
    else:
        for name, pts in groups.items():
            tr = {"type": kind, "name": name or y, "x": [p[0] for p in pts], "y": [p[1] for p in pts]}
            if chart in ("line", "multi-line"):
                tr["mode"] = "lines+markers" if len(pts) <= 40 else "lines"
            if chart == "step":
                tr["mode"] = "lines"; tr["line"] = {"shape": "hv"}
            if chart in ("area", "stacked-area"):
                tr["mode"] = "lines"; tr["fill"] = "tonexty" if series else "tozeroy"
                if chart == "stacked-area":
                    tr["stackgroup"] = "one"
            if chart in ("scatter", "bubble"):
                tr["mode"] = "markers"
            if kind == "box":
                tr = {"type": "box", "name": name or y, "y": [p[1] for p in pts]}
            traces.append(tr)
        if chart == "stacked-bar":
            layout["barmode"] = "stack"
        if chart == "grouped-bar":
            layout["barmode"] = "group"
    return json.dumps({"data": traces, "layout": layout}, indent=1, ensure_ascii=False) + "\n"


def build_chartjs(chart, rows, x, y, series, title):
    kind = {"line": "line", "multi-line": "line", "area": "line", "step": "line", "bar": "bar", "column": "bar", "grouped-bar": "bar",
            "stacked-bar": "bar", "pie": "pie", "donut": "doughnut", "scatter": "scatter", "bubble": "bubble", "radar": "radar",
            "polar-area": "polarArea"}.get(chart)
    if not kind:
        raise ValueError(f"chartjs has no recipe for '{chart}'")
    groups = _series_split(rows, x, y, series)
    labels = list(dict.fromkeys(r[x] for r in rows))
    datasets = []
    for name, pts in groups.items():
        d = dict(pts)
        if kind in ("scatter", "bubble"):
            datasets.append({"label": name or y, "data": [{"x": _num(p[0]), "y": p[1]} for p in pts]})
        else:
            ds = {"label": name or y, "data": [d.get(l) for l in labels]}
            if chart == "area":
                ds["fill"] = True
            if chart == "step":
                ds["stepped"] = True
            datasets.append(ds)
    cfg = {"type": kind, "data": {"labels": labels, "datasets": datasets},
           "options": {"responsive": True, "plugins": {"title": {"display": True, "text": title or f"{y} by {x}"},
                                                       "legend": {"display": bool(series) or kind in ("pie", "doughnut", "polarArea")}}}}
    if chart == "stacked-bar":
        cfg["options"]["scales"] = {"x": {"stacked": True}, "y": {"stacked": True}}
    return json.dumps(cfg, indent=1, ensure_ascii=False) + "\n"


def build_matplotlib(chart, rows, x, y, series, title, out):
    groups = _series_split(rows, x, y, series)
    out = out or "chart.png"
    lines = ["import matplotlib", "matplotlib.use('Agg')", "import matplotlib.pyplot as plt", "",
             "fig, ax = plt.subplots(figsize=(8, 4.2), dpi=150)"]
    t = title or f"{y} by {x}"
    if chart in ("waterfall", "dumbbell", "bullet"):
        if chart == "waterfall":
            xs = [r[x] for r in rows]; ys = [_num(r[y]) for r in rows]
            lines += [f"xs, ys = {xs!r}, {ys!r}", "start, bottoms, colors = 0, [], []",
                      "for v in ys:", "    bottoms.append(start if v >= 0 else start + v); colors.append('#2a78d6' if v >= 0 else '#e34948'); start += v",
                      "ax.bar(xs, [abs(v) for v in ys], bottom=bottoms, color=colors)", "ax.axhline(0, color='#333', linewidth=0.8)",
                      "for i in range(len(xs) - 1):", "    ax.plot([i + 0.4, i + 0.6], [bottoms[i] + abs(ys[i]) if ys[i] >= 0 else bottoms[i]] * 2, color='#999', linewidth=1)",
                      f"ax.set_xlabel({x!r}); ax.set_ylabel({y!r})"]
        elif chart == "dumbbell":
            cats, a, b, names = _two_ends(rows, x, y, series)
            lines += [f"cats, a, b = {cats!r}, {a!r}, {b!r}", "ax.hlines(cats, a, b, color='#bbb', linewidth=3)",
                      f"ax.scatter(a, cats, s=80, color='#2a78d6', label={names[0]!r}, zorder=3)", f"ax.scatter(b, cats, s=80, color='#e34948', label={names[1]!r}, zorder=3)",
                      "ax.invert_yaxis()", f"ax.set_xlabel({y!r})", "ax.legend()"]
        else:
            if not _Y2:
                raise ValueError("bullet needs --y2 <target column>")
            cats = [r[x] for r in rows]; act = [_num(r[y]) for r in rows]; tgt = [_num(r[_Y2]) for r in rows]
            if series:
                lines.append(f"ax.barh({cats!r}, {[_num(r[series]) for r in rows]!r}, height=0.8, color='#d9d9d9', label={series!r})")
            lines += [f"ax.barh({cats!r}, {act!r}, height=0.35, color='#2a78d6', label={y!r})",
                      f"ax.scatter({tgt!r}, {cats!r}, marker='|', s=400, color='#222', linewidths=3, label={_Y2!r}, zorder=3)",
                      "ax.invert_yaxis()", f"ax.set_xlabel({y!r})", "ax.legend(loc='lower right')"]
        lines += ["ax.spines[['top','right']].set_visible(False)", "ax.grid(axis='x' if " + repr(chart != "waterfall") + " else 'y', alpha=0.3)",
                  f"ax.set_title({t!r})", "fig.tight_layout()", f"fig.savefig({out!r}); print('wrote', {out!r})"]
        return "\n".join(lines) + "\n"
    for name, pts in groups.items():
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        label = f", label={name!r}" if name else ""
        if chart in ("line", "multi-line", "step"):
            ds = ", drawstyle='steps-post'" if chart == "step" else ""
            lines.append(f"ax.plot({xs!r}, {ys!r}, marker='o', linewidth=2{ds}{label})")
        elif chart == "area":
            lines.append(f"ax.fill_between(range(len({xs!r})), {ys!r}, alpha=0.35{label}); ax.plot({ys!r}, linewidth=2); ax.set_xticks(range(len({xs!r})), {xs!r})")
        elif chart in ("bar", "column", "grouped-bar"):
            lines.append(f"ax.bar({xs!r}, {ys!r}{label})")
        elif chart == "scatter":
            lines.append(f"ax.scatter([float(v) for v in {xs!r}], {ys!r}{label})")
        elif chart == "histogram":
            lines.append(f"ax.hist({ys!r}, bins='auto')")
        elif chart in ("pie", "donut"):
            wp = ", wedgeprops=dict(width=0.4)" if chart == "donut" else ""
            lines.append(f"ax.pie({ys!r}, labels={xs!r}, autopct='%1.0f%%', startangle=90{wp}); ax.axis('equal')")
        elif chart == "boxplot":
            lines.append(f"ax.boxplot([{ys!r}], tick_labels=[{(name or y)!r}])")
        else:
            raise ValueError(f"matplotlib has no recipe for '{chart}'")
    if chart not in ("pie", "donut"):
        lines += [f"ax.set_xlabel({x!r}); ax.set_ylabel({y!r})", "ax.spines[['top','right']].set_visible(False)", "ax.grid(axis='y', alpha=0.3)"]
        if len(rows) > 8:
            lines.append("plt.setp(ax.get_xticklabels(), rotation=45, ha='right')")
    lines += [f"ax.set_title({t!r})", "ax.legend()" if series else "", "fig.tight_layout()",
              f"fig.savefig({out!r}); print('wrote', {out!r})"]
    return "\n".join(l for l in lines if l) + "\n"


BLOCKS = "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"


def build_terminal(chart, rows, x, y, series, title):
    """Unicode charts for chat replies and terminals: sparkline (line, sparkline), block bars (bar, column)."""
    groups = _series_split(rows, x, y, series)
    out = [title or f"{y} by {x}"]
    if chart in ("line", "sparkline", "multi-line", "area", "step"):
        for name, pts in groups.items():
            vals = [v for _, v in pts if v is not None]
            lo, hi = min(vals), max(vals)
            spark = "".join(BLOCKS[0 if hi == lo else int((v - lo) / (hi - lo) * 7)] for v in vals)
            label = f"{name}: " if name else ""
            out.append(f"{label}{spark}  {vals[0]:g} -> {vals[-1]:g} (min {lo:g}, max {hi:g}, {len(vals)} points, {pts[0][0]} to {pts[-1][0]})")
        return "\n".join(out) + "\n"
    if chart in ("bar", "column"):
        pts = groups[""] if "" in groups else [p for g in groups.values() for p in g]
        width = max(len(str(k)) for k, _ in pts)
        hi = max(v for _, v in pts) or 1
        for k, v in pts:
            out.append(f"{str(k):<{width}}  {BLOCKS[-1] * int(round(v / hi * 30)):<30} {v:g}")
        return "\n".join(out) + "\n"
    raise ValueError(f"terminal has no recipe for '{chart}' (line, sparkline, bar, column); use a table")


def build_echarts(chart, rows, x, y, series, title):
    """Apache ECharts option JSON. Covers the cartesian basics plus pie, radar, funnel, sankey, heatmap."""
    groups = _series_split(rows, x, y, series)
    t = title or f"{y} by {x}"
    opt = {"title": {"text": t}, "tooltip": {"trigger": "axis"}, "legend": {"show": bool(series)}, "grid": {"containLabel": True}}
    xs = list(dict.fromkeys(r[x] for r in rows))
    kind = {"line": "line", "multi-line": "line", "step": "line", "area": "line", "stacked-area": "line", "bar": "bar", "column": "bar",
            "grouped-bar": "bar", "stacked-bar": "bar", "stacked-bar-100": "bar", "scatter": "scatter", "bubble": "scatter",
            "pie": "pie", "donut": "pie", "radar": "radar", "funnel": "funnel", "sankey": "sankey", "alluvial": "sankey", "heatmap": "heatmap"}.get(chart)
    if not kind:
        raise ValueError(f"echarts has no recipe for '{chart}'")
    if kind == "pie":
        opt["tooltip"] = {"trigger": "item"}; opt["legend"] = {"show": True}
        opt["series"] = [{"type": "pie", "radius": ["45%", "70%"] if chart == "donut" else "65%", "label": {"formatter": "{b}: {d}%"},
                          "data": [{"name": r[x], "value": _num(r[y])} for r in rows]}]
    elif kind == "funnel":
        opt["tooltip"] = {"trigger": "item"}
        opt["series"] = [{"type": "funnel", "sort": "descending", "label": {"formatter": "{b}: {c}"}, "data": [{"name": r[x], "value": _num(r[y])} for r in rows]}]
    elif kind == "sankey":
        nodes = list(dict.fromkeys([r[x] for r in rows] + [r[series] for r in rows]))
        opt["tooltip"] = {"trigger": "item"}
        opt["series"] = [{"type": "sankey", "data": [{"name": n} for n in nodes], "links": [{"source": r[x], "target": r[series], "value": _num(r[y])} for r in rows]}]
    elif kind == "radar":
        axes = list(dict.fromkeys(r[x] for r in rows))
        opt["radar"] = {"indicator": [{"name": a} for a in axes]}
        opt["tooltip"] = {"trigger": "item"}; opt["legend"] = {"show": True}
        opt["series"] = [{"type": "radar", "data": [{"name": name or y, "value": [dict(pts).get(a) for a in axes]} for name, pts in groups.items()]}]
    elif kind == "heatmap":
        ys = list(dict.fromkeys(r[series] for r in rows))
        vals = [_num(r[y]) for r in rows]
        opt["tooltip"] = {"trigger": "item"}
        opt["xAxis"] = {"type": "category", "data": xs}; opt["yAxis"] = {"type": "category", "data": ys}
        opt["visualMap"] = {"min": min(vals), "max": max(vals), "calculable": True, "orient": "horizontal", "left": "center", "bottom": 0}
        opt["series"] = [{"type": "heatmap", "data": [[xs.index(r[x]), ys.index(r[series]), _num(r[y])] for r in rows], "label": {"show": True}}]
    elif kind == "scatter":
        opt["tooltip"] = {"trigger": "item"}
        opt["xAxis"] = {"type": "value", "name": x}; opt["yAxis"] = {"type": "value", "name": y}
        opt["series"] = [{"type": "scatter", "name": name or y, "data": [[_num(px), py] for px, py in pts],
                          **({"symbolSize": 12} if chart == "scatter" else {})} for name, pts in groups.items()]
    else:
        opt["xAxis"] = {"type": "category", "data": xs, "name": x, "boundaryGap": kind == "bar"}
        opt["yAxis"] = {"type": "value", "name": y}
        ser = []
        for name, pts in groups.items():
            d = dict(pts)
            item = {"type": kind, "name": name or y, "data": [d.get(v) for v in xs]}
            if chart == "step":
                item["step"] = "end"
            if chart in ("area", "stacked-area"):
                item["areaStyle"] = {}
            if chart in ("stacked-area", "stacked-bar", "stacked-bar-100"):
                item["stack"] = "total"
            if chart in ("line", "multi-line", "area", "stacked-area"):
                item["smooth"] = False; item["symbol"] = "circle" if len(pts) <= 40 else "none"
            ser.append(item)
        opt["series"] = ser
        if chart == "stacked-bar-100":
            opt["yAxis"]["max"] = 100
            totals = {v: sum((dict(pts).get(v) or 0) for pts in groups.values()) for v in xs}
            for item in ser:
                item["data"] = [round(100 * (val or 0) / totals[v], 2) if totals[v] else 0 for v, val in zip(xs, item["data"])]
    return json.dumps(opt, indent=1, ensure_ascii=False) + "\n"


def build_pptx(chart, rows, x, y, series, title, out):
    """A python-pptx script that writes a native, editable PowerPoint chart. Run it with cw.py render --target pptx."""
    kind = {"bar": "BAR_CLUSTERED", "column": "COLUMN_CLUSTERED", "grouped-bar": "COLUMN_CLUSTERED", "stacked-bar": "COLUMN_STACKED",
            "stacked-bar-100": "COLUMN_STACKED_100", "line": "LINE_MARKERS", "multi-line": "LINE_MARKERS", "area": "AREA", "stacked-area": "AREA_STACKED",
            "pie": "PIE", "donut": "DOUGHNUT", "radar": "RADAR", "scatter": "XY_SCATTER", "bubble": "BUBBLE"}.get(chart)
    if not kind:
        raise ValueError(f"pptx has no native chart for '{chart}'; insert a PNG from the vega-lite target instead")
    groups = _series_split(rows, x, y, series)
    out = out or "chart.pptx"
    t = title or f"{y} by {x}"
    lines = ["from pptx import Presentation", "from pptx.chart.data import CategoryChartData, XyChartData, BubbleChartData",
             "from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION", "from pptx.util import Inches, Pt", "",
             "prs = Presentation()", "slide = prs.slides.add_slide(prs.slide_layouts[5])", f"slide.shapes.title.text = {t!r}"]
    if kind in ("XY_SCATTER", "BUBBLE"):
        lines.append("data = XyChartData()" if kind == "XY_SCATTER" else "data = BubbleChartData()")
        for name, pts in groups.items():
            lines.append(f"s = data.add_series({(name or y)!r})")
            for px, py in pts:
                lines.append(f"s.add_data_point({_num(px)!r}, {py!r})" if kind == "XY_SCATTER" else f"s.add_data_point({_num(px)!r}, {py!r}, 1)")
    else:
        xs = list(dict.fromkeys(r[x] for r in rows))
        lines += ["data = CategoryChartData()", f"data.categories = {xs!r}"]
        for name, pts in groups.items():
            d = dict(pts)
            lines.append(f"data.add_series({(name or y)!r}, {[d.get(v) for v in xs]!r})")
    lines += [f"gf = slide.shapes.add_chart(XL_CHART_TYPE.{kind}, Inches(0.7), Inches(1.5), Inches(8.6), Inches(5), data)", "chart = gf.chart",
              f"chart.has_legend = {bool(series) or kind in ('PIE', 'DOUGHNUT')}", "if chart.has_legend:", "    chart.legend.position = XL_LEGEND_POSITION.BOTTOM; chart.legend.include_in_layout = False",
              "plot = chart.plots[0]", "plot.has_data_labels = " + ("True" if kind in ("PIE", "DOUGHNUT") else "False"),
              "if plot.has_data_labels:", "    plot.data_labels.number_format = '0%'; plot.data_labels.show_percentage = True; plot.data_labels.show_value = False",
              f"prs.save({out!r}); print('wrote', {out!r})"]
    return "\n".join(lines) + "\n"


def build_xlsx(chart, rows, x, y, series, title, out):
    """An openpyxl script that writes the data to a sheet and a native Excel chart beside it."""
    kind = {"bar": ("BarChart", "bar"), "column": ("BarChart", "col"), "grouped-bar": ("BarChart", "col"), "stacked-bar": ("BarChart", "stacked"),
            "stacked-bar-100": ("BarChart", "percentStacked"), "line": ("LineChart", None), "multi-line": ("LineChart", None), "area": ("AreaChart", None),
            "stacked-area": ("AreaChart", "stacked"), "pie": ("PieChart", None), "donut": ("DoughnutChart", None), "radar": ("RadarChart", None),
            "scatter": ("ScatterChart", None), "bubble": ("BubbleChart", None)}.get(chart)
    if not kind:
        raise ValueError(f"xlsx has no native chart for '{chart}'; insert a PNG with openpyxl.drawing.image.Image instead")
    cls, style = kind
    groups = _series_split(rows, x, y, series)
    out = out or "chart.xlsx"
    t = title or f"{y} by {x}"
    xs = list(dict.fromkeys(r[x] for r in rows))
    names = [n or y for n in groups]
    lines = [f"from openpyxl import Workbook", f"from openpyxl.chart import {cls}, Reference, Series", "",
             "wb = Workbook(); ws = wb.active; ws.title = 'data'", f"ws.append({[x] + names!r})"]
    for v in xs:
        lines.append(f"ws.append({[v] + [dict(pts).get(v) for pts in groups.values()]!r})")
    n = len(xs); m = len(names)
    lines += [f"chart = {cls}()", f"chart.title = {t!r}", "chart.height = 9; chart.width = 18"]
    if cls in ("ScatterChart", "BubbleChart"):
        lines += [f"xref = Reference(ws, min_col=1, min_row=2, max_row={n + 1})"]
        for i, name in enumerate(names):
            lines.append(f"chart.series.append(Series(Reference(ws, min_col={i + 2}, min_row=1, max_row={n + 1}), xref, title_from_data=True))")
        lines += [f"chart.x_axis.title = {x!r}; chart.y_axis.title = {y!r}"]
    else:
        lines += [f"data = Reference(ws, min_col=2, max_col={m + 1}, min_row=1, max_row={n + 1})",
                  f"cats = Reference(ws, min_col=1, min_row=2, max_row={n + 1})",
                  "chart.add_data(data, titles_from_data=True); chart.set_categories(cats)"]
        if cls == "BarChart":
            lines.append("chart.type = 'bar'" if style == "bar" else "chart.type = 'col'")
            if style in ("stacked", "percentStacked"):
                lines.append(f"chart.grouping = {style!r}; chart.overlap = 100")
        if cls == "AreaChart" and style == "stacked":
            lines.append("chart.grouping = 'stacked'")
        if cls not in ("PieChart", "DoughnutChart", "RadarChart"):
            lines.append(f"chart.x_axis.title = {x!r}; chart.y_axis.title = {y!r}")
    lines += [f"chart.legend = chart.legend if {m > 1 or cls in ('PieChart', 'DoughnutChart')} else None",
              f"ws.add_chart(chart, '{chr(ord('A') + m + 2)}2')", f"wb.save({out!r}); print('wrote', {out!r})"]
    return "\n".join(lines) + "\n"


def build_quickchart(chart, rows, x, y, series, title):
    """A QuickChart image URL (Chart.js 4 config) and the markdown image line; no install, renders remotely."""
    import urllib.parse
    cfg = json.loads(build_chartjs(chart, rows, x, y, series, title))
    url = "https://quickchart.io/chart?version=4&w=800&h=400&c=" + urllib.parse.quote(json.dumps(cfg, separators=(",", ":")), safe="")
    return f"![{title or f'{y} by {x}'}]({url})\n"


def _nice_max(vals):
    """A round axis ceiling at or above the largest value (10, 50, 120, 1100...)."""
    hi = max(vals) if vals else 1
    if hi <= 0:
        return 1
    import math
    mag = 10 ** math.floor(math.log10(hi))
    for f in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if f * mag >= hi:
            return int(f * mag) if f * mag >= 10 else f * mag
    return hi


def build_plantuml(chart, rows, x, y, series, title):
    """PlantUML @startchart (1.2026.0+): bar, line, area, scatter series on shared axes; no pie."""
    kind = {"bar": "bar", "column": "bar", "grouped-bar": "bar", "stacked-bar": "bar", "line": "line", "multi-line": "line",
            "sparkline": "line", "area": "area", "stacked-area": "area", "scatter": "scatter"}.get(chart)
    if not kind:
        raise ValueError(f"plantuml has no chart recipe for '{chart}' (bar, column, grouped-bar, stacked-bar, line, multi-line, area, stacked-area, scatter)")
    groups = _series_split(rows, x, y, series)
    t = title or f"{y} by {x}"
    lines = ["@startchart", f"title {_mq(t)}"]
    if chart in ("stacked-bar", "stacked-area"):
        lines.append("stackMode stacked")
    vals = [v for pts in groups.values() for _, v in pts if v is not None]
    if kind == "scatter":
        xs = [_num(px) for pts in groups.values() for px, _ in pts]
        if any(v is None for v in xs):
            raise ValueError("plantuml scatter needs a numeric x column")
        lines += [f"h-axis {_mq(x)} 0 --> {_g(_nice_max(xs))}", f"v-axis {_mq(y)} 0 --> {_g(_nice_max(vals))}"]
        for name, pts in groups.items():
            lines.append(f"scatter {_mq(name or y)} [" + ", ".join(f"({_g(_num(px))}, {_g(py)})" for px, py in pts) + "]")
    else:
        xs = list(dict.fromkeys(r[x] for r in rows))
        top = _nice_max([sum(dict(p).get(v) or 0 for p in groups.values()) for v in xs]) if chart in ("stacked-bar", "stacked-area") else _nice_max(vals)
        lines += ["h-axis [" + ", ".join(str(v) for v in xs) + "]", f"v-axis {_mq(y)} 0 --> {_g(top)}"]
        for name, pts in groups.items():
            d = dict(pts)
            lines.append(f"{kind} {_mq(name or y)} [" + ", ".join(_g(d.get(v)) for v in xs) + "]")
    if len(groups) > 1:
        lines.append("legend right")
    lines.append("@endchart")
    return "\n".join(lines) + "\n"


def build_d2(chart, rows, x, y, series, title):
    """D2 has no data charts; it draws node-and-edge diagrams, so only network and tree shapes are built here.
    network: --x source, --series target, --y weight (edge label). tree/dendrogram: --x child, --series parent."""
    if chart not in ("network", "tree", "dendrogram"):
        raise ValueError(f"d2 draws diagrams, not data charts: no recipe for '{chart}' (network, tree, dendrogram)")
    if not series:
        raise ValueError(f"{chart} needs --series (target or parent column)")
    t = title or f"{x} to {series}"
    lines = [f"# {t}", "direction: " + ("down" if chart != "network" else "right")]
    for r in rows:
        a, b = str(r[x]).strip(), str(r[series]).strip()
        if not a or not b:
            continue
        w = _num(r[y]) if y else None
        if chart == "network":
            lines.append(f"{_d2id(a)} -> {_d2id(b)}" + (f": {_g(w)}" if w is not None else ""))
        else:
            lines.append(f"{_d2id(b)} -> {_d2id(a)}" + (f": {_g(w)}" if w is not None and chart == "dendrogram" else ""))
    return "\n".join(lines) + "\n"


def _d2id(s):
    return s if re.fullmatch(r"[A-Za-z0-9_]+", s) else '"' + s.replace('"', "'") + '"'


def build_observable_plot(chart, rows, x, y, series, title):
    """Observable Plot 0.6 marks as a JS snippet (data inline); --html wraps it in a page with the UMD build."""
    groups = _series_split(rows, x, y, series)
    data = [{"x": px, "y": py, **({"s": name} if series else {})} for name, pts in groups.items() for px, py in pts]
    for d in data:
        if _num(d["x"]) is not None and not _is_time(d["x"]):
            d["x"] = _num(d["x"])
    if series and all(_num(d["s"]) is not None for d in data):
        for d in data:
            d["s"] = _num(d["s"])  # a numeric series column (bubble size) stays a number
    xt = all(_is_time(d["x"]) for d in data)
    if xt:
        for d in data:
            d["x"] = f"__DATE__{d['x']}"
    s = ', stroke: "s"' if series else ""
    f = ', fill: "s"' if series else ""
    t = title or f"{y} by {x}"
    opts = {"line": f'Plot.lineY(data, {{x: "x", y: "y"{s}}})', "multi-line": f'Plot.lineY(data, {{x: "x", y: "y"{s}}})',
            "sparkline": f'Plot.lineY(data, {{x: "x", y: "y"{s}}})', "step": f'Plot.lineY(data, {{x: "x", y: "y", curve: "step-after"{s}}})',
            "connected-scatter": f'Plot.lineY(data, {{x: "x", y: "y", marker: true{s}}})',
            "area": f'Plot.areaY(data, {{x: "x", y: "y"{f}}})', "stacked-area": f'Plot.areaY(data, {{x: "x", y: "y"{f}}})',
            "column": f'Plot.barY(data, {{x: "x", y: "y"{f}}})', "stacked-bar": f'Plot.barY(data, {{x: "x", y: "y"{f}}})',
            "bar": f'Plot.barX(data, {{y: "x", x: "y", sort: {{y: "-x"}}{f}}})',
            "grouped-bar": 'Plot.barY(data, {x: "s", y: "y", fill: "s", fx: "x"})',
            "stacked-bar-100": 'Plot.barY(data, Plot.stackY({offset: "normalize"}, {x: "x", y: "y", fill: "s"}))',
            "diverging-bar": 'Plot.barX(data, {y: "x", x: "y", fill: d => d.y < 0 ? "#c0392b" : "#2a78d6", sort: {y: "x"}})',
            "lollipop": f'Plot.ruleX(data, {{x: "x", y: "y"}}), Plot.dot(data, {{x: "x", y: "y", fill: "currentColor"}})',
            "dot-plot": f'Plot.dot(data, {{x: "y", y: "x", fill: "currentColor", sort: {{y: "-x"}}}})',
            "scatter": f'Plot.dot(data, {{x: "x", y: "y"{s}}})', "bubble": 'Plot.dot(data, {x: "x", y: "y", r: "s"})',
            "strip": f'Plot.tickX(data, {{x: "y", y: "x"}})', "beeswarm": 'Plot.dot(data, Plot.dodgeY({x: "y", fill: "currentColor"}))',
            "boxplot": 'Plot.boxY(data, {x: "x", y: "y"})', "histogram": 'Plot.rectY(data, Plot.binX({y: "count"}, {x: "y"}))',
            "heatmap": 'Plot.cell(data, {x: "x", y: "s", fill: "y"}), Plot.text(data, {x: "x", y: "s", text: "y", fill: "white"})',
            "correlogram": 'Plot.cell(data, {x: "x", y: "s", fill: "y"})', "adjacency-matrix": 'Plot.cell(data, {x: "x", y: "s", fill: "y"})',
            "calendar-heatmap": 'Plot.cell(data, {x: d => d3.utcWeek.count(d3.utcYear(d.x), d.x), y: d => d.x.getUTCDay(), fill: "y"})',
            "waffle": f'Plot.waffleY(data, {{x: "x", y: "y"{f}}})', "small-multiples": 'Plot.barY(data, {x: "x", y: "y", fx: "s"})',
            "density-2d": 'Plot.density(data, {x: "x", y: "y"}), Plot.dot(data, {x: "x", y: "y", r: 1})',
            "hexbin": 'Plot.dot(data, Plot.hexbin({r: "count"}, {x: "x", y: "y"}))',
            "slope": 'Plot.lineY(data, {x: "x", y: "y", stroke: "s", marker: true}), Plot.text(data, Plot.selectLast({x: "x", y: "y", z: "s", text: "s", textAnchor: "start", dx: 6}))',
            "choropleth": None}
    if _Y2:
        y2 = {r[x]: _num(r[_Y2]) for r in rows}
        for d in data:
            d["y2"] = y2.get(d["x"] if not xt else str(d["x"]).replace("__DATE__", ""))
        opts["range-band"] = 'Plot.areaY(data, {x: "x", y1: "y", y2: "y2", fillOpacity: 0.3}), Plot.lineY(data, {x: "x", y: "y"}), Plot.lineY(data, {x: "x", y: "y2"})'
        opts["timeline"] = 'Plot.barX(data, {y: "x", x1: "y", x2: "y2"})'
        opts["dumbbell"] = 'Plot.link(data, {x1: "y", x2: "y2", y: "x"}), Plot.dot(data, {x: "y", y: "x", fill: "#2a78d6"}), Plot.dot(data, {x: "y2", y: "x", fill: "#e34948"})'
    mark = opts.get(chart)
    if not mark:
        raise ValueError(f"observable-plot has no recipe for '{chart}' (cw.py show {chart} --section build; range-band, timeline and dumbbell need --y2)")
    if chart in ("grouped-bar", "stacked-bar-100", "small-multiples", "heatmap", "correlogram", "adjacency-matrix", "bubble", "slope") and not series:
        raise ValueError(f"{chart} needs --series")
    color = ', color: {legend: true' + (', scheme: "blues"' if chart in ("heatmap", "correlogram", "adjacency-matrix", "calendar-heatmap") else "") + "}" if (series or chart in ("heatmap", "calendar-heatmap")) else ""
    yzero = ', y: {grid: true, label: ' + json.dumps(y) + (', zero: true' if chart in ("column", "stacked-bar", "grouped-bar", "lollipop", "area", "stacked-area") else "") + "}"
    xlab = ', x: {label: ' + json.dumps(x) + "}"
    if chart in ("bar", "dot-plot", "diverging-bar", "strip"):
        yzero, xlab = ', y: {label: null}', ', x: {grid: true, label: ' + json.dumps(y) + ', zero: true}'
    js = json.dumps(data, ensure_ascii=False)
    js = re.sub(r'"__DATE__([^"]+)"', r'new Date("\1")', js)
    marks = ("[Plot.ruleY([0]), " if chart in ("line", "multi-line", "step", "connected-scatter", "column", "stacked-bar", "grouped-bar", "lollipop", "area", "stacked-area", "histogram", "waffle", "small-multiples") else "[") + mark + "]"
    return (f"const data = {js};\n"
            f"const chart = Plot.plot({{title: {json.dumps(t)}, width: 720, height: 400, marginLeft: 60{xlab}{yzero}{color}, marks: {marks}}});\n")


def build_gsheets(chart, rows, x, y, series, title):
    """Google Sheets API: the data as a values grid plus a spreadsheets.batchUpdate addChart request (sheetId 0).
    Write the values with spreadsheets.values.update on A1, then send the requests with batchUpdate."""
    basic = {"bar": ("BAR", "NOT_STACKED"), "column": ("COLUMN", "NOT_STACKED"), "grouped-bar": ("COLUMN", "NOT_STACKED"),
             "stacked-bar": ("COLUMN", "STACKED"), "stacked-bar-100": ("COLUMN", "PERCENT_STACKED"), "line": ("LINE", "NOT_STACKED"),
             "multi-line": ("LINE", "NOT_STACKED"), "area": ("AREA", "NOT_STACKED"), "stacked-area": ("AREA", "STACKED"),
             "step": ("STEPPED_AREA", "NOT_STACKED"), "scatter": ("SCATTER", "NOT_STACKED")}
    if chart not in basic and chart not in ("pie", "donut"):
        raise ValueError(f"gsheets has no builder for '{chart}' (kb/targets/gsheets.md lists the other EmbeddedChart specs to write by hand)")
    groups = _series_split(rows, x, y, series)
    xs = list(dict.fromkeys(r[x] for r in rows))
    names = [n or y for n in groups]
    values = [[x] + names] + [[v] + [dict(pts).get(v) for pts in groups.values()] for v in xs]
    n, m = len(xs), len(names)
    t = title or f"{y} by {x}"

    def rng(col):
        return {"sourceRange": {"sources": [{"sheetId": 0, "startRowIndex": 0, "endRowIndex": n + 1, "startColumnIndex": col, "endColumnIndex": col + 1}]}}

    if chart in ("pie", "donut"):
        spec = {"title": t, "pieChart": {"legendPosition": "LABELED_LEGEND", "domain": rng(0), "series": rng(1), **({"pieHole": 0.5} if chart == "donut" else {})}}
    else:
        ct, st = basic[chart]
        spec = {"title": t, "basicChart": {"chartType": ct, "stackedType": st, "legendPosition": "BOTTOM_LEGEND" if m > 1 else "NO_LEGEND", "headerCount": 1,
                                           "axis": [{"position": "BOTTOM_AXIS", "title": x}, {"position": "LEFT_AXIS", "title": y}],
                                           "domains": [{"domain": rng(0)}], "series": [{"series": rng(i + 1), "targetAxis": "LEFT_AXIS"} for i in range(m)]}}
    req = {"addChart": {"chart": {"spec": spec, "position": {"overlayPosition": {"anchorCell": {"sheetId": 0, "rowIndex": 0, "columnIndex": m + 2}, "widthPixels": 720, "heightPixels": 400}}}}}
    return json.dumps({"range": "A1", "values": values, "requests": [req]}, indent=1, ensure_ascii=False) + "\n"


def build_docx(chart, rows, x, y, series, title, out, data_path):
    """A python-docx script: renders the Vega-Lite spec to PNG in memory (vl_convert) and writes a Word document
    with a heading, the picture at 6 in wide and a caption. Run it with cw.py render --target docx."""
    spec = build_vega_lite(chart, rows, x, y, series, title, data_path)
    t = title or f"{y} by {x}"
    out = out or "chart.docx"
    lines = ["import io, json", "import vl_convert as vlc", "from docx import Document", "from docx.shared import Inches", "",
             f"spec = {spec.strip()!r}", "png = vlc.vegalite_to_png(spec, scale=2)", "doc = Document()", f"doc.add_heading({t!r}, level=2)",
             "doc.add_picture(io.BytesIO(png), width=Inches(6))",
             f"cap = doc.add_paragraph({('Figure: ' + t + '. ' + chart + ' of ' + y + ' by ' + x + '.')!r}); cap.style = doc.styles['Caption']",
             f"doc.save({out!r}); print('wrote', {out!r})"]
    return "\n".join(lines) + "\n"


HTML_PLOT = """<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script src="https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6"></script>
<style>body{{font-family:system-ui,sans-serif;margin:16px}}</style></head>
<body><div id="chart" role="img" aria-label="{title}"></div>
<script>{spec}
document.getElementById('chart').append(chart);</script></body></html>
"""


HTML_ECHARTS = """<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@6/dist/echarts.min.js"></script></head>
<body><div id="chart" style="max-width:900px;height:420px" role="img" aria-label="{title}"></div>
<script>const chart = echarts.init(document.getElementById('chart')); chart.setOption({spec}); window.addEventListener('resize', () => chart.resize());</script></body></html>
"""

HTML_VL = """<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/vega@6"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@6"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@7"></script>
<style>body{{font-family:system-ui,sans-serif;margin:16px}}#vis{{width:100%;max-width:900px}}</style></head>
<body><div id="vis"></div>
<script>vegaEmbed('#vis', {spec}, {{actions: false}});</script></body></html>
"""
HTML_PLOTLY = """<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<script src="https://cdn.plot.ly/plotly-4.1.1.min.js" charset="utf-8"></script></head>
<body><div id="chart" style="max-width:900px;height:420px"></div>
<script>const fig = {spec}; Plotly.newPlot('chart', fig.data, fig.layout, {{responsive: true, displaylogo: false}});</script></body></html>
"""
HTML_CHARTJS = """<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script></head>
<body><div style="max-width:900px"><canvas id="chart" role="img" aria-label="{title}"></canvas></div>
<script>new Chart(document.getElementById('chart'), {spec});</script></body></html>
"""
HTML_WRAPPERS = {"vega-lite": HTML_VL, "plotly": HTML_PLOTLY, "chartjs": HTML_CHARTJS, "echarts": HTML_ECHARTS, "observable-plot": HTML_PLOT}


def cmd_build(a):
    global _AGG, _Y2
    _AGG = a.agg
    _Y2 = a.y2
    _FLAGS.clear()
    _FLAGS.update(a.flag or [])
    cols, rows = read_csv(a.data)
    for c in (a.x, a.y, a.series, a.y2):
        if c and c not in cols:
            print(f"column '{c}' not in {cols}")
            return 1
    t = a.target
    if t == "mermaid":
        text = build_mermaid(a.chart, rows, a.x, a.y, a.series, a.title)
    elif t == "vega-lite":
        text = build_vega_lite(a.chart, rows, a.x, a.y, a.series, a.title, a.data)
    elif t == "plotly":
        text = build_plotly(a.chart, rows, a.x, a.y, a.series, a.title)
    elif t == "chartjs":
        text = build_chartjs(a.chart, rows, a.x, a.y, a.series, a.title)
    elif t == "matplotlib":
        text = build_matplotlib(a.chart, rows, a.x, a.y, a.series, a.title, a.png)
    elif t == "terminal":
        text = build_terminal(a.chart, rows, a.x, a.y, a.series, a.title)
    elif t == "echarts":
        text = build_echarts(a.chart, rows, a.x, a.y, a.series, a.title)
    elif t == "pptx":
        text = build_pptx(a.chart, rows, a.x, a.y, a.series, a.title, a.png)
    elif t == "xlsx":
        text = build_xlsx(a.chart, rows, a.x, a.y, a.series, a.title, a.png)
    elif t == "quickchart":
        text = build_quickchart(a.chart, rows, a.x, a.y, a.series, a.title)
    elif t == "plantuml":
        text = build_plantuml(a.chart, rows, a.x, a.y, a.series, a.title)
    elif t == "d2":
        text = build_d2(a.chart, rows, a.x, a.y, a.series, a.title)
    elif t == "observable-plot":
        text = build_observable_plot(a.chart, rows, a.x, a.y, a.series, a.title)
    elif t == "gsheets":
        text = build_gsheets(a.chart, rows, a.x, a.y, a.series, a.title)
    elif t == "docx":
        text = build_docx(a.chart, rows, a.x, a.y, a.series, a.title, a.png, a.data)
    elif t == "gdocs":
        print("gdocs has no builder: build a quickchart URL or a vega-lite PNG and follow kb/targets/gdocs.md")
        return 1
    else:
        print(f"unknown target '{t}' (mermaid, vega-lite, plotly, chartjs, matplotlib, terminal, echarts, pptx, xlsx, quickchart, plantuml, d2, observable-plot, gsheets, docx)")
        return 1
    if a.html:
        tpl = HTML_WRAPPERS.get(t)
        if not tpl:
            print("--html applies to vega-lite, plotly, chartjs, echarts, observable-plot")
            return 1
        text = tpl.format(title=a.title or f"{a.y} by {a.x}", spec=text.strip())
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"wrote {a.out} ({len(text)} chars)")
    else:
        sys.stdout.write(text)


# ---------------------------------------------------------------- render
def _which(*names):
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return None


def cmd_render(a):
    src, out = Path(a.infile), Path(a.out)
    ext = out.suffix.lower().lstrip(".")
    if a.target == "vega-lite":
        try:
            import vl_convert as vlc  # type: ignore
        except ImportError:
            print("vl_convert missing: pip install vl-convert-python")
            return 1
        spec = src.read_text(encoding="utf-8")
        if ext == "svg":
            out.write_text(vlc.vegalite_to_svg(spec), encoding="utf-8")
        elif ext == "png":
            out.write_bytes(vlc.vegalite_to_png(spec, scale=a.scale))
        elif ext == "pdf":
            out.write_bytes(vlc.vegalite_to_pdf(spec))
        elif ext == "html":
            out.write_text(HTML_VL.format(title=out.stem, spec=spec.strip()), encoding="utf-8")
        else:
            print("vega-lite renders svg, png, pdf, html")
            return 1
    elif a.target == "mermaid":
        text = src.read_text(encoding="utf-8")
        m = re.search(r"```mermaid\n(.*?)```", text, re.S)
        if m:
            tmp = src.with_suffix(".mmd")
            tmp.write_text(m.group(1), encoding="utf-8")
            src = tmp
        mmdc = _which("mmdc", "mmdc.cmd")
        npx = _which("npx", "npx.cmd")
        if mmdc:
            cmd = [mmdc]
        elif npx:
            cmd = [npx, "--yes", "-p", "@mermaid-js/mermaid-cli", "mmdc"]
        else:
            print("no mmdc and no npx: npm i -g @mermaid-js/mermaid-cli")
            return 1
        r = subprocess.run(cmd + ["-i", str(src), "-o", str(out), "-b", "white"], capture_output=True, text=True)
        if m and src.exists():
            src.unlink()  # the extracted block, not the user's file
        if r.returncode:
            print(r.stderr.strip()[-800:])
            return 1
    elif a.target in ("matplotlib", "pptx", "xlsx", "docx"):
        r = subprocess.run([sys.executable, str(src)], capture_output=True, text=True, cwd=str(out.parent or "."))
        if r.returncode:
            print(r.stderr.strip()[-800:])
            return 1
    elif a.target in ("plotly", "chartjs", "echarts", "observable-plot"):
        out.write_text(HTML_WRAPPERS[a.target].format(title=out.stem, spec=src.read_text(encoding="utf-8").strip()), encoding="utf-8")
    elif a.target == "d2":
        d2 = _which("d2", "d2.exe")
        if not d2:
            print("no d2 binary: https://d2lang.com/tour/install, or paste the .d2 into https://play.d2lang.com")
            return 1
        r = subprocess.run([d2, str(src), str(out)], capture_output=True, text=True)
        if r.returncode:
            print(r.stderr.strip()[-800:])
            return 1
    elif a.target == "plantuml":
        pu = _which("plantuml", "plantuml.cmd")
        if not pu:
            import base64, zlib
            raw = src.read_text(encoding="utf-8").encode("utf-8")
            url = "https://kroki.io/plantuml/" + (ext or "svg") + "/" + base64.urlsafe_b64encode(zlib.compress(raw, 9)).decode()
            print(f"no plantuml on PATH; render via Kroki: {url}")
            return 1
        r = subprocess.run([pu, f"-t{ext}", "-o", str(out.parent.resolve()), str(src)], capture_output=True, text=True)
        if r.returncode:
            print(r.stderr.strip()[-800:])
            return 1
        made = src.with_suffix(f".{ext}")
        if made.exists() and made != out:
            made.replace(out)
    else:
        print("render targets: vega-lite, mermaid, matplotlib, pptx, xlsx, docx, plotly, chartjs, echarts, observable-plot, d2, plantuml")
        return 1
    if out.exists():
        print(f"wrote {out} ({out.stat().st_size} bytes)")
    else:
        print(f"render produced no file at {out}")
        return 1


def cmd_doctor(a):
    info = {"python": sys.version.split()[0], "platform": sys.platform, "plugin_root": str(ROOT)}
    for mod in ("vl_convert", "matplotlib", "plotly", "altair", "pptx", "openpyxl"):
        try:
            m = __import__(mod)
            info[mod] = getattr(m, "__version__", "present")
        except Exception:
            info[mod] = None
    info["mmdc"] = _which("mmdc", "mmdc.cmd")
    info["node"] = _which("node")
    info["npx"] = _which("npx", "npx.cmd")
    info["kb_charts"] = len(list(CHARTS.glob("*.md")))
    info["kb_targets"] = len(list(TARGETS.glob("*.md")))
    info["advice"] = []
    if not info["vl_convert"]:
        info["advice"].append("pip install vl-convert-python  (Vega-Lite -> PNG/SVG without a browser)")
    if not info["mmdc"] and not info["npx"]:
        info["advice"].append("install Node, then npm i -g @mermaid-js/mermaid-cli  (only needed to rasterize Mermaid)")
    if not info["matplotlib"]:
        info["advice"].append("pip install matplotlib  (static charts; optional)")
    print(json.dumps(info, indent=1))


# ---------------------------------------------------------------- authoring
CHART_STUB = """---
name: {name}
slug: {slug}
aliases: []
family: {family}
also: []
question: TODO one line, the question this chart answers
shapes: [{shapes}]
goals: [TODO]
max_series: 0
max_categories: 0
evidence: medium
popularity: niche
status: experimental
support:
{support}
added: {today}
last_verified: {today}
sources: []
---

# {name}

## When to use

- TODO

## When not to use

- TODO

## Substitutes

- TODO

## Evidence

- TODO (cite; say how strong)

## Accessibility

- TODO

## Build

{build}## Notes

- {today}: created by `cw.py new-chart`.
"""


def cmd_new_chart(a):
    p = CHARTS / f"{a.slug}.md"
    if p.exists() and not a.force:
        print(f"{p} exists (use --force)")
        return 1
    tg = list(targets().keys()) or ["mermaid", "vega-lite", "plotly", "chartjs", "matplotlib"]
    support = "\n".join(f"  {t}: none" for t in tg)
    build = "".join(f"### {t}\n\nTODO\n\n" for t in tg)
    shapes = ", ".join(f'"{s}"' for s in (a.shapes or ["n,q"]))
    p.write_text(CHART_STUB.format(name=a.name, slug=a.slug, family=a.family, shapes=shapes, support=support, build=build, today=TODAY), encoding="utf-8")
    print(f"wrote {p}; fill the TODOs, then cw.py validate && cw.py index")


TARGET_STUB = """---
name: {name}
slug: {slug}
kind: {kind}
renders_in: []
version_checked: "TODO"
last_verified: {today}
renderer: none
sources: []
---

# {name}

## What it can draw

| chart | support | note |
|---|---|---|
| TODO | native | |

## Syntax essentials

TODO

## Limits

TODO

## Render

TODO

## Notes

- {today}: created by `cw.py new-target`. Add a `{slug}:` line to every chart's `support:` map (cw.py validate lists the gaps).
"""


def cmd_new_target(a):
    p = TARGETS / f"{a.slug}.md"
    if p.exists() and not a.force:
        print(f"{p} exists (use --force)")
        return 1
    p.write_text(TARGET_STUB.format(name=a.name, slug=a.slug, kind=a.kind, today=TODAY), encoding="utf-8")
    print(f"wrote {p}")


def cmd_note(a):
    p = CHARTS / f"{a.slug}.md"
    if not p.exists():
        p = TARGETS / f"{a.slug}.md"
    if not p.exists():
        print(f"no chart or target '{a.slug}'")
        return 1
    text = p.read_text(encoding="utf-8")
    entry = f"- {TODAY}: {a.text.strip()}"
    if "## Notes" in text:
        text = text.rstrip("\n") + "\n" + entry + "\n"
    else:
        text = text.rstrip("\n") + "\n\n## Notes\n\n" + entry + "\n"
    p.write_text(text, encoding="utf-8")
    print(f"noted in {p.name}: {entry}")


def cmd_tested(a):
    """Record that a target was tested on a platform: appends to `tested:` in the target frontmatter and a dated note."""
    p = TARGETS / f"{a.slug}.md"
    if not p.exists():
        print(f"no target '{a.slug}'")
        return 1
    text = p.read_text(encoding="utf-8")
    entry = f"{a.platform} {TODAY}: {a.text.strip()}"
    if re.search(r"^tested: untested\s*$", text, re.M):
        text = re.sub(r"^tested: untested\s*$", f"tested:\n  - {entry}", text, count=1, flags=re.M)
    elif re.search(r"^tested:\s*$", text, re.M):
        text = re.sub(r"^tested:\s*$", f"tested:\n  - {entry}", text, count=1, flags=re.M)
    else:
        print(f"{p.name} has no tested: block; add one by hand")
        return 1
    text = text.rstrip("\n") + f"\n- {TODAY}: tested on {a.platform}: {a.text.strip()}\n"
    p.write_text(text, encoding="utf-8")
    print(f"recorded in {p.name}: {entry}; run cw.py index")


def cmd_targets(a):
    for slug, t in targets().items():
        tested = t.get("tested")
        flag = "untested" if tested in (None, "untested", []) else f"tested x{len(tested) if isinstance(tested, list) else 1}"
        print(f"{slug:16} {str(t.get('kind')):9} {flag:10} {t.get('name')}  [{t.get('renderer')}]")


# ---------------------------------------------------------------- main
def _hoist_globals(argv):
    """Accept --json and --strict after the subcommand too (cw.py pick ... --json), by moving them to the front."""
    argv = list(argv)
    front = [f for f in ("--json", "--strict") if f in argv]
    return front + [a for a in argv if a not in ("--json", "--strict")]


def main(argv=None):
    global STRICT
    for stream in (sys.stdout, sys.stderr):  # Unicode sparklines on a cp1252 Windows console
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="cw.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true", help="exit non-zero on problems")
    ap.add_argument("--json", action="store_true")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("index").set_defaults(fn=cmd_index)
    sp.add_parser("validate").set_defaults(fn=cmd_validate)
    p = sp.add_parser("list"); p.add_argument("--family"); p.add_argument("--target"); p.set_defaults(fn=cmd_list)
    p = sp.add_parser("show"); p.add_argument("slug"); p.add_argument("--section", nargs="*"); p.add_argument("--target"); p.set_defaults(fn=cmd_show)
    p = sp.add_parser("pick"); p.add_argument("--question", default=""); p.add_argument("--shape"); p.add_argument("--series", type=int)
    p.add_argument("--categories", type=int); p.add_argument("--target"); p.add_argument("--top", type=int, default=3); p.set_defaults(fn=cmd_pick)
    p = sp.add_parser("data"); p.add_argument("data"); p.set_defaults(fn=cmd_data)
    p = sp.add_parser("build"); p.add_argument("--chart", required=True); p.add_argument("--target", required=True); p.add_argument("--data", required=True)
    p.add_argument("--x", required=True); p.add_argument("--y", required=True); p.add_argument("--series"); p.add_argument("--y2", help="second numeric column: bullet target, range-band upper bound"); p.add_argument("--title")
    p.add_argument("--out"); p.add_argument("--png", help="matplotlib/pptx/xlsx/docx: the file the generated script writes (chart.png, chart.pptx, chart.xlsx, chart.docx)")
    p.add_argument("--html", action="store_true", help="wrap a web spec in a standalone page")
    p.add_argument("--flag", nargs="*", help="showData, dataByUrl, container, namedSeries")
    p.add_argument("--agg", default="sum", choices=["sum", "mean", "none"], help="how duplicate x values within a series combine (default sum)"); p.set_defaults(fn=cmd_build)
    p = sp.add_parser("render"); p.add_argument("--target", required=True); p.add_argument("--in", dest="infile", required=True); p.add_argument("--out", required=True)
    p.add_argument("--scale", type=float, default=2.0); p.set_defaults(fn=cmd_render)
    p = sp.add_parser("new-chart"); p.add_argument("slug"); p.add_argument("--name", required=True); p.add_argument("--family", required=True, choices=FAMILIES)
    p.add_argument("--shapes", nargs="*"); p.add_argument("--force", action="store_true"); p.set_defaults(fn=cmd_new_chart)
    p = sp.add_parser("new-target"); p.add_argument("slug"); p.add_argument("--name", required=True)
    p.add_argument("--kind", required=True, choices=["markdown", "web", "image", "office", "terminal"]); p.add_argument("--force", action="store_true"); p.set_defaults(fn=cmd_new_target)
    p = sp.add_parser("note"); p.add_argument("slug"); p.add_argument("text"); p.set_defaults(fn=cmd_note)
    sp.add_parser("doctor").set_defaults(fn=cmd_doctor)
    sp.add_parser("targets").set_defaults(fn=cmd_targets)
    p = sp.add_parser("tested", help="record a platform test for a target"); p.add_argument("slug"); p.add_argument("--platform", required=True, help="Windows, macOS, Linux, or a host name"); p.add_argument("text"); p.set_defaults(fn=cmd_tested)
    a = ap.parse_args(_hoist_globals(argv if argv is not None else sys.argv[1:]))
    STRICT = a.strict
    try:
        rc = a.fn(a) or 0
    except (ValueError, FileNotFoundError) as e:
        print(f"note: {e}")
        rc = 1
    return rc if STRICT else 0


if __name__ == "__main__":
    sys.exit(main())
