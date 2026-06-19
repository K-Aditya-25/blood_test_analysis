"""Generate randomized *example* blood-report data for public presentation.

This module reproduces the same Test/Patient structure the PDF pipeline
produces, but with values sampled from normal distributions centred on
standard published adult reference ranges (sources: American Heart
Association, Cleveland Clinic, NFK/KDOQI, American Thyroid Association,
Mayo Clinic and common Indian lab report ranges). It contains **no
patient data** - only synthetic, reproducible sample values.

Reference ranges and units here are standard adult-male values used purely
to drive the visualization; the real ranges come from the parsed PDFs.

Switch on with the environment variable ``VITALS_DATA_MODE=example``.
"""

from .catalog import TESTS
from .models import Patient, Test
from .ranges import status_for_value

# ---------------------------------------------------------------------------
# Reference ranges + sampling distributions
#   NUM_RANGES[key] = (unit, low, high, ref_text, mean, sd, decimals)
#   low/high of None  -> one-sided range (parsed as "<x" or ">x")
# ---------------------------------------------------------------------------
NUM_RANGES: dict[str, tuple] = {
    # kidneys / liver
    "creatinine":   ("mg/dL", 0.6, 1.2, "0.6 - 1.2", 0.90, 0.10, 1),
    "gfr":          ("mL/min/1.73m2", 60, None, "> 60", 100.0, 12.0, 0),
    "urea":         ("mg/dL", 15, 40, "15 - 40", 26.0, 4.0, 0),
    "uric_acid":    ("mg/dL", 3.4, 7.0, "3.4 - 7.0", 5.0, 0.6, 1),
    "ast":          ("U/L", 10, 40, "10 - 40", 24.0, 5.0, 0),
    "alt":          ("U/L", 10, 40, "10 - 40", 24.0, 6.0, 0),
    "ggtp":         ("U/L", 9, 48, "9 - 48", 28.0, 7.0, 0),
    "alp":          ("U/L", 40, 129, "40 - 129", 85.0, 15.0, 0),
    "bili_total":   ("mg/dL", 0.2, 1.2, "0.2 - 1.2", 0.6, 0.17, 1),
    "bili_direct":  ("mg/dL", 0.0, 0.4, "0.0 - 0.4", 0.15, 0.08, 1),
    "albumin":      ("g/dL", 3.5, 5.2, "3.5 - 5.2", 4.4, 0.25, 1),
    "globulin":     ("g/dL", 2.0, 3.5, "2.0 - 3.5", 2.7, 0.30, 1),
    "amylase":      ("U/L", 30, 110, "30 - 110", 70.0, 15.0, 0),
    # electrolytes
    "calcium":      ("mg/dL", 8.6, 10.3, "8.6 - 10.3", 9.4, 0.3, 1),
    "phosphorus":   ("mg/dL", 2.5, 4.5, "2.5 - 4.5", 3.5, 0.4, 1),
    "sodium":       ("mEq/L", 135, 145, "135 - 145", 140.0, 1.8, 0),
    "potassium":     ("mEq/L", 3.5, 5.1, "3.5 - 5.1", 4.3, 0.3, 1),
    "chloide":      ("mEq/L", 98, 107, "98 - 107", 102.0, 2.0, 0),
    # heart / metabolic
    "chol_total":   ("mg/dL", None, 200, "< 200", 165.0, 22.0, 0),
    "triglycerides":("mg/dL", None, 150, "< 150", 120.0, 30.0, 0),
    "hdl":          ("mg/dL", 40, None, "> 40", 52.0, 8.0, 0),
    "ldl":          ("mg/dL", None, 100, "< 100", 95.0, 22.0, 0),
    "hba1c":        ("%", 4.0, 5.6, "4.0 - 5.6", 5.0, 0.25, 1),
    "glucose_f":    ("mg/dL", 70, 99, "70 - 99", 88.0, 7.0, 0),
    "hscrp":        ("mg/L", None, 1.0, "< 1.0", 0.6, 0.35, 1),
    "apo_a1":       ("mg/dL", 120, 160, "120 - 160", 140.0, 12.0, 0),
    "apo_b":        ("mg/dL", 60, 110, "60 - 110", 85.0, 12.0, 0),
    # blood cells (adult male)
    "hemoglobin":   ("g/dL", 13.0, 17.0, "13.0 - 17.0", 15.2, 0.8, 1),
    "pcv":          ("%", 40, 50, "40 - 50", 45.0, 2.0, 1),
    "rbc":          ("million/uL", 4.5, 5.9, "4.5 - 5.9", 5.2, 0.23, 2),
    "mcv":          ("fL", 80, 100, "80 - 100", 90.0, 3.0, 1),
    "mch":          ("pg", 27, 33, "27 - 33", 30.0, 1.2, 1),
    "mchc":         ("g/dL", 32, 36, "32 - 36", 34.0, 0.8, 1),
    "rdw":          ("%", 11.5, 14.5, "11.5 - 14.5", 13.0, 0.6, 1),
    "tlc":          ("/uL", 4000, 11000, "4000 - 11000", 7000.0, 1200.0, 0),
    "neutrophils":  ("%", 40, 75, "40 - 75", 58.0, 6.0, 0),
    "lymphocytes":  ("%", 20, 45, "20 - 45", 34.0, 5.0, 0),
    "monocytes":    ("%", 2, 10, "2 - 10", 6.0, 1.5, 0),
    "eosinophils":  ("%", 1, 6, "1 - 6", 3.0, 1.2, 0),
    "basophils":    ("%", 0, 2, "0 - 2", 1.0, 0.4, 0),
    "platelets":    ("x10^3/uL", 150, 450, "150 - 450", 250.0, 45.0, 0),
    "mpv":          ("fL", 7.4, 10.4, "7.4 - 10.4", 9.0, 0.6, 1),
    "esr":          ("mm/hr", 0, 15, "0 - 15", 6.0, 3.0, 0),
    # vitamins / iron
    "vit_b12":      ("pg/mL", 200, 900, "200 - 900", 450.0, 120.0, 0),
    "vit_d":        ("ng/mL", 30, 100, "30 - 100", 35.0, 8.0, 1),
    "iron":         ("ug/dL", 60, 170, "60 - 170", 110.0, 25.0, 0),
    "tibc":         ("ug/dL", 250, 450, "250 - 450", 350.0, 40.0, 0),
    "transf_sat":   ("%", 20, 50, "20 - 50", 32.0, 7.0, 0),
    # thyroid
    "t3_free":      ("pg/mL", 2.0, 4.4, "2.0 - 4.4", 3.1, 0.4, 1),
    "t4_free":      ("ng/dL", 0.7, 1.8, "0.7 - 1.8", 1.2, 0.2, 1),
    "tsh":          ("uIU/mL", 0.4, 4.0, "0.4 - 4.0", 2.0, 0.7, 2),
    # urine (numeric)
    "ur_sp_grav":   ("", 1.003, 1.030, "1.003 - 1.030", 1.018, 0.005, 3),
    "ur_ph":        ("", 5.0, 8.0, "5.0 - 8.0", 6.2, 0.6, 1),
}

