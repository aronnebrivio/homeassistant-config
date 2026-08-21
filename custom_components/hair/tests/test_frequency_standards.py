"""Tests for the IR carrier-frequency standards helpers."""
from __future__ import annotations

from custom_components.hair.frequency_standards import (
    IR_CARRIER_STANDARDS_HZ,
    ON_STANDARD_TOLERANCE_HZ,
    is_on_standard,
    nearest_standard,
)


class TestNearestStandard:
    """nearest_standard() picks the closest carrier, lower wins on a tie."""

    def test_each_standard_maps_to_itself(self):
        for std in IR_CARRIER_STANDARDS_HZ:
            assert nearest_standard(std) == std

    def test_in_between_rounds_to_closest(self):
        assert nearest_standard(39700) == 40000
        assert nearest_standard(34600) == 36000
        assert nearest_standard(31000) == 30000

    def test_tie_breaks_to_lower(self):
        # 37000 is equidistant from 36000 and 38000; the lower one wins.
        assert nearest_standard(37000) == 36000
        # 39000 is equidistant from 38000 and 40000; the lower one wins.
        assert nearest_standard(39000) == 38000

    def test_extremes_clamp_to_endpoints(self):
        assert nearest_standard(1000) == 30000
        assert nearest_standard(100000) == 56000


class TestIsOnStandard:
    """is_on_standard() honours the tolerance band around each carrier."""

    def test_exact_standard_is_on(self):
        for std in IR_CARRIER_STANDARDS_HZ:
            assert is_on_standard(std) is True

    def test_within_tolerance_is_on(self):
        assert is_on_standard(38000 + ON_STANDARD_TOLERANCE_HZ) is True
        assert is_on_standard(38000 - ON_STANDARD_TOLERANCE_HZ) is True

    def test_just_past_tolerance_is_off(self):
        assert is_on_standard(38000 + ON_STANDARD_TOLERANCE_HZ + 1) is False

    def test_clearly_off_is_off(self):
        assert is_on_standard(37000) is False
        assert is_on_standard(39000) is False
        assert is_on_standard(42000) is False
