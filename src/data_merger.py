from pathlib import Path
from utils import read_json, write_json

# Define data directory path
DATA_DIR = Path("data")

def merge_building_addresses(
    buildings_path: Path = DATA_DIR / "all_buildings.json",
    address_path: Path = DATA_DIR / "building_addresses.json",
    output_path: Path = DATA_DIR / "updated_buildings.json"
) -> dict:
    """
    Merges address data into each building's entry, placing 'address' as the first field.
    If an address is missing, defaults to 'Unknown'.

    Returns the updated building dictionary.
    """
    # Load data from JSON files
    address_dict = read_json(address_path)
    buildings_dict = read_json(buildings_path)

    updated_dict = {}

    for building_id, b_data in buildings_dict.items():
        address = address_dict.get(building_id, "Unknown")

        # Create new dict with address as the first key
        new_data = {"address": address}
        new_data.update(b_data)

        updated_dict[building_id] = new_data

    # Save the result to output_path
    write_json(updated_dict, output_path)
    return updated_dict


if __name__ == "__main__":
    print("Running src/data_merger.py as a script...")
    # merged = merge_building_addresses()
    # print(f"Merged {len(merged)} buildings with addresses.")
