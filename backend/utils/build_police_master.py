from bs4 import BeautifulSoup
import pandas as pd
import os

folder = "datasets/police/raw"

rows = []

files = sorted(os.listdir(folder))

for file in files:

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

        rows.append({
            "district_id": district_id,
            "police_station_name": name,
            "address": parts[0].strip(),
            "email": parts[1].strip(),
            "phone": parts[2].strip(),
            "circle": parts[3].strip(),
            "latitude": parts[4].strip(),
            "longitude": parts[5].strip()
        })

df = pd.DataFrame(rows)

os.makedirs("datasets/processed", exist_ok=True)

df.to_csv(
    "datasets/processed/police_station_master.csv",
    index=False
)

print(df.head())

print("\nTotal Police Stations:", len(df))