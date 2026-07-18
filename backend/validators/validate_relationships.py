from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
MASTER_DIR = BASE_DIR / "datasets" / "masters"

CASE_MASTER = pd.read_csv(MASTER_DIR / "case_master.csv")
INVESTIGATION_MASTER = pd.read_csv(MASTER_DIR / "investigation_master.csv")
ARREST_MASTER = pd.read_csv(MASTER_DIR / "arrest_master.csv")
ACCUSED_MASTER = pd.read_csv(MASTER_DIR / "accused_master.csv")
CHARGESHEET_MASTER = pd.read_csv(MASTER_DIR / "chargesheet_master.csv")
OCCURRENCE_MASTER = pd.read_csv(MASTER_DIR / "inv_occurrence_master.csv")

print(f"Cases: {len(CASE_MASTER)}")
print(f"Investigations: {len(INVESTIGATION_MASTER)}")
print(f"Arrests: {len(ARREST_MASTER)}")
print(f"Accused: {len(ACCUSED_MASTER)}")
print(f"Chargesheets: {len(CHARGESHEET_MASTER)}")
print(f"Occurrences: {len(OCCURRENCE_MASTER)}")

print("\n========== RELATIONSHIP VALIDATION ==========\n")

# Rule 1: Every case should have exactly one investigation
investigation_counts = (
    INVESTIGATION_MASTER
    .groupby("case_id")
    .size()
)

missing_cases = set(CASE_MASTER["case_id"]) - set(investigation_counts.index)

duplicate_cases = investigation_counts[investigation_counts > 1]

if len(missing_cases) == 0:
    print("✅ Every case has an investigation.")
else:
    print(f"❌ Cases without investigation: {len(missing_cases)}")
    print(list(missing_cases)[:10])

if duplicate_cases.empty:
    print("✅ No case has multiple investigations.")
else:
    print(f"❌ Cases with multiple investigations: {len(duplicate_cases)}")
    print(duplicate_cases.head(10))

# Rule 2: Arrest consistency

arrested_accused = set(
    ACCUSED_MASTER.loc[
        ACCUSED_MASTER["is_arrested"] == True,
        "accused_person_id"
    ]
)

arrest_records = set(
    ARREST_MASTER["accused_person_id"]
)

missing_arrests = arrested_accused - arrest_records

extra_arrests = arrest_records - arrested_accused

if len(missing_arrests) == 0:
    print("✅ Every arrested accused has an arrest record.")
else:
    print(f"❌ Arrested accused without arrest record: {len(missing_arrests)}")
    print(list(missing_arrests)[:10])

if len(extra_arrests) == 0:
    print("✅ No invalid arrest records found.")
else:
    print(f"❌ Arrest records exist for non-arrested accused: {len(extra_arrests)}")
    print(list(extra_arrests)[:10])

# Rule 3: Cases with "Charge Sheet Filed" must have a chargesheet

chargesheet_cases = set(
    CASE_MASTER.loc[
        CASE_MASTER["case_status"] == "Charge Sheet Filed",
        "case_id"
    ]
)

chargesheet_records = set(
    CHARGESHEET_MASTER["case_id"]
)

missing_chargesheets = chargesheet_cases - chargesheet_records

extra_chargesheets = chargesheet_records - chargesheet_cases

if len(missing_chargesheets) == 0:
    print("✅ Every 'Charge Sheet Filed' case has a chargesheet.")
else:
    print(f"❌ Cases marked 'Charge Sheet Filed' without chargesheet: {len(missing_chargesheets)}")
    print(list(missing_chargesheets)[:10])

if len(extra_chargesheets) == 0:
    print("✅ No unnecessary chargesheet records found.")
else:
    print(f"❌ Chargesheets exist for cases not marked 'Charge Sheet Filed': {len(extra_chargesheets)}")
    print(list(extra_chargesheets)[:10])