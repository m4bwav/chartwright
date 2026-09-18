---
name: Word document (PNG via python-docx)
slug: docx
kind: office
renders_in: [Microsoft Word, LibreOffice Writer, Google Docs (imported .docx), Pages]
version_checked: "python-docx 1.2.0; no native chart API (issue 179 open since 2015); vl-convert-python 1.9 for the PNG"
last_verified: 2026-09-18
renderer: python
tested:
  - Windows 2026-09-18: python-docx script rendered; word/media/image1.png present in the zip; not opened in Word
sources: [https://python-docx.readthedocs.io/en/latest/, https://github.com/python-openxml/python-docx/issues/179]
---

# Word document (PNG via python-docx)

Word has native charts, but python-docx cannot write them, so a chart in a generated .docx is a picture: render at 2x, insert at the text width (6 in on Letter with 1.25 in margins), and caption it. Every chart type is therefore `image` here. When the reader must edit the chart, build it in PowerPoint (`pptx` target) or Excel (`xlsx`) and paste, or hand them the data.

## What it can draw

| chart | support | note |
|---|---|---|
| everything | image | any chart the `vega-lite` or `matplotlib` target renders; `cw.py build --target docx` covers what `vega-lite` builds and writes the picture plus a caption |

## Syntax essentials

```python
import io, json
import vl_convert as vlc
from docx import Document
from docx.shared import Inches
spec = json.load(open("chart.vl.json"))
png = vlc.vegalite_to_png(json.dumps(spec), scale=2)
doc = Document()                       # or Document("existing.docx") to append
doc.add_heading("Sales by region", level=2)
doc.add_picture(io.BytesIO(png), width=Inches(6))
cap = doc.add_paragraph("Figure 1. South leads; East trails at about 60% of it."); cap.style = doc.styles["Caption"]
doc.save("report.docx")
```

- Insert into an existing document at a position: find the paragraph after the claim and use `paragraph.insert_paragraph_before()` then `run.add_picture(...)` on a run in that new paragraph.
- Alt text: python-docx has no API for it; set `docPr.descr` on the inline shape's XML (`inline._inline.docPr.set("descr", text)`) or add the text alternative as the caption.
- The `docx` skill (anthropic-skills:docx) prefers the `docx` npm package; when it is missing, python-docx as above is the fallback, and both need only the PNG.

## Limits

- Not editable in Word; the numbers live outside the document, so keep the source CSV next to the .docx or in an appendix table.
- No preview without Word or LibreOffice; verify by listing `word/media/` in the zip and reading back `doc.inline_shapes`.
- `pip install python-docx vl-convert-python` to run the generated script.

## Render

- `cw.py build --chart bar --target docx --data sales.csv --x region --y sales --out chart.py --png report.docx` then `cw.py render --target docx --in chart.py --out report.docx` writes a one-figure document; for a longer document, generate the PNG with `cw.py render --target vega-lite` and place it with the snippet above or through the docx skill.

## Notes

- 2026-09-18: added after a fresh-session test wrote sales-summary.docx (60 KB, one 6 in picture, caption, data table) with python-docx because the docx skill's npm package was absent; the skill's reference now points here for Word destinations.
