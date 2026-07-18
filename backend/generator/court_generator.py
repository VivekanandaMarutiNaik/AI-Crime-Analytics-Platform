from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

DISTRICT_FILE = (
    BASE_DIR
    / "datasets"
    / "raw"
    / "districts.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "datasets"
    / "masters"
    / "court_master.csv"
)

districts = pd.read_csv(DISTRICT_FILE)

courts = []

COURT_TYPES = [
    "District and Sessions Court",
    "Senior Civil Court",
    "Civil Judge and JMFC Court",
    "Family Court",
    "Special Court",
]

court_id = 1

for _, district in districts.iterrows():

    district_name = district["district_name"]

    for court_type in COURT_TYPES:

        courts.append({
            "court_id": f"CRT{court_id:04d}",
            "court_name": f"{district_name} {court_type}",
            "district": district_name,
            "court_type": court_type,
        })

        court_id += 1

court_df = pd.DataFrame(courts)

court_df.to_csv(
    OUTPUT_FILE,
    index=False,
)

print(court_df.head())

print(f"\nGenerated {len(court_df)} courts.")

print(f"Saved to {OUTPUT_FILE}")