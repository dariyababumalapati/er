from utils import write_json, read_json

adress_json = "data/building_addresses.json"
buildings_json = "data/all_buildings.json"

address_dict = read_json(adress_json)
buildings_dict = read_json(buildings_json)
output_json = "data/updated_buildings.json"

# print(buildings_dict['148A'])

for building_id, b_data in buildings_dict.items():
    if building_id in address_dict:
        b_data['address'] = address_dict[building_id]
    else:
        b_data['address'] = "Unknown"

    write_json(buildings_dict, output_json)

