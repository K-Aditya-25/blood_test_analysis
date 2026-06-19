
from src.loader import load_all, patient_summary
from src.models import Patient, Test
from src.sections import SECTIONS


def _make_patient() -> Patient:
    return Patient(
        name="Test", age=30, gender="Male",
        lab_no="1", collected="x", reported="y",
        tests=[
            Test("a", "A", "kidneys_liver", 0.5, "", "u", 0.6, 1.2, "0.6-1.2", "low"),
            Test("b", "B", "kidneys_liver", 1.0, "", "u", 0.6, 1.2, "0.6-1.2", "normal"),
            Test("c", "C", "heart_meta", 3.0, "", "u", 0, 2, "0-2", "high"),
            Test("d", "D", "thyroid", 1.0, "", "u", 0, 2, "0-2", "normal"),
        ],
    )


class TestPatientSummary:
    def test_flagged_count(self):
        s = patient_summary(_make_patient())
        assert s["flagged_count"] == 2

    def test_total_count(self):
        s = patient_summary(_make_patient())
        assert s["total_count"] == 4

    def test_all_sections_present(self):
        s = patient_summary(_make_patient())
        for sec in SECTIONS:
            assert sec.key in s["by_section"]

    def test_section_counts(self):
        s = patient_summary(_make_patient())
        assert s["by_section"]["kidneys_liver"] == 1
        assert s["by_section"]["heart_meta"] == 1
        assert s["by_section"]["thyroid"] == 0

    def test_flagged_keys(self):
        s = patient_summary(_make_patient())
        assert set(s["flagged_keys"]) == {"a", "c"}


class TestExampleMode:
    def test_example_mode_returns_two_patients(self, monkeypatch):
        monkeypatch.setenv("VITALS_DATA_MODE", "example")
        patients = load_all()
        assert len(patients) == 2

    def test_example_mode_names(self, monkeypatch):
        monkeypatch.setenv("VITALS_DATA_MODE", "example")
        patients = load_all()
        assert patients[0].name == "Aditya Kharbanda"
        assert patients[1].name == "Siddharth"

    def test_example_mode_has_notes(self, monkeypatch):
        monkeypatch.setenv("VITALS_DATA_MODE", "example")
        patients = load_all()
        for p in patients:
            for t in p.tests:
                if t.status in ("high", "low", "flag"):
                    assert t.note != "", f"{t.key} note is empty"

    def test_example_mode_has_summary(self, monkeypatch):
        monkeypatch.setenv("VITALS_DATA_MODE", "example")
        patients = load_all()
        for p in patients:
            assert "flagged_count" in p.summary
            assert "total_count" in p.summary
            assert p.summary["total_count"] == len(p.tests)
