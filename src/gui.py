import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from main import generate_report_for_building
from utils import read_json

# === CONFIGURATION ===
BUILDING_JSON_PATH = Path("data/updated_buildings.json")

# === Load Building Codes from JSON ===
def load_building_codes(json_path: Path):
    data = read_json(json_path)
    return sorted(data.keys())

# === GUI Application ===
def run_gui():
    root = tk.Tk()
    root.title("Building Report Generator")
    root.geometry("800x400")

    # Label
    tk.Label(root, text="Select Building Code:", font=("Arial", 12)).pack(pady=10)

    # Dropdown + Search Bar
    building_codes = load_building_codes(BUILDING_JSON_PATH)
    selected_code = tk.StringVar()
    combo = ttk.Combobox(root, textvariable=selected_code, values=building_codes)
    combo.pack(pady=5)

    placeholder = "Search or type..."
    combo.set(placeholder)

    def on_focus_in(event):
        if selected_code.get() == placeholder:
            combo.set("")

    def on_focus_out(event):
        if selected_code.get() == "":
            combo.set(placeholder)

    combo.bind("<FocusIn>", on_focus_in)
    combo.bind("<FocusOut>", on_focus_out)

    # Generate Button
    def generate():
        code = selected_code.get()
        if code not in building_codes:
            messagebox.showerror("Invalid Code", "Please select a valid building code.")
            return

        initialfile = f"{code}_report.docx"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx")],
            title="Save Report As",
            initialfile=initialfile
        )
        if not file_path:
            return

        success = generate_report_for_building(code, Path(file_path))
        if success:
            messagebox.showinfo("Success", f"Report generated for building {code}.")
        else:
            messagebox.showerror("Error", f"Failed to generate report for {code}.")

    tk.Button(root, text="Generate Report", command=generate, bg="green", fg="white").pack(pady=20)

    root.mainloop()

# === Run GUI directly if this script is executed ===
if __name__ == "__main__":
    run_gui()
