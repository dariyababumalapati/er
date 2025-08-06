# 🏗️ Building Report Automation Tool — Development Plan

## 🚧 PHASE 0: Project Setup
> Prepare folder structure and tools

### Tasks:
- [x] Create project folders using Bash (`/src`, `/data`, `/output`, etc.)
- [x] Initialize Git repo and add `.gitignore`
- [x] Set up `requirements.txt`
- [x] Create starter Python files:
  - `main.py`
  - `excel_reader.py`
  - `matrix_mapper.py`
  - `report_generator.py`

---

## 📊 PHASE 1: Read and Parse Excel File
> Extract building identifiers and data

### Tasks:
- [ ] Use `pandas` to read `Scheda per software.xlsx`
- [ ] Extract building IDs (e.g. `148A`, `150A`) from relevant column
- [ ] Store each building’s data as a Python `dict`
- [ ] Add function: `get_building_list()` and `get_building_data(building_id)`

---

## 🧩 PHASE 2: Matrix Mapping Logic
> Match building attributes to vulnerability matrix

### Tasks:
- [ ] Design or import a fixed vulnerability matrix (as JSON, dictionary, or table)
- [ ] Write function to map building data to corresponding matrix values
- [ ] Highlight chosen values (keep track of selected row/cell)
- [ ] Compute `Fj * Ci` and total score
- [ ] Create data structure for export (e.g., `MatrixResult` object)

---

## 📄 PHASE 3: Generate Report (.docx / PDF)
> Build and export a well-formatted report

### Tasks:
- [ ] Use `python-docx` to generate Word report:
  - [ ] Insert building metadata
  - [ ] Insert vulnerability matrix with highlights
  - [ ] Show `Fj * Ci` row and total
- [ ] Optional: use `docx2pdf` to convert to PDF
- [ ] Save report in `/output/` folder

---

## 🧪 PHASE 4: Testing & Debugging
> Make sure each module works as expected

### Tasks:
- [ ] Write simple test functions or use `pytest`
- [ ] Check:
  - [ ] Excel parsing
  - [ ] Matrix mapping logic
  - [ ] Word/PDF generation
- [ ] Validate formatting, highlighting, and computed values

---

## 🎛️ PHASE 5: CLI User Interface
> Create an interactive script to guide the user

### Tasks:
- [ ] In `main.py`:
  - [ ] Show list of buildings
  - [ ] Let user select one
  - [ ] Generate report for that building
- [ ] Add error handling:
  - [ ] Invalid selections
  - [ ] Missing data
- [ ] Print report location after generation

---

## 🚀 PHASE 6: (Optional) Advanced Features
> Add polish and power

### Ideas:
- [ ] Batch report generation (generate all at once)
- [ ] Use a template `.docx` with styles/logos
- [ ] GUI interface (e.g., Flask or tkinter)
- [ ] Logging module for traceability
- [ ] Configuration file (`config.json`) for settings

---

## 📁 Example File Output
