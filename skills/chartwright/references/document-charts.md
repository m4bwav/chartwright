# Charts for a document (chartwright Step 2a, full detail)

Read this when the request is "add charts to", "illustrate", "visualize this report", or a document is open and the ask is to enrich it. Rules behind it: `kb/rules/selection.md` §7.

## Procedure

1. Read the document once. List every claim that carries a number or a comparison: grew, fell, more than, share of, correlated, spread, flows to, where, ranks.
2. Keep the claims a reader would want to verify or feel. Drop decoration: a chart per paragraph is noise; two to five per section is typical.
3. For each kept claim write one line: the claim as the chart title, the chart family the verb implies, the data it needs and where that data is (a CSV, a table in the text, numbers in the prose), and the position (right after the claim).
4. Data in prose goes to a small CSV beside the document first (`<topic>.csv`), so the build reads a file and the numbers are auditable. Data already in a CSV is referenced, never retyped.
5. Show the plan as a short list before building when there are more than three charts, then build each with the normal pick and build steps (`CW pick` per claim, `CW build`, render check).
6. Target follows the document: a `.md` in a repo gets Mermaid where the type is native and linked images otherwise; a `.docx` or Google Doc gets PNGs; an HTML page or artifact gets Vega-Lite or ECharts.
7. Each chart keeps the claim's wording as its title and, where the host allows, a one-line caption with the key number. Never change the document's prose beyond inserting the chart and caption.

## Example plan (from `examples/report/quarterly-summary.md`)

- "Revenue grew from 410k to 540k": change over time, metrics.csv, line, after the first paragraph.
- "Churn fell from 3.1% to 1.9%": change over time, metrics.csv, line (own chart, different scale; never a dual axis).
- "Funnel loses most users at activation": stages with drop-off, funnel.csv, funnel (bar in Mermaid, which has no funnel), after the funnel paragraph.
- "Regional revenue North 610k ...": magnitude and ranking, numbers in prose → regional-revenue.csv, sorted bar.

## What not to do

- No chart for a single number (write the number, or a stat tile if the host is a dashboard).
- No dual-axis chart to combine two claims; two charts.
- No chart whose title is a variable name; the title is the claim.
- No inline data pasted into specs when a CSV exists beside the document.
