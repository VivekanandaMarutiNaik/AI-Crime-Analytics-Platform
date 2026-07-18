from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

CRIME_FILE = (
    BASE_DIR
    / "datasets"
    / "raw"
    / "crime_cases.csv"
)

LAW_FILE = (
    BASE_DIR
    / "datasets"
    / "masters"
    / "crime_law_mapping.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "datasets"
    / "masters"
    / "case_master.csv"
)

crime_df = pd.read_csv(CRIME_FILE)
print(crime_df.columns.tolist())   # optional debug line
law_df = pd.read_csv(LAW_FILE)

case_df = crime_df.merge(
    law_df,
    on="crime_type",
    how="left",
)

case_master = pd.DataFrame({
    "case_id": case_df["crime_id"],
    "crime_datetime": case_df["crime_datetime"],
    "district": case_df["district"],
    "taluk": case_df["taluk"],
    "police_station": case_df["police_station_name"],
    "crime_category": case_df["crime_category"],
    "crime_type": case_df["crime_type"],
    "crime_severity": case_df["crime_severity"],
    "case_status": case_df["case_status"],
    "fir_registered": case_df["fir_registered"],
    "act_id": case_df["act_id"],
    "section_id": case_df["section_id"],
})

case_master.to_csv(
    OUTPUT_FILE,
    index=False,
)

print(case_master.head())

print(f"\nGenerated {len(case_master)} cases.")

print(f"Saved to {OUTPUT_FILE}")