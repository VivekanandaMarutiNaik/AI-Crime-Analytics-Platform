import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

# Load datasets
master_locations = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "master_locations.csv"
)

police_master = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "police_master.csv"
)

mapping_rows = []

# Process district by district
for district_id in sorted(master_locations["district_id"].unique()):

    villages = (
        master_locations[
            master_locations["district_id"] == district_id
        ]
        .sort_values("village_name")
        .reset_index(drop=True)
    )

    stations = (
        police_master[
            (police_master["district_id"] == district_id) &
            (police_master["latitude"].notna()) &
            (police_master["longitude"].notna()) &
            (police_master["latitude"] != 0) &
            (police_master["longitude"] != 0)
        ]
        .sort_values("police_station_name")
        .reset_index(drop=True)
    )

    # Skip districts with no police stations
    if stations.empty:
        continue

    station_count = len(stations)

    # Assign villages to stations in round-robin fashion
    for i, (_, village) in enumerate(villages.iterrows()):

        station = stations.iloc[i % station_count]

        mapping_rows.append({
            "district_id": village["district_id"],
            "district_name": village["district_name"],
            "taluk_id": village["taluk_id"],
            "taluk_name": village["taluk_name"],
            "gp_id": village["gp_id"],
            "gp_name": village["gp_name"],
            "village_id": village["village_id"],
            "village_name": village["village_name"],
            "police_station_name": station["police_station_name"],
            "police_station_latitude": station["latitude"],
            "police_station_longitude": station["longitude"]
        })

mapping_df = pd.DataFrame(mapping_rows)

output_path = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "police_village_mapping.csv"
)

mapping_df.to_csv(output_path, index=False)

print(f"Generated {len(mapping_df)} mappings.")
print(f"Saved to: {output_path}")