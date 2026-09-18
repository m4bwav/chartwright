---
name: Google Docs (images via HTML import or Drive upload)
slug: gdocs
kind: office
renders_in: [Google Docs]
version_checked: "Google Drive API v3 HTML-to-Doc conversion; Docs API has no chart resource (checked 2026-09-18)"
last_verified: 2026-09-18
renderer: none
sources: [https://developers.google.com/workspace/docs/api/reference/rest, https://developers.google.com/workspace/drive/api/guides/manage-uploads, https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/charts]
---

# Google Docs (images via HTML import or Drive upload)

Google Docs has no chart API: a chart in a Doc is either an image or an embedded Google Sheets chart. Every chart type is therefore `image` here, and the work is getting the image into the document.

## What it can draw

| chart | support | note |
|---|---|---|
| everything | image | render a PNG (vega-lite or matplotlib target) or use a `quickchart` URL, then embed |
| any chart that must stay editable | approx | build it in Google Sheets (`EmbeddedChart` via the Sheets API: BAR, COLUMN, LINE, AREA, COMBO, pie, bubble, candlestick, histogram, waterfall, treemap, scorecard) and insert the linked chart from Sheets into the Doc by hand |

## Syntax essentials

Three routes, in order of preference:

1. New document from HTML (works through the Claude Google Drive connector's `create_file` with `contentMimeType: text/html`): write the document as HTML with `<img src="<public URL>" alt="<text alternative>">`; Drive converts it to a Doc and fetches the images at import. `quickchart` URLs are the easiest public source; a PNG uploaded to Drive with public sharing also works. Verified 2026-09-18: the Doc was created; the connector's text view omits images, so confirm visually.
2. Existing document, Docs API available: `documents.batchUpdate` with `insertInlineImage` (`uri` must be publicly fetchable, under 50 MB, PNG/JPEG/GIF) at the index after the claim's paragraph.
3. Manual: render a PNG at 2x, upload to Drive, and insert with Insert > Image, or paste. State this plainly when no API route exists in the session.

Alt text: Docs keeps the `alt` attribute from HTML import as the image description; always set it to the chart's text alternative.

## Limits

- No native chart object; the reader cannot edit the data unless the chart comes from Sheets.
- Remote images must be public at import time; confidential data must go through a Drive-hosted PNG, not a QuickChart URL.
- The Drive connector cannot edit an existing Doc's body (metadata only), so route 1 creates a new document; merging into an existing one is manual or needs the Docs API.

## Render

- `cw.py build --chart <slug> --target quickchart ...` for the image URL, or `cw.py render --target vega-lite --in spec.vl.json --out chart.png` for a PNG to upload. Wrap the document as HTML and create it through Drive, or hand the PNG to the Docs API.

## Notes

- 2026-09-18: added after a live test: a Q2 summary Doc created from HTML with two QuickChart images through the Drive connector.
