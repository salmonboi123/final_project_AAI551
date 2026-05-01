import argparse
from pathlib import Path

from energy_site import SolarFarm, WindFarm
from utils import data_chunk_generator


def build_site(args):
    """Create the right site object based on the option the user picked."""
    if args.solar:
        return SolarFarm(args.name, args.capacity)
    if args.wind:
        return WindFarm(args.name, args.capacity)
    raise ValueError("Choose either --solar or --wind.")


def run_analysis(args):
    """Load the selected dataset, run calculations, and print summary metrics."""
    site = build_site(args)
    site.load_data(args.file)

    if "expected_power_kw" not in site.data.columns:
        site.estimate_expected_power()

    results = site.calculate_yield_gap()

    avg_ratio = results["performance_ratio"].mean()
    avg_gap = results["yield_gap_kw"].mean()

    print("--- REEA System Initialized ---")
    print(f"Site: {site.name}")
    print(f"Capacity: {site.capacity_kw} kW")
    print(f"Rows analyzed: {len(site.data)}")
    print(f"Average performance ratio: {avg_ratio:.2f}")
    print(f"Average yield gap: {avg_gap:.2f} kW")

    if args.show_chunks:
        first_chunk = next(data_chunk_generator(args.file, chunk_size=5))
        print("\nFirst few rows from chunk generator:")
        print(first_chunk.head())


def parse_args():
    """Parse command-line options for the renewable energy analyzer."""
    parser = argparse.ArgumentParser(description="Renewable Energy Efficiency Analyzer")
    parser.add_argument("--file", required=True, help="Path to the input CSV file")
    parser.add_argument("--name", default="Demo Site", help="Name of the energy site")
    parser.add_argument("--capacity", type=float, required=True, help="Site capacity in kW")

    site_type = parser.add_mutually_exclusive_group(required=True)
    site_type.add_argument("--solar", action="store_true", help="Analyze the file as solar data")
    site_type.add_argument("--wind", action="store_true", help="Analyze the file as wind data")

    parser.add_argument("--show-chunks", action="store_true", help="Show a small example of chunk loading")
    return parser.parse_args()


def main():
    """Run the command-line version of the renewable energy analyzer."""
    args = parse_args()

    if not Path(args.file).exists():
        raise FileNotFoundError(f"Could not find input file: {args.file}")

    run_analysis(args)


if __name__ == "__main__":
    main()
