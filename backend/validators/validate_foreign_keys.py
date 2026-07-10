from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
MASTER_DIR = BASE_DIR / "datasets" / "masters"

# Child Table, Foreign Key, Parent Table, Parent Key
FOREIGN_KEYS = [
    ("complainant_master.csv", "case_id", "case_master.csv", "case_id"),
    ("victim_master.csv", "case_id", "case_master.csv", "case_id"),
    ("accused_master.csv", "case_id", "case_master.csv", "case_id"),

    ("investigation_master.csv", "case_id", "case_master.csv", "case_id"),
    ("investigation_master.csv", "investigating_officer_id", "employee_master.csv", "employee_id"),

    ("arrest_master.csv", "case_id", "case_master.csv", "case_id"),
    ("arrest_master.csv", "accused_person_id", "accused_master.csv", "accused_person_id"),
    ("arrest_master.csv", "arresting_officer_id", "employee_master.csv", "employee_id"),

    ("chargesheet_master.csv", "case_id", "case_master.csv", "case_id"),
    ("chargesheet_master.csv", "court_id", "court_master.csv", "court_id"),
    ("chargesheet_master.csv", "filing_officer_id", "employee_master.csv", "employee_id"),

    ("crime_law_mapping.csv", "act_id", "act_master.csv", "act_id"),
    ("crime_law_mapping.csv", "section_id", "section_master.csv", "section_id"),
]

for child_file, foreign_key, parent_file, parent_key in FOREIGN_KEYS:

    print(f"\nChecking {child_file} -> {parent_file}")

    child_df = pd.read_csv(MASTER_DIR / child_file)
    parent_df = pd.read_csv(MASTER_DIR / parent_file)

    # Check if required columns exist
    if foreign_key not in child_df.columns:
        print(f"❌ Foreign key '{foreign_key}' not found in {child_file}")
        continue

    if parent_key not in parent_df.columns:
        print(f"❌ Parent key '{parent_key}' not found in {parent_file}")
        continue

    # Parent key values
    parent_values = set(parent_df[parent_key].dropna())

    # Child values
    child_values = child_df[foreign_key].dropna()

    # Find invalid foreign keys
    invalid_rows = child_df[~child_df[foreign_key].isin(parent_values)]

    if invalid_rows.empty:
        print(f"✅ {foreign_key} is valid.")
    else:
        print(f"❌ Invalid foreign keys found: {len(invalid_rows)}")

        print(
            invalid_rows[
                [foreign_key]
            ].drop_duplicates().head(10)
        )