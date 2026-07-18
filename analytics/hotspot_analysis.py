import pandas as pd
import folium
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/raw/crime_cases.csv")

print("Total crimes:", len(df))

print("Missing crime coordinates:")
print(
    df[
        ["crime_latitude", "crime_longitude"]
    ].isna().sum()
)

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
#invalid_stations = [
 #   "Basavanagudi Traffic PS",
 #   "Bommanahalli PS",
  #  "Kalaburagi CEN Crime PS",
  #  "Puttur Town PS",
  #  "Thilaknagar PS"
#]

#df = df[
   # ~df["police_station_name"].isin(invalid_stations)
#].copy()

print(f"Records available for hotspot analysis: {len(df)}")


import matplotlib.pyplot as plt

plt.figure(figsize=(8, 8))

plt.scatter(
    df["crime_longitude"],
    df["crime_latitude"],
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

hotspot_centers = (
    df.groupby(
        [
            "district",
            "taluk",
            "police_station_name",
            "police_station_latitude",
            "police_station_longitude",
        ]
    )
    .agg(
        crime_count=("crime_id", "count"),
        avg_hotspot_score=("hotspot_score", "mean"),
    )
    .reset_index()
)

hotspot_centers = hotspot_centers.sort_values(
    "crime_count",
    ascending=False
).head(150)



hotspot_centers = hotspot_centers.sort_values(
    "crime_count",
    ascending=False
).head(150)

hotspot_centers.rename(
    columns={
        "police_station_latitude": "latitude",
        "police_station_longitude": "longitude",
        "police_station_name": "police_station",
    },
    inplace=True,
)

hotspot_centers["recommended_cctv"] = (
    hotspot_centers["crime_count"] / 5
).round().clip(lower=1).astype(int)

print(hotspot_centers.head()) 
hotspot_centers = hotspot_centers[
    (hotspot_centers["latitude"] >= 11.3)
    & (hotspot_centers["latitude"] <= 18.7)
    & (hotspot_centers["longitude"] >= 73.8)
    & (hotspot_centers["longitude"] <= 78.9)
]
hotspot_centers.to_csv(
    "datasets/processed/crime_hotspots.csv",
    index=False,
)

print("Saved crime hotspots to datasets/processed/crime_hotspots.csv")

crime_map = folium.Map(
    location=[15.3173, 75.7139],  # Center of Karnataka
    zoom_start=7,
    tiles="OpenStreetMap"
)

def get_hotspot_color(crime_count):
    if crime_count >= 40:
        return "darkred"
    elif crime_count >= 25:
        return "red"
    elif crime_count >= 15:
        return "orange"
    else:
        return "yellow"
    
print(hotspot_centers["crime_count"].head(10))

for count in hotspot_centers["crime_count"].head(10):
    print(count, "->", get_hotspot_color(count))

for _, row in hotspot_centers.iterrows():
    risk = (
    "Critical" if row["crime_count"] >= 40 else
    "High" if row["crime_count"] >= 25 else
    "Medium" if row["crime_count"] >= 15 else
    "Low"
)
    folium.CircleMarker(
        location=[
            row["latitude"],
            row["longitude"]
        ],
        radius=min(18, max(6, row["crime_count"] / 8)),
        color=get_hotspot_color(row["crime_count"]),
        fill=True,
        fill_color=get_hotspot_color(row["crime_count"]),
        fill_opacity=0.7,
      popup=(
            f"<b>Police Station:</b> {row['police_station']}<br>"
            f"<b>District:</b> {row['district']}<br>"
            f"<b>Crime Count:</b> {int(row['crime_count'])}<br>"
            f"<b>Risk:</b> {risk}<br>"
            f"<b>Avg Hotspot Score:</b> {row['avg_hotspot_score']:.1f}"
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
