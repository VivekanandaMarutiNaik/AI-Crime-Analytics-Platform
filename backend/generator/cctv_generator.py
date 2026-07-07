import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

BASE_DIR = Path(__file__).resolve().parents[2]

POLICE_STATIONS = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "police_master.csv"
)

POLICE_STATIONS = POLICE_STATIONS[
    (POLICE_STATIONS["latitude"].notna()) &
    (POLICE_STATIONS["longitude"].notna()) &
    (POLICE_STATIONS["latitude"] != 0) &
    (POLICE_STATIONS["longitude"] != 0)
].copy()

print(f"Police stations with valid coordinates: {len(POLICE_STATIONS)}")

LOCATION_MASTER = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "police_village_mapping.csv"
)

LANDMARKS = [
    "Bus Stand",
    "Market",
    "Government Hospital",
    "School",
    "College",
    "Bank",
    "ATM",
    "Traffic Junction",
    "Government Office",
    "Railway Station"
]


def random_offset():
    return random.uniform(-0.0015, 0.0015)


cctv_records = []

for i, (_, location) in enumerate(POLICE_STATIONS.iterrows(), start=1):

    camera_count = random.randint(3, 6)

    for cam in range(camera_count):

        landmark = random.choice(LANDMARKS)

        # Pick one real location from the same district
        district_locations = LOCATION_MASTER[
            LOCATION_MASTER["district_id"] == location["district_id"]
        ]

        if district_locations.empty:
            print(
                f"No mapped villages for district_id={location['district_id']}, "
                f"Police Station={location['police_station_name']}"
            )
            continue

        place = district_locations.sample(1).iloc[0]
        cctv = {
            "cctv_id": f"CCTV{i:05d}_{cam+1}",
            "cctv_name": f"{location['police_station_name']} - {landmark} CCTV",

            "district_id": place["district_id"],
            "district": place["district_name"],

            "taluk_id": place["taluk_id"],
            "taluk": place["taluk_name"],

            "gp_id": place["gp_id"],
            "gram_panchayat": place["gp_name"],

            "village_id": place["village_id"],
            "village": place["village_name"],

            "latitude": float(location["latitude"]) + random_offset(),
            "longitude": float(location["longitude"]) + random_offset(),

            "location_type": landmark,
            "coverage_radius_meters": random.choice([100, 150, 200]),

            "status": random.choice([
                "Active",
                "Active",
                "Active",
                "Maintenance"
            ]),

            "nearest_police_station": location["police_station_name"],
        }

        cctv_records.append(cctv)


# -------------------------
# SAVE ONLY ONCE
# -------------------------

cctv_df = pd.DataFrame(cctv_records)

output_path = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "cctv_master.csv"
)

cctv_df.to_csv(output_path, index=False)

print(f"\nGenerated {len(cctv_df)} CCTV records.")
print(f"Saved to: {output_path}")

print("\nFirst 5 CCTV records:")
print(cctv_df.head())