import sys, json
sys.path.insert(0, ".")
from src.loader import load_all

patients = load_all()
for p in patients:
    print(f"\n===== {p.name} | {p.age}{p.gender} | lab {p.lab_no} =====")
    print(f"tests parsed: {len(p.tests)} | flagged: {p.summary['flagged_count']}")
    for t in p.tests:
        flag = {"high": "HIGH", "low": "LOW", "flag": "FLAG", "info": "info"}.get(t.status, "ok")
        val = t.value if t.value is not None else t.value_text
        print(f"  [{flag:4}] {t.section:14} {t.name:28} {str(val):>8} {t.unit:14} ref:{t.ref_text}")
