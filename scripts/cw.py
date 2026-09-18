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
    trows = [{k: t.get(k) for k in ("slug", "name", "kind", "renders_in", "version_checked", "renderer", "last_verified")}
             for t in tg.values()]
    idx = {"generated": TODAY, "charts": rows, "targets": trows, "families": FAMILIES}
    (KB / "index.json").write_text(json.dumps(idx, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tslugs = list(tg.keys())
    lines = ["# Chart index (generated by `cw.py index`; do not edit)", "",
             f"{len(rows)} chart types, {len(trows)} targets, generated {TODAY}. Read this first; open a chart file only for the section you need (`cw.py show <slug> --section when`).",
             "", "Support: N native, A approximate, I image only, . none. Target columns in order: " + ", ".join(tslugs), "",
             "| slug | family | question | shapes | series/cat cap | evid | pop | " + " ".join(tslugs) + " |",
             "|---|---|---|---|---|---|---|---|"]
    abbr = {"native": "N", "approx": "A", "image": "I", "none": ".", None: "?"}
    for r in rows:
        sup = r.get("support") or {}
        cells = "".join(abbr.get(sup.get(t), "?") for t in tslugs)
        caps = f"{r.get('max_series') or '-'}/{r.get('max_categories') or '-'}"
        lines.append(f"| {r['slug']} | {r['family']} | {r.get('question') or ''} | {' '.join(str(s) for s in (r.get('shapes') or []))} | {caps} | "
                     f"{str(r.get('evidence') or '?')[:1]} | {r.get('popularity') or '?'} | {cells} |")
    lines += ["", "## Families", "", ", ".join(FAMILIES), "", "## Targets", ""]
    for t in trows:
        lines.append(f"- **{t['slug']}** ({t.get('kind')}): {t.get('name')}; renders in {', '.join(t.get('renders_in') or [])}; renderer `{t.get('renderer')}`")
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
        for k in ("name", "slug", "kind", "renderer", "last_verified"):
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
        hits = [g for g in goals if any(g == x or (len(g) > 3 and g in x) for x in cg)]
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
        lines = ["xychart-beta", f"    title {_mq(t)}",
                 "    x-axis [" + ", ".join(_mq(v) for v in xs) + "]", f"    y-axis {_mq(y)}"]
        for name, pts in groups.items():
            d = dict(pts)
            lines.append(f"    {kind} [" + ", ".join(_g(d.get(v)) for v in xs) + "]")
        note = "" if len(groups) == 1 else f"%% xychart has no legend: series in order are {', '.join(groups)}\n"
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


def build_vega_lite(chart, rows, x, y, series, title, data_path):
    if chart not in VL_MARKS:
        raise ValueError(f"vega-lite has no recipe for '{chart}'")
    xk = "temporal" if all(_is_time(r[x]) for r in rows) else ("quantitative" if all(_num(r[x]) is not None for r in rows) else "nominal")
    spec = {"$schema": "https://vega.github.io/schema/vega-lite/v6.json", "title": title or f"{y} by {x}",
            "data": {"url": Path(data_path).name} if a_flag("dataByUrl") else {"values": rows},
            "mark": VL_MARKS[chart], "width": "container" if a_flag("container") else 600, "height": 320, "encoding": {}}
    for r in rows:  # numbers as numbers so Vega-Lite does not treat them as strings
        for k in (x, y, series):
            if k and _num(r.get(k)) is not None and not _is_time(r.get(k)):
                r[k] = _num(r[k])
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
        if xk == "temporal":
            xe["scale"] = {"type": "utc"}  # ISO dates parse as UTC; a local scale shifts them by a day
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


def build_plotly(chart, rows, x, y, series, title):
    groups = _series_split(rows, x, y, series)
    traces = []
    kind = {"line": "scatter", "multi-line": "scatter", "area": "scatter", "stacked-area": "scatter", "scatter": "scatter",
            "bar": "bar", "column": "bar", "grouped-bar": "bar", "stacked-bar": "bar", "pie": "pie", "donut": "pie",
            "histogram": "histogram", "boxplot": "box", "heatmap": "heatmap", "bubble": "scatter", "step": "scatter"}.get(chart)
    if not kind:
        raise ValueError(f"plotly has no recipe for '{chart}'")
    layout = {"title": {"text": title or f"{y} by {x}"}, "xaxis": {"title": {"text": x}}, "yaxis": {"title": {"text": y}},
              "template": "plotly_white", "margin": {"t": 50, "r": 20}}
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
    t = title or f"{y} by {x}"
    lines += [f"ax.set_title({t!r})", "ax.legend()" if series else "", "fig.tight_layout()",
              f"fig.savefig({out!r}); print('wrote', {out!r})"]
    return "\n".join(l for l in lines if l) + "\n"


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
HTML_WRAPPERS = {"vega-lite": HTML_VL, "plotly": HTML_PLOTLY, "chartjs": HTML_CHARTJS}


def cmd_build(a):
    global _AGG
    _AGG = a.agg
    _FLAGS.clear()
    _FLAGS.update(a.flag or [])
    cols, rows = read_csv(a.data)
    for c in (a.x, a.y, a.series):
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
    else:
        print(f"unknown target '{t}' (mermaid, vega-lite, plotly, chartjs, matplotlib)")
        return 1
    if a.html:
        tpl = HTML_WRAPPERS.get(t)
        if not tpl:
            print("--html applies to vega-lite, plotly, chartjs")
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
        if r.returncode:
            print(r.stderr.strip()[-800:])
            return 1
    elif a.target == "matplotlib":
        r = subprocess.run([sys.executable, str(src)], capture_output=True, text=True, cwd=str(out.parent or "."))
        if r.returncode:
            print(r.stderr.strip()[-800:])
            return 1
    elif a.target in ("plotly", "chartjs"):
        out.write_text(HTML_WRAPPERS[a.target].format(title=out.stem, spec=src.read_text(encoding="utf-8").strip()), encoding="utf-8")
    else:
        print("render targets: vega-lite, mermaid, matplotlib, plotly, chartjs")
        return 1
    if out.exists():
        print(f"wrote {out} ({out.stat().st_size} bytes)")
    else:
        print(f"render produced no file at {out}")
        return 1


def cmd_doctor(a):
    info = {"python": sys.version.split()[0], "platform": sys.platform, "plugin_root": str(ROOT)}
    for mod in ("vl_convert", "matplotlib", "plotly", "altair"):
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


def cmd_targets(a):
    for slug, t in targets().items():
        print(f"{slug:12} {str(t.get('kind')):9} {t.get('name')}  [{t.get('renderer')}]")


# ---------------------------------------------------------------- main
def main(argv=None):
    global STRICT
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
    p.add_argument("--x", required=True); p.add_argument("--y", required=True); p.add_argument("--series"); p.add_argument("--title")
    p.add_argument("--out"); p.add_argument("--png", help="matplotlib: image path the generated script writes")
    p.add_argument("--html", action="store_true", help="wrap a web spec in a standalone page")
    p.add_argument("--flag", nargs="*", help="showData, dataByUrl, container")
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
    a = ap.parse_args(argv)
    STRICT = a.strict
    try:
        rc = a.fn(a) or 0
    except (ValueError, FileNotFoundError) as e:
        print(f"note: {e}")
        rc = 1
    return rc if STRICT else 0


if __name__ == "__main__":
    sys.exit(main())
