import pandas as pd
import pytest

from energy_site import InvalidDataError, SolarFarm


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

    site = SolarFarm("Schema Test", 100)
    site.load_data("fake_path.csv")

    assert "irradiance_wm2" in site.data.columns
    assert "wind_speed_ms" in site.data.columns


def test_negative_output_raises_invalid_data_error(monkeypatch):
    """Verify invalid negative energy output is rejected."""
    invalid_data = pd.DataFrame({"actual_output_kw": [-10], "expected_power_kw": [100]})
    monkeypatch.setattr(pd, "read_csv", lambda file_path: invalid_data)

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
    assert str(combined_site) == "Combined: East Array & West Array (350 kW)"
