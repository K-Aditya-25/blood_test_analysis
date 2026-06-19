"""Assemble the self-contained HTML visualization and write it to disk."""

import json
from pathlib import Path

from .exporter import build_document
from .assets_css import CSS
from .assets_js import JS
from .loader import load_all

OUTPUT = Path(__file__).resolve().parent.parent / "output" / "index.html"

HTML = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vitals - Your Blood Report, Visualized</title>
<style>{css}</style>
</head>
<body>
<header class="top">
  <div class="brand">
    <div class="mark"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2 5 4-12 2 7h6"/></svg></div>
    <div><div class="t1">Vitals</div><div class="t2">your blood report, visualized</div></div>
  </div>
  <div class="head-right">
    <div class="switcher" id="switcher" role="tablist" aria-label="Switch patient"></div>
    <button class="theme-toggle" id="theme-toggle" aria-label="Toggle dark mode" title="Toggle light / dark">
      <span class="knob">
        <svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        <svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
      </span>
    </button>
  </div>
</header>
<main id="app"></main>
<footer>For education only - not a diagnosis. <b>Always discuss results with your doctor.</b></footer>
<script id="data" type="application/json">{data}</script>
<script>{js}</script>
</body>
</html>
"""


def build() -> Path:
    patients = load_all()
    doc = build_document(patients)
    html = HTML.format(
        css=CSS,
        data=json.dumps(doc, ensure_ascii=False),
        js=JS,
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    return OUTPUT
