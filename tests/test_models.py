from src.models import Patient, Test


def _make_test(status: str = "normal") -> Test:
    return Test(
        key="t", name="T", section="s",
        value=1.0, value_text="", unit="u",
        ref_low=0.0, ref_high=2.0, ref_text="0-2",
        status=status,
    )


class TestInRange:
    def test_normal_is_in_range(self):
        assert _make_test("normal").in_range is True

    def test_high_not_in_range(self):
        assert _make_test("high").in_range is False

    def test_low_not_in_range(self):
        assert _make_test("low").in_range is False

    def test_flag_not_in_range(self):
        assert _make_test("flag").in_range is False


class TestPatientBySection:
    def _make_patient(self) -> Patient:
        return Patient(
            name="Test", age=30, gender="Male",
            lab_no="1", collected="x", reported="y",
            tests=[
                Test("a", "A", "kidneys_liver", 1.0, "", "u", 0, 2, "0-2", "normal"),
                Test("b", "B", "kidneys_liver", 3.0, "", "u", 0, 2, "0-2", "high"),
                Test("c", "C", "thyroid", 1.0, "", "u", 0, 2, "0-2", "normal"),
            ],
        )

    def test_filters_by_section(self):
        p = self._make_patient()
        kl = p.by_section("kidneys_liver")
        assert len(kl) == 2
        assert {t.key for t in kl} == {"a", "b"}

    def test_empty_section(self):
        p = self._make_patient()
        assert p.by_section("urine") == []
