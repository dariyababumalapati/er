from pathlib import Path
from docxtpl import DocxTemplate

from template_context import get_template_context
from factors import extract_factor_data
from report_generator import get_risk_level
from utils import read_json

# === CONFIGURATION ===
BUILDING_CODE = "154A"
DATA_DIR = Path("data")
TEMPLATE_PATH = DATA_DIR / "building_template.docx"
BUILDING_JSON_PATH = DATA_DIR / "updated_buildings.json"
OUTPUT_DOCX_PATH = DATA_DIR / "final_reports" / f"{BUILDING_CODE}_report.docx"

# === STEP 1: Load base context ===
context = get_template_context(BUILDING_CODE, json_path=BUILDING_JSON_PATH)

# === STEP 2: Extract building data & factors ===
all_buildings = read_json(BUILDING_JSON_PATH)
building_data = all_buildings.get(BUILDING_CODE, {})
factors_dict = extract_factor_data(building_data)

# === STEP 3: Get risk level (plain + colored total) ===
risk_dict, rich_total = get_risk_level(float(factors_dict.get("total", 0)))


# === STEP 4: Add F1, V1, ..., TOTAL to context ===
for key, value in factors_dict.items():
    context[key.upper()] = value

context["RISK"] = risk_dict["label"]  # plain text for label
context["TOTAL"] = rich_total          # colored RichText for total value

# === STEP 5: Render template ===
doc = DocxTemplate(TEMPLATE_PATH)
doc.render(context)

# === STEP 6: Save output ===
OUTPUT_DOCX_PATH.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUTPUT_DOCX_PATH)

print(f"✅ Report generated for building {BUILDING_CODE}: {OUTPUT_DOCX_PATH}")
