"""Compute per-test chart scales and build the exportable data document."""

from .models import Patient, Test
from .names import first_name
from .section_plain import SECTION_PLAIN
from .sections import SECTIONS
from .summaries import headline, section_summaries


def _scale(t: Test) -> tuple[float, float, float | None, float | None]:
    v = t.value or 0.0
    low, high = t.ref_low, t.ref_high
    if low is None and high is not None:
        return 0.0, max(v, high) * 1.25, 0.0, float(high)
    if low is not None and high is None:
        top = max(v, low) * 1.25
        return 0.0, top, float(low), top
    if low is not None and high is not None:
        span = high - low or 1.0
        amin = max(0.0, low - 0.8 * span)
        amax = high + 0.8 * span
        if v < amin:
            amin = max(0.0, v - 0.4 * span)
        if v > amax:
            amax = v + 0.4 * span
        return amin, amax, float(low), float(high)
    return 0.0, v * 1.6 or 1.0, None, None


def _test_dict(t: Test) -> dict:
    amin, amax, blow, bhigh = _scale(t)
    return {
        "key": t.key, "name": t.name, "section": t.section,
        "value": t.value, "value_text": t.value_text, "unit": t.unit,
        "ref_text": t.ref_text, "status": t.status, "note": t.note,
        "axis_min": round(amin, 4), "axis_max": round(amax, 4),
        "band_low": None if blow is None else round(blow, 4),
        "band_high": None if bhigh is None else round(bhigh, 4),
    }


def _headline(p: Patient) -> str:
    return headline(p)


def _patient_dict(p: Patient) -> dict:
    return {
        "name": p.name, "first_name": first_name(p.name),
        "age": p.age, "gender": p.gender,
        "lab_no": p.lab_no, "collected": p.collected, "reported": p.reported,
        "headline": _headline(p),
        "flagged_count": p.summary["flagged_count"],
        "total_count": p.summary["total_count"],
        "section_summary": section_summaries(p),
        "tests": [_test_dict(t) for t in p.tests],
    }


def build_document(patients: list[Patient]) -> dict:
    return {
        "sections": [
            {"key": s.key, "title": s.title, "icon": s.icon,
             "story": s.story, "area": SECTION_PLAIN[s.key]["area"],
             "chart_type": s.chart_type, "order": s.order}
            for s in SECTIONS
        ],
        "patients": [_patient_dict(p) for p in patients],
    }
