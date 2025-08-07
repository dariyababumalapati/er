import pandas as pd
from pathlib import Path

from utils import write_json, read_json

DATA_DIR = Path("data")

def extract_building_data(df: pd.DataFrame, building_id: str) -> dict:
    df.iloc[:, 0] = df.iloc[:, 0].ffill()
    match_rows = df[df.iloc[:, 0].astype(str).str.upper() == building_id.upper()]
    if match_rows.empty:
        return {}

    row_idx = match_rows.index[0]
    label_row = df.iloc[row_idx]
    ci_row = df.iloc[row_idx + 1] if row_idx + 1 < len(df) else None
    building_id_col = df.columns[0]
    result = {}

    for col in df.columns:
        if col == building_id_col:
            continue

        field, _ = col
        if 'Unnamed' in str(field) or pd.isna(field):
            continue

        key = str(field).strip()
        label_val = label_row[col]
        ci_val = ci_row[col] if ci_row is not None else None

        if pd.notna(label_val):
            try:
                ci_val = float(ci_val) if pd.notna(ci_val) else None
            except:
                ci_val = None

            result[key] = [str(label_val), ci_val]

    return {building_id: {k: v for k, v in result.items() if v[1] is not None}}


def extract_all_buildings(excel_path: str) -> dict:
    df = pd.read_excel(excel_path, header=[0, 1], sheet_name=3)
    df.iloc[:, 0] = df.iloc[:, 0].ffill()
    building_ids = df[df.columns[0]].dropna().astype(str).str.upper().unique()

    all_data = {}
    for building_id in building_ids:
        if building_id.upper() == "EDIFICIO":
            continue
        building_dict = extract_building_data(df, building_id)
        if building_dict:
            all_data.update(building_dict)

    return all_data


def load_or_cache_building_data(excel_path: str, cache_path: Path = DATA_DIR / "all_buildings.json") -> dict:
    if cache_path.exists():
        return read_json(cache_path)
    else:
        all_data = extract_all_buildings(excel_path)
        write_json(all_data, cache_path)
        return all_data

def extract_building_addresses(excel_path: str, sheet_index: int = 4) -> dict:
    # Read Sheet 4 (index 3)
    df = pd.read_excel(excel_path, sheet_name=sheet_index)

    # Normalize column names just in case
    df.columns = [col.strip() for col in df.columns]

    # Expected column names
    id_col = "Nome edificio"
    address_col = "Indirizzo"

    # Drop rows with missing IDs or addresses
    df = df.dropna(subset=[id_col, address_col])

    # Create the dictionary
    address_dict = dict(zip(df[id_col].astype(str).str.strip(), df[address_col].astype(str).str.strip()))

    return address_dict

if __name__ == "__main__":
    excel_path = DATA_DIR / "xdb.xlsx"
    json_path = DATA_DIR / "all_buildings2.json"
    building_data_dict = load_or_cache_building_data(excel_path, json_path)
