import random
from datetime import timedelta

import pandas as pd

# Load master datasets
CASE_MASTER = pd.read_csv("datasets/masters/case_master.csv")
EMPLOYEE_MASTER = pd.read_csv("datasets/masters/employee_master.csv")

print(f"Cases loaded: {len(CASE_MASTER)}")
print(f"Employees loaded: {len(EMPLOYEE_MASTER)}")

# Store generated investigation records
investigations = []

# Generate Investigation ID
def generate_investigation_id(index):
    return f"INV{index:06d}"

for index, case in CASE_MASTER.iterrows():
    investigation_id = generate_investigation_id(index + 1)

    # Get police station name from the case
    police_station_name = case["police_station"]

    # Find employees posted in the same police station
    station_employees = EMPLOYEE_MASTER[
        EMPLOYEE_MASTER["police_station_name"] == police_station_name
    ]

    # If no employees are found, skip this case
    if station_employees.empty:
        continue

    # Randomly assign one investigating officer
    investigating_officer_id = station_employees.sample(1).iloc[0]["employee_id"]

    # Crime date and time
    crime_datetime = pd.to_datetime(case["crime_datetime"])

    # Investigation starts 0–3 days after the crime
    investigation_start_date = crime_datetime + timedelta(days=random.randint(0, 3))

    # Investigation status depends on case status
    case_status = case["case_status"]

    if case_status == "Under Investigation":
        investigation_status = "Ongoing"

    elif case_status == "Charge Sheet Filed":
        investigation_status = "Completed"

    elif case_status == "Pending Trial":
        investigation_status = "Completed"

    elif case_status == "Closed":
        investigation_status = "Closed"

    else:
        investigation_status = "Ongoing"

    # Investigation end date depends on investigation status
    if investigation_status == "Ongoing":
        investigation_end_date = None
    else:
        investigation_end_date = investigation_start_date + timedelta(
            days=random.randint(15, 180)
        )
    
    # Evidence collected (85% Yes)
    evidence_collected = random.choices(
        ["Yes", "No"],
        weights=[85, 15],
        k=1
    )[0]

    # Generate witness count
    witness_group = random.choices(
        ["low", "medium", "high"],
        weights=[20, 50, 30],
        k=1
    )[0]

    if witness_group == "low":
        witness_count = random.randint(0, 2)
    elif witness_group == "medium":
        witness_count = random.randint(3, 5)
    else:
        witness_count = random.randint(6, 10)

    # Whether forensic examination is required (35% Yes)
    forensic_required = random.choices(
        ["Yes", "No"],
        weights=[35, 65],
        k=1
    )[0]

    # Forensic completion depends on whether it was required
    if forensic_required == "Yes":
        forensic_completed = random.choices(
            ["Yes", "No"],
            weights=[90, 10],
            k=1
        )[0]
    else:
        forensic_completed = "No"

    # Generate remarks based on investigation status
    if investigation_status == "Completed":
        remarks = random.choice([
            "Investigation completed successfully.",
            "Evidence verified and case completed.",
            "Witness statements recorded.",
            "Charge sheet preparation underway."
        ])
    elif investigation_status == "Ongoing":
        remarks = random.choice([
            "Investigation in progress.",
            "Awaiting forensic report.",
            "Additional witnesses being examined.",
            "Evidence collection in progress."
        ])
    else:  # Closed
        remarks = random.choice([
            "Case closed due to insufficient evidence.",
            "Complaint found to be false.",
            "Investigation closed after verification."
        ])
    # Add investigation record
    investigations.append({
        "investigation_id": investigation_id,
        "case_id": case["case_id"],
        "investigating_officer_id": investigating_officer_id,
        "investigation_start_date": investigation_start_date.strftime("%Y-%m-%d"),
        "investigation_end_date": (
            investigation_end_date.strftime("%Y-%m-%d")
            if investigation_end_date is not None else None
        ),
        "investigation_status": investigation_status,
        "evidence_collected": evidence_collected,
        "witness_count": witness_count,
        "forensic_required": forensic_required,
        "forensic_completed": forensic_completed,
        "remarks": remarks
    })

# Create DataFrame
investigation_df = pd.DataFrame(investigations)

# Save to CSV
output_path = "datasets/masters/investigation_master.csv"
investigation_df.to_csv(output_path, index=False)

print(f"Generated {len(investigation_df)} investigation records.")
print(f"Saved to: {output_path}")