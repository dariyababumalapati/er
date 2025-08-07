from pathlib import Path
from utils import read_json, write_json

DATA_PATH = Path("data/updated_buildings.json")

def get_template_context(building_code: str, json_path: Path = DATA_PATH) -> dict:
    """
    Extract context variables for docxtpl from the building JSON.

    Returns a dictionary like:
    {
        "NUMERO": "148",
        "LETTERA": "A",
        "ADDRESS": "Viale Carso 57"
    }
    """
    all_data = read_json(json_path)

    if building_code not in all_data:
        raise ValueError(f"Building code {building_code} not found in JSON data.")


    address = all_data[building_code].get("address", "N/A")
    destination_use = all_data[building_code].get("Destinazione d'uso", ["N/A"])[0]
    number_of_floors = all_data[building_code].get("Numero Piani", ["N/A"])[0]
    struttura = all_data[building_code].get("Struttura", ["N/A"])[0]
    fondazioni = all_data[building_code].get("Fondazioni", ["N/A"])[0]
    quadro_fessurativo = all_data[building_code].get("Quadro Fessurativo", ["N/A"])[0]

    return {
        "BUILDING_CODE": building_code,
        "ADDRESS": address,
        "DESTINATION_USE": destination_use,
        "NUMBER_OF_FLOORS": number_of_floors,
        "STRUTTURA": struttura,
        "FONDAZIONI": fondazioni,
        "QUADRO_FESSURATIVO": quadro_fessurativo,
        
    }

def add_factors_to_context(context: dict, f_v_dict: dict) -> dict:
    """
    Updates the context dictionary with factor and value fields.

    Example: Adds "F1": "label\nci", "V1": "fj*ci" from the f_v_dict.
    """
    for i in range(1, 11):  # Assuming 10 factors
        f_key = f"f{i}"
        v_key = f"v{i}"

        context[f"F{i}"] = f_v_dict.get(f_key, "N/A")
        context[f"V{i}"] = f_v_dict.get(v_key, "N/A")

    context["TOTAL"] = f_v_dict.get("total", "N/A")
    return context

if __name__ == "__main__":
    from utils import read_json

    BUILDING_CODE = "150A"
    FACTOR_PATH = Path("data/factor_data.json")

    base_context = get_template_context(BUILDING_CODE)
    f_v_data = read_json(FACTOR_PATH)

    full_context = add_factors_to_context(base_context, f_v_data)
    write_json(full_context, Path("data/full_context.json"))  # Save the context for debugging

    print(full_context)
