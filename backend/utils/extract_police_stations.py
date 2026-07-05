import geopandas as gpd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

KML_FILE = BASE_DIR / "datasets" / "police" / "police_stations.kml"
OUTPUT_FILE = BASE_DIR / "datasets" / "raw" / "police_stations.csv"

# Read KML
gdf = gpd.read_file(KML_FILE, driver="KML")

print(gdf.head())

print("\nColumns:")
print(gdf.columns.tolist())

print(f"\nTotal Police Stations: {len(gdf)}")

# Save raw extraction
gdf.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved to: {OUTPUT_FILE}")