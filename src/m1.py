from pathlib import Path
from docxtpl import DocxTemplate
from template_context import get_template_context, add_factors_to_context
from factors import extract_factor_data
from report_generator import get_risk_level_label
from utils import read_json

def generate_report_for_building(building_code: str, output_path: Path) -> bool:
    DATA_DIR = Path("data")
    TEMPLATE_PATH = DATA_DIR / "building_template.docx"
    BUILDING_JSON_PATH = DATA_DIR / "updated_buildings.json"

    # === STEP 1: Load base context (main variables) ===
    context = get_template_context(building_code, json_path=BUILDING_JSON_PATH)

    # === STEP 2: Generate factor/value fields ===
    all_buildings = read_json(BUILDING_JSON_PATH)
    building_data = all_buildings.get(building_code, {})
    if not building_data:
        return False

    factors_dict = extract_factor_data(building_data)
    risk_level = get_risk_level_label(float(factors_dict.get("total", 0)))
    context["RISK"] = risk_level["label"]

    # Add F1, V1, ..., TOTAL to context
    for key, value in factors_dict.items():
        context[key.upper()] = value

    # === STEP 3: Render template ===
    doc = DocxTemplate(TEMPLATE_PATH)
    doc.render(context)

    # === STEP 4: Save output ===
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)

    print(f"✅ Report generated for building {building_code}: {output_path}")
    return True

# If needed for CLI execution
if __name__ == "__main__":
    from sys import argv
    if len(argv) != 3:
        print("Usage: python main.py <BUILDING_CODE> <OUTPUT_PATH>")
    else:
        code = argv[1]
        out_path = Path(argv[2])
        success = generate_report_for_building(code, out_path)
        if not success:
            print(f"❌ Failed to generate report for {code}")
