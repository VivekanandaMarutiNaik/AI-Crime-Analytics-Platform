from bs4 import BeautifulSoup
import pandas as pd
import os

folder = "datasets/police/raw"

rows = []

files = sorted(os.listdir(folder))

for file in files:

    if not file.startswith("district_"):
        continue

    district_id = int(file.replace("district_", "").replace(".html", ""))

    path = os.path.join(folder, file)

    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    for option in soup.find_all("option"):

        name = option.text.strip()
        value = option.get("value", "").strip()

        if not name:
            continue

        if name == "Select Police Station":
            continue

        if "!@#$%" not in value:
            continue

        parts = value.split("!@#$%")

        if len(parts) < 6:
            continue

        lat_str = parts[4].strip()
        lon_str = parts[5].strip()

        # Skip stations with missing coordinates
        if lat_str == "" or lon_str == "":
            continue

        lat = float(lat_str)
        lon = float(lon_str)

        # Fix swapped coordinates
        if lat > 20 and lon < 20:
            lat, lon = lon, lat

        # Ignore obviously wrong coordinates
        if lat == 0 or lon == 0:
            continue

        # Skip known incorrect coordinates from official source
        BAD_COORDINATES = [
            (15.8578, 74.50571),
            (12.97071, 77.53777),
            (12.960586, 77.564034),
        ]

        if any(
            abs(lat - bad_lat) < 0.0001 and
            abs(lon - bad_lon) < 0.0001
            for bad_lat, bad_lon in BAD_COORDINATES
        ):
            continue

        rows.append({
            "district_id": district_id,
            "police_station_name": name,
            "address": parts[0].strip(),
            "email": parts[1].strip(),
            "phone": parts[2].strip(),
            "circle": parts[3].strip(),
            "latitude": lat,
            "longitude": lon
        })

zero_coords = [
    row for row in rows
    if row["latitude"] == "0.0" or row["longitude"] == "0.0"
]

print(f"Police stations with 0.0 coordinates: {len(zero_coords)}")

for row in zero_coords[:10]:
    print(row)

print("\nChecking Mysuru Women PS before saving...\n")

for row in rows:
    if "Women PS" in row["police_station_name"]:
        print(row)

df = pd.DataFrame(rows)

os.makedirs("datasets/processed", exist_ok=True)
# Fix incorrect coordinates from KSP website

df.loc[
    df["police_station_name"] == "Puttur Town PS",
    ["latitude", "longitude"],
] = [12.7597, 75.2010]

# Fix incorrect Thilaknagar PS coordinates (official KSP site points to Mumbai)
df.loc[
    df["police_station_name"] == "Thilaknagar PS",
    ["latitude", "longitude"],
] = [12.9238, 77.5567]

# Fix incorrect Subramanya PS coordinates (official KSP data is incorrect)
df.loc[
    df["police_station_name"] == "Subramanya PS",
    ["latitude", "longitude"],
] = [12.6628, 75.6000]

df.to_csv(
    "datasets/processed/police_station_master.csv",
    index=False
)

print(df.head())

print("\nTotal Police Stations:", len(df))