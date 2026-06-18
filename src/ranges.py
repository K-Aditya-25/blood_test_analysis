"""Parse reference-interval text and decide if a value is in range."""

import re

RANGE_RE = re.compile(r"([\d.]+)\s*-\s*([\d.]+)")
LESS_RE = re.compile(r"<\s*([\d.]+)")
GREATER_RE = re.compile(r">\s*([\d.]+)")


def parse_ref(ref_text: str) -> tuple[float | None, float | None]:
    """Return (low, high) bounds parsed from a reference string."""
    t = ref_text.strip()
    if not t:
        return None, None
    m = RANGE_RE.search(t)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = LESS_RE.search(t)
    if m:
        return None, float(m.group(1))
    m = GREATER_RE.search(t)
    if m:
        return float(m.group(1)), None
    return None, None


def status_for_value(value: float, low: float | None, high: float | None) -> str:
    """Return 'normal', 'high' or 'low' for a numeric value vs bounds."""
    if low is not None and value < low:
        return "low"
    if high is not None and value > high:
        return "high"
    return "normal"
