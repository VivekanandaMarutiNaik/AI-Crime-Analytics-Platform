import pandas as pd

# -------------------------
# Load datasets
# -------------------------

police = pd.read_csv(
    "datasets/processed/police_station_master.csv"
)

districts = pd.read_csv(
    "datasets/processed/district_master.csv"
)

mapping = pd.read_csv(
    "datasets/processed/district_mapping.csv"
)

# -------------------------
# Add KSP district name
# -------------------------

police = police.merge(
    districts,
    on="district_id",
    how="left",
)


police.rename(
    columns={
        "district_name": "ksp_district"
    },
    inplace=True,
)

# -------------------------
# Map to LGD district
# -------------------------

police = police.merge(
    mapping,
    on="ksp_district",
    how="left",
)

# Get the correct LGD district_id from master_locations
lgd_ids = (
    pd.read_csv("datasets/processed/master_locations.csv")[
        ["district_id", "district_name"]
    ]
    .drop_duplicates()
)

police = police.merge(
    lgd_ids,
    left_on="lgd_district",
    right_on="district_name",
    how="left",
)

# Replace KSP district_id with LGD district_id
police["district_id"] = police["district_id_y"]

police.drop(
    columns=[
        "district_id_x",
        "district_id_y",
        "district_name",
    ],
    inplace=True,
)
# -------------------------
# Remove SPECIAL districts
# -------------------------

police = police[
    police["lgd_district"] != "SPECIAL"
].copy()

# -------------------------
# IMPORTANT
# Keep original coordinates exactly as they are.
# Do NOT regenerate or modify them.
# -------------------------

police = police[
    [
        "district_id",
        "ksp_district",
        "lgd_district",
        "police_station_name",
        "address",
        "email",
        "phone",
        "circle",
        "latitude",
        "longitude",
    ]
]

police.to_csv(
    "datasets/processed/police_master.csv",
    index=False,
)

print("Police Master Created")
print(police.head())

print("\nTotal Stations:", len(police))
print("Unique Districts:", police["lgd_district"].nunique())