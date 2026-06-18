"""Clean and normalize patient names extracted from PDF headers.

The lab report sometimes contains a typo in the name (e.g. a repeated
trailing letter). This module applies known corrections so the displayed
name matches the person's actual name.
"""

# Known corrections keyed by the raw, uppercased name from the PDF.
NAME_FIXES = {
    "ADITYA KHARBANDAA": "Aditya Kharbanda",
}


_TITLES = {"mr", "mrs", "ms", "miss", "dr", "smt", "shri"}


def clean_name(raw: str) -> str:
    """Return a properly capitalized, corrected patient name (titles removed)."""
    parts = raw.replace(".", " ").split()
    while parts and parts[0].lower() in _TITLES:
        parts = parts[1:]
    key = " ".join(parts).upper()
    if key in NAME_FIXES:
        return NAME_FIXES[key]
    return " ".join(w.capitalize() for w in parts)


def first_name(full: str) -> str:
    """Return the given (first) name, ignoring any title like Mr/Mrs."""
    parts = full.replace(".", " ").split()
    while parts and parts[0].lower() in _TITLES:
        parts = parts[1:]
    return parts[0] if parts else full
