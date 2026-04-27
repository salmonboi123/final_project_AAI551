import pandas as pd
import numpy as np

# Create 24 hours of data
times = pd.date_range("2024-01-01", periods=24, freq="H")
data = {
    "timestamp": times,
    "actual_output_kw": np.random.uniform(50, 450, size=24),
    "irradiance_w_m2": np.random.uniform(200, 1000, size=24),
    "temperature_c": np.random.uniform(15, 35, size=24),
    "wind_speed_m_s": np.random.uniform(0, 20, size=24)
}

df = pd.DataFrame(data)
df.to_csv("data/sample_data.csv", index=False)
print("Dataset created: data/sample_data.csv")