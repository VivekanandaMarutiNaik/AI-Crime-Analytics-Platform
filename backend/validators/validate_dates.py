from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
MASTER_DIR = BASE_DIR / "datasets" / "masters"

CASE_MASTER = pd.read_csv(MASTER_DIR / "case_master.csv")
INVESTIGATION_MASTER = pd.read_csv(MASTER_DIR / "investigation_master.csv")
ARREST_MASTER = pd.read_csv(MASTER_DIR / "arrest_master.csv")
CHARGESHEET_MASTER = pd.read_csv(MASTER_DIR / "chargesheet_master.csv")

print(f"Cases loaded: {len(CASE_MASTER)}")
print(f"Investigations loaded: {len(INVESTIGATION_MASTER)}")
print(f"Arrests loaded: {len(ARREST_MASTER)}")
print(f"Chargesheets loaded: {len(CHARGESHEET_MASTER)}")

# Convert date columns to datetime
CASE_MASTER["crime_datetime"] = pd.to_datetime(CASE_MASTER["crime_datetime"])

INVESTIGATION_MASTER["investigation_start_date"] = pd.to_datetime(
    INVESTIGATION_MASTER["investigation_start_date"]
)

INVESTIGATION_MASTER["investigation_end_date"] = pd.to_datetime(
    INVESTIGATION_MASTER["investigation_end_date"],
    errors="coerce"
)

ARREST_MASTER["arrest_date"] = pd.to_datetime(
    ARREST_MASTER["arrest_date"]
)

CHARGESHEET_MASTER["filing_date"] = pd.to_datetime(
    CHARGESHEET_MASTER["filing_date"]
)

timeline_df = CASE_MASTER[
    ["case_id", "crime_datetime"]
].merge(
    INVESTIGATION_MASTER[
        [
            "case_id",
            "investigation_start_date",
            "investigation_end_date",
        ]
    ],
    on="case_id",
    how="left",
).merge(
    ARREST_MASTER[
        [
            "case_id",
            "arrest_date",
        ]
    ],
    on="case_id",
    how="left",
).merge(
    CHARGESHEET_MASTER[
        [
            "case_id",
            "filing_date",
        ]
    ],
    on="case_id",
    how="left",
)

print(timeline_df.head())

# Create date-only columns (ignore time)
timeline_df["crime_date"] = timeline_df["crime_datetime"].dt.date

timeline_df["investigation_start"] = (
    timeline_df["investigation_start_date"].dt.date
)

timeline_df["investigation_end"] = (
    timeline_df["investigation_end_date"].dt.date
)

timeline_df["arrest"] = (
    timeline_df["arrest_date"].dt.date
)

timeline_df["filing"] = (
    timeline_df["filing_date"].dt.date
)

print("\n========== DATE VALIDATION ==========\n")

# Rule 1
crime_date = timeline_df["crime_datetime"].dt.date
investigation_date = timeline_df["investigation_start_date"].dt.date

invalid = timeline_df[
    timeline_df["investigation_start"] < timeline_df["crime_date"]
]

if invalid.empty:
    print("✅ Investigation starts after crime date.")
else:
    print(f"❌ Investigation starts before crime date: {len(invalid)}")
    print(invalid[["case_id"]].head())

# Rule 2
invalid = timeline_df[
    timeline_df["arrest"].notna() &
    (timeline_df["arrest"] < timeline_df["crime_date"])
]

if invalid.empty:
    print("✅ Arrest occurs after crime date.")
else:
    print(f"❌ Arrest before crime date: {len(invalid)}")
    print(invalid[["case_id"]].head())

# Rule 3
invalid = timeline_df[
    timeline_df["investigation_end"].notna() &
    (
        timeline_df["investigation_end"] <
        timeline_df["investigation_start"]
    )
]

if invalid.empty:
    print("✅ Investigation end date is valid.")
else:
    print(f"❌ Investigation ends before it starts: {len(invalid)}")
    print(invalid[["case_id"]].head())

# Rule 4
invalid = timeline_df[
    timeline_df["filing"].notna() &
    (
        timeline_df["filing"] <
        timeline_df["investigation_start"]
    )
]

if invalid.empty:
    print("✅ Chargesheet filing date is valid.")
else:
    print(f"❌ Chargesheet filed before investigation started: {len(invalid)}")
    print(invalid[["case_id"]].head())

print("\n========== VALIDATION COMPLETE ==========")