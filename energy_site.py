import numpy as np
import pandas as pd
from pathlib import Path
from utils import InvalidDataError, logger


class EnergySite:
    """Base class for a renewable energy site."""

    def __init__(self, name, capacity_kw):
        self.name = name
        self.capacity_kw = capacity_kw
        self.data = None

    def __str__(self):
        """Return a readable summary of the energy site."""
        rows = len(self.data) if self.data is not None else 0
        return f"{type(self).__name__}('{self.name}', {self.capacity_kw} kW, {rows} rows loaded)"

    def __repr__(self):
        """Developer-facing representation. Useful for debugging in the
        Python shell where __str__ would be too long."""
        return f"{type(self).__name__}(name={self.name!r}, capacity_kw={self.capacity_kw})"

    def __len__(self):
        """Return the number of loaded data rows."""
        if self.data is None:
            return 0
        return len(self.data)

    @logger
    def load_data(self, file_path):
        """Load the CSV file and do a few basic cleanup checks."""
        # Check the file actually exists before pandas tries to open it.
        # This gives a clearer error than pandas would.
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Could not find data file: {file_path}")

        data = pd.read_csv(file_path)

        if data.empty:
            raise InvalidDataError("The CSV file is empty.")

        if "timestamp" in data.columns:
            data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")

        data = data.rename(
            columns={
                "irradiance_w_m2": "irradiance_wm2",
                "wind_speed_m_s": "wind_speed_ms",
            }
        )

        numeric_columns = data.select_dtypes(include=["number"]).columns
        data[numeric_columns] = data[numeric_columns].fillna(0)

        output_columns = [column for column in ("actual_output_kw", "power_output_kw") if column in data.columns]
        for column in output_columns:
            if (data[column] < 0).any():
                raise InvalidDataError("Power output cannot be negative.")

        self.data = data
        return self.data

    def calculate_yield_gap(self):
        """Calculate yield gap and performance ratio for loaded data."""
        if self.data is None:
            raise InvalidDataError("Load data before calculating yield gap.")

        if "actual_output_kw" not in self.data.columns:
            raise InvalidDataError("Missing required column: actual_output_kw")

        if "expected_power_kw" not in self.data.columns:
            raise InvalidDataError("Missing required column: expected_power_kw")

        self.data["yield_gap_kw"] = self.data["expected_power_kw"] - self.data["actual_output_kw"]
        self.data["performance_ratio"] = np.where(
            self.data["expected_power_kw"] > 0,
            self.data["actual_output_kw"] / self.data["expected_power_kw"],
            0,
        )
        
        return self.data


class SolarFarm(EnergySite):
    """Solar site with a simple irradiance-based expected power model."""

    def __init__(self, name, capacity_kw, panel_efficiency=0.20):
        super().__init__(name, capacity_kw)
        self.panel_efficiency = panel_efficiency

    def __str__(self):
        """Solar-specific string. Shows panel efficiency too."""
        base = super().__str__()
        return f"{base[:-1]}, panel_eff={self.panel_efficiency:.0%})"

    def estimate_expected_power(self):
        """Estimate solar output from irradiance if expected power is not already listed."""
        if self.data is None:
            raise InvalidDataError("Load data before estimating solar output.")

        if "irradiance_wm2" not in self.data.columns:
            raise InvalidDataError("Missing required column for solar data: irradiance_wm2")

        irradiance_ratio = self.data["irradiance_wm2"].clip(lower=0) / 1000
        expected = self.capacity_kw * irradiance_ratio * self.panel_efficiency / 0.20
        self.data["expected_power_kw"] = expected.clip(lower=0, upper=self.capacity_kw)
        return self.data["expected_power_kw"]

    def __add__(self, other):
        """Let two solar farms be combined with the + operator."""
        if not isinstance(other, SolarFarm):
            raise TypeError("Can only add two SolarFarm objects.")

        new_name = f"Combined: {self.name} & {other.name}"
        new_capacity = self.capacity_kw + other.capacity_kw
        return SolarFarm(new_name, new_capacity, self.panel_efficiency)


class WindFarm(EnergySite):
    """Wind site with a basic cut-in and rated-speed model."""

    def __init__(self, name, capacity_kw, cut_in_speed=3.0, rated_speed=12.0, cut_out_speed=25.0):
        super().__init__(name, capacity_kw)
        self.cut_in_speed = cut_in_speed
        self.rated_speed = rated_speed
        self.cut_out_speed = cut_out_speed

    def __str__(self):
        """Wind-specific string. Shows cut-in and cut-out speeds."""
        base = super().__str__()
        return f"{base[:-1]}, cut-in={self.cut_in_speed} m/s, cut-out={self.cut_out_speed} m/s)"

    def estimate_expected_power(self):
        """Estimate wind output from wind speed if expected power is not already listed."""
        if self.data is None:
            raise InvalidDataError("Load data before estimating wind output.")

        if "wind_speed_ms" not in self.data.columns:
            raise InvalidDataError("Missing required column for wind data: wind_speed_ms")

        wind_speed = self.data["wind_speed_ms"].to_numpy(dtype=float)
        if (wind_speed < 0).any():
            raise InvalidDataError("Wind speed cannot be negative.")

        expected = np.zeros_like(wind_speed, dtype=float)
        ramp_mask = (wind_speed >= self.cut_in_speed) & (wind_speed < self.rated_speed)
        rated_mask = (wind_speed >= self.rated_speed) & (wind_speed <= self.cut_out_speed)

        expected[ramp_mask] = self.capacity_kw * (
            (wind_speed[ramp_mask] - self.cut_in_speed)
            / (self.rated_speed - self.cut_in_speed)
        ) ** 3
        expected[rated_mask] = self.capacity_kw

        self.data["expected_power_kw"] = expected
        return self.data["expected_power_kw"]

    def __add__(self, other):
        """Let two wind farms be combined with the + operator."""
        if not isinstance(other, WindFarm):
            raise TypeError("Can only add two WindFarm objects.")

        new_name = f"Combined: {self.name} & {other.name}"
        new_capacity = self.capacity_kw + other.capacity_kw
        return WindFarm(new_name, new_capacity, self.cut_in_speed, self.rated_speed, self.cut_out_speed)