# Calculated / derived tests: value computed from sampled primaries so the
# example stays internally consistent (e.g. VLDL = triglycerides/5).
#   DERIVED[key] = (unit, low, high, ref_text, decimals, fn)
DERIVED: dict[str, tuple] = {
    "protein_total": ("g/dL", 6.0, 8.3, "6.0 - 8.3", 1,
                      lambda v: v["albumin"] + v["globulin"]),
    "ast_alt_ratio": ("ratio", 0.7, 1.4, "0.7 - 1.4", 2,
                      lambda v: v["ast"] / v["alt"] if v["alt"] else 0.0),
    "ag_ratio":      ("ratio", 1.0, 2.1, "1.0 - 2.1", 2,
                      lambda v: v["albumin"] / v["globulin"] if v["globulin"] else 0.0),
    "vldl":          ("mg/dL", 2, 30, "2 - 30", 1,
                      lambda v: v["triglycerides"] / 5.0),
    "non_hdl":       ("mg/dL", None, 130, "< 130", 0,
                      lambda v: v["chol_total"] - v["hdl"]),
    "apo_ratio":     ("ratio", None, 0.98, "< 0.98", 2,
                      lambda v: v["apo_b"] / v["apo_a1"] if v["apo_a1"] else 0.0),
    "eag":           ("mg/dL", None, None, "-", 0,
                      lambda v: 28.7 * v["hba1c"] - 46.7),
}

# Qualitative urine tests: value text + reference text for a normal result.
QUAL: dict[str, tuple[str, str]] = {
    "ur_protein": ("Negative", "Negative"),
    "ur_glucose": ("Negative", "Negative"),
    "ur_ketones": ("Negative", "Negative"),
    "ur_bili":    ("Negative", "Negative"),
    "ur_blood":   ("Negative", "Negative"),
    "ur_le":      ("Negative", "Negative"),
    "ur_nitrite": ("Negative", "Negative"),
    "ur_uro":     ("Negative", "Negative"),
}

