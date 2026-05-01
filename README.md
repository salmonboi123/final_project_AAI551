# Renewable Energy Efficiency Analyzer (REEA)

**Course:** AAI/CPE/EE 551  
**Team Members:** Riley Parker, Tyler Komentani, and Bryan Barzola

## Team Information

Before final submission, replace the placeholders below with each member's official Stevens information.

| Team Member | Email | Stevens ID | Main Contributions |
| --- | --- | --- | --- |
| Riley Parker | rparker3@stevens.edu | 20019955 | Project setup, renewable energy class design, README development |
| Tyler Komentani | tkometan@stevens.edu | 20024594 | Notebook workflow, pytest coverage, validation improvements |
| Bryan Barzola | bbarzola@stevens.edu | TODO | Dataset preparation, analysis review, documentation support |

## Project Overview

The Renewable Energy Efficiency Analyzer is a Python project that studies renewable energy site performance. It compares actual power output with expected power output, then calculates two key metrics:

- **Yield gap:** expected output minus actual output
- **Performance ratio:** actual output divided by expected output

This helps identify when a solar or wind energy site is producing less power than expected. The project uses a local CSV dataset, object-oriented design, NumPy calculations, and Pandas data processing.

## Dependencies

Use Python **3.12, 3.13, or 3.14**.

Required Python libraries:

- `pandas`
- `numpy`
- `pytest`

Install dependencies with:

```bash
python -m pip install pandas numpy pytest
```

## File Structure

```text
final_project_AAI551/
├── main.ipynb                 # Main notebook workflow for the assignment
├── main.py                    # Optional command-line runner
├── energy_site.py             # EnergySite, SolarFarm, and WindFarm classes
├── utils.py                   # Custom exception, logger decorator, CSV generator
├── data/
│   └── sample_data.csv        # Sample renewable energy dataset
└── tests/
    ├── test_calculations.py   # Pytest tests for calculations and validation
    └── generate_data.py       # Helper script for creating sample data
```

## How to Run

The required main workflow is in `main.ipynb`. Open the notebook and run each cell from top to bottom.

You can also run the command-line version:

```bash
python main.py --file data/sample_data.csv --name "Demo Solar Site" --capacity 500 --solar
```

To show an example of generator-based chunk loading:

```bash
python main.py --file data/sample_data.csv --name "Demo Solar Site" --capacity 500 --solar --show-chunks
```

## How to Test

Run the Pytest suite with:

```bash
python -m pytest tests -q
```

If Windows temp-folder permissions cause issues, use:

```bash
python -m pytest tests -q -p no:cacheprovider
```

## Requirement Coverage

- **Classes with inheritance:** `EnergySite` is the parent class; `SolarFarm` and `WindFarm` inherit from it.
- **Meaningful functions:** `build_site`, `run_analysis`, `data_chunk_generator`, and class methods perform project logic.
- **Advanced libraries:** Pandas loads and cleans CSV data; NumPy performs vectorized performance calculations.
- **Exception handling:** The project checks for missing files, empty data, missing required columns, and invalid negative output.
- **Data I/O:** The program reads `data/sample_data.csv`.
- **Loops and conditionals:** Loops are used in validation and generator processing; conditionals select site type and validate inputs.
- **Mutable and immutable types:** Lists, dictionaries, DataFrames, strings, numbers, and tuples are used throughout the project.
- **Operator overloading:** `__str__`, `__len__`, and `__add__` are implemented.
- **Part 2 features:** The project uses `__name__`, a generator function, built-in modules, and list comprehension.
