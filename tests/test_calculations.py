import os
import sys
import pandas as pd
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from energy_site import InvalidDataError, SolarFarm, WindFarm


def test_calculate_yield_gap_and_performance_ratio():
    """Verify yield gap and performance ratio calculations."""
    site = SolarFarm("Test Solar", 100)
    site.data = pd.DataFrame(
        {
            "actual_output_kw": [80, 45],
            "expected_power_kw": [100, 50],
        }
    )

    results = site.calculate_yield_gap()

    assert results["yield_gap_kw"].tolist() == [20, 5]
    assert results["performance_ratio"].tolist() == [0.8, 0.9]


def test_sample_column_names_are_normalized(monkeypatch):
    """Verify sample CSV column names are converted to internal names."""
    sample_data = pd.DataFrame(
        {
            "actual_output_kw": [50],
            "expected_power_kw": [100],
            "irradiance_w_m2": [700],
            "wind_speed_m_s": [8],
        }
    )
    monkeypatch.setattr(pd, "read_csv", lambda file_path: sample_data)
    from pathlib import Path
    monkeypatch.setattr(Path, "exists", lambda self: True)

    site = SolarFarm("Schema Test", 100)
    site.load_data("fake_path.csv")

    assert "irradiance_wm2" in site.data.columns
    assert "wind_speed_ms" in site.data.columns


def test_negative_output_raises_invalid_data_error(monkeypatch):
    """Verify invalid negative energy output is rejected."""
    invalid_data = pd.DataFrame({"actual_output_kw": [-10], "expected_power_kw": [100]})
    monkeypatch.setattr(pd, "read_csv", lambda file_path: invalid_data)
    from pathlib import Path
    monkeypatch.setattr(Path, "exists", lambda self: True)

    site = SolarFarm("Invalid Solar", 100)

    with pytest.raises(InvalidDataError):
        site.load_data("fake_path.csv")


def test_adding_solar_farms_combines_capacity():
    """Verify the overloaded + operator combines solar site capacity."""
    first_site = SolarFarm("East Array", 150)
    second_site = SolarFarm("West Array", 200)

    combined_site = first_site + second_site

    assert combined_site.name == "Combined: East Array & West Array"
    assert combined_site.capacity_kw == 350
    combined_str = str(combined_site)
    assert "East Array" in combined_str and "West Array" in combined_str
    assert "350" in combined_str


def test_len_returns_zero_when_no_data_loaded():
    """len(site) should return 0 before load_data is called."""
    site = SolarFarm("Empty Site", 100)
    assert len(site) == 0


def test_str_includes_panel_efficiency_for_solar():
    """SolarFarm's __str__ should include panel efficiency."""
    site = SolarFarm("Solar Test", 100, panel_efficiency=0.22)
    assert "22%" in str(site)


def test_str_includes_cut_speeds_for_wind():
    """WindFarm's __str__ should include cut-in and cut-out speeds."""
    site = WindFarm("Wind Test", 500, cut_in_speed=3.5, cut_out_speed=24.0)
    text = str(site)
    assert "3.5" in text
    assert "24.0" in text


def test_load_data_raises_for_missing_file(tmp_path):
    """load_data should raise FileNotFoundError when the CSV doesn't exist."""
    site = SolarFarm("Missing", 100)
    bad_path = tmp_path / "does_not_exist.csv"
    with pytest.raises(FileNotFoundError):
        site.load_data(str(bad_path))


def test_adding_wind_farms_combines_capacity():
    """Two wind farms can be combined with +, capacities should add."""
    a = WindFarm("North Ridge", 400)
    b = WindFarm("South Ridge", 600)
    combined = a + b
    assert combined.capacity_kw == 1000
    assert "North Ridge" in combined.name
    assert "South Ridge" in combined.name


def test_cannot_add_solar_to_wind():
    """Adding a SolarFarm and WindFarm should raise TypeError."""
    solar = SolarFarm("S", 100)
    wind = WindFarm("W", 100)
    with pytest.raises(TypeError):
        _ = solar + wind
