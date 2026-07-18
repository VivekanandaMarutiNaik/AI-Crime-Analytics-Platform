import pandas as pd

df = pd.read_csv("datasets/processed/police_master_updated.csv")

# Karnataka approximate bounding box
MIN_LAT = 11.3
MAX_LAT = 18.7
MIN_LON = 73.8
MAX_LON = 78.9

bad = df[
    (df["latitude"] < MIN_LAT) |
    (df["latitude"] > MAX_LAT) |
    (df["longitude"] < MIN_LON) |
    (df["longitude"] > MAX_LON)
]

print("=" * 60)
print(f"Total Police Stations : {len(df)}")
print(f"Invalid Coordinates   : {len(bad)}")
print("=" * 60)

if len(bad) > 0:
    print(
        bad[
            [
                "police_station_name",
                "ksp_district",
                "latitude",
                "longitude",
            ]
        ]
    )