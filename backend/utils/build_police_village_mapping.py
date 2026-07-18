import pandas as pd
from pathlib import Path
import random
import hashlib
offset = 0.02  # about 2 km

BASE_DIR = Path(__file__).resolve().parents[2]

# Load datasets
master_locations = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "master_locations.csv"
)

police_master = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "police_master.csv"
)

district_mapping = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "district_mapping.csv"
)

master_locations = master_locations.merge(
    district_mapping,
    left_on="district_name",
    right_on="lgd_district",
    how="left",
)

mapping_rows = []
def get_deterministic_offset(village_id):

    h = hashlib.md5(str(village_id).encode()).hexdigest()

    seed = int(h[:8], 16)

    lat_offset = ((seed % 4000) / 100000) - 0.02
    lon_offset = (((seed // 4000) % 4000) / 100000) - 0.02

    return lat_offset, lon_offset

# Process district by district
for district in sorted(master_locations["ksp_district"].dropna().unique()):

    villages = (
        master_locations[
            master_locations["ksp_district"] == district
        ]
        .sort_values("village_name")
        .reset_index(drop=True)
    )

    stations = (
        police_master[
            (police_master["ksp_district"] == district) &
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

        offset_lat = random.uniform(-0.02, 0.02)
        offset_lon = random.uniform(-0.02, 0.02)

        lat_offset, lon_offset = get_deterministic_offset(
            village["village_id"]
        )

        mapping_rows.append({
            "district_id": village["district_id"],
            "district_name": village["lgd_district"],
            "taluk_id": village["taluk_id"],
            "taluk_name": village["taluk_name"],
            "gp_id": village["gp_id"],
            "gp_name": village["gp_name"],
            "village_id": village["village_id"],
            "village_name": village["village_name"],

            "police_station_name": station["police_station_name"],

            "police_station_latitude": round(
                station["latitude"] + lat_offset,
                6
            ),
            "police_station_longitude": round(
                station["longitude"] + lon_offset,
                6
            ),
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