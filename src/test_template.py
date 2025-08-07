from docxtpl import DocxTemplate
from pathlib import Path
from template_context import get_template_context

# Load the template
template_path = Path("data/building_template.docx")
doc = DocxTemplate(template_path)

# Set the values for placeholders
building_code = "150A"
context = get_template_context(building_code)

# Render and save
doc.render(context)
output_path = Path("data/t6.docx")
doc.save(output_path)

print(f"Saved filled docx to: {output_path}")
