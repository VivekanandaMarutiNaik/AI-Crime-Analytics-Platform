import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import random

stations = pd.read_csv(
    "datasets/police/master/police_stations_master.csv"
)

centroids = pd.read_csv(
    "datasets/police/master/district_centroids.csv"
)

centroid_map = centroids.set_index("district")[["latitude", "longitude"]].to_dict("index")


def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat/2)**2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon/2)**2
    )

    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


corrected = 0

for idx, row in stations.iterrows():

    district = row["district"]

    if district not in centroid_map:
        continue

    clat = centroid_map[district]["latitude"]
    clon = centroid_map[district]["longitude"]

    lat = row["latitude"]
    lon = row["longitude"]

    if pd.isna(lat) or pd.isna(lon):

        stations.at[idx, "latitude"] = clat + random.uniform(-0.08, 0.08)
        stations.at[idx, "longitude"] = clon + random.uniform(-0.08, 0.08)
        corrected += 1
        continue

    distance = haversine(lat, lon, clat, clon)

    if distance > 80:

        stations.at[idx, "latitude"] = clat + random.uniform(-0.08, 0.08)
        stations.at[idx, "longitude"] = clon + random.uniform(-0.08, 0.08)

        corrected += 1


stations.to_csv(
    "datasets/processed/police_station_master.csv",
    index=False
)
print("Corrected:", corrected)
print("Saved cleaned dataset.")