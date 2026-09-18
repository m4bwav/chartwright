# Evidence behind the rules

The studies and practitioner sources the selection rules rest on, with what each actually showed and how far to trust it. Each chart file's `## Evidence` section points back here by author-year. Research log: `ai-docs/research/`.

## Perception studies

- **Cleveland and McGill 1984**, "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods", JASA 79(387). Ranked elementary perceptual tasks by accuracy: position on a common scale > position on non-aligned scales > length, direction, angle > area > volume, curvature > shading, colour saturation. Basis for "bars and dots beat pies, pies beat bubbles". Strong, replicated.
- **Heer and Bostock 2010**, "Crowdsourcing Graphical Perception", CHI. Replicated Cleveland and McGill on Mechanical Turk; added rectangular area (treemap) and circular area (bubble), both worse than length. Strong.
- **Skau and Kosara 2016**, "Arcs, Angles, or Areas: Individual Data Encodings in Pie and Donut Charts", EuroVis (summary https://eagereyes.org/pie-charts). Pie readers use arc length or area, not angle; donuts read as well as pies; exploded and 3D pies read worst. Practical: pies are acceptable for up to about 5 slices and "is A plus B a majority" questions. Medium-strong.
- **Franconeri, Padilla, Shah, Zacks and Hullman 2021**, "The Science of Visual Data Communication: What Works", Psychological Science in the Public Interest 22(3), https://journals.sagepub.com/doi/10.1177/15291006211051956. Review of the perception literature: viewers extract global statistics and shapes fast but compare subsets slowly, one pair at a time; the layout decides which comparison is easy; annotate and label directly; beware axis truncation, aspect ratio, colour scales, 3D; show uncertainty as distributions or quantile dot plots rather than error bars. Strong (review).
- **Bateman et al. 2010**, "Useful Junk?", CHI. Embellished (Holmes-style) charts were recalled better after a delay with no loss of immediate accuracy. Tufte's data-ink ratio is a heuristic, not a law: remove ink that competes with data, keep embellishment that carries meaning. Medium.
- **Correll and Gleicher 2014** (error bars considered harmful) and **Kay, Kola, Hullman and Munson 2016** (quantile dot plots): bare error bars are misread as hard limits; gradient bands, violins and quantile dot plots are read more accurately. Medium.
- **Cleveland 1993** banking to 45 degrees: choose the aspect ratio so typical line slopes are near 45 degrees. Medium; often ignored, still useful.

## Colour

- **Okabe and Ito 2002/2008**, colour-universal design palette (https://jfly.uni-koeln.de/color/): black, orange #E69F00, sky blue #56B4E9, bluish green #009E73, yellow #F0E442, blue #0072B2, vermilion #D55E00, reddish purple #CC79A7. The safest categorical default for up to 8 classes.
- **Viridis family** (Smith and van der Walt 2015): perceptually uniform, colour-blind-safe sequential ramps (viridis, magma, plasma, cividis).
- **ColorBrewer** (Brewer and Harrower): sequential, diverging and qualitative schemes with a colour-blind-safe filter.
- **WCAG 2.x** 1.4.1 (use of colour), 1.4.3 (text contrast), 1.4.11 (3:1 for graphical objects). Never encode with colour alone.
- The bundled Claude `dataviz` skill ships a validated eight-hue palette and a runnable validator (`validate_palette.js`); when that skill is present, its palette and checks override any palette advice here.

## Practitioner guidance (secondary, widely adopted)

- **Financial Times Visual Vocabulary** (https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary): the nine families and the one-line caveat per chart; the taxonomy this knowledge base uses.
- **Datawrapper blog**: "Which chart type should I use?" (Muth 2025), stacked column advice (2025-02), dual-axis warning, small multiples (2023-2024), log scales. Editorial, well-argued, current.
- **From Data to Viz** (https://www.data-to-viz.com): decision tree from data shape to chart, with a caveat page per chart.
- **Data Visualisation Catalogue** (https://datavizcatalogue.com): the widest list of chart names and functions.
- **Storytelling with Data** (Knaflic): a deliberately small chart set (text, table, heat table, scatter, line, slope, bar variants, waterfall, square area) and the direct-labelling habit.
- **Chartability** (Fizz Studio) and WCAG: accessibility heuristics for charts (text alternative in the "type, what it shows, key finding" pattern; data table alternative; keyboard access).

## How AI systems choose charts (2024-2026)

- **Draco / Draco 2** (Moritz et al. 2019; Yang et al. 2023): visualization design knowledge as soft and hard constraints over Vega-Lite specs, weights learned from perception studies. The closest formal counterpart of `cw.py pick`.
- **CompassQL / Voyager** (Wongsuphasawat et al. 2016-2017): enumerate and rank specs by effectiveness; **LIDA** (Dibia 2023) generates code and self-repairs; **Data Formulator** (Microsoft, v0.7 2026-05) lets the model transform data and pick encodings; **VegaChat** (2026, arXiv 2601.15385) reports 0% visualization errors generating Vega-Lite vs about 30% for code generation.
- Benchmarks: nvBench 2.0 (NeurIPS 2025), VisEval, ChartMimic, Plot2Code, Chart2Code (ACL 2026). Common criteria: chart-type appropriateness for the question, encoding correctness (field types, aggregation), readability (labels, legend, ticks), and spec validity. Lesson for this plugin: generate declarative specs, validate them mechanically, and keep the type decision in a rule table rather than free reasoning.

## Confidence key used in chart files

`high`: replicated perception studies support the chart doing its job. `medium`: one study or consistent practitioner consensus. `low`: convention or a tool's popularity only; the chart file says what would change the verdict.
