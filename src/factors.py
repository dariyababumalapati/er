from utils import read_json, write_json
from fj_weights import FJ_WEIGHTS

def extract_factor_data(building_data: dict, fj_weights: dict = FJ_WEIGHTS) -> dict:
    data = {}
    total = 0
    index = 1

    SECTION_GROUPS = {
        "EDIFICIO": [
            "Struttura", "Fondazioni", "Numero Piani",
            "Dimensioni in Pianta Rapporto tra Profondità e Fronte Tracciato 1/b",
            "Confini in Pianta", "Quadro Fessurativo", "Destinazione d'uso"
        ],
        "SOTTOSUOLO": [
            "Relazione terreni di fondazione-terreni attraversati",
            "piezometrica correlata al tracciato",
            "cavità in funzione del tracciato"
        ]
    }

    for section, factors in SECTION_GROUPS.items():
        for factor in factors:
            if factor not in building_data:
                continue

            label, ci = building_data[factor]
            fj = fj_weights.get(factor)

            if fj is None or ci is None:
                continue

            label_ci_text = f"{label}\n{ci}"
            val = round(fj * ci, 3)
            total += val

            data[f"f{index}"] = label_ci_text
            data[f"v{index}"] = str(val)

            index += 1

    data["total"] = str(round(total, 3))
    return data

if __name__ == "__main__":
    code = '151A'  # Example building code
    BUILDING_CODE = code
    BUILDING_JSON_PATH = "data/updated_buildings.json"
    OUTPUT_JSON_PATH = f"data/factor_data_{code}.json"

    building_data = read_json(BUILDING_JSON_PATH).get(BUILDING_CODE, {})
    factor_data = extract_factor_data(building_data)

    write_json(factor_data, OUTPUT_JSON_PATH)  # ✅ correct argument order
