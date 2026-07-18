from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

mapping_file = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "police_station_taluk_mapping.csv"
)

master_locations_file = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "master_locations.csv"
)

mapping = pd.read_csv(mapping_file, dtype={"taluk": "string"})
mapping["taluk"] = mapping["taluk"].fillna("")
locations = pd.read_csv(master_locations_file)

# Unique taluks for each district
taluks = (
    locations[
        ["district_id", "district_name", "taluk_name"]
    ]
    .drop_duplicates()
)

filled = 0

for idx, row in mapping.iterrows():

    district_id = row["district_id"]
    ps_name = str(row["police_station_name"]).lower()

    district_taluks = taluks[
        taluks["district_id"] == district_id
    ]

    matched = None

    for taluk in district_taluks["taluk_name"]:

        if str(taluk).lower() in ps_name:
            matched = taluk
            break

    if matched:
        mapping.at[idx, "taluk"] = matched
        filled += 1

mapping.to_csv(mapping_file, index=False)

print(f"Filled automatically: {filled}")
print(f"Remaining blank: {(mapping['taluk'] == '').sum()}")
print(f"\nSaved: {mapping_file}")
