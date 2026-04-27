import pandas as pd
import numpy as np
from utils import logger, InvalidDataError

class EnergySite:
    def __init__(self, name, capacity_kw):
        self.name = name
        self.capacity_kw = capacity_kw
        self.data = None

    @logger
    def load_data(self, file_path):
        """Loads CSV into a DataFrame."""
        # Member 1 logic here
        pass

    def calculate_yield_gap(self):
        """Vectorized math using NumPy."""
        # Member 2 logic here
        pass

class SolarFarm(EnergySite):
    def __init__(self, name, capacity_kw, panel_efficiency=0.20):
        super().__init__(name, capacity_kw)
        self.panel_efficiency = panel_efficiency

    def __add__(self, other):
        """Operator Overloading: Adds two SolarFarms together."""
        if not isinstance(other, SolarFarm):
            raise TypeError("Can only add two SolarFarm objects.")
        new_name = f"Combined: {self.name} & {other.name}"
        new_capacity = self.capacity_kw + other.capacity_kw
        return SolarFarm(new_name, new_capacity)

class WindFarm(EnergySite):
    def __init__(self, name, capacity_kw, cut_in_speed=3.0):
        super().__init__(name, capacity_kw)
        self.cut_in_speed = cut_in_speed