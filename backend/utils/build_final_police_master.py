import pandas as pd

# Load datasets
police = pd.read_csv("datasets/processed/police_station_master.csv")
districts = pd.read_csv("datasets/processed/district_master.csv")
mapping = pd.read_csv("datasets/processed/district_mapping.csv")

# Add KSP district names to police stations
police = police.merge(
    districts,
    on="district_id",
    how="left"
)

# Rename for clarity
police.rename(
    columns={"district_name": "ksp_district"},
    inplace=True
)

# Map KSP districts to LGD districts
police = police.merge(
    mapping,
    on="ksp_district",
    how="left"
)

# Remove special police organizations
police = police[police["lgd_district"] != "SPECIAL"]

# Reorder columns
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

# Save final master
police.to_csv(
    "datasets/processed/police_master.csv",
    index=False
)

print(police.head())

print("\nTotal Police Stations:", len(police))

print("\nUnique LGD Districts:", police["lgd_district"].nunique())