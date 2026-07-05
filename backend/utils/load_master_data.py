import pandas as pd
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Raw data folder
RAW_DATA = BASE_DIR / "datasets" / "raw"

# File paths
districts_file = RAW_DATA / "districts.csv"
taluks_file = RAW_DATA / "taluks.csv"
gram_panchayats_file = RAW_DATA / "gram_panchayats.csv"
police_stations_file = RAW_DATA / "police_stations.csv"

# Load CSV files
districts_df = pd.read_csv(districts_file)
taluks_df = pd.read_csv(taluks_file)
gram_panchayats_df = pd.read_csv(gram_panchayats_file)
police_stations_df = pd.read_csv(police_stations_file)


def validate_columns(df, required_columns, file_name):
    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(
            f"{file_name} is missing columns: {', '.join(missing)}"
        )

    print(f"✓ {file_name} columns are valid")


validate_columns(
    districts_df,
    ["district_id", "district_name"],
    "districts.csv"
)

validate_columns(
    taluks_df,
    ["taluk_id", "district_id", "taluk_name"],
    "taluks.csv"
)

validate_columns(
    gram_panchayats_df,
    ["gp_id", "taluk_id", "gp_name"],
    "gram_panchayats.csv"
)

validate_columns(
    police_stations_df,
    [
        "station_id",
        "district_id",
        "taluk_id",
        "station_name",
        "station_type",
        "latitude",
        "longitude"
    ],
    "police_stations.csv"
)

def validate_foreign_key(
    child_df,
    parent_df,
    child_column,
    parent_column,
    child_name,
    parent_name
):
    invalid = child_df[
        ~child_df[child_column].isin(parent_df[parent_column])
    ]

    if not invalid.empty:
        raise ValueError(
            f"{child_name} contains invalid {child_column} values "
            f"that do not exist in {parent_name}"
        )

    print(f"✓ {child_name} -> {parent_name} relationship is valid")
validate_foreign_key(
    taluks_df,
    districts_df,
    "district_id",
    "district_id",
    "taluks.csv",
    "districts.csv"
)

validate_foreign_key(
    gram_panchayats_df,
    taluks_df,
    "taluk_id",
    "taluk_id",
    "gram_panchayats.csv",
    "taluks.csv"
)

validate_foreign_key(
    police_stations_df,
    districts_df,
    "district_id",
    "district_id",
    "police_stations.csv",
    "districts.csv"
)

validate_foreign_key(
    police_stations_df,
    taluks_df,
    "taluk_id",
    "taluk_id",
    "police_stations.csv",
    "taluks.csv"
)
    
print("\n✅ All master datasets loaded successfully!")