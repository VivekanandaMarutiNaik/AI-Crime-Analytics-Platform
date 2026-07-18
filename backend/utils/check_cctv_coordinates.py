import pandas as pd

df = pd.read_csv("datasets/processed/cctv_master.csv")

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

print("=" * 50)
print(f"Total CCTV : {len(df)}")
print(f"Invalid : {len(bad)}")
print("=" * 50)

if len(bad):
    print(
        bad[
            [
                "cctv_name",
                "district",
                "latitude",
                "longitude",
            ]
        ]
    )