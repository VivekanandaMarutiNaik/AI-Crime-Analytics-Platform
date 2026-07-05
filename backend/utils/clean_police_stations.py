import pandas as pd
import geopandas as gpd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

gdf = gpd.read_file(
    BASE_DIR / "datasets" / "police" / "police_stations.kml",
    driver="KML"
)

stations = (
    gdf["POL_STAName"]
    .dropna()
    .astype(str)
    .str.strip()
    .sort_values()
)

print(stations.head(100).to_string(index=False))

print(gdf[[
    "POL_STAName",
    "KGISVillageID",
    "KGISWardID",
    "KGISPSCode",
    "KGISCode"
]].head(20))

master = pd.read_csv("datasets/processed/master_locations.csv")

matches = master[
    master["village_id"].isin(gdf["KGISVillageID"])
]

print("Matching villages:", len(matches))
print(matches.head())