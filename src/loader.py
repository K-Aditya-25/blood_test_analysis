"""Orchestrate: read PDF -> parse -> build Patient objects with summaries."""

import os
from pathlib import Path

from .interpretations import note_for
from .models import Patient
from .names import clean_name
from .pdf_parser import parse_header, parse_tests
from .sections import SECTIONS

REPORTS_DIR = Path(__file__).resolve().parent.parent / "private_reports"

# Backend flag: set VITALS_DATA_MODE=example to serve randomized sample data
# (no patient PDFs read) for public presentation. Default "real" keeps the
# private PDF pipeline unchanged.
_EXAMPLE_TOKENS = {"example", "demo", "sample", "1", "true", "yes", "on"}


def load_patient(pdf_path: Path) -> Patient:
    import pdfplumber
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    raw = "\n".join(text)
    header = parse_header(raw)
    tests = parse_tests(raw)
    for t in tests:
        t.status  # noqa
    return Patient(
        name=clean_name(header["name"]), age=header["age"], gender=header["gender"],
        lab_no=header["lab_no"], collected=header["collected"],
        reported=header["reported"], tests=tests,
    )


def _attach_notes(patient: Patient) -> None:
    for t in patient.tests:
        t.note = note_for(t.key, t.status)


def patient_summary(patient: Patient) -> dict:
    flagged = [t for t in patient.tests if t.status in ("high", "low", "flag")]
    watch = [t for t in patient.tests if t.status in ("high", "low", "flag")]
    by_sec = {s.key: [t for t in flagged if t.section == s.key] for s in SECTIONS}
    return {
        "flagged_count": len(flagged),
        "total_count": len(patient.tests),
        "by_section": {k: len(v) for k, v in by_sec.items()},
        "flagged_keys": [t.key for t in watch],
    }


def load_all() -> list[Patient]:
    mode = os.environ.get("VITALS_DATA_MODE", "real").strip().lower()
    if mode in _EXAMPLE_TOKENS:
        from .example_data import build_example_patients
        print("VITALS_DATA_MODE=example - using randomized sample data (no patient data).",
              flush=True)
        patients = build_example_patients()
        for p in patients:
            _attach_notes(p)
            p.summary = patient_summary(p)
        return patients

    patients = []
    for pdf in sorted(REPORTS_DIR.glob("*.pdf")):
        p = load_patient(pdf)
        _attach_notes(p)
        p.summary = patient_summary(p)
        patients.append(p)
    return patients
