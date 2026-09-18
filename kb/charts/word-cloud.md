---
name: Word cloud
slug: word-cloud
aliases: [tag cloud, wordle, text cloud, keyword cloud]
family: magnitude
also: [ranking]
question: Which words or terms appear most often in a body of text?
shapes: ["text", "n,q"]
goals: [magnitude, word cloud, frequent words, keywords, tags, text, most common terms, survey responses, themes, buzzwords]
max_series: 0
max_categories: 100
evidence: low
popularity: declining
status: stable
support:
  mermaid: none
  vega-lite: approx
  plotly: image
  chartjs: approx
  matplotlib: native
  terminal: none
  echarts: approx
  pptx: image
  quickchart: none
added: 2026-09-17
last_verified: 2026-09-17
sources: [https://datavizcatalogue.com/methods/wordcloud.html, https://www.data-to-viz.com/graph/wordcloud.html, https://vega.github.io/vega/examples/word-cloud/, https://github.com/sgratzl/chartjs-chart-wordcloud, https://github.com/amueller/word_cloud, https://www.datawrapper.de/blog/chart-types-guide]
---

# Word cloud

## When to use

- Decoration or a quick impression of a text's vocabulary: a poster, a slide opener, a workshop summary of sticky notes, where the exact frequencies do not matter and nobody will make a decision from it.
- The reader wants to spot a few dominant terms and the tone of a corpus at a glance, and a ranked list would look too formal for the setting.
- Free-text survey answers when the audience expects a word cloud and a `bar` of the top terms sits next to it with the numbers.
- Excels at: engagement and recall (Bateman et al. 2010 on embellishment), not at conveying quantities.

## When not to use

- Any question about how much more often one term appears than another: font size is a poor encoding, long words look bigger, and placement is random; a `bar` of the top 15 to 20 terms is the honest chart (Data to Viz caveat; selection rules item 4 list word clouds among charts to redesign).
- Comparing two texts or two groups: two clouds cannot be compared; use a `dumbbell` or `diverging-bar` of term frequencies.
- Terms that are phrases, or words whose meaning depends on context (negations, "not good"): the cloud strips context; use a table of phrases with counts.
- Serious analytical or executive audiences: guides from Datawrapper to the Data Visualisation Catalogue mark word clouds as discouraged; the popularity here is `declining`.
- Colour that means nothing: random hues suggest categories that do not exist.

## Substitutes

- The default: `bar` (horizontal) of the top terms, sorted, with counts.
- Many terms with a long tail: `lollipop` or `dot-plot` of the top 30.
- Terms by group or over time: `heatmap` (term by period) or `small-multiples` of bars.
- Two texts compared: `diverging-bar` (term frequency difference) or `dumbbell`.
- Share of themes after coding the responses: `stacked-bar-100` or `waffle`.

## Evidence

- Rated `low`: no study shows word clouds convey frequency accurately, and several usability critiques (Hearst and Rosner 2008 on tag clouds) show that longer words and central placement bias the reading. Font size is an area-like encoding, ranked below length and position (Cleveland and McGill 1984).
- Bateman et al. 2010: embellished charts were recalled better with no loss of immediate accuracy, which is the strongest argument for a word cloud as a memorable poster next to a bar of the same data.
- Practitioner consensus (Datawrapper, Data to Viz, Data Visualisation Catalogue) is to prefer a ranked bar; this file exists so the substitute is offered rather than the request refused.

## Accessibility

- Provide the ranked table of terms and counts; the cloud itself is not readable by screen readers and rotated words are hard for everyone.
- No rotated words, one or two hues only (colour by a real category if any), minimum font size about 10 px at the final scale, 4.5:1 contrast for the smallest words.
- Text alternative: "Word cloud of <corpus>; most frequent terms <A> (<n>), <B> (<n>), <C> (<n>)." That sentence is usually the better deliverable.
- Remove stop words and state the cleaning done (stemming, case folding) in the caption.

## Build

Not supported by `cw.py build`; hand-written. Input is either raw text (count the terms first, drop stop words) or `term,count` rows. Always build the `bar` of the top terms alongside.

### vega-lite

Vega-Lite has no word cloud; full Vega has the `wordcloud` transform (the `word-cloud` example: `countpattern` on text, `wordcloud` transform with `size` from count, `rotate` 0, then a `text` mark). Render without a browser through vl-convert's `vega_to_png`. The composition lives in Vega, not Vega-Lite, hence `approx`.

### chartjs

`chartjs-chart-wordcloud` plugin: `type: "wordCloud"`, `data: {labels: terms, datasets: [{data: counts}]}`, options `rotate: 0`, `minRotation: 0`, `fit: true`, `color: "#0072B2"`. Community plugin (sgratzl), canvas output, so add `aria-label` and the table in the fallback content.

### matplotlib

`pip install wordcloud`, then `from wordcloud import WordCloud, STOPWORDS; wc = WordCloud(width=1200, height=600, background_color="white", stopwords=STOPWORDS, prefer_horizontal=1.0, colormap="Blues", max_words=80).generate_from_frequencies(counts); ax.imshow(wc, interpolation="bilinear"); ax.set_axis_off()`. `generate(text)` does the counting for raw text. Render with `cw.py render --target matplotlib --in cloud.py --out cloud.png`.

### echarts

Hand-written: echarts-wordcloud extension. See `kb/targets/echarts.md`.

## Notes

- 2026-09-17: written from the 2026-09-17 taxonomy research. `plotly` is `image`: no word cloud trace, and a scatter-with-text imitation has no layout algorithm; render with the matplotlib route and embed the picture. When a user asks for a word cloud, offer the bar chart first and produce both if they insist.
