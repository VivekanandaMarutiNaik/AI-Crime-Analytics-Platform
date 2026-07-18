from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "police_master.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "datasets"
    / "validation"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

REPORT_FILE = OUTPUT_DIR / "police_validation_report.csv"

MIN_LAT = 11.3
MAX_LAT = 18.7

MIN_LON = 73.8
MAX_LON = 78.9


df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("POLICE MASTER VALIDATION")
print("=" * 60)

# --------------------------------------------------
# Missing coordinates
# --------------------------------------------------

missing = df[
    df["latitude"].isna()
    | df["longitude"].isna()
]

# --------------------------------------------------
# Zero coordinates
# --------------------------------------------------

zero = df[
    (df["latitude"] == 0)
    | (df["longitude"] == 0)
]

# --------------------------------------------------
# Outside Karnataka
# --------------------------------------------------

outside = df[
    (df["latitude"] < MIN_LAT)
    | (df["latitude"] > MAX_LAT)
    | (df["longitude"] < MIN_LON)
    | (df["longitude"] > MAX_LON)
]

# --------------------------------------------------
# Duplicate station names
# --------------------------------------------------

duplicate_station = df[
    df.duplicated(
        subset=["police_station_name"],
        keep=False,
    )
]

# --------------------------------------------------
# Duplicate coordinates
# --------------------------------------------------

duplicate_coordinates = df[
    df.duplicated(
        subset=["latitude", "longitude"],
        keep=False,
    )
]

# --------------------------------------------------
# Validation report
# --------------------------------------------------

report = []

for _, row in missing.iterrows():
    report.append(
        {
            "issue": "Missing Coordinates",
            **row.to_dict(),
        }
    )

for _, row in zero.iterrows():
    report.append(
        {
            "issue": "Zero Coordinates",
            **row.to_dict(),
        }
    )

for _, row in outside.iterrows():
    report.append(
        {
            "issue": "Outside Karnataka",
            **row.to_dict(),
        }
    )

report_df = pd.DataFrame(report)

report_df.to_csv(
    REPORT_FILE,
    index=False,
)

print(f"Total Police Stations : {len(df)}")
print(f"Missing Coordinates   : {len(missing)}")
print(f"Zero Coordinates      : {len(zero)}")
print(f"Outside Karnataka     : {len(outside)}")
print(f"Duplicate Stations    : {duplicate_station['police_station_name'].nunique()}")
print(f"Duplicate Coordinates : {len(duplicate_coordinates)}")

print()

if len(report_df) == 0:
    print("✅ VALIDATION PASSED")
else:
    print("❌ VALIDATION FAILED")
    print(f"Report saved to:\n{REPORT_FILE}")