---
name: Static image via Python (matplotlib and friends)
slug: matplotlib
kind: image
renders_in: [PNG/SVG/PDF files for Word, Google Docs, PowerPoint, Slack, email, LaTeX, any markdown as an image link]
version_checked: "matplotlib 3.11.2 (2026-09-11), seaborn 0.13.2 (2024, flat), plotnine 0.15.8, Altair 6.3.0 + vl-convert 1.9.0.post1, plotly 7.1 + kaleido 1.4.0, bokeh 3.10"
last_verified: 2026-09-17
renderer: python
tested:
  - Windows 2026-09-18: script built and PNG rendered with matplotlib 3.11; inspected
sources: [https://matplotlib.org/stable/users/explain/figure/backends.html, https://matplotlib.org/stable/gallery/index.html, https://seaborn.pydata.org/, https://plotnine.org/, https://github.com/vega/vl-convert]
---

# Static image via Python (matplotlib and friends)

The universal fallback: every host shows a PNG. matplotlib draws anything (the widest type coverage of any tool, including the statistical and scientific charts), seaborn adds statistical defaults, plotnine gives a grammar-of-graphics API. For simple charts prefer Altair plus vl-convert (same Vega-Lite spec as the web target, no browser); use matplotlib when the chart type is outside Vega-Lite or the output needs print-quality control.

## What it can draw

| chart | support | note |
|---|---|---|
| everything in the knowledge base except interactive-only forms | native | line, bar, stacked/grouped, area, stackplot, step, scatter, bubble, hist, hist2d/hexbin, boxplot, violinplot, errorbar, fill_between (bands), pie (donut via wedgeprops), imshow/pcolormesh (heatmap), contour, quiver, stem (lollipop), broken_barh (gantt), polar axes (radar, radial bar), table; seaborn: kdeplot, ecdfplot, stripplot, swarmplot (beeswarm), catplot, pairplot (splom), FacetGrid (small multiples), heatmap, clustermap; plotnine: geom_* including geom_density_ridges via extras |
| treemap, sankey, chord, network, waffle, ridgeline, raincloud, upset | native via add-on | squarify, matplotlib.sankey (basic) or plotly, mpl_chord_diagram, networkx, pywaffle, joypy/ridgeplot, ptitprince, upsetplot |
| choropleth, maps | native via add-on | geopandas + matplotlib, cartopy, or plotly |

## Syntax essentials

```python
import matplotlib
matplotlib.use("Agg")            # headless; set before importing pyplot
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=150)
ax.plot(dates, prices, marker="o", linewidth=2, label="2026")
ax.set_title("Price over time"); ax.set_xlabel("date"); ax.set_ylabel("price")
ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig("chart.png")   # or .svg / .pdf
```

- Clean defaults: hide top/right spines, light y grid, `constrained_layout=True` or `tight_layout()`, `plt.style.use("seaborn-v0_8-whitegrid")` or a `.mplstyle` file for a house style. Colour cycle: `plt.rcParams["axes.prop_cycle"] = plt.cycler(color=[...])` with the Okabe-Ito or the dataviz skill palette.
- Long category labels: horizontal bars (`ax.barh`) beat rotated ticks.
- Dates: pass `datetime` objects, then `ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %Y"))`.
- DPI: 150 to 200 for documents and slides, 300 for print; `scale_factor=2` equivalent. SVG for docs sites and dark mode (`currentColor` tricks need post-processing); PNG for Word, Google Docs and Slack (they reject SVG or rasterise it badly).
- Altair path: `alt.Chart(df).mark_line().encode(x="date:T", y="price:Q").save("chart.png", scale_factor=2)`.

## Limits

- No interactivity. First import on Windows builds a font cache (about 10 s) once.
- `plt.show()` hangs headless sessions; always `savefig`.
- seaborn has had no release since 2024-01; fine, but do not expect new features. plotly static export needs Chrome (kaleido 1.x); bokeh export needs Selenium: avoid both for images.

## Render

- `cw.py build --chart line --target matplotlib --data prices.csv --x date --y price --out chart.py --png chart.png` writes a script; `cw.py render --target matplotlib --in chart.py --out chart.png` runs it with the current Python. `pip install matplotlib` once.
- For anything the builder lacks, write the script by hand from the recipe in the chart's `### matplotlib` section and run it the same way; save the script beside the image so the chart can be regenerated.

## Notes

- 2026-09-17: created from the 2026-09-17 library research.