# ---------------------------------------------------------------------------
# Example patients (names kept as requested).
# A small set of curated, *mildly* out-of-range overrides per person so the
# dashboard's "watch"/"attention" summaries and high/low/flag UI states are
# exercised realistically across every section (metabolic + vitamin nudges
# typical of healthy young adults). Everything else is sampled from the
# distribution above.
# ---------------------------------------------------------------------------
_EXAMPLE_PATIENTS = [
    {
        "name": "Aditya Kharbanda",
        "age": 22, "gender": "Male",
        "lab_no": "EX-ADT-01", "collected": "10 Jun 2026", "reported": "12 Jun 2026",
        "seed": 101,
        "overrides": {
            # kidneys_liver
            "uric_acid": 7.5,    # high (>7.0) - common in young men
            # electrolytes
            "sodium": 134,       # low (<135) - usually hydration
            # heart_meta
            "triglycerides": 172,# high (>150)
            "ldl": 120,          # high (>100)
            "chol_total": 195,   # normal (<200)
            "hdl": 46,           # normal (>40)
            "hscrp": 1.3,        # high (>1.0)
            # blood_cells
            "platelets": 140,    # low (<150) - mild
            # vitamins_iron
            "vit_d": 21.0,       # low (<30)
            "vit_b12": 920,      # high (>900) - common with supplementation
            # thyroid
            "tsh": 4.3,          # high (>4.0) - subclinical, very mild
        },
        "qual_overrides": {
            "ur_blood": "Trace", # flag - minor, common
        },
    },
    {
        "name": "Siddharth",
        "age": 18, "gender": "Male",
        "lab_no": "EX-SID-01", "collected": "10 Jun 2026", "reported": "12 Jun 2026",
        "seed": 202,
        "overrides": {
            # kidneys_liver
            "creatinine": 1.3,   # high (>1.2) - mild
            # electrolytes
            "potassium": 3.4,    # low (<3.5) - mild
            # heart_meta
            "triglycerides": 160,# high (>150)
            "ldl": 122,          # high (>100)
            "chol_total": 190,   # normal (<200)
            "hdl": 37,           # low (<40)
            # blood_cells
            "hemoglobin": 12.8, # low (<13.0) - mild anaemia
            "rdw": 15.0,         # high (>14.5) - mixed cell size
            "esr": 18,           # high (>15) - mild inflammation
            # vitamins_iron
            "vit_d": 18.0,       # low (<30)
            "iron": 55,          # low (<60) - low iron stores
            "transf_sat": 18,    # low (<20) - early iron shortage
            # thyroid
            "tsh": 0.35,         # low (<0.4) - subclinical, very mild
        },
        "qual_overrides": {
            "ur_protein": "Trace",  # flag - minor, common
        },
    },
]


def _sample_primary(rng, spec: tuple) -> float:
    unit, low, high, ref_text, mean, sd, dec = spec
    val = rng.gauss(mean, sd)
    if val < 0:
        val = 0.0
    return round(val, dec)


def _make_test(key: str, display: str, section: str, value, unit: str,
               low, high, ref_text: str, status: str) -> Test:
    return Test(
        key=key, name=display, section=section,
        value=value, value_text="",
        unit=unit, ref_low=low, ref_high=high, ref_text=ref_text,
        status=status, note="",
    )


def _status(value: float, low, high) -> str:
    if low is None and high is None:
        return "info"
    return status_for_value(value, low, high)


def _build_patient(spec: dict) -> Patient:
    import random
    rng = random.Random(spec["seed"])
    overrides = spec.get("overrides", {})
    qual_overrides = spec.get("qual_overrides", {})
    values: dict[str, float] = {}
    qual_text: dict[str, str] = {}

    # Phase 1: sample all primaries (and fix qual text) into lookup dicts.
    for key, _section, _display, _search, kind in TESTS:
        if key in DERIVED:
            continue
        if kind == "num":
            unit, low, high, ref_text, mean, sd, dec = NUM_RANGES[key]
            v = overrides.get(key)
            if v is None:
                v = _sample_primary(rng, NUM_RANGES[key])
            else:
                v = round(float(v), dec)
            values[key] = v
        else:
            qual_text[key] = qual_overrides.get(key, QUAL[key][0])

    # WBC differential percentages must sum to ~100 in real reports.
    # Rescale so the donut center reads sensibly and the UI looks correct.
    _WBC_KEYS = ("neutrophils", "lymphocytes", "monocytes",
                 "eosinophils", "basophils")
    wbc_sum = sum(values[k] for k in _WBC_KEYS)
    if wbc_sum > 0:
        scale = 100.0 / wbc_sum
        for k in _WBC_KEYS:
            values[k] = round(values[k] * scale)

    # Phase 2: build Test objects in catalog order (derived computed on the fly).
    tests: list[Test] = []
    for key, section, display, _search, kind in TESTS:
        if kind == "qual":
            _default, ref_text = QUAL[key]
            val_text = qual_text[key]
            ok = val_text.lower() == ref_text.lower() or not ref_text
            t = _make_test(key, display, section, None, "", None, None,
                           ref_text, "normal" if ok else "flag")
            t.value_text = val_text
            tests.append(t)
            continue
        if key in DERIVED:
            unit, low, high, ref_text, dec, fn = DERIVED[key]
            v = round(fn(values), dec)
            if v < 0:
                v = 0.0
            values[key] = v
            tests.append(_make_test(key, display, section, v, unit,
                                    low, high, ref_text, _status(v, low, high)))
        else:
            unit, low, high, ref_text, *_ = NUM_RANGES[key]
            v = values[key]
            tests.append(_make_test(key, display, section, v, unit,
                                    low, high, ref_text, _status(v, low, high)))

    return Patient(
        name=spec["name"], age=spec["age"], gender=spec["gender"],
        lab_no=spec["lab_no"], collected=spec["collected"],
        reported=spec["reported"], tests=tests,
    )


def build_example_patients() -> list[Patient]:
    """Return deterministic, randomized example patients (no real data)."""
    return [_build_patient(s) for s in _EXAMPLE_PATIENTS]
