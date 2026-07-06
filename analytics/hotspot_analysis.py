import pandas as pd
import folium
from sklearn.cluster import DBSCAN

df = pd.read_csv("datasets/raw/crime_cases.csv")

# Remove records with missing official GPS coordinates
df = df[
    (df["police_station_latitude"] != 0) &
    (df["police_station_longitude"] != 0)
].copy()

# Remove records with missing coordinates
df = df.dropna(
    subset=[
        "police_station_latitude",
        "police_station_longitude"
    ]
).copy()

# Remove police stations with incorrect official coordinates
invalid_stations = [
    "Basavanagudi Traffic PS",
    "Bommanahalli PS",
    "Kalaburagi CEN Crime PS",
    "Puttur Town PS",
    "Thilaknagar PS"
]

df = df[
    ~df["police_station_name"].isin(invalid_stations)
].copy()

print(f"Records available for hotspot analysis: {len(df)}")


import matplotlib.pyplot as plt

plt.figure(figsize=(8, 8))

plt.scatter(
    df["police_station_longitude"],
    df["police_station_latitude"],
    s=2
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Crime Locations (Police Station Coordinates)")

invalid_coords = df[
    (df["police_station_latitude"] < 8) |
    (df["police_station_latitude"] > 19) |
    (df["police_station_longitude"] < 73) |
    (df["police_station_longitude"] > 79)
]


coordinates = df[
    [
        "police_station_latitude",
        "police_station_longitude"
    ]
]

dbscan = DBSCAN(
    eps=0.10,
    min_samples=5
)

df["cluster"] = dbscan.fit_predict(coordinates)

hotspots = (
    df[df["cluster"] != -1]
    .groupby("cluster")
    .size()
    .sort_values(ascending=False)
)

print(hotspots.head(10))

hotspot_centers = (
    df[df["cluster"] != -1]
    .groupby("cluster")
    .agg(
        latitude=("police_station_latitude", "mean"),
        longitude=("police_station_longitude", "mean"),
        crime_count=("cluster", "size"),
    )
    .reset_index()
)

hotspot_centers["recommended_cctv"] = (
    hotspot_centers["crime_count"] // 100
).clip(lower=1)

print(hotspot_centers.head())

crime_map = folium.Map(
    location=[15.3173, 75.7139],  # Center of Karnataka
    zoom_start=7,
    tiles="OpenStreetMap"
)

def get_hotspot_color(crime_count):
    if crime_count >= 500:
        return "darkred"
    elif crime_count >= 200:
        return "red"
    elif crime_count >= 100:
        return "orange"
    elif crime_count >= 50:
        return "yellow"
    else:
        return "green"
    
print(hotspot_centers["crime_count"].head(10))

for count in hotspot_centers["crime_count"].head(10):
    print(count, "->", get_hotspot_color(count))

for _, row in hotspot_centers.iterrows():
    folium.CircleMarker(
        location=[
            row["latitude"],
            row["longitude"]
        ],
        radius=max(5, row["crime_count"] / 50),
        color=get_hotspot_color(row["crime_count"]),
        fill=True,
        fill_color=get_hotspot_color(row["crime_count"]),
        fill_opacity=0.7,
        popup=(
            f"<b>Hotspot ID:</b> {int(row['cluster'])}<br>"
            f"<b>Crime Count:</b> {int(row['crime_count'])}<br>"
            f"<b>Risk Level:</b> "
            f"{'Critical' if row['crime_count'] >= 500 else 'High' if row['crime_count'] >= 200 else 'Medium' if row['crime_count'] >= 100 else 'Low'}"
        )
    ).add_to(crime_map)

#for _, row in df.iterrows():
  #  folium.CircleMarker(
  #      location=[
  #          row["police_station_latitude"],
   #         row["police_station_longitude"]
    #    ],
     #   radius=2,
      #  color="red",
       # fill=True,
        #fill_color="red",
       # fill_opacity=0.6,
   # ).add_to(crime_map)

crime_map.save("crime_hotspots.html")

print("Crime hotspot map saved as crime_hotspots.html")

plt.show()
