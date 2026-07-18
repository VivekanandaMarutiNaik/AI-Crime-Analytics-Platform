import random
import pandas as pd

# ----------------------------
# Files
# ----------------------------
POLICE_FILE = "datasets/processed/police_master.csv"
DISTRICT_FILE = "datasets/masters/district_centers.csv"
OUTPUT_FILE = "datasets/processed/police_master_updated.csv"

# ----------------------------
# Load data
# ----------------------------
police_df = pd.read_csv(POLICE_FILE)
district_df = pd.read_csv(DISTRICT_FILE)

district_lookup = {
    row["district"].strip().lower(): (
        row["latitude"],
        row["longitude"]
    )
    for _, row in district_df.iterrows()
}

DISTRICT_MAPPING = {
    "bagalkot": "bagalkote",
    "belagavi city": "belagavi",
    "belagavi dist": "belagavi",
    "bengaluru city": "bengaluru urban",
    "bengaluru dist": "bengaluru rural",
    "bengaluru south": "bengaluru urban",
    "chickballapura": "chikkaballapura",
    "hubballi dharwad city": "dharwad",
    "k.g.f": "kolar",
    "kalaburagi city": "kalaburagi",
    "mangaluru city": "dakshina kannada",
    "mysuru city": "mysuru",
    "mysuru dist": "mysuru",
    "vijayapur": "vijayapura",
}
# ----------------------------
# Generate realistic coordinates
# ----------------------------

def random_offset():
    """
    About 300 m to 5 km
    """
    return random.uniform(-0.04, 0.04)

missing = []

new_lat = []
new_lon = []

for _, row in police_df.iterrows():

    district = str(row["ksp_district"]).strip().lower()

    district = DISTRICT_MAPPING.get(district, district)

    if district not in district_lookup:
        missing.append(row["ksp_district"])
        new_lat.append(None)
        new_lon.append(None)
        continue

    center_lat, center_lon = district_lookup[district]

    lat = center_lat + random_offset()
    lon = center_lon + random_offset()

    new_lat.append(round(lat, 6))
    new_lon.append(round(lon, 6))

police_df["latitude"] = new_lat
police_df["longitude"] = new_lon

police_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=" * 50)
print("Police stations updated successfully")
print("=" * 50)

print(f"Total Stations : {len(police_df)}")
print(f"Missing Districts : {len(set(missing))}")

if missing:
    print("\nMissing:")
    print(sorted(set(missing)))