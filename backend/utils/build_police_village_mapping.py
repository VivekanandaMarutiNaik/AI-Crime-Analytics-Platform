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

print(master_locations.columns.tolist())
# Keep only mappings where the police district matches the village district

print("Rows before filter:", len(master_locations))


print("Rows after filter:", len(master_locations))
mapping_rows = []
def get_deterministic_offset(village_id):

    h = hashlib.md5(str(village_id).encode()).hexdigest()

    seed = int(h[:8], 16)

    lat_offset = ((seed % 4000) / 100000) - 0.02
    lon_offset = (((seed // 4000) % 4000) / 100000) - 0.02

    return lat_offset, lon_offset

# Process district by district
for district in sorted(master_locations["district_name"].dropna().unique()):
    ksp_names = district_mapping[
        district_mapping["lgd_district"] == district
    ]["ksp_district"].unique()
    if district == "Vijayanagara":
        print("KSP Names:", ksp_names)
    
    villages = (
        master_locations[
            master_locations["district_name"] == district
        ]
        .drop_duplicates(subset="village_id")
        .sort_values("village_name")
        .reset_index(drop=True)
    )
    stations = (
        police_master[
            police_master["ksp_district"].isin(ksp_names)
        ]
        .query(
            "latitude.notna() and longitude.notna() and latitude != 0 and longitude != 0"
        )
        .sort_values("police_station_name")
        .reset_index(drop=True)
    )

    if district == "Vijayanagara":
        print("Stations found:", len(stations))
    print(
        master_locations[
            master_locations["village_id"] == 597114
        ][[
            "district_name",
            "ksp_district",
            "taluk_name",
            "village_name"
        ]]
    )
    # Skip districts with no police stations
    if stations.empty:
        continue

    station_count = len(stations)

  # One police station per GP (Gram Panchayat)

    gp_station_map = {}

    gps = (
        villages[villages["gp_id"].notna()][["gp_id"]]
        .drop_duplicates()
        .sort_values("gp_id")
        .reset_index(drop=True)
    )

    for i, row in gps.iterrows():
        gp_station_map[row["gp_id"]] = stations.iloc[i % station_count]

    for i, (_, village) in enumerate(villages.iterrows()):

        if pd.notna(village["gp_id"]):
            station = gp_station_map[village["gp_id"]]
        else:
            # fallback for villages without GP
            station = stations.iloc[i % station_count]
        

        
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