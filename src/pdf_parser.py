"""Parse extracted PDF text into structured Test records."""

import re

from .catalog import TESTS
from .models import Test
from .ranges import parse_ref, status_for_value

NUM_RE = r"(?m)^\s*{name}\s+(?P<val>[\d.]+)\s*(?P<rest>.*)$"
QUAL_RE = r"(?m)^\s*{name}\s+(?P<val>\S+)(?:\s+(?P<ref>.+))?$"
NAME_RE = re.compile(r"Name\s*:\s*(.+?)\s*$", re.M)
LAB_RE = re.compile(r"Lab No\.\s*:\s*(\S+)\s+Age\s*:\s*(\d+)", re.M)
GENDER_RE = re.compile(r"Gender\s*:\s*(\w+)", re.M)
DATES_RE = re.compile(
    r"Collected\s*:\s*(.+?)\s+Reported\s*:\s*(.+?)$", re.M
)


def _split_unit_ref(rest: str) -> tuple[str, str]:
    rest = rest.strip()
    if not rest:
        return "", ""
    first, _, after = rest.partition(" ")
    starts_value = first and (first[0].isdigit() or first[0] in "<>")
    if starts_value:
        return "", rest
    return first, after.strip()


def parse_header(text: str) -> dict:
    name = NAME_RE.search(text).group(1).strip()
    lab = LAB_RE.search(text)
    gender = GENDER_RE.search(text).group(1).strip()
    dates = DATES_RE.search(text)
    return {
        "name": name, "age": int(lab.group(2)), "gender": gender,
        "lab_no": lab.group(1),
        "collected": dates.group(1).strip(),
        "reported": dates.group(2).strip(),
    }


def parse_tests(text: str) -> list[Test]:
    marker = "URINE EXAMINATION ROUTINE"
    idx = text.find(marker)
    tail = "" if idx < 0 else text[idx:]
    out = []
    for key, section, display, search_name, kind in TESTS:
        scope = tail if section == "urine" else text
        if kind == "num":
            m = re.search(NUM_RE.format(name=re.escape(search_name)), scope)
            if not m:
                continue
            val = float(m.group("val"))
            unit, ref_text = _split_unit_ref(m.group("rest"))
            low, high = parse_ref(ref_text)
            status = status_for_value(val, low, high) if (low or high) else "info"
            out.append(Test(key, display, section, val, "", unit, low, high, ref_text, status))
        else:
            m = re.search(QUAL_RE.format(name=re.escape(search_name)), scope)
            if not m:
                continue
            val_text = m.group("val")
            ref_text = (m.group("ref") or "").strip()
            ok = val_text.lower() == ref_text.lower() or not ref_text
            out.append(Test(key, display, section, None, val_text, "", None, None, ref_text,
                            "normal" if ok else "flag"))
    return out
