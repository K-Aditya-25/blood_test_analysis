"""Build plain-language section summaries and the patient headline."""

from .models import Patient
from .sections import SECTIONS, THEME
from .layman import topic
from .section_plain import template


def _situation(flagged_count: int) -> str:
    if flagged_count == 0:
        return "all_clear"
    if flagged_count <= 2:
        return "watch"
    return "attention"


def _join(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def section_summaries(patient: Patient) -> dict[str, str]:
    out = {}
    for s in SECTIONS:
        tests = [t for t in patient.tests if t.section == s.key]
        flagged = [t for t in tests if t.status in ("high", "low", "flag")]
        sit = _situation(len(flagged))
        text = template(s.key, sit)
        if sit == "all_clear":
            out[s.key] = text
        else:
            n = len(flagged)
            out[s.key] = text.format(
                n=n, list=_join([topic(t.key) for t in flagged]),
                readings="reading" if n == 1 else "readings",
                verb="is" if n == 1 else "are",
            )
    return out


def headline(patient: Patient) -> str:
    flagged = [t for t in patient.tests if t.status in ("high", "low", "flag")]
    total = len(patient.tests)
    ok = total - len(flagged)
    if not flagged:
        return (f"Great news - all {total} of your results are within their healthy ranges. "
                "Nothing here needs urgent attention.")
    themes = []
    for s in SECTIONS:
        if any(t.section == s.key and t.status in ("high", "low", "flag") for t in flagged):
            themes.append(THEME.get(s.key, s.title.lower()))
    return (f"Most of your results look healthy - {ok} of {total} are within range. "
            f"{len(flagged)} are worth a closer look, mainly around your {_join(themes)}. "
            "Nothing here is an emergency, but it's a good idea to discuss them with your doctor.")
