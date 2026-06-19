from src.catalog import TESTS
from src.example_data import DERIVED, NUM_RANGES, QUAL, build_example_patients
from src.sections import SECTIONS

VALID_SECTIONS = {s.key for s in SECTIONS}
_WBC_KEYS = ("neutrophils", "lymphocytes", "monocytes", "eosinophils", "basophils")


class TestBuildExamplePatients:
    def test_returns_two_patients(self):
        patients = build_example_patients()
        assert len(patients) == 2

    def test_names(self):
        patients = build_example_patients()
        assert patients[0].name == "Aditya Kharbanda"
        assert patients[1].name == "Siddharth"

    def test_all_sections_present(self):
        for patient in build_example_patients():
            present = {t.section for t in patient.tests}
            assert present == VALID_SECTIONS

    def test_test_count_matches_catalog(self):
        for patient in build_example_patients():
            assert len(patient.tests) == len(TESTS)

    def test_deterministic(self):
        a = build_example_patients()
        b = build_example_patients()
        for pa, pb in zip(a, b):
            for ta, tb in zip(pa.tests, pb.tests):
                assert ta.value == tb.value
                assert ta.value_text == tb.value_text

    def test_numeric_values_non_negative(self):
        for patient in build_example_patients():
            for t in patient.tests:
                if t.value is not None:
                    assert t.value >= 0, f"{t.key} is negative: {t.value}"

    def test_all_statuses_valid(self):
        valid = {"normal", "high", "low", "flag", "info"}
        for patient in build_example_patients():
            for t in patient.tests:
                assert t.status in valid, f"{t.key} has bad status: {t.status}"

    def test_wbc_differential_sums_to_100(self):
        for patient in build_example_patients():
            vals = {t.key: t.value for t in patient.tests if t.key in _WBC_KEYS}
            assert sum(vals.values()) == 100, f"WBC sum is {sum(vals.values())}"

    def test_overrides_applied(self):
        patients = build_example_patients()
        aditya = patients[0]
        by_key = {t.key: t for t in aditya.tests}
        assert by_key["uric_acid"].value == 7.5
        assert by_key["sodium"].value == 134
        assert by_key["platelets"].value == 140
        assert by_key["vit_d"].value == 21.0

    def test_qual_overrides_applied(self):
        patients = build_example_patients()
        aditya = patients[0]
        by_key = {t.key: t for t in aditya.tests}
        assert by_key["ur_blood"].value_text == "Trace"
        assert by_key["ur_blood"].status == "flag"

    def test_siddharth_overrides(self):
        patients = build_example_patients()
        sid = patients[1]
        by_key = {t.key: t for t in sid.tests}
        assert by_key["creatinine"].value == 1.3
        assert by_key["hemoglobin"].value == 12.8
        assert by_key["tsh"].value == 0.35
        assert by_key["ur_protein"].value_text == "Trace"


class TestDerivedTests:
    def test_protein_total_is_sum(self):
        for patient in build_example_patients():
            vals = {t.key: t.value for t in patient.tests}
            expected = round(vals["albumin"] + vals["globulin"], 1)
            assert vals["protein_total"] == expected

    def test_vldl_is_trig_div_5(self):
        for patient in build_example_patients():
            vals = {t.key: t.value for t in patient.tests}
            expected = round(vals["triglycerides"] / 5.0, 1)
            assert vals["vldl"] == expected

    def test_non_hdl(self):
        for patient in build_example_patients():
            vals = {t.key: t.value for t in patient.tests}
            expected = round(vals["chol_total"] - vals["hdl"], 0)
            assert vals["non_hdl"] == expected

    def test_eag_formula(self):
        for patient in build_example_patients():
            vals = {t.key: t.value for t in patient.tests}
            expected = round(28.7 * vals["hba1c"] - 46.7, 0)
            assert vals["eag"] == expected

    def test_ag_ratio(self):
        for patient in build_example_patients():
            vals = {t.key: t.value for t in patient.tests}
            expected = round(vals["albumin"] / vals["globulin"], 2)
            assert vals["ag_ratio"] == expected


class TestRangesConsistency:
    def test_all_num_ranges_have_seven_fields(self):
        for key, spec in NUM_RANGES.items():
            assert len(spec) == 7, f"{key} has {len(spec)} fields"

    def test_all_derived_have_six_fields(self):
        for key, spec in DERIVED.items():
            assert len(spec) == 6, f"{key} has {len(spec)} fields"

    def test_qual_has_two_fields(self):
        for key, spec in QUAL.items():
            assert len(spec) == 2, f"{key} has {len(spec)} fields"
