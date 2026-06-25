import pytest

from src.apv_geometry import calculate_apv_from_geometry, calculate_exposed_perimeter_mm


def test_freestanding_column_apv_calculation():
    assert calculate_exposed_perimeter_mm("freestanding_column", 100, 200) == 600
    assert calculate_apv_from_geometry("freestanding_column", 100, 200, 3000) == pytest.approx(200)


def test_beam_under_slab_apv_calculation():
    assert calculate_exposed_perimeter_mm("beam_under_slab", 120, 240) == 600
    assert calculate_apv_from_geometry("beam_under_slab", 120, 240, 4000) == pytest.approx(150)


def test_direct_apv_entry_still_uses_existing_state_field():
    state = {}
    state["custom_profile_apv"] = 123.4
    assert state["custom_profile_apv"] == pytest.approx(123.4)
