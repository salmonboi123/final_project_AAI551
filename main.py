from energy_site import SolarFarm, WindFarm
from utils import data_chunk_generator

def main():
    print("--- REEA System Initialized ---")
    
    # Example Setup
    site_a = SolarFarm("North Field", 500)
    site_b = SolarFarm("South Field", 300)
    
    # Test Operator Overloading
    mega_site = site_a + site_b
    print(f"Created {mega_site.name} with capacity {mega_site.capacity_kw}kW")

    # Example Generator usage
    # gen = data_chunk_generator('data/sample_data.csv')
    # first_batch = next(gen)

if __name__ == "__main__":
    main()