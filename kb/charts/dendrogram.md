---
name: Dendrogram
slug: dendrogram
aliases: [cluster tree, hierarchical clustering plot, phylogenetic tree, cluster dendrogram]
family: hierarchy
also: [distribution, relationship]
question: How do items cluster together, and at what distance do the clusters merge?
shapes: ["hier,q", "q+"]
goals: [clustering, cluster, similarity, hierarchical clustering, merge, distance, phylogeny, taxonomy, groups, linkage, dendrogram]
max_series: 0
max_categories: 100
evidence: low
popularity: niche
status: stable
support:
  mermaid: image
  vega-lite: approx
  plotly: approx
  chartjs: none
  matplotlib: approx
  terminal: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html, https://plotly.com/python/dendrogram/, https://seaborn.pydata.org/generated/seaborn.clustermap.html, https://vega.github.io/vega/examples/tree-layout/, https://www.data-to-viz.com/graph/dendrogram.html]
---

# Dendrogram

## When to use

- The output of hierarchical clustering (agglomerative linkage): which items join first, and the height (distance) at which each merge happens.
- Choosing a number of clusters: a horizontal cut through the tree at a chosen height shows the groups, and long vertical gaps show natural splits.
- Phylogenies and taxonomies where branch length carries meaning (evolutionary distance).
- Beside a heatmap (a clustermap): the dendrogram orders rows and columns so the heatmap shows blocks.
- Excels at: turning a distance matrix into a readable picture of nested similarity, with the merge heights as an aligned scale.

## When not to use

- Structure without distances (an org chart): a `tree` is the plain form; the height axis would be meaningless.
- More than about a hundred leaves without truncation: labels overlap; use `truncate_mode` (show the last p merges) or a `heatmap` with cluster colour bars.
- Readers unfamiliar with clustering: the height axis and the linkage method need a caption; a `table` of cluster memberships may serve better.
- Reading horizontal proximity as similarity: leaf order is partly arbitrary (branches can flip), only the merge height is meaningful. Say so.
- Interactive drill-down requirements: it is a static form; Plotly's helper draws lines, not a hierarchy object.

## Substitutes

- No heights: `tree`; sizes instead of distances: `treemap` or `icicle`.
- Pairwise similarity for many items: `heatmap` of the distance matrix (with the dendrogram as its margin).
- Two-dimensional cluster structure: `scatter` of an embedding, coloured by cluster.
- Groups over a threshold only: a `bar` of cluster sizes.

## Evidence

- Merge heights are position on a common scale, the best-read encoding (Cleveland and McGill 1984), which is why the height axis works; the leaf ordering has no perceptual backing and is the main misreading. `low`: convention in statistics and biology (scipy, R `hclust`), no dedicated perception study.
- Franconeri et al. 2021: state the intended comparison (the cut height, the number of clusters) on the chart; readers will otherwise compare adjacent leaves.
- Popularity `niche`: scipy, seaborn clustermap and Plotly's `figure_factory` draw it; general charting libraries and Mermaid do not.

## Accessibility

- Leaf labels horizontal (use a horizontal dendrogram, `orientation="left"`) and a labelled height axis with the linkage method and distance metric in the caption.
- Colour the branches below the cut height per cluster (at most 8 colour-blind-safe hues); above the cut in grey.
- Text alternative: "Dendrogram of <N> items by <metric>, <linkage> linkage; cutting at <h> gives <k> clusters: <cluster 1: members>, ..." Provide the membership table.
- Lines at 2 px and 3:1 contrast; leaf labels in at least the body text size, which is what caps the leaf count.

## Build

### mermaid

No Mermaid dendrogram; a `flowchart` can show the merge order but not the heights. Render with matplotlib and link the image.

### vega-lite

Full Vega only: `stratify` on the merge tree, then `tree` with `"method": "cluster"` and the y position overridden by the merge height (`"formula": "scale('y', datum.height)"`) so branch lengths are meaningful, `treelinks` and `linkpath` with `"orient": "vertical", "shape": "orthogonal"`. Hand-written; the linkage itself is computed in Python or R first. `approx`.

### plotly

Hand-written in Python: `import plotly.figure_factory as ff; fig = ff.create_dendrogram(X, labels=names, orientation="left", color_threshold=h)` runs scipy linkage and draws the lines as scatter traces; `fig.write_html("chart.html", include_plotlyjs="cdn")`. `approx`, a helper rather than a trace type.

### chartjs

Not available. Use a matplotlib image.

### matplotlib

Hand-written: `from scipy.cluster.hierarchy import linkage, dendrogram; Z = linkage(X, method="ward"); dendrogram(Z, labels=names, orientation="left", color_threshold=h, ax=ax); ax.axvline(h, linestyle="--")` (draw the cut); `seaborn.clustermap(df)` when a heatmap should accompany it. Render with `cw.py render --target matplotlib --in chart.py --out chart.png`. `approx`: scipy computes and draws, matplotlib only hosts the axes.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research.
