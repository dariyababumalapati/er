from pathlib import Path
from docxtpl import RichText

from utils import read_json, write_json
from fj_weights import FJ_WEIGHTS

# Define data directory path
DATA_DIR = Path("data")

def generate_table_data(building_data: dict, fj_weights: dict) -> list:
    table = [[
        {"text": "FATTORI", "colspan": 2},
        {"text": "Fj"},
        {"text": "CAMPI (Ci)"},
        {"text": "Fj × Ci"}
    ]]

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

    total = 0
    for section, factors in SECTION_GROUPS.items():
        rowspan = len(factors)
        first = True

        for factor in factors:
            if factor not in building_data:
                continue

            label, ci = building_data[factor]
            fj = fj_weights.get(factor)

            if fj is None or ci is None:
                continue

            total += fj * ci

            row = []

            # First column: section header only once with rowspan
            if first:
                row.append({"text": section, "rowspan": rowspan})
                first = False
            else:
                row.append(None)

            # Fill the rest
            row.append({"text": factor})
            row.append({"value": fj})
            row.append({"text": f"{label}\n{ci}", "value": ci})
            row.append({
                "text": str(round(fj * ci, 3)),
                "value": round(fj * ci, 3),
                "color": "red"
            })

            table.append(row)

    total = round(total, 3)

    # Append the total row
    # table.append([
    #     {"text": "Indice di vulnerabilità V = Σ (Fj × Ci)", "colspan": 4},
    #     {"value": total},
    # ])

    # Define risk level
    risk_level = get_risk_level_label(total)
    risk_label = risk_level["label"]

    table.append([
        {
            "rich_text": [
                {"text": "Indice di vulnerabilità V = Σ (Fj × Ci)\n\n", "colspan": 4},
                {"text": "Livelli di rischio:\n", "bold": True},  # 🔹 Add this line
                {"text": "0 ≤ V < 4 = assente o lieve – ", "color": "gray"},
                # {"text": "assente o lieve – "},
                {"text": "4 ≤ V < 6 = moderato – ", "color": "green"},
                # {"text": "moderato – "},
                {"text": "6 ≤ V < 8 = significativo – ", "color": "blue"},
                # {"text": "significativo – "},
                {"text": "8 ≤ V ≤ 10 = elevato", "color": "red"},
                # {"text": "elevato"}
            ],
            "colspan": 4
        },
        {
            "rich_text": [
                {"text": f"{total}\n", "color": risk_level["color"], 'size': 20},
                # {"text": risk_level["label"], "color": risk_level["color"]}
            ]
        }
    ])

    return table, risk_label


def get_risk_level_label(v):
    if 0 <= v < 4:
        return {"label": "assente o lieve", "color": "gray"}
    elif 4 <= v < 6:
        return {"label": "moderato", "color": "green"}
    elif 6 <= v < 8:
        return {"label": "significativo", "color": "blue"}
    elif 8 <= v <= 10:
        return {"label": "elevato", "color": "red"}
    else:
        return {"label": "n/a", "color": "black"}

def get_risk_level(v):
    rt = RichText()
    val = str(round(v, 3))

    if 0 <= v < 4:
        color = "808080"  # gray
        label = "assente o lieve"
    elif 4 <= v < 6:
        color = "008000"  # green
        label = "moderato"
    elif 6 <= v < 8:
        color = "0070C0"  # blue
        label = "significativo"
    elif 8 <= v <= 10:
        color = "FF0000"  # red
        label = "elevato"
    else:
        color = "000000"  # black
        label = "n/a"

    rt.add(val, color=color, bold=True)
    return {"label": label, "color": color}, rt



if __name__ == "__main__":

    # Define input and output paths using pathlib
    input_file: Path = DATA_DIR / "updated_buildings.json"
    output_file: Path = DATA_DIR / "vt4.json"

    updated_buildings_data = read_json(input_file)

    building_data = updated_buildings_data.get("148A", {})

    # Generate the table
    table = generate_table_data(building_data, FJ_WEIGHTS)

    # Save to file using pathlib-compatible write_json
    write_json(table, output_file)
