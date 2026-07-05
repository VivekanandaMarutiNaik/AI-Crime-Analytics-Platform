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