import random
from datetime import timedelta

import pandas as pd

# Load master datasets
CASE_MASTER = pd.read_csv("datasets/masters/case_master.csv")
INVESTIGATION_MASTER = pd.read_csv("datasets/masters/investigation_master.csv")
COURT_MASTER = pd.read_csv("datasets/masters/court_master.csv")
EMPLOYEE_MASTER = pd.read_csv("datasets/masters/employee_master.csv")

print(f"Cases loaded: {len(CASE_MASTER)}")
print(f"Investigations loaded: {len(INVESTIGATION_MASTER)}")
print(f"Courts loaded: {len(COURT_MASTER)}")
print(f"Employees loaded: {len(EMPLOYEE_MASTER)}")

# Store generated chargesheet records
chargesheets = []

# Generate Chargesheet ID
def generate_chargesheet_id(index):
    return f"CHG{index:06d}"

for index, investigation in INVESTIGATION_MASTER.iterrows():

    # Only cases marked as "Charge Sheet Filed" should have a chargesheet
    case = CASE_MASTER[
        CASE_MASTER["case_id"] == investigation["case_id"]
    ]

    if case.empty:
        continue

    case = case.iloc[0]

    if case["case_status"] != "Charge Sheet Filed":
        continue

    chargesheet_id = generate_chargesheet_id(len(chargesheets) + 1)

    case_id = investigation["case_id"]


    # Get district of the case
    district = case["district"]

    # Find courts in the same district
    district_courts = COURT_MASTER[
        COURT_MASTER["district"] == district
    ]

    # Skip if no court exists for the district
    if district_courts.empty:
        continue

    # Randomly assign one court
    court = district_courts.sample(1).iloc[0]

    court_id = court["court_id"]
    court_name = court["court_name"]

    # Investigation end date
    investigation_end_date = pd.to_datetime(
        investigation["investigation_end_date"]
    )

    # Chargesheet is filed 1–30 days after investigation completion
    filing_date = investigation_end_date + timedelta(
        days=random.randint(1, 30)
    )

    # Investigating Officer files the chargesheet
    filing_officer_id = investigation["investigating_officer_id"]

    # Chargesheet status
    chargesheet_status = random.choices(
        ["Filed", "Accepted", "Returned for Correction"],
        weights=[70, 25, 5],
        k=1
    )[0]

    # Add chargesheet record
    chargesheets.append({
        "chargesheet_id": chargesheet_id,
        "case_id": case_id,
        "court_id": court_id,
        "court_name": court_name,
        "filing_date": filing_date.strftime("%Y-%m-%d"),
        "filing_officer_id": filing_officer_id,
        "chargesheet_status": chargesheet_status
    })

# Create DataFrame
chargesheet_df = pd.DataFrame(chargesheets)

# Save to CSV
output_path = "datasets/masters/chargesheet_master.csv"
chargesheet_df.to_csv(output_path, index=False)

print(f"Generated {len(chargesheet_df)} chargesheet records.")
print(f"Saved to: {output_path}")