import pdfplumber
import sys
from pathlib import Path

REPORTS_DIR = Path(__file__).parent.parent / "private_reports"


def extract_text(pdf_path: Path) -> str:
    out = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            out.append(f"\n===== PAGE {i} =====\n")
            out.append(page.extract_text() or "")
            tables = page.extract_tables()
            for j, tbl in enumerate(tables, 1):
                out.append(f"\n----- TABLE {j} on page {i} -----\n")
                for row in tbl:
                    out.append(" | ".join("" if c is None else str(c) for c in row))
                    out.append("\n")
    return "".join(out)


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else None
    pdfs = sorted(REPORTS_DIR.glob("*.pdf"))
    if name:
        pdfs = [p for p in pdfs if name.lower() in p.name.lower()]
    for p in pdfs:
        print(f"\n########## FILE: {p.name} ##########")
        print(extract_text(p))
