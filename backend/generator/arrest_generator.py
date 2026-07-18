import random
from datetime import timedelta

import pandas as pd

# Load master datasets
CASE_MASTER = pd.read_csv("datasets/masters/case_master.csv")
INVESTIGATION_MASTER = pd.read_csv("datasets/masters/investigation_master.csv")
ACCUSED_MASTER = pd.read_csv("datasets/masters/accused_master.csv")
EMPLOYEE_MASTER = pd.read_csv("datasets/masters/employee_master.csv")

print(f"Cases loaded: {len(CASE_MASTER)}")
print(f"Investigations loaded: {len(INVESTIGATION_MASTER)}")
print(f"Accused loaded: {len(ACCUSED_MASTER)}")
print(f"Employees loaded: {len(EMPLOYEE_MASTER)}")

# Store generated arrest records
arrests = []

# Generate Arrest ID
def generate_arrest_id(index):
    return f"ARR{index:06d}"

for index, accused in ACCUSED_MASTER.iterrows():

    # Skip accused who were not arrested
    if not accused["is_arrested"]:
        continue

    arrest_id = generate_arrest_id(len(arrests) + 1)

    case_id = accused["case_id"]
    accused_person_id = accused["accused_person_id"]

    # Get investigation details for this case
    investigation = INVESTIGATION_MASTER[
        INVESTIGATION_MASTER["case_id"] == case_id
    ]

    # Skip if no investigation exists
    if investigation.empty:
        continue

    investigation = investigation.iloc[0]

    investigation_start_date = pd.to_datetime(
        investigation["investigation_start_date"]
    )

    investigating_officer_id = investigation["investigating_officer_id"]

    # Arrest takes place 0–30 days after investigation starts
    arrest_date = investigation_start_date + timedelta(
        days=random.randint(0, 30)
    )

    # Add arrest record
    arrests.append({
        "arrest_id": arrest_id,
        "case_id": case_id,
        "accused_person_id": accused_person_id,
        "arrest_date": arrest_date.strftime("%Y-%m-%d"),
        "arresting_officer_id": investigating_officer_id
    })

# Create DataFrame
arrest_df = pd.DataFrame(arrests)

# Save to CSV
output_path = "datasets/masters/arrest_master.csv"
arrest_df.to_csv(output_path, index=False)

print(f"Generated {len(arrest_df)} arrest records.")
print(f"Saved to: {output_path}")