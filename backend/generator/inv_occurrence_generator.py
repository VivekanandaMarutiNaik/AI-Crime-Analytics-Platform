import random

import pandas as pd
from pathlib import Path



# Load master datasets
CASE_MASTER = pd.read_csv("datasets/masters/case_master.csv")

BASE_DIR = Path(__file__).resolve().parents[2]

CRIME_CASES = pd.read_csv(
    BASE_DIR / "datasets" / "raw" / "crime_cases.csv"
)
print(f"Cases loaded: {len(CASE_MASTER)}")
print(f"Crime records loaded: {len(CRIME_CASES)}")

crime_lookup = CRIME_CASES.set_index("crime_id").to_dict("index")

# Store generated occurrence records
occurrences = []

# Generate Occurrence ID
def generate_occurrence_id(index):
    return f"OCC{index:06d}"

for _, case in CASE_MASTER.iterrows():
    occurrence_id = generate_occurrence_id(len(occurrences) + 1)

    case_id = case["case_id"]

    # Get original crime record
    crime = crime_lookup.get(case_id)

    if crime is None:
        continue

    occurrences.append({
        "occurrence_id": occurrence_id,
        "case_id": case_id,
        "occurrence_datetime": crime["crime_datetime"],
        "time_slot": crime["time_slot"],
        "district": crime["district"],
        "taluk": crime["taluk"],
        "gram_panchayat": crime["gram_panchayat"],
        "village": crime["village"],
        "police_station": crime["police_station_name"],
        "crime_latitude": crime["crime_latitude"],
        "crime_longitude": crime["crime_longitude"]
    })

occurrence_df = pd.DataFrame(occurrences)

output_path = "datasets/masters/inv_occurrence_master.csv"
occurrence_df.to_csv(output_path, index=False)

print(f"Generated {len(occurrence_df)} occurrence records.")
print(f"Saved to: {output_path}")