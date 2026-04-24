# final_project_AAI551
Final Project Repo for AA1 551


# Renewable Energy Efficiency Analyzer (REEA)

**Course:** AAI/CPE/EE 551  
**Team Members:** Riley Parker, Tyler Komentani, and Bryan Barzola

## Project Overview
The **Renewable Energy Efficiency Analyzer (REEA)** is a Python-based tool designed to solve a critical engineering challenge: quantifying the impact of environmental variables on renewable energy output. While solar panels and wind turbines have theoretical "nameplate" capacities, real-world factors like temperature, irradiance, and wind speed fluctuations often lead to performance gaps.

REEA allows users to input energy datasets, automatically clean the data, calculate key efficiency metrics, and identify "underperformance events" where hardware may be failing or environmental conditions are sub-optimal.

## Core Features
- **Object-Oriented Design:** Modular class structure for different energy site types (Solar and Wind).
- **Efficiency Analytics:** Calculates "Yield Gaps" and "Performance Ratios" using NumPy for high-performance vector calculations.
- **Anomaly Detection:** Identifies "bad days" where production drops significantly below a rolling average.
- **Large Dataset Support:** Utilizes Python Generators to process massive time-series datasets without exhausting system memory.
- **Data Visualization:** Integrated Matplotlib plots to visualize Actual vs. Predicted output and efficiency correlations.

---

## Technical Implementation

### 1. Class Hierarchy (OOP)
- **`EnergySite` (Parent):** Manages basic site metadata (location, nameplate capacity) and CSV data ingestion via Pandas.
- **`SolarFarm` (Child):** Implements solar-specific logic, including temperature-adjusted performance ratios.
- **`WindFarm` (Child):** Handles wind-specific constraints such as "Cut-in" and "Cut-out" speed safety logic.

### 2. Advanced Python Functionality
- **Operator Overloading:** The `+` operator is overloaded to allow merging two `SolarFarm` or `WindFarm` objects into a single virtual site with combined capacity and data.
- **Decorators:** A custom `@logger` decorator tracks function execution and performance in the console.
- **Generators:** Data is yielded in chunks to ensure the program remains performant even with minute-by-minute annual data.

### 3. Data Science Stack
- **Pandas:** Used for timestamp alignment and data cleaning.
- **NumPy:** Handles the mathematical heavy lifting for theoretical vs. actual yield calculations.
- **Matplotlib:** Generates scatter plots and line graphs for performance analysis.

---

## Installation & Usage

### Prerequisites
- Python 3.8+
- Requirements: `pandas`, `numpy`, `matplotlib`, `pytest`

### Setup (NEED TO WORK ON)
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/REEA.git](https://github.com/your-username/REEA.git)
