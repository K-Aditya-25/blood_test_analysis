"""Export the parsed blood-report document as JSON for the Next.js app.

This keeps the existing Python PDF pipeline as the data source. The Next.js
dashboard reads the generated ``next-app/src/data/report.json`` file.

Run with:  python3 -m src.export_json   (or:  uv run python -m src.export_json)
"""

import json
from pathlib import Path

from .exporter import build_document
from .loader import load_all

OUT = Path(__file__).resolve().parent.parent / "next-app" / "src" / "data" / "report.json"


def main() -> None:
    patients = load_all()
    doc = build_document(patients)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Next.js data written to: {OUT}")
    print(f"Patients: {len(doc['patients'])} | "
          f"Tests: {sum(len(p['tests']) for p in doc['patients'])}")


if __name__ == "__main__":
    main()
