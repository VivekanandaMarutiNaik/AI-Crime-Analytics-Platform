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

df = pd.DataFrame(rows)

os.makedirs("datasets/processed", exist_ok=True)

df.to_csv(
    "datasets/processed/police_station_master.csv",
    index=False
)

print(df.head())

print("\nTotal Police Stations:", len(df))