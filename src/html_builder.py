"""Assemble the self-contained HTML visualization and write it to disk."""

import json
from pathlib import Path

from .exporter import build_document
from .assets_css import CSS
from .assets_js import JS
from .loader import load_all

OUTPUT = Path(__file__).resolve().parent.parent / "output" / "index.html"
CHART_JS = "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Health Story - Blood Report</title>
<style>{css}</style>
<script src="{chartjs}"></script>
</head>
<body>
<header class="top">
  <div class="brand">Health Story <small>interpreting your blood report</small></div>
  <button id="toggle">View <span id="next-name"></span> ▸</button>
</header>
<main id="app"></main>
<footer>For education only - not a diagnosis. Always discuss results with your doctor.</footer>
<script id="data" type="application/json">{data}</script>
<script>{js}</script>
</body>
</html>
"""


def build() -> Path:
    patients = load_all()
    doc = build_document(patients)
    html = HTML.format(
        css=CSS, chartjs=CHART_JS,
        data=json.dumps(doc, ensure_ascii=False),
        js=JS,
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    return OUTPUT
