import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

mapping = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "police_village_mapping.csv"
)

villages = mapping[
    [
        "village_id",
        "village_name",
        "taluk_id",
        "taluk_name",
        "district_id",
        "district_name",
        "gp_id",
        "gp_name",
        "police_station_name",          # <-- ADD THIS
        "police_station_latitude",
        "police_station_longitude",
    ]
].copy()

villages = villages.rename(
    columns={
        "police_station_latitude": "latitude",
        "police_station_longitude": "longitude",
    }
)

villages = villages.drop_duplicates(subset="village_id")

villages = villages.rename(
    columns={
        "police_station_latitude": "latitude",
        "police_station_longitude": "longitude",
    }
)

villages = villages.drop_duplicates(subset="village_id")

output = BASE_DIR / "datasets" / "processed" / "village_coordinates.csv"

villages.to_csv(output, index=False)

print(f"Generated {len(villages)} village coordinates.")
print(villages.head())