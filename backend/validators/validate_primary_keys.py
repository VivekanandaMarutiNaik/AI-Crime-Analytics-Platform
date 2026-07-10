from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
MASTER_DIR = BASE_DIR / "datasets" / "masters"

# Table -> Primary Key mapping
PRIMARY_KEYS = {
    "case_master.csv": "case_id",
    "complainant_master.csv": "complainant_id",
    "victim_master.csv": "victim_id",
    "accused_master.csv": "accused_person_id",
    "investigation_master.csv": "investigation_id",
    "arrest_master.csv": "arrest_id",
    "chargesheet_master.csv": "chargesheet_id",
    "employee_master.csv": "employee_id",
    "court_master.csv": "court_id",
    "act_master.csv": "act_id",
    "section_master.csv": "section_id",
    "occupation_master.csv": "occupation_id",
    "religion_master.csv": "religion_id",
    "caste_master.csv": "caste_id",
    "case_status_master.csv": "case_status_id",
}

for file_name, primary_key in PRIMARY_KEYS.items():

    file_path = MASTER_DIR / file_name

    if not file_path.exists():
        print(f"❌ Missing file: {file_name}")
        continue

    df = pd.read_csv(file_path)

    print(f"\nChecking {file_name}...")

    # Check if primary key column exists
    if primary_key not in df.columns:
        print(f"❌ Primary key '{primary_key}' not found.")
        continue

    # Check for missing primary keys
    missing_count = df[primary_key].isna().sum()

    if missing_count > 0:
        print(f"❌ Missing primary keys: {missing_count}")
    else:
        print("✅ No missing primary keys.")

    # Check for duplicate primary keys
    duplicate_count = df[primary_key].duplicated().sum()

    if duplicate_count > 0:
        print(f"❌ Duplicate primary keys: {duplicate_count}")

        duplicates = df[df[primary_key].duplicated(keep=False)]
        print(duplicates[[primary_key]])
    else:
        print("✅ No duplicate primary keys.")