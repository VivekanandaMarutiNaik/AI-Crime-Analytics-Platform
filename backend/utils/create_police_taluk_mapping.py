import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

# Read police master
police = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "police_master.csv"
)

# Create mapping template
mapping = police[
    [
        "district_id",
        "lgd_district",
        "police_station_name"
    ]
].copy()

mapping.rename(
    columns={
        "lgd_district": "district"
    },
    inplace=True
)

# Empty taluk column to be filled once
mapping["taluk"] = ""

# Remove duplicates if any
mapping = mapping.drop_duplicates()

# Sort for easier editing
mapping = mapping.sort_values(
    ["district", "police_station_name"]
)

output = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "police_station_taluk_mapping.csv"
)

mapping.to_csv(output, index=False)

print(f"Saved: {output}")
print(f"Total Police Stations: {len(mapping)}")