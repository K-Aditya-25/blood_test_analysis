from src.ranges import parse_ref, status_for_value


class TestParseRef:
    def test_range(self):
        assert parse_ref("0.6 - 1.2") == (0.6, 1.2)

    def test_range_with_spaces(self):
        assert parse_ref("  135  -  145  ") == (135.0, 145.0)

    def test_less_than(self):
        assert parse_ref("< 200") == (None, 200.0)

    def test_greater_than(self):
        assert parse_ref("> 60") == (60.0, None)

    def test_empty(self):
        assert parse_ref("") == (None, None)

    def test_whitespace_only(self):
        assert parse_ref("   ") == (None, None)

    def test_nonsense(self):
        assert parse_ref("See note") == (None, None)

    def test_decimal_range(self):
        assert parse_ref("3.4 - 7.0") == (3.4, 7.0)


class TestStatusForValue:
    def test_normal(self):
        assert status_for_value(0.9, 0.6, 1.2) == "normal"

    def test_low(self):
        assert status_for_value(0.5, 0.6, 1.2) == "low"

    def test_high(self):
        assert status_for_value(1.5, 0.6, 1.2) == "high"

    def test_at_low_boundary(self):
        assert status_for_value(0.6, 0.6, 1.2) == "normal"

    def test_at_high_boundary(self):
        assert status_for_value(1.2, 0.6, 1.2) == "normal"

    def test_one_sided_high_only(self):
        assert status_for_value(50, None, 100) == "normal"
        assert status_for_value(150, None, 100) == "high"

    def test_one_sided_low_only(self):
        assert status_for_value(50, 60, None) == "low"
        assert status_for_value(70, 60, None) == "normal"
