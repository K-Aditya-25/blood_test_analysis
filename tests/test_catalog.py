from src.catalog import TESTS

VALID_SECTIONS = {
    "kidneys_liver", "electrolytes", "heart_meta",
    "blood_cells", "vitamins_iron", "thyroid", "urine",
}
VALID_KINDS = {"num", "qual"}


class TestCatalog:
    def test_keys_unique(self):
        keys = [t[0] for t in TESTS]
        assert len(keys) == len(set(keys))

    def test_all_sections_valid(self):
        for _key, section, _display, _search, _kind in TESTS:
            assert section in VALID_SECTIONS, f"unknown section: {section}"

    def test_all_kinds_valid(self):
        for _key, _section, _display, _search, kind in TESTS:
            assert kind in VALID_KINDS, f"unknown kind: {kind}"

    def test_test_count(self):
        assert len(TESTS) == 68

    def test_tuple_arity(self):
        for entry in TESTS:
            assert len(entry) == 5
