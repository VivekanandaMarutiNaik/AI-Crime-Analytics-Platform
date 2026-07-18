import pandas as pd

df = pd.read_csv("datasets/raw/crime_cases.csv")

MIN_LAT = 11.3
MAX_LAT = 18.7
MIN_LON = 73.8
MAX_LON = 78.9

bad = df[
    (df["crime_latitude"] < MIN_LAT) |
    (df["crime_latitude"] > MAX_LAT) |
    (df["crime_longitude"] < MIN_LON) |
    (df["crime_longitude"] > MAX_LON)
]

print("=" * 50)
print(f"Total Crimes : {len(df)}")
print(f"Invalid : {len(bad)}")
print("=" * 50)

if len(bad):
    print(
        bad[
            [
                "crime_id",
                "district",
                "police_station_name",
                "police_station_latitude",
                "police_station_longitude",
                "crime_latitude",
                "crime_longitude",
            ]
        ]
    )